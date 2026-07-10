# 실습: COBRApy로 재구축·Gap-Filling·품질 관리 수행하기

> 💡 **실습:** 아래 스니펫들은 이 장의 핵심 개념(질량/전하 균형 점검, gap-filling, MEMOTE 품질 평가)을 최소 코드로 보여줍니다. 전체 실행 가능한 예제와 데이터 준비 과정은 `raw_data/GEM_lecture_notes/gem9_w02_lab.ipynb`(재구축·gap-filling·MEMOTE)와 `gem9_w06_lab.ipynb`(인체 GEM·tINIT)를 참고하십시오. 실습 환경은 Python 3.10+, COBRApy 0.29+ 기준입니다. 1장에서 불러온 `e_coli_core`는 반응 95개짜리 교육용 축소 모델이므로, 이 장의 실습에서는 완전한 게놈 규모로 큐레이션된 iML1515(유전자 1,516·반응 2,712·대사물 1,877, 3개 구획)를 대상으로 재구축·QC 절차를 시연합니다 — 같은 대장균이지만 "교육용 축소판"과 "실전 재구축 대상"의 규모 차이를 직접 느껴보십시오.

## 실습 1. 질량·전하 균형 직접 점검하기

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

`gapfill`의 반환값은 "추가하면 biomass flux를 회복시키는 최소 반응 집합"의 리스트이며, `iterations`를 늘리면 서로 다른 대안 해(alternative optima)를 여러 개 얻어 §4.2의 합의적 모델링처럼 후보 간 교차 검증에 활용할 수 있습니다. 실무에서는 이렇게 추가된 반응이 §5.4의 gene-less 반응이 되지 않도록, 반드시 추가 BLASTP로 유전자 후보를 재검색해 GPR을 보완해야 합니다.

## 실습 4. CarveMe 자동 재구축과 수동 모델 비교

CarveMe 1.6 계열의 첫 위치 인자는 단백질 FASTA이며 `--genome` 옵션을 쓰지 않습니다. Diamond와 MILP solver도 필요합니다. 검증된 M9 생장을 강제하려면 `--gapfill`을, 출력 모델의 기본 배지를 M9로 설정하려면 `--init`을 별도로 지정합니다.

{% hint style="warning" %}
📦 **외부 자산·별도 도구 필요:** `genome.faa`는 분석할 생물의 단백질 FASTA여야 하며 이 저장소에는 포함되어 있지 않습니다. 아래 명령은 CarveMe가 설치된 별도 환경에서 실행하고, 생성된 `draft_model.xml`을 다음 Python 블록의 작업 디렉터리에 두십시오. 입력 FASTA의 출처·checksum과 CarveMe·Diamond·solver 버전도 함께 기록해야 비교를 재현할 수 있습니다.
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

반응 수가 비슷하다고 두 모델의 품질이 같은 것은 아닙니다. 성장률까지 비교하려면 먼저 두 모델의 교환 반응을 매핑하고 **동일한 배지와 uptake bounds**를 적용해야 합니다. CarveMe 공식 사용법은 [문서](https://carveme.readthedocs.io/en/latest/usage.html)를 참조하십시오.

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

---
