# 실습: 조건부 필수성, 합성 치사와 상태 변환 점수

## 재현 환경과 범위

이 실습은 Python 3.10, [COBRApy](https://opencobra.github.io/cobrapy/) 0.30.0, [`textbook`](http://bigg.ucsd.edu/models/e_coli_core) 모델과 optlang [GLPK](https://www.gnu.org/software/glpk/) 인터페이스에서 검증하였다. `textbook`은 *E. coli* 교육 모델이므로 결과는 암 표적 예측이 아니다. 인간 암 모델에 적용하기 전에 [Chapter 6](../chapter-6/README.md)의 맥락 특이화, 정상 조직 대조와 외부 검증이 필요하다.

외부 암 모델·[DepMap](https://depmap.org/portal/) 파일이나 별도 노트북을 가정하지 않는다. [MTA](../glossary.md)의 MIQP optimizer도 재구현하지 않으며, 마지막 절에서는 이미 얻은 flux에 원 TS를 적용하는 사후 계산만 검증한다.

```python
import cobra
import numpy as np
import pandas as pd
from cobra.flux_analysis import double_gene_deletion, single_gene_deletion
from cobra.io import load_model

model = load_model("textbook")
print(cobra.__version__, model.id, model.solver.interface.__name__)
print(len(model.reactions), len(model.metabolites), len(model.genes))
```

기준 출력은 COBRApy 0.30.0, `e_coli_core`, GLPK, 반응 95개·대사물 72개·유전자 137개이다.

## 1. 단일 유전자 결손

결손 결과의 `ids` 열은 문자열이 아니라 집합이므로 명시적으로 gene ID를 추출한다. 야생형이 최적 상태가 아니거나 목적값이 0에 가까우면 상대 성장을 계산하지 않는다.

```python
def single_deletion_table(current_model, label):
    wildtype = current_model.optimize()
    if wildtype.status != "optimal" or wildtype.objective_value <= 1e-9:
        raise RuntimeError(f"{label}: valid wild-type growth was not obtained")

    result = single_gene_deletion(current_model, method="fba", processes=1).copy()
    result["gene_id"] = result["ids"].map(lambda ids: next(iter(ids)))
    result["growth"] = pd.to_numeric(result["growth"], errors="coerce")
    result["feasible"] = result["status"].eq("optimal") & result["growth"].notna()
    result["relative_growth"] = (
        result["growth"] / wildtype.objective_value
    ).where(result["feasible"])
    result.loc[result["relative_growth"].abs() < 1e-9, "relative_growth"] = 0.0
    # A deletion only narrows the FBA feasible set; values slightly above 1 are solver noise.
    result["relative_growth"] = result["relative_growth"].clip(lower=0.0, upper=1.0)
    # 이 실습의 screen policy: infeasible deletion은 growth 0으로 분류하되
    # 원 상태와 NaN을 feasible/status 열에 보존한다.
    result["screen_growth"] = result["relative_growth"].fillna(0.0)
    result["effect"] = 1.0 - result["screen_growth"]
    result["condition"] = label
    return result[[
        "gene_id", "growth", "relative_growth", "screen_growth", "effect",
        "feasible", "status", "condition",
    ]], wildtype.objective_value


single_default, wt_growth = single_deletion_table(model, "aerobic_glucose")
print(round(wt_growth, 6), len(single_default))
lethal_by_policy = (
    (~single_default["feasible"])
    | (single_default["relative_growth"] < 0.01)
)
print(lethal_by_policy.sum(), (~single_default["feasible"]).sum())
```

이 환경에서는 기준 성장률이 약 0.873922 $$\mathrm{h^{-1}}$$이고 137개 유전자가 평가된다. 유한 최적해의 상대 성장 0.01 미만은 5개이고, 결손 뒤 `infeasible`인 유전자는 2개이므로 위 screen policy의 치사 후보는 7개이다. `infeasible`을 성장 0으로 분류하는 정책과 0.01 임계값은 분석자가 명시해야 하며, 원 solver 상태를 지우지 않는다.

## 2. 환경에 따른 조건부 필수성

같은 모델에서 산소 uptake만 닫아 무산소 조건을 만든다. 모델 구조, 포도당 uptake, biomass와 solver는 그대로 유지한다.

```python
anaerobic_model = model.copy()
anaerobic_model.reactions.get_by_id("EX_o2_e").lower_bound = 0.0

single_anaerobic, anaerobic_growth = single_deletion_table(
    anaerobic_model, "anaerobic_glucose"
)

comparison = single_default[["gene_id", "effect"]].merge(
    single_anaerobic[["gene_id", "effect"]],
    on="gene_id",
    suffixes=("_aerobic", "_anaerobic"),
)
comparison["anaerobic_selectivity"] = (
    comparison["effect_anaerobic"] - comparison["effect_aerobic"]
)
comparison = comparison.sort_values(
    ["anaerobic_selectivity", "gene_id"], ascending=[False, True]
)

print(round(anaerobic_growth, 6))
print(comparison.head(3).to_string(index=False))
```

무산소 기준 성장률은 약 0.211663 $$\mathrm{h^{-1}}$$이다. `b3956` 결손은 이 스냅샷에서 호기 조건보다 무산소 조건에 훨씬 큰 영향을 준다. 이 차이는 환경 조건부 의존성을 보여주지만 암-정상 선택성이나 약물 안전성을 뜻하지 않는다.

## 3. 이중 결손과 합성 치사 후보

아래 교육용 판정은 단일 상대 성장 0.5 초과, 이중 상대 성장 0.05 미만을 사용한다. 연구에서는 생물학적 endpoint와 측정오차에 맞추어 임계값을 사전 정의한다.

```python
def synthetic_lethal_table(
    current_model,
    single_min_fraction=0.50,
    double_max_fraction=0.05,
):
    single, wildtype = single_deletion_table(current_model, "single")
    single_map = single.set_index("gene_id")["relative_growth"].to_dict()

    double = double_gene_deletion(current_model, method="fba", processes=1)
    rows = []
    for record in double.itertuples(index=False):
        genes = sorted(record.ids)
        if len(genes) != 2:
            continue
        gene_a, gene_b = genes
        if gene_a not in single_map or gene_b not in single_map:
            continue

        relative_a = single_map[gene_a]
        relative_b = single_map[gene_b]
        if not np.isfinite(relative_a) or not np.isfinite(relative_b):
            continue

        double_feasible = record.status == "optimal" and np.isfinite(record.growth)
        relative_ab = (
            max(0.0, min(1.0, float(record.growth) / wildtype))
            if double_feasible else 0.0
        )
        if (
            relative_a > single_min_fraction
            and relative_b > single_min_fraction
            and relative_ab < double_max_fraction
        ):
            rows.append({
                "gene_a": gene_a,
                "gene_b": gene_b,
                "relative_a": relative_a,
                "relative_b": relative_b,
                "relative_ab": relative_ab,
                "double_feasible": double_feasible,
                "double_status": record.status,
                "bliss_delta": relative_ab - relative_a * relative_b,
            })

    columns = [
        "gene_a", "gene_b", "relative_a", "relative_b", "relative_ab",
        "double_feasible", "double_status", "bliss_delta",
    ]
    result = pd.DataFrame(rows, columns=columns)
    if result.empty:
        return result
    return result.sort_values(
        ["relative_ab", "gene_a", "gene_b"]
    ).reset_index(drop=True)


sl_pairs = synthetic_lethal_table(model)
print(len(sl_pairs))
print(sl_pairs.head(5).to_string(index=False))
```

기준 스냅샷에서는 이 임계값과 `infeasible`=치사 정책으로 23개 쌍이 검출된다. 이 가운데 10개는 이중 결손 LP가 `infeasible`이고 13개는 feasible하지만 성장률이 임계값보다 작다. `bliss_delta`가 음수이면 이중 성장률이 단일 성장률 곱보다 작다는 뜻이다. 이 값은 deterministic FBA 결과의 상호작용 요약이며 통계적 유의성이나 임상 SL을 증명하지 않는다.

## 4. 외부 필수성 자료의 평가 방향

다음 배열은 metric 계산을 검산하기 위한 합성 자료이다. 실제 분석에서는 DepMap release, cell line, gene identifier와 gene-effect 종류를 명시하고 모델 조정에 사용하지 않은 자료를 사용한다.

```python
from scipy.stats import spearmanr
from sklearn.metrics import average_precision_score, roc_auc_score

toy = pd.DataFrame({
    "model_effect": [0.95, 0.80, 0.70, 0.30, 0.20, 0.05],
    "gene_effect": [-1.30, -0.90, -0.70, -0.20, 0.00, 0.10],
    "essential_label": [1, 1, 1, 0, 0, 0],
})

# DepMap-type gene effect는 더 음수일수록 강한 의존성이므로 부호를 뒤집는다.
rho, p_value = spearmanr(toy["model_effect"], -toy["gene_effect"])
roc_auc = roc_auc_score(toy["essential_label"], toy["model_effect"])
pr_auc = average_precision_score(toy["essential_label"], toy["model_effect"])

print(round(rho, 3), round(roc_auc, 3), round(pr_auc, 3))
```

이 합성 자료는 세 값이 모두 1이 되도록 구성되어 있다. 실제 자료의 PR-AUC 기준선은 양성 비율이며, 이 예제의 완전 분리를 성능 기대값으로 사용하지 않는다.

## 5. Flux-sampling AFR 계산 구조

AFR은 표본별 해당·OXPHOS ATP 생성 플럭스를 집계한 뒤 표본 평균의 비로 계산한다. 아래 데이터는 계산 구조만 보이는 합성 표본이다.

```python
flux_samples = pd.DataFrame({
    "glycolytic_atp_1": [8.0, 10.0, 12.0],
    "glycolytic_atp_2": [7.0, 9.0, 11.0],
    "oxphos_atp": [12.0, 10.0, 8.0],
})

glycolytic_atp = flux_samples[[
    "glycolytic_atp_1", "glycolytic_atp_2"
]].sum(axis=1)
oxphos_atp = flux_samples["oxphos_atp"]

if oxphos_atp.mean() <= 1e-12:
    raise ZeroDivisionError("mean OXPHOS ATP flux is zero")
afr = glycolytic_atp.mean() / oxphos_atp.mean()
print(round(afr, 3))
```

합성 표본의 AFR은 1.9이다. 실제 모델에서는 ATP-producing reaction 집합, stoichiometric ATP yield, 방향, sampling 수렴과 배지를 원 연구 정의에 맞추어야 한다.

## 6. MTA transformation score의 사후 계산

다음 함수는 MTA MIQP를 풀지 않으며, 기준 flux가 비영이고 결과 flux가 부호를 넘지 않는 반응만 처리한다. 주어진 $$\mathbf v^{\mathrm{ref}}$$와 $$\mathbf v^{\mathrm{res}}$$에서 성공·실패 반응을 분류하고 TS 비율을 계산한다. 원 MTA의 기준 0 가역 반응과 sign-crossing 판정은 구현하지 않으므로 입력에서 명시적으로 거부한다.

```python
def transformation_score_sign_stable(
    v_ref, v_res, r_s, r_f, r_b, epsilon, tolerance=1e-12
):
    v_ref = np.asarray(v_ref, dtype=float)
    v_res = np.asarray(v_res, dtype=float)
    epsilon = np.broadcast_to(np.asarray(epsilon, dtype=float), v_ref.shape)
    delta = v_res - v_ref
    changed = set(r_f) | set(r_b)

    if any(abs(v_ref[i]) <= tolerance for i in changed):
        raise ValueError("zero-reference reversible reactions require full MTA logic")
    if any(v_ref[i] * v_res[i] < -tolerance for i in changed):
        raise ValueError("sign-crossing reactions require full MTA logic")

    success = {
        *[i for i in r_f if delta[i] >= epsilon[i]],
        *[i for i in r_b if delta[i] <= -epsilon[i]],
    }
    unsuccessful = changed - success

    numerator = sum(abs(delta[i]) for i in success) - sum(
        abs(delta[i]) for i in unsuccessful
    )
    denominator = sum(abs(delta[i]) for i in r_s)
    if denominator <= tolerance:
        return np.nan
    return numerator / denominator


v_ref = np.array([10.0, 5.0, -2.0, 8.0])
v_res = np.array([10.5, 7.0, -2.2, 7.9])
ts = transformation_score_sign_stable(
    v_ref, v_res,
    r_s={0, 3}, r_f={1}, r_b={2},
    epsilon=np.ones(4),
)
print(round(ts, 3))
```

반응 1은 forward 변화에 성공하고 반응 2는 backward 변화 기준을 충족하지 못한다. 분자는 $$2.0-0.2=1.8$$, $$R_S$$ 변화의 합은 $$0.5+0.1=0.6$$이므로 TS는 3.0이다. 분모가 0이면 함수는 `NaN`을 반환하며, 임의의 큰 점수로 대체하지 않는다. 연구용 MTA 구현은 원 Supplementary Methods의 가역 반응 성공 판정을 사용해야 한다.

## 7. 검산

```python
assert len(model.reactions) == 95
assert len(model.genes) == 137
assert abs(wt_growth - 0.8739215069684307) < 1e-8
assert abs(anaerobic_growth - 0.2116629497353107) < 1e-8
assert len(sl_pairs) == 23
assert (~sl_pairs["double_feasible"]).sum() == 10
assert abs(afr - 1.9) < 1e-12
assert abs(ts - 3.0) < 1e-12

for invalid_ref, invalid_res in [
    ([0.0, 1.0], [2.0, 1.0]),      # changed reaction has zero reference
    ([1.0, 1.0], [-2.0, 1.0]),     # changed reaction crosses sign
]:
    try:
        transformation_score_sign_stable(
            invalid_ref, invalid_res,
            r_s={1}, r_f={0}, r_b=set(), epsilon=np.ones(2),
        )
    except ValueError:
        pass
    else:
        raise AssertionError("reversible-reaction edge case was not rejected")
print("all checks passed")
```

패키지나 예제 모델 버전이 달라 assertion이 실패하면 기대값을 덮어쓰기 전에 모델 파일, 기본 배지, 목적함수와 solver 차이를 기록한다.
