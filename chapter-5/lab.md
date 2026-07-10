# 실습: COBRApy로 재구축·Gap-Filling·품질 관리 수행하기

> 💡 **실습:** 아래 스니펫들은 이 장의 핵심 개념(질량/전하 균형 점검, gap-filling, MEMOTE 품질 평가)을 최소 코드로 보여줍니다. 전체 실행 가능한 예제와 데이터 준비 과정은 `raw_data/GEM_lecture_notes/gem9_w02_lab.ipynb`(재구축·gap-filling·MEMOTE)와 `gem9_w06_lab.ipynb`(인체 GEM·tINIT)를 참고하십시오. 실습 환경은 Python 3.10+, COBRApy 0.29+ 기준입니다. 1장에서 불러온 `e_coli_core`는 반응 95개짜리 교육용 축소 모델이므로, 이 장의 실습에서는 완전한 게놈 규모로 큐레이션된 iML1515(유전자 1,516·반응 2,712·대사물 1,877, 3개 구획)를 대상으로 재구축·QC 절차를 시연합니다 — 같은 대장균이지만 "교육용 축소판"과 "실전 재구축 대상"의 규모 차이를 직접 느껴보십시오.

## 실습 0. 계산기로 손 계산 검산하기 — E-value 공식

본격적인 COBRApy 실습에 앞서, §2.2의 E-value 손 계산을 그대로 코드로 옮겨 검산해봅시다. 이렇게 손 계산과 코드가 같은 결과를 내는지 직접 확인하는 습관은, 이후 복잡한 MILP 결과를 "블랙박스로만" 믿지 않고 검증하는 태도로 이어집니다.

```python
import math

def evalue(K, m, n, S, lam):
    """단순화된 E-value 공식(§2.2)을 그대로 구현."""
    return K * m * n * math.exp(-lam * S)

K, m, n, lam = 0.1, 300, 1e7, 0.3

for S in (60, 100, 150):
    E = evalue(K, m, n, S, lam)
    print(f"S={S:>3}: E = {E:.3e}")

# 기대 출력:
# S= 60: E = 4.569e+00
# S=100: E = 2.807e-05
# S=150: E = 8.588e-12
```

세 값 모두 §2.2 본문에서 손으로 계산한 근사치(각각 약 4.5, 약 $$2.8\times10^{-5}$$, 약 $$8.7\times10^{-12}$$)와 자릿수 수준에서 일치합니다 — 손 계산은 중간 반올림을 여러 번 거쳤으므로 정밀한 코드 결과와 소수점 이하 몇 자리는 다를 수 있지만, 핵심 결론("점수가 조금 오르면 E-value가 몇 자릿수씩 떨어진다")은 동일하게 확인됩니다. `evalue` 함수의 `S`만 바꿔가며 실행해보면, 점수가 조금만 올라가도 E-value가 왜 그렇게 급격히 떨어지는지(지수함수의 효과) 직접 체감할 수 있습니다.

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

## 실습 6. §1.1 벤치마크 다시 만들어보기 — 유전자 필수성 예측

§1.1과 §6.3에서 손으로 계산했던 필수성 판정식과 confusion matrix를 COBRApy로 직접 재현해봅시다. `e_coli_core`는 유전자 137개뿐이라 전수 결손 계산이 몇 초 안에 끝나므로, 이 실습에는 iML1515 대신 `e_coli_core`를 사용합니다.

```python
import cobra
from cobra.flux_analysis import single_gene_deletion

model = cobra.io.load_model("e_coli_core")
wt_growth = model.slim_optimize()

theta = 0.05
threshold = theta * wt_growth

result = single_gene_deletion(model)          # 모든 유전자를 하나씩 결손시키며 성장률 계산
result["ratio"] = result["growth"] / wt_growth
predicted_essential = result[result["growth"] < threshold]

print(f"야생형 성장률: {wt_growth:.3f} /h")
print(f"필수성 임계값(theta=0.05 x WT): {threshold:.4f} /h")
print(f"예측된 essential 유전자 수: {len(predicted_essential)} / {len(model.genes)}")
# 기대 출력: 야생형 성장률은 약 0.874 /h로 Chapter 4에서 계산한 값과 일치합니다.
# 예측 essential 유전자 수는 솔버·COBRApy 버전에 따라 소폭 달라질 수 있으므로
# 정확한 개수 대신 "0보다 크고 137보다 훨씬 작다"는 자릿수만 확인해도 충분합니다.
```

이렇게 얻은 예측 결과를 §1.1·§6.3의 confusion matrix 공식(Sensitivity, Specificity, Precision, F1)에 대입하려면, 비교 대상이 될 **실제 실험 필수성 데이터**(예: Keio collection 같은 단일 유전자 결손 라이브러리)가 별도로 필요합니다. 이 저장소에는 그런 실험 데이터가 포함되어 있지 않으므로, 아래는 "실제 데이터가 주어졌을 때 지표를 계산하는 방법"만 보여주는 뼈대 코드입니다.

```python
def confusion_matrix_metrics(predicted_essential_ids, true_essential_ids, all_gene_ids):
    """§1.1/§6.3의 공식을 그대로 코드로 옮긴 것."""
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

# 사용 예(true_essential_ids는 사용자가 실제 실험 데이터에서 가져와야 함):
# metrics = confusion_matrix_metrics(
#     predicted_essential_ids=predicted_essential.index,
#     true_essential_ids=true_essential_ids,   # 실제 데이터로 채울 것
#     all_gene_ids=[g.id for g in model.genes],
# )
# print(metrics)
```

이 뼈대 함수는 §6.3에서 손으로 계산했던 iML1515 confusion matrix 예시(TP=270, FN=26, FP=30, TN=1190)를 그대로 입력하면 Sensitivity≈0.91, Specificity≈0.98과 같은 결과를 재현하는지 검산하는 용도로도 쓸 수 있습니다 — 코드와 손 계산이 일치하는지 서로 검증하는 습관을 들이십시오.

---
