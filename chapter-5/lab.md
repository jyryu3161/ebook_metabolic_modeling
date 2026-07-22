# 실습: COBRApy를 이용한 재구축 품질 검사

## 이 실습에서 하는 일

이 실습에서는 게놈 규모 대사 모델(GEM)을 만든 뒤 반드시 거쳐야 하는 **품질 검사와 gap-filling**을 COBRApy로 직접 실행해 봅니다. 서열 정렬 통계(E-value)의 수치 검산에서 시작해, 반응의 질량·전하 균형, 위상학적 dead-end, [MILP](../glossary.md) [gap-filling](../glossary.md), CarveMe 자동 재구축과 수동 모델 비교, [MEMOTE](../glossary.md) 리포트, 단일 유전자 결손 평가까지 한 번에 따라 합니다. 이 장 본문([5장 1절](01.md)~[6절](06.md))에서 개념으로 설명한 검사들을, 여기서는 실제로 실행되는 코드로 확인합니다.

검증 환경은 Python 3.10 이상과 COBRApy 0.30.0입니다. 구조 통계의 기준 파일은 [BiGG Models](http://bigg.ucsd.edu/models/iML1515)가 배포하는 iML1515 SBML이며, 원 논문은 [Monk et al. (2017)](https://doi.org/10.1038/nbt.3956)입니다. 2026년 7월 22일에 내려받은 `iML1515.xml.gz`의 SHA-256은 `2555e0f7e55a8cb8e770b9bb29cdaeb5db171941c414e7a232ff2d8e0228e308`이고, 압축을 푼 `iML1515.xml`은 `9c772d44ca43350e40dc7ee86c7aa148796856be1eea45e5406c6df8f7dcde28`입니다. 이 파일에서 genes 1,516, reactions 2,712, metabolites 1,877이 집계됩니다. 집계 기준은 다음과 같습니다. reactions는 경계 반응 337개(교환 331개, demand 6개)를 포함한 전체 반응 수이고, metabolites는 구획별 화학종 수(세포질 1,071 · periplasm 465 · 세포외 341)이므로 구획을 무시한 고유 화합물 수 1,169와 다릅니다. 이 수치는 종의 고정 특성이 아니라 이 release 파일의 속성이므로, 소프트웨어와 모델 release가 바뀌면 결과를 다시 기록합니다.

## 학습 목표

이 실습을 마치면 다음을 수행할 수 있습니다.

1. Karlin–Altschul E-value 식을 코드로 **구현**하고 raw score와 E-value의 지수 관계를 **검산합니다**.
2. `check_mass_balance()`로 반응별 질량·전하 불균형을 **탐지하고**, 일반 반응인지 biomass·polymer 반응인지 **분류합니다**.
3. 계수 부호만 보는 위상학적 screen으로 dead-end 대사물을 **찾아냅니다**.
4. `cobra.flux_analysis.gapfill`로 최소 반응 gap-filling을 **실행하고** 결과를 **해석합니다**.
5. CarveMe 출력과 iML1515를 동일한 구조 지표로 **비교하고**, 단일 유전자 결손으로 필수 유전자 후보를 **예측합니다**.

## 준비물

시작하기 전에 다음을 갖춥니다.

- **실행 환경**: [Chapter 11 §1의 가상환경](../chapter-11/01.md) 또는 [설치 가이드](../installation.md)를 따라 만든 Python 3.10 이상 환경. 이 실습의 모든 숫자는 COBRApy 0.30.0 + 기본 GLPK 솔버에서 얻은 값입니다.
- **필수 패키지**: `cobra`(COBRApy). 가상환경을 활성화한 뒤 `pip install "cobra==0.30.0"`으로 설치합니다. 단계 6·7의 외부 도구(CarveMe, Diamond, MEMOTE)는 해당 단계에서 별도로 설치합니다.
- **모델**: iML1515와 `textbook` 모델은 COBRApy에 내장되어 있어 `cobra.io.load_model(...)`이 자동으로 내려받습니다. 별도 다운로드가 필요 없습니다.
- **선행 지식(선택)**: 정렬 통계는 [5장 2절](02.md), gap-filling 정식화는 [5장 5절](05.md), 품질 관리 개념은 [5장 6절](06.md)에서 다룹니다. 먼저 읽지 않아도 실습은 따라올 수 있습니다.

각 단계의 코드는 위에서 아래로 순서대로 실행합니다. 특히 단계 2에서 만든 `model` 변수를 단계 3에서 그대로 사용하므로, 셀 순서를 건너뛰지 않습니다.

---

### 단계 1. E-value 식으로 정렬 점수와 유의성 검산하기

**무엇을·왜.** 게놈에서 반응을 추론하는 첫걸음은 단백질 서열을 데이터베이스와 정렬해 상동성 근거를 얻는 일입니다([5장 2절](02.md)). 그 유의성을 나타내는 값이 E-value입니다. 여기서는 Karlin–Altschul 식 $$E=Kmn\,e^{-\lambda S}$$의 지수 관계를 임의의 매개변수로 직접 계산해, raw score가 오를 때 E-value가 어떻게 변하는지 눈으로 확인합니다. 이 코드는 NCBI BLAST의 실제 E-value를 재현하는 코드가 아니며, 실제 유효 검색공간과 통계 매개변수는 BLAST가 계산합니다.

**코드.** 아래 코드는 세 가지 raw score `S`(60, 100, 150)에 대해 E-value를 계산해 출력합니다.

```python
import math

def evalue(K, m, n, S, lam):
    """단순화된 E-value 공식(§2.2)을 그대로 구현."""
    return K * m * n * math.exp(-lam * S)

K, m, n, lam = 0.1, 300, 1e7, 0.3

for S in (60, 100, 150):
    E = evalue(K, m, n, S, lam)
    print(f"S={S:>3}: E = {E:.3e}")

# 이 매개변수에 대한 회귀 기준:
# S= 60: E = 4.569e+00
# S=100: E = 2.807e-05
# S=150: E = 8.588e-12
```

**예상 출력.**

```text
S= 60: E = 4.569e+00
S=100: E = 2.807e-05
S=150: E = 8.588e-12
```

**확인 포인트.** 세 줄이 위와 정확히 같은 값(`4.569e+00`, `2.807e-05`, `8.588e-12`)으로 나오면 성공입니다. `4.569e+00`은 4.569, `8.588e-12`는 0.000000000008588을 뜻하는 지수 표기입니다. score `S`가 커질수록 E-value가 지수적으로 **작아진다**(= 우연히 그 점수가 나올 가능성이 작아진다)는 점을 확인합니다.

**해석상의 주의.** 이 계산은 다른 항이 고정될 때 raw score가 증가하면 E-value가 지수적으로 감소함을 확인합니다. 데이터베이스 크기 `n`을 두 배로 바꾸면 E-value도 두 배가 되는지 추가로 검산할 수 있습니다.

**자주 나는 오류와 해결.** 값이 회귀 기준과 다르게 나온다면 `K, m, n, lam` 네 매개변수 중 하나를 다르게 입력했을 가능성이 큽니다. `n = 1e7`은 정수 10,000,000이 아니라 부동소수점으로 입력해야 하며, `lam`은 0.3입니다. `NameError: name 'lam' is not defined`가 나오면 대입 줄(`K, m, n, lam = ...`)을 먼저 실행하지 않은 것입니다.

### 단계 2. 반응의 질량·전하 균형 점검하기

**무엇을·왜.** 내부 생화학 반응은 양변의 원소 수와 전하가 같아야 합니다. 균형이 깨진 반응은 외부 공급 없이 원자나 전하를 만들어 내므로 모델의 신뢰성을 떨어뜨립니다([5장 6절](06.md)). COBRApy는 각 `Reaction` 객체의 `check_mass_balance()` 메서드로 반응별 원소·전하 불균형을 확인합니다. 여기서는 iML1515 전체 모델에서 내부 반응을 점검합니다.

**코드.** 이 코드는 모델을 불러온 뒤 경계(교환·유입) 반응을 제외하고 모든 내부 반응의 균형을 검사해, 불균형 반응의 개수와 처음 몇 건을 출력합니다.

```python
import cobra

model = cobra.io.load_model("iML1515")

unbalanced = {}
for rxn in model.reactions:
    if rxn.boundary:          # 교환/유입 반응은 정의상 불균형이므로 제외
        continue
    imbalance = rxn.check_mass_balance()
    if imbalance:
        unbalanced[rxn.id] = imbalance

print(f"질량/전하 불균형 반응 수: {len(unbalanced)} / {len(model.reactions)}")
for rxn_id, diff in list(unbalanced.items())[:5]:
    print(f"  {rxn_id}: {diff}")
```

**예상 출력.** COBRApy 0.30이 제공하는 iML1515에서는 불균형 반응이 3건 보고됩니다. 첫 줄이 다음과 같이 나오고, 이어서 반응별 불균형 내역이 최대 5줄 출력됩니다.

```text
질량/전하 불균형 반응 수: 3 / 2712
  ...
```

**확인 포인트.** 첫 줄의 개수가 `3 / 2712`이면 성공입니다. `check_mass_balance()`가 반환하는 딕셔너리에 `'charge'` 키가 포함되어 있으면 전하 균형도 함께 깨진 것입니다.

**해석상의 주의.** 보고된 3건 중 2건은 조성을 모아 쓰는 biomass 의사반응이고, `PUACGAMS`의 `R`은 고정된 원소가 아닌 generic side group입니다. 따라서 반환값이 있다고 곧바로 큐레이션 오류로 판정하지 말고, **일반 화학반응인지 biomass·polymer·generic-formula 반응인지** 먼저 분류해야 합니다. 결과 수는 release와 COBRApy 버전에 따라 달라질 수 있으며, 일반 반응에서 발견된 H$$_2$$O·H$$^+$$·cofactor 누락과 화학식 오류는 `metabolites`와 근거 문헌을 재검토합니다.

**자주 나는 오류와 해결.** `ModuleNotFoundError: No module named 'cobra'`가 나오면 가상환경이 활성화되지 않았거나 COBRApy가 설치되지 않은 것입니다([준비물](#준비물) 참조). `cobra.io.load_model("iML1515")`은 처음 실행 시 모델을 내려받으므로 인터넷 연결이 필요합니다. 오프라인 환경이라면 미리 받아 둔 SBML 파일을 `cobra.io.read_sbml_model("경로.xml")`로 불러옵니다.

### 단계 3. Dead-end 대사물로 연결성 검증하기

**무엇을·왜.** dead-end 대사물은 네트워크에서 생성만 되거나 소비만 되어 정상상태에서 균형을 맞출 수 없는 대사물입니다([5장 5절](05.md)). 이런 대사물이 있으면 관련 반응이 flux를 나를 수 없어 모델 기능이 막힙니다. 여기서는 각 대사물이 참여하는 내부 반응의 **계수 부호만** 보고 생산/소비 반응이 하나도 없는 대사물을 빠르게 찾습니다. 이 코드는 단계 2에서 만든 `model` 변수를 그대로 사용합니다.

**코드.** 이 코드는 각 대사물에 대해 생산(계수 > 0)·소비(계수 < 0) 반응 수를 세어, 어느 한쪽이 0인 대사물을 dead-end로 수집합니다.

```python
def find_dead_end_metabolites(model):
    """비-경계 반응 기준으로 생산 또는 소비가 전혀 없는 대사물을 찾는다."""
    dead_ends = []
    for met in model.metabolites:
        internal_rxns = [r for r in met.reactions if not r.boundary]
        if not internal_rxns:
            continue
        producing = sum(1 for r in internal_rxns if r.metabolites[met] > 0)
        consuming = sum(1 for r in internal_rxns if r.metabolites[met] < 0)
        if producing == 0:
            dead_ends.append((met.id, met.name, "생산 불가(SOURCE 없음)"))
        elif consuming == 0:
            dead_ends.append((met.id, met.name, "소비 불가(SINK 없음)"))
    return dead_ends

dead_ends = find_dead_end_metabolites(model)
print(f"Dead-end 대사물 수: {len(dead_ends)}")
```

**예상 출력.** 출력은 다음 형식의 한 줄입니다. 정확한 개수는 모델 release에 따라 달라집니다.

```text
Dead-end 대사물 수: <정수>
```

**확인 포인트.** `Dead-end 대사물 수:` 뒤에 정수가 출력되면 성공입니다. `dead_ends` 리스트를 출력해 보면 각 항목이 `(대사물 ID, 이름, 사유)` 형태로, "생산 불가" 또는 "소비 불가" 중 어느 쪽인지 확인할 수 있습니다.

**해석상의 주의.** 이 코드는 계수 부호만 보는 **빠른 위상학적 screen**입니다. 가역 반응과 실제 bounds까지 고려한 producibility/consumability 또는 blocked-reaction 판정은 FVA·flux-consistency 알고리즘으로 별도 확인해야 합니다.

**자주 나는 오류와 해결.** `NameError: name 'model' is not defined`가 나오면 단계 2의 코드를 먼저 실행하지 않은 것입니다. 이 단계는 단계 2에서 만든 `model`을 재사용하므로, 새 세션에서 시작했다면 단계 2의 `cobra.io.load_model("iML1515")`부터 다시 실행합니다.

### 단계 4. MILP gap-filling으로 누락 반응 채우기

**무엇을·왜.** 초안 모델이 필요한 대사물을 만들지 못하면, 후보 반응 집합에서 최소한의 반응을 추가해 기능을 회복시키는 절차가 gap-filling입니다([5장 5절](05.md)). COBRApy는 이를 `cobra.flux_analysis.gapfill` 함수로 제공합니다. PGI를 제거해도 *E. coli*는 pentose phosphate pathway로 우회해 성장할 수 있으므로, PGI 제거를 "성장 불능 갭" 예제로 쓰면 재현되지 않습니다. 아래는 누락 반응이 정확히 하나인 최소 모델로 원리를 검증합니다.

**코드.** 이 코드는 (1) 전구체 B를 만들 수 없어 성장률이 0인 초안 모델을 만들고, (2) 유일한 후보 반응 `A → B`를 담은 universal 모델을 준비한 뒤, (3) `gapfill`로 성장을 회복시키는 최소 반응 집합을 찾아 추가합니다.

```python
from cobra import Model, Reaction, Metabolite
from cobra.flux_analysis import gapfill

# Draft: A는 공급되지만 biomass 전구체 B를 만드는 반응이 없다.
draft = Model("draft_gap")
a = Metabolite("a_c", compartment="c")
b = Metabolite("b_c", compartment="c")

source_a = Reaction("SOURCE_A")
source_a.bounds = (0, 10)
source_a.add_metabolites({a: 1})

biomass = Reaction("BIOMASS")
biomass.bounds = (0, 1000)
biomass.add_metabolites({b: -1})

draft.add_reactions([source_a, biomass])
draft.objective = biomass
print("Gap-filling 전:", draft.slim_optimize())  # 0.0

# Universal DB에는 누락 후보 A -> B만 둔다.
universal = Model("universal")
r_ab = Reaction("R_AB")
r_ab.bounds = (0, 1000)
r_ab.add_metabolites({
    Metabolite("a_c", compartment="c"): -1,
    Metabolite("b_c", compartment="c"): 1,
})
universal.add_reactions([r_ab])

solutions = gapfill(
    draft, universal, lower_bound=0.1,
    demand_reactions=False, exchange_reactions=False, iterations=1,
)
print([rxn.id for rxn in solutions[0]])  # ['R_AB']

with draft:
    draft.add_reactions(solutions[0])
    print("Gap-filling 후:", draft.slim_optimize())  # 10.0
```

**예상 출력.**

```text
Gap-filling 전: 0.0
['R_AB']
Gap-filling 후: 10.0
```

**확인 포인트.** 세 줄이 위와 같이 `0.0` → `['R_AB']` → `10.0`으로 나오면 성공입니다. gap-filling 전에는 전구체 B를 만들 방법이 없어 성장률이 0이고, 후보 반응 `R_AB` 하나를 추가하면 성장률이 회복(10.0)됩니다.

**해석상의 주의.** `gapfill`은 지정한 조건에서 최소 biomass flux를 회복시키는 후보 집합을 반환합니다. `iterations`를 늘려 얻는 여러 해는 대안 후보이며 서로 독립적인 증거가 아닙니다. 추가 반응은 서열·문헌 근거와 새로운 cycle을 검토하고, [GPR](../chapter-3/README.md)을 확인할 수 없으면 gap-filled hypothesis로 표시합니다.

**자주 나는 오류와 해결.** `gapfill`은 내부적으로 MILP 솔버를 사용합니다. 기본 GLPK로도 이 최소 예제는 즉시 풀리지만, `Infeasible` 관련 오류가 나면 `lower_bound=0.1`(회복시킬 최소 성장률)이 코드 그대로인지, 후보 반응 `R_AB`의 bounds가 `(0, 1000)`인지 확인합니다. `with draft:` 블록은 반응 추가를 임시로 적용했다가 블록을 벗어나면 되돌리므로, 원본 `draft`는 변경되지 않습니다.

### 단계 5. CarveMe 자동 재구축과 수동 모델 비교하기

**무엇을·왜.** 자동 재구축 도구는 초안 모델을 빠르게 만들어 주지만, 그 출력이 곧 검증된 모델은 아닙니다([5장 4절](04.md)). 여기서는 CarveMe로 초안을 만들고, 그 결과를 수동 큐레이션 모델인 iML1515와 **동일한 구조 지표**(유전자·반응·대사물 수, GPR coverage)로 비교합니다. CarveMe 1.6 문서에서 첫 위치 인자는 기본적으로 단백질 FASTA입니다. Diamond와 MILP solver가 필요합니다. 검증된 M9 생장을 요구하려면 `--gapfill`, 출력 모델의 초기 배지를 M9로 설정하려면 `--init`을 사용합니다. 두 옵션은 서로 다른 기능입니다.

{% hint style="warning" %}
**외부 입력과 별도 도구:** `genome.faa`는 대상 생물의 protein FASTA이며 이 저장소에는 포함되어 있지 않습니다. 입력 FASTA의 accession·checksum과 CarveMe·Diamond·solver 버전을 기록합니다.
{% endhint %}

**명령·코드.** 먼저 터미널에서 CarveMe와 Diamond를 설치하고 초안 모델을 만듭니다.

```bash
pip install carveme
conda install -c bioconda diamond

# 유전적 증거만으로 재구축(특정 배지 gap-filling 없음)
carve genome.faa -o draft_model.xml

# M9 생장을 gap-fill하고, M9를 출력 모델의 초기 배지로 설정
carve genome.faa -o draft_m9.xml -g M9 -i M9
```

이어서 Python에서 두 모델의 구조 지표를 같은 함수로 요약해 나란히 출력합니다.

```python
"""동일한 구조 지표로 CarveMe 출력과 iML1515를 비교한다."""

def summarize_model(m, label):
    gpr_coverage = sum(1 for r in m.reactions if r.gene_reaction_rule) / len(m.reactions)
    return {
        "label": label, "genes": len(m.genes), "reactions": len(m.reactions),
        "metabolites": len(m.metabolites),
        "gpr_coverage_%": round(gpr_coverage * 100, 1),
    }

manual_model = cobra.io.load_model("iML1515")
draft_model = cobra.io.read_sbml_model("draft_model.xml")  # CarveMe 출력 예시 경로

for stats in (summarize_model(manual_model, "수동 큐레이션 (iML1515)"),
              summarize_model(draft_model, "CarveMe 자동 재구축")):
    print(stats)
```

**예상 출력.** 두 줄이 각각 딕셔너리 형태로 출력됩니다. iML1515 줄은 `genes` 1516, `reactions` 2712, `metabolites` 1877을 담고, CarveMe 줄의 값은 입력 게놈에 따라 달라집니다.

```text
{'label': '수동 큐레이션 (iML1515)', 'genes': 1516, 'reactions': 2712, 'metabolites': 1877, 'gpr_coverage_%': ...}
{'label': 'CarveMe 자동 재구축', 'genes': ..., 'reactions': ..., 'metabolites': ..., 'gpr_coverage_%': ...}
```

**확인 포인트.** 두 모델의 지표가 한 줄씩, 같은 키(`genes`, `reactions`, `metabolites`, `gpr_coverage_%`)로 출력되면 성공입니다.

**해석상의 주의.** 반응 수와 GPR coverage는 구조 지표일 뿐 품질 순위가 아닙니다. 성장률을 비교하려면 두 모델의 교환 반응을 정규화하고 동일한 배지, uptake bounds, objective 및 maintenance를 적용합니다. 명령행 정의는 [CarveMe 1.6 사용 문서](https://carveme.readthedocs.io/en/latest/usage.html)를 참조합니다.

**자주 나는 오류와 해결.** `FileNotFoundError: draft_model.xml`은 CarveMe를 아직 실행하지 않았거나 파일 경로가 다른 경우입니다. `genome.faa`는 직접 준비해야 하는 외부 파일이므로, 없으면 `carve` 명령이 실패합니다. `carve: command not found`는 CarveMe가 설치되지 않았거나 가상환경 밖에 설치된 경우이며, Diamond가 없으면 정렬 단계에서 오류가 납니다. Python 비교 코드는 단계 2에서 `import cobra`를 실행한 뒤라야 `cobra`를 사용할 수 있습니다.

### 단계 6. MEMOTE 리포트 생성하기

**무엇을·왜.** MEMOTE는 대사 모델의 구조·일관성·주석을 표준화된 시험으로 평가하고, 버전 관리·지속적 통합(CI)에 연결할 수 있는 도구입니다([5장 6절](06.md)). 여기서는 모델 파일에 대해 스냅샷 HTML 리포트를 만들거나 콘솔에서 전체 테스트를 실행하는 명령을 익힙니다.

**명령.** 아래 명령은 터미널에서 실행합니다. 옵션은 model 경로 **앞에** 둡니다.

```bash
# 설치: pip install memote

# 1) 스냅샷 HTML 리포트 생성(옵션은 model 경로 앞에 둔다)
memote report snapshot --filename report.html model.xml

# 2) HTML 없이 전체 테스트를 콘솔에서 실행
memote run model.xml

# 3) traceback을 줄인 콘솔 실행(pytest 인자 전달)
memote run -a "--tb no" model.xml

# 새 전용 모델 저장소를 대화형으로 만들 때만 사용
memote new
```

**예상 출력.** `memote report snapshot`은 현재 폴더에 `report.html` 파일을 생성합니다. 이 파일을 브라우저로 열면 범주별 점수와 개별 시험 결과를 볼 수 있습니다. `memote run`은 콘솔에 통과·실패 시험 목록을 출력합니다.

**확인 포인트.** `report.html`이 생성되고 브라우저에서 Basic·Biomass·Consistency·Annotation 범주가 보이면 성공입니다.

**해석상의 주의.** `memote new`는 현재 프로젝트 안에서 가볍게 실행하는 초기화 명령이 아니라, 질문에 답해 별도의 버전 관리 모델 저장소를 만드는 명령입니다. 기존 저장소에서는 먼저 snapshot/run으로 평가하고, 그 결과를 바탕으로 CI 구성을 설계합니다. 총점에는 고정된 25/25/35/15 가중치나 보편적 합격선이 없으므로, HTML 리포트에 표시된 실제 weight·실패 테스트·버전 정보를 함께 기록합니다.

**자주 나는 오류와 해결.** `memote: command not found`는 MEMOTE가 설치되지 않은 것이므로 `pip install memote`를 실행합니다. `model.xml`은 예시 경로이므로, 실제로는 검사할 SBML 파일 이름으로 바꿉니다. 옵션(`--filename`, `-a`)을 model 경로 뒤에 두면 인식되지 않을 수 있으니 반드시 앞에 둡니다.

### 단계 7. 단일 유전자 결손으로 필수 유전자 예측하기

**무엇을·왜.** 유전자를 하나씩 제거하며 성장률이 얼마나 떨어지는지 계산하면, 성장에 꼭 필요한 필수(essential) 유전자를 예측할 수 있습니다([5장 6절](06.md)). 계산량을 줄이기 위해 iML1515 대신 137 genes를 포함한 COBRApy `textbook` 모델을 사용합니다. 이 결과는 교육용 core model의 기본 조건에 대한 값이며 iML1515의 필수성 성능으로 해석하지 않습니다.

**코드.** 이 코드는 야생형 성장률을 구한 뒤, 모든 유전자를 하나씩 결손시키며 성장률을 계산하고, 야생형의 5%(theta=0.05) 미만으로 떨어지는 유전자를 필수로 판정합니다.

```python
import cobra
from cobra.flux_analysis import single_gene_deletion

model = cobra.io.load_model("textbook")
wt_growth = model.slim_optimize()

theta = 0.05
threshold = theta * wt_growth

result = single_gene_deletion(model, processes=1)   # 모든 유전자를 하나씩 결손시키며 성장률 계산
result["ratio"] = result["growth"] / wt_growth
predicted_essential = result[result["growth"] < threshold]

# COBRApy의 단일 결손 결과는 유전자 ID를 index가 아니라 `ids` 열의
# 한 원소짜리 frozenset으로 저장한다.
def extract_single_gene_id(ids):
    if len(ids) != 1:
        raise ValueError(f"단일 유전자 결손이 아닌 결과: {ids}")
    return next(iter(ids))

result["gene_id"] = result["ids"].map(extract_single_gene_id)
predicted_essential_ids = set(
    result.loc[result["growth"] < threshold, "gene_id"]
)

print(f"야생형 성장률: {wt_growth:.3f} /h")
print(f"필수성 임계값(theta=0.05 x WT): {threshold:.4f} /h")
print(f"예측된 essential 유전자 수: {len(predicted_essential)} / {len(model.genes)}")
# COBRApy 0.30.0, GLPK, 기본 bounds, processes=1의 회귀 기준:
# 야생형 성장률 약 0.874 /h, theta=0.05에서 predicted essential genes 5개.
```

**예상 출력.**

```text
야생형 성장률: 0.874 /h
필수성 임계값(theta=0.05 x WT): 0.0437 /h
예측된 essential 유전자 수: 5 / 137
```

**확인 포인트.** 야생형 성장률이 약 `0.874 /h`, 예측된 필수 유전자가 `5 / 137`이면 성공입니다. 솔버와 버전에 따라 소수점 자리는 조금 달라질 수 있습니다.

**해석상의 주의.** Sensitivity, specificity, precision 및 F1을 계산하려면 동일한 균주·배지의 실험 필수성 자료가 필요합니다. 이 저장소에는 해당 자료가 없으므로 다음 함수는 ID 집합이 준비된 뒤에만 사용합니다.

```python
def confusion_matrix_metrics(predicted_essential_ids, true_essential_ids, all_gene_ids):
    """양성 class를 essential gene으로 둔 분류 지표."""
    predicted, true_set, all_set = (
        set(predicted_essential_ids), set(true_essential_ids), set(all_gene_ids))

    tp = len(predicted & true_set)
    fn = len(true_set - predicted)
    fp = len(predicted - true_set)
    tn = len(all_set - predicted - true_set)

    sensitivity = tp / (tp + fn) if (tp + fn) else float("nan")
    specificity = tn / (tn + fp) if (tn + fp) else float("nan")
    precision = tp / (tp + fp) if (tp + fp) else float("nan")
    f1 = (2 * precision * sensitivity / (precision + sensitivity)
          if (precision + sensitivity) else float("nan"))
    return {"TP": tp, "FN": fn, "FP": fp, "TN": tn,
            "sensitivity": sensitivity, "specificity": specificity,
            "precision": precision, "F1": f1}

# 사용 예(true_essential_ids는 조건이 일치하는 실험 자료에서 가져온다):
# metrics = confusion_matrix_metrics(
#     predicted_essential_ids=predicted_essential_ids,
#     true_essential_ids=true_essential_ids,   # 실제 데이터로 채울 것
#     all_gene_ids=[g.id for g in model.genes],
# )
# print(metrics)
```

실험 데이터와 모델의 유전자 식별자 체계가 다르면 명시적인 ID mapping을 적용하고, mapping되지 않은 항목을 분모에서 어떻게 처리했는지 보고합니다. Mapping 실패를 임의로 음성으로 간주하면 모든 분류 지표가 왜곡될 수 있습니다.

**자주 나는 오류와 해결.** `single_gene_deletion` 결과는 유전자 ID를 DataFrame의 index가 아니라 `ids` 열의 한 원소짜리 frozenset으로 저장합니다. 그래서 위 코드는 `extract_single_gene_id`로 frozenset에서 ID를 꺼냅니다. `KeyError: 'gene_id'`가 나면 이 변환 줄을 건너뛴 것입니다. `processes=1`은 재현성을 위해 단일 프로세스로 고정하는 인자이므로 지우지 마십시오. COBRApy 0.30.0의 기본값은 사용 가능한 코어 수만큼 병렬 실행하는 것이어서, 환경에 따라 워커 생성(spawn)이 실패하거나 출력이 흔들릴 수 있습니다. 실행이 느리게 느껴지면 `textbook` 모델(137 genes)을 쓰고 있는지 확인합니다. iML1515(1,516 genes)로 바꾸면 시간이 크게 늘어납니다.

---

## 정리

이 실습에서는 다음을 직접 실행했습니다.

- Karlin–Altschul E-value 식을 구현해 raw score와 유의성의 지수 관계를 검산했습니다(단계 1).
- iML1515에서 질량·전하 불균형 반응 3건을 찾아, biomass·generic-formula 반응과 일반 반응을 구분하는 판단을 연습했습니다(단계 2).
- 계수 부호만 보는 빠른 screen으로 dead-end 대사물을 탐색했습니다(단계 3).
- 최소 예제로 MILP gap-filling을 실행해 성장률이 0.0에서 10.0으로 회복되는 과정을 확인했습니다(단계 4).
- CarveMe 자동 재구축과 iML1515를 동일 지표로 비교하고, MEMOTE 리포트로 표준 품질 시험을 실행했으며, `textbook` 모델에서 필수 유전자 5개를 예측했습니다(단계 5~7).

이 과정에서 반복해 확인한 원칙은, **자동 도구의 출력이나 계산 결과는 검증의 출발점일 뿐 최종 결론이 아니라는** 점입니다. 각 지표는 근거·버전·조건과 함께 기록해야 재현 가능한 품질 판단이 됩니다.

## 스스로 해보기

1. **데이터베이스 크기 효과 검산.** 단계 1에서 `n`을 `1e7`에서 `2e7`로 바꾸면 세 E-value가 정확히 두 배가 되는지 확인해 보십시오. 식 $$E=Kmn\,e^{-\lambda S}$$에서 왜 그런지 함께 설명해 봅니다.
2. **dead-end 목록 살펴보기.** 단계 3의 `dead_ends` 리스트를 출력해, "생산 불가"와 "소비 불가" 항목이 각각 몇 개인지 세어 보십시오. 어떤 대사물이 어느 쪽에 속하는지 몇 개만 이름으로 확인해 봅니다.
3. **필수성 임계값 바꿔 보기.** 단계 7에서 `theta`를 0.05에서 0.01로 낮추면 예측된 필수 유전자 수가 어떻게 달라지는지 관찰하십시오. 임계값을 엄격하게(낮게) 잡으면 필수로 판정되는 유전자가 늘어날지 줄어들지 먼저 예상한 뒤 실행해 확인합니다.

이어지는 [5장 6절](06.md)에서는 여기서 실행한 품질 시험들을 release 체크리스트와 회귀 검증 계획으로 묶는 방법을 다룹니다. 맥락 특이 모델 추출은 [Chapter 6](../chapter-6/README.md)에서 이어집니다.
