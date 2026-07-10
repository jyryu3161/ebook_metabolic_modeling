# 💡 실습: 항암 표적 예측과 대사 정상화 파이프라인

> 아래 스니펫들은 핵심 로직을 보여주는 발췌본입니다. 전체 실행 가능한 노트북은 `gem9_w07_lab.ipynb`(항암 표적 예측: 시뮬레이션 TCGA 데이터, 맥락 특이적 모델, 선택성 필터, SL 탐색, DepMap 검증)와 `gem9_w08_lab.ipynb`(MTA: iMAT 베이스라인, 반응 분류, 체계적 KO, Transformation Score, MTA vs MOMA/ROOM 비교)를 참고하십시오. 맥락 특이적 모델 구축·RNA-seq 전처리 실습은 [Chapter 6](../chapter-6/README.md)에, gene KO 메커니즘 실습은 [Chapter 8](../chapter-8/README.md)에 있습니다.

이 실습의 다섯 블록은 §3~§6에서 배운 이론을 순서대로 따라갑니다 — 실습 1~2는 §3(필수성·선택성), 실습 3은 §4(합성 치사), 실습 4는 §3.6(DepMap 검증), 실습 5는 §6(MTA 파이프라인)에 대응합니다. 각 블록을 실행하기 전에 해당 절의 수식과 코드를 먼저 복습하면, 아래 실행 결과의 숫자가 어떤 계산에서 나온 것인지 훨씬 쉽게 따라갈 수 있습니다.

{% hint style="warning" %}
📦 **외부 자산 필요:** 실습 1–4는 이 저장소에 포함되지 않은 `cancer_model.xml`, `matched_normal_model.xml`, `Achilles_gene_effect.csv`와 앞 절에서 정의한 보조 함수가 필요합니다. 따라서 아래 블록은 파일 형식과 분석 순서를 보여 주는 **워크플로 골격**입니다. 파일 없이 처음부터 실행하려면 [Chapter 10의 완전 실행형 COBRApy 튜토리얼](../chapter-10/README.md)을 먼저 진행하십시오. 실습 5는 별도로 표시한 의사코드입니다.
{% endhint %}

## 실습 1: 단일 유전자 KO 스크리닝과 표적 랭킹

이 실습은 §3.3의 `calculate_ko_effect()`와 `rank_targets()`를 모델의 **모든** 유전자에 대해 반복 실행하여, 전체 유전자를 상대 성장률 순으로 정렬한 표를 만듭니다. `try/except`로 감싸는 이유에 주목하십시오 — 일부 유전자는 KO 시 LP가 infeasible해지거나 예외를 일으킬 수 있으므로, 전체 스크리닝이 한 유전자의 오류 때문에 중단되지 않도록 방어적으로 처리합니다.

**실행 조건:** 📦 외부 SBML · 🔗 §3.3 함수 필요

```python
import cobra, pandas as pd
from cobra.flux_analysis import single_gene_deletion

model = cobra.io.read_sbml_model("cancer_model.xml")  # Ch.6에서 구축한 맥락 특이적 모델

results = []
for gene in model.genes:
    try:
        r = calculate_ko_effect(model, gene.id, method='fba')  # §3.3 정의
        results.append(r)
    except Exception as e:
        print(f"Error for gene {gene.id}: {e}")

results_df = pd.DataFrame(results)
top_targets = rank_targets(results_df, top_n=50)  # §3.3 정의
print(top_targets[['gene_id', 'relative_growth', 'reduction_percent', 'is_lethal']].head(10))
# 실제 상위 유전자는 사용한 모델 버전·배지·목적함수에 따라 달라진다.
```

## 실습 2: 선택성 필터와 IDH1 돌연변이 통합

이 실습은 세 단계로 구성됩니다 — 정상 모델에 같은 KO 스크리닝을 반복하고(§3.3), 두 결과를 합쳐 §3.5의 선택성 지수를 계산하고, 마지막으로 §1.4에서 정의한 IDH1 R132H 네오몰픽 돌연변이를 모델에 주입해 생물량 변화를 확인합니다. 세 번째 단계가 앞의 두 단계와 독립적으로 보일 수 있지만, 실제 연구에서는 "이 돌연변이 배경의 암세포에서 어떤 유전자가 선택적으로 필수인가"를 물을 때 1~3단계를 순서대로 연결해서 사용합니다 — 즉 `mutant_model`을 만든 뒤 그 모델에 다시 실습 1의 스크리닝을 돌리는 식으로 확장할 수 있습니다.

