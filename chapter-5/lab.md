# 실습: COBRApy를 이용한 재구축 품질 검사

이 실습은 E-value 식의 수치 검산, 반응 균형, 위상학적 dead end, [MILP](../glossary.md) [gap-filling](../glossary.md), CarveMe 출력 비교, [MEMOTE](../glossary.md) 실행 및 단일 유전자 결손 평가를 다룬다. 검증 환경은 Python 3.10 이상과 COBRApy 0.30.0이다. iML1515의 구조 통계는 이 release에서 genes 1,516, reactions 2,712, metabolites 1,877이다. 소프트웨어와 모델 release가 바뀌면 결과를 다시 기록한다.

## 실습 0. E-value 식의 수치 검산

다음 코드는 Karlin–Altschul 식의 지수 관계를 임의의 매개변수로 계산한다. NCBI BLAST의 실제 E-value를 재현하는 코드는 아니며, 실제 유효 검색공간과 통계 매개변수는 BLAST가 계산한다.

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

이 계산은 다른 항이 고정될 때 raw score가 증가하면 E-value가 지수적으로 감소함을 확인한다. 데이터베이스 크기 `n`을 두 배로 바꾸면 E-value도 두 배가 되는지 추가로 검산할 수 있다.

## 실습 1. 질량·전하 균형 점검

COBRApy는 각 `Reaction` 객체의 `check_mass_balance()` 메서드로 반응별 원소·전하 불균형을 확인합니다. 아래는 iML1515 전체 모델에서 내부 반응을 점검하는 예입니다.

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

`check_mass_balance()`가 반환하는 딕셔너리에 `'charge'` 키가 포함되어 있으면 전하 균형도 함께 깨진 것입니다. COBRApy 0.30이 제공하는 iML1515에서는 이 코드가 3건을 보고합니다. 그중 2건은 조성을 모아 쓰는 biomass 의사반응이고, `PUACGAMS`의 `R`은 고정된 원소가 아닌 generic side group입니다. 따라서 반환값이 있다고 곧바로 큐레이션 오류로 판정하지 말고, **일반 화학반응인지 biomass·polymer·generic-formula 반응인지** 먼저 분류해야 합니다. 결과 수는 release와 COBRApy 버전에 따라 달라질 수 있으며, 일반 반응에서 발견된 H$$_2$$O·H$$^+$$·cofactor 누락과 화학식 오류는 `metabolites`와 근거 문헌을 재검토합니다.

## 실습 2. Dead-end 대사산물 탐색 (연결성 검증)

```python
def find_dead_end_metabolites(model):
    """비-경계 반응 기준으로 생산 또는 소비가 전혀 없는 대사산물을 찾는다."""
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
print(f"Dead-end 대사산물 수: {len(dead_ends)}")
```

이 코드는 계수 부호만 보는 **빠른 위상학적 screen**입니다. 가역 반응과 실제 bounds까지 고려한 producibility/consumability 또는 blocked-reaction 판정은 FVA·flux-consistency 알고리즘으로 별도 확인해야 합니다.

## 실습 3. Gap-Filling: `cobra.flux_analysis.gapfill`

COBRApy는 §5.2의 전통적 MILP gap-filling을 `cobra.flux_analysis.gapfill` 함수로 제공합니다. PGI를 제거해도 *E. coli*는 pentose phosphate pathway로 우회해 성장할 수 있으므로, PGI 제거를 "성장 불능 갭" 예제로 쓰면 재현되지 않습니다. 아래는 누락 반응이 정확히 하나인 최소 모델로 원리를 검증합니다.

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

`gapfill`은 지정한 조건에서 최소 biomass flux를 회복시키는 후보 집합을 반환한다. `iterations`를 늘려 얻는 여러 해는 대안 후보이며 서로 독립적인 증거가 아니다. 추가 반응은 서열·문헌 근거와 새로운 cycle을 검토하고, [GPR](../chapter-3/README.md)을 확인할 수 없으면 gap-filled hypothesis로 표시한다.

## 실습 4. CarveMe 자동 재구축과 수동 모델 비교

CarveMe 1.6 문서에서 첫 위치 인자는 기본적으로 단백질 FASTA이다. Diamond와 MILP solver가 필요하다. 검증된 M9 생장을 요구하려면 `--gapfill`, 출력 모델의 초기 배지를 M9로 설정하려면 `--init`을 사용한다. 두 옵션은 서로 다른 기능이다.

{% hint style="warning" %}
**외부 입력과 별도 도구:** `genome.faa`는 대상 생물의 protein FASTA이며 이 저장소에는 포함되어 있지 않다. 입력 FASTA의 accession·checksum과 CarveMe·Diamond·solver 버전을 기록한다.
{% endhint %}

```bash
pip install carveme
conda install -c bioconda diamond

# 유전적 증거만으로 재구축(특정 배지 gap-filling 없음)
carve genome.faa -o draft_model.xml

# M9 생장을 gap-fill하고, M9를 출력 모델의 초기 배지로 설정
carve genome.faa -o draft_m9.xml -g M9 -i M9
```

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

반응 수와 GPR coverage는 구조 지표일 뿐 품질 순위가 아니다. 성장률을 비교하려면 두 모델의 교환 반응을 정규화하고 동일한 배지, uptake bounds, objective 및 maintenance를 적용한다. 명령행 정의는 [CarveMe 1.6 사용 문서](https://carveme.readthedocs.io/en/latest/usage.html)를 참조한다.

## 실습 5. MEMOTE 리포트 생성하기

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

`memote new`는 현재 프로젝트 안에서 가볍게 실행하는 초기화 명령이 아니라, 질문에 답해 별도의 버전 관리 모델 저장소를 만드는 명령입니다. 기존 저장소에서는 먼저 snapshot/run으로 평가하고, 그 결과를 바탕으로 CI 구성을 설계하십시오. 총점에는 고정된 25/25/35/15 가중치나 보편적 합격선이 없으므로, HTML 리포트에 표시된 실제 weight·실패 테스트·버전 정보를 함께 기록합니다.

## 실습 6. 유전자 필수성 예측

계산량을 줄이기 위해 iML1515 대신 137 genes를 포함한 COBRApy `textbook` 모델을 사용한다. 이 결과는 교육용 core model의 기본 조건에 대한 값이며 iML1515의 필수성 성능으로 해석하지 않는다.

```python
import cobra
from cobra.flux_analysis import single_gene_deletion

model = cobra.io.load_model("textbook")
wt_growth = model.slim_optimize()

theta = 0.05
threshold = theta * wt_growth

result = single_gene_deletion(model)          # 모든 유전자를 하나씩 결손시키며 성장률 계산
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
# COBRApy 0.30.0, GLPK, 기본 bounds의 회귀 기준:
# 야생형 성장률 약 0.874 /h, theta=0.05에서 predicted essential genes 5개.
```

Sensitivity, specificity, precision 및 F1을 계산하려면 동일한 균주·배지의 실험 필수성 자료가 필요하다. 이 저장소에는 해당 자료가 없으므로 다음 함수는 ID 집합이 준비된 뒤에만 사용한다.

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

실험 데이터와 모델의 유전자 식별자 체계가 다르면 명시적인 ID mapping을 적용하고, mapping되지 않은 항목을 분모에서 어떻게 처리했는지 보고한다. Mapping 실패를 임의로 음성으로 간주하면 모든 분류 지표가 왜곡될 수 있다.

---
