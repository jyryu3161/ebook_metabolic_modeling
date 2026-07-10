# 💡 실습: 항암 표적 예측과 대사 정상화 파이프라인

> 아래 스니펫들은 핵심 로직을 보여주는 발췌본입니다. 전체 실행 가능한 노트북은 `gem9_w07_lab.ipynb`(항암 표적 예측: 시뮬레이션 TCGA 데이터, 맥락 특이적 모델, 선택성 필터, SL 탐색, DepMap 검증)와 `gem9_w08_lab.ipynb`(MTA: iMAT 베이스라인, 반응 분류, 체계적 KO, Transformation Score, MTA vs MOMA/ROOM 비교)를 참고하십시오. 맥락 특이적 모델 구축·RNA-seq 전처리 실습은 [Chapter 6](../chapter-6/README.md)에, gene KO 메커니즘 실습은 [Chapter 8](../chapter-8/README.md)에 있습니다.

{% hint style="warning" %}
📦 **외부 자산 필요:** 실습 1–4는 이 저장소에 포함되지 않은 `cancer_model.xml`, `matched_normal_model.xml`, `Achilles_gene_effect.csv`와 앞 절에서 정의한 보조 함수가 필요합니다. 따라서 아래 블록은 파일 형식과 분석 순서를 보여 주는 **워크플로 골격**입니다. 파일 없이 처음부터 실행하려면 [Chapter 10의 완전 실행형 COBRApy 튜토리얼](../chapter-10/README.md)을 먼저 진행하십시오. 실습 5는 별도로 표시한 의사코드입니다.
{% endhint %}

## 실습 1: 단일 유전자 KO 스크리닝과 표적 랭킹

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

---