**실행 조건:** 📦 정상·암 SBML · 🔗 실습 1 및 앞 절 함수 필요

```python
# 1. 정상 모델에도 동일한 KO 스크리닝 적용
normal_model = cobra.io.read_sbml_model("matched_normal_model.xml")
normal_results = pd.DataFrame(
    [calculate_ko_effect(normal_model, g.id) for g in normal_model.genes]
)

# 2. 암-정상 선택성 계산 (§3.5)
selective_targets = calculate_selectivity(results_df, normal_results)
print(f"선택적 표적 수: {len(selective_targets)}")

# 3. IDH1 R132H 돌연변이 통합 후 재스크리닝 (§1.4)
mutant_model = integrate_idh1_mutation(model, 'R132H')
mutant_solution = mutant_model.optimize()
print(f"IDH1-R132H 모델 생물량: {mutant_solution.objective_value:.4f}")
```

## 실습 3: 합성 치사 쌍 탐색

**실행 조건:** 📦 외부 SBML · 🔗 §4.3 함수 필요

이 실습은 모델 전체 유전자가 아니라 처음 100개(`model.genes[:100]`)만 후보로 사용한다는 점에 주의하십시오. §4.5에서 배웠듯 이중 KO 탐색은 $$\binom{N}{2}$$로 조합이 늘어나므로, 실습에서는 계산 시간을 줄이기 위해 후보를 미리 좁혔습니다. 실제 연구에서는 이 100개를 무작위로 고르는 대신, 실습 1의 단일 KO 스크리닝에서 "부분적으로만 성장에 영향을 주는(치명적이지 않은)" 유전자들을 우선 후보로 골라 탐색 효율을 높입니다.

```python
sl_pairs = find_synthetic_lethal_pairs(
    model,
    candidate_genes=[g.id for g in model.genes[:100]],
    method='fba', lethal_threshold=0.01
)
print(f"발견된 SL 쌍 수: {len(sl_pairs)}")
print(sl_pairs.head(10))
```

## 실습 4: DepMap 기반 검증

**실행 조건:** 📦 DepMap CSV · 🔗 실습 1 결과 필요

이 실습은 실습 1에서 만든 예측(`results_df`의 `reduction_percent`)을 실제 CRISPR 실험 데이터(DepMap Achilles)와 대조합니다. §3.6에서 강조했듯 gene-effect 점수는 **더 음수일수록 더 강한 의존성**을 뜻하므로, "가장 의존적인 10%"를 고를 때는 상위 분위수가 아니라 **하위 분위수**(`quantile(0.10)`)를 기준으로 삼아야 합니다 — 이 부호 방향을 거꾸로 적용하는 실수는 초심자가 가장 흔히 저지르는 실수 중 하나입니다.

```python
gene_effect = pd.read_csv("Achilles_gene_effect.csv", index_col=0)
depmap_mcf7 = gene_effect.loc['MCF7_BREAST']

evaluation = evaluate_prediction(
    predicted_scores=results_df.set_index('gene_id')['reduction_percent'],
    depmap_essentiality=depmap_mcf7, top_percentile=10
)
print(f"ROC-AUC: {evaluation['roc_auc']:.3f}, Precision@10%: {evaluation['precision_at_k']:.3f}")
```

## 실습 5: MTA 파이프라인 의사코드 (실행 코드 아님)

{% hint style="danger" %}
아래 블록은 함수 입출력과 단계 순서를 설명하는 **의사코드**입니다. `simple_v_ref()`의 FBA 해는 iMAT+sampling 평균을 대신할 수 없고, `compute_ko_transformation_score()`에는 MIQP와 원 TS 계산이 구현되어 있지 않으므로 연구 결과 생성에 실행하지 마십시오.
{% endhint %}

```python
import numpy as np
from scipy import stats

# PSEUDOCODE ONLY — 실제 계산에는 iMAT MILP, flux sampling, MIQP 구현이 필요
# Step 1: source 기준 flux를 만드는 인터페이스의 자리표시자
def simple_v_ref(model, disease_expression, percentile=50):
    threshold = np.percentile(disease_expression, percentile)
    high_genes = disease_expression >= threshold
    # ... GPR 매핑 후 FBA/샘플링으로 v_ref 산출 (전체 구현은 gem9_w08_lab.ipynb 참고)
    return model.optimize().fluxes  # 단순화된 자리표시자

# Step 2: 반응 분류 (§6.5 Step 2)
def classify_reactions(model, healthy_expr, disease_expr, gene_names, p_threshold=0.05):
    """t-test 기반 차등발현 → GPR 매핑 → R_S/R_F/R_B 분류"""
    pvals, logfcs = [], []
    for i in range(len(gene_names)):
        _, p = stats.ttest_ind(disease_expr[i, :], healthy_expr[i, :])
        pvals.append(p)
        logfcs.append(np.mean(disease_expr[i, :]) - np.mean(healthy_expr[i, :]))
    # GPR을 통해 유전자 수준 결과를 반응 수준(R_S=0, R_F=+1, R_B=-1)으로 매핑
    # (전체 GPR 파싱 로직은 §6.5, Chapter 6 참고)
    return pvals, logfcs

# Step 3~4: 체계적 단일 반응 KO와 Transformation Score (개념적 정의, §6.4~6.5)
def compute_ko_transformation_score(model, v_ref, R_S, R_F, R_B, ko_idx, alpha=0.66, epsilon=2.0):
    """반응 ko_idx를 KO한 뒤 MIQP 목적함수를 근사 계산 (실제 MIQP 솔버는 CPLEX/Gurobi 필요)"""
    # 결손 반응 고정 -> FBA/샘플링으로 v_ko 계산 -> R_S 페널티, R_F/R_B 보상 항 산출
    # 상세 구현: gem9_w08_lab.ipynb Section 6
    pass

# 상위 표적 랭킹 (TS 내림차순)
# ranked = results_df.sort_values('transformation_score', ascending=False)
# print(ranked.head(15)[['reaction_name', 'transformation_score', 'growth']])
```

> 위 블록은 개념 골격일 뿐입니다. 실제 계산은 검증된 MTA/rMTA 구현, MIQP를 지원하는 솔버, 샘플링 수렴 진단과 §6.4의 원 TS 정의를 사용해야 합니다. 노트북의 단순화 구현도 원 알고리즘과 동일한지 별도로 대조하십시오.

이 의사코드가 왜 "실행 코드가 아님"이라고 강조되는지 다시 짚어봅시다. `simple_v_ref()`는 단순히 `model.optimize().fluxes`(순수 FBA 해 하나)를 반환하지만, §6.5 Step 1이 요구하는 것은 iMAT으로 얻은 활성/비활성 패턴과 일치하는 해 공간에서 2,000개를 **샘플링한 평균**입니다. 이 둘은 수학적으로 전혀 다른 대상입니다 — 하나의 최적해와 여러 해의 평균은 같은 값이 될 이유가 없습니다. 마찬가지로 `compute_ko_transformation_score()`의 `pass`는 실제로 MIQP를 풀지 않는다는 뜻이며, 이 함수를 그대로 호출하면 아무 값도 반환하지 않습니다. 이 실습 5는 "MTA 파이프라인이 어떤 순서로, 어떤 입출력을 주고받는 함수들로 구성되는지"를 코드의 형태로 보여주는 데 목적이 있으며, 실제 연구 결과를 만들기 위해서는 각 함수를 §6.4~§6.5에서 배운 완전한 수식대로 구현하거나 검증된 rMTA 패키지를 사용해야 합니다.

{% hint style="info" %}
📌 **실습 마무리.** 실습 1~4는 §3~§4의 "죽이기" 파이프라인을, 실습 5는 §6의 "고치기" 파이프라인의 골격을 코드로 확인했습니다. 다섯 실습 모두 공통적으로 강조하는 것은 **함수 하나의 출력이 다음 단계 함수의 입력으로 정확히 이어져야 한다**는 점과, **부호·분위수·임계값 방향을 실수하면 결과가 정반대로 해석될 수 있다**는 점입니다(특히 실습 4의 DepMap 분위수 방향). 이 장의 [요약 페이지](summary.md)에서 전체 개념을 다시 정리해 보십시오.
{% endhint %}

---
