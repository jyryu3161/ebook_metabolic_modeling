# 실습: 조건부 필수성, 합성 치사와 상태 변환 점수

## 이 실습에서 하는 일

이 실습에서는 *E. coli* 교육용 모델 하나로 질병 대사 모델링의 핵심 계산 절차를 처음부터 끝까지 따라 실행합니다. 유전자를 하나씩 꺼서 성장에 미치는 영향을 재는 [단일 유전자 결손](../glossary.md), 두 유전자를 함께 꺼서 [합성 치사(synthetic lethality)](../glossary.md) 후보를 찾는 이중 결손, 외부 필수성 자료와 모델 예측을 견주는 평가 지표, 그리고 [MTA](../glossary.md)의 상태 변환 점수(transformation score, TS) 사후 계산을 차례로 다룹니다.

여기서 쓰는 `textbook` 모델은 *E. coli* 교육 모델이므로 계산 결과는 암 표적 예측이 아닙니다. 인간 암 모델에 적용하려면 [Chapter 6](../chapter-6/README.md)의 맥락 특이화, 정상 조직 대조와 외부 검증이 별도로 필요합니다.

{% hint style="warning" %}
**해석상의 주의** — 외부 암 모델·[DepMap](https://depmap.org/portal/) 파일이나 별도 노트북을 가정하지 않습니다. [MTA](../glossary.md)의 MIQP optimizer도 재구현하지 않으며, 마지막 절에서는 이미 얻은 flux에 원 TS를 적용하는 사후 계산만 검증합니다.
{% endhint %}

## 학습 목표

이 실습을 마치면 다음을 할 수 있습니다.

1. COBRApy로 예제 모델을 불러오고 반응·대사물·유전자 수를 **확인한다.**
2. GPR 규칙에 따른 단일 유전자 결손의 상대 성장을 **계산하고** 치사 후보를 **판정한다.**
3. 산소 uptake를 닫아 무산소 조건을 만들고 환경에 따른 조건부 필수성을 **비교한다.**
4. 이중 결손 결과로 합성 치사 후보와 Bliss 편차를 **해석한다.**
5. 합성 자료로 ROC-AUC·PR-AUC·Spearman 상관을 **검산한다.**
6. AFR과 MTA 상태 변환 점수의 계산 구조를 **재현한다.**

## 준비물

이 실습을 시작하기 전에 다음을 갖춥니다.

- **실행 환경**: 이 장 전용 가상환경을 먼저 만듭니다. 만드는 방법은 [Chapter 11 1절](../chapter-11/01.md) 또는 [설치 가이드](../installation.md)를 그대로 따르면 됩니다. 가상환경을 활성화한 상태에서 아래 코드를 실행합니다.
- **검증 환경**: 이 실습은 Python 3.10, [COBRApy](https://opencobra.github.io/cobrapy/) 0.30.0, [`textbook`](http://bigg.ucsd.edu/models/e_coli_core) 모델과 optlang [GLPK](https://www.gnu.org/software/glpk/) 인터페이스에서 검증하였습니다.
- **필요한 패키지**: `cobra`(0.30.0), `numpy`, `pandas`, `scipy`, `scikit-learn`. 가상환경 안에서 `python -m pip install "cobra==0.30.0" numpy pandas scipy scikit-learn` 로 설치할 수 있습니다.
- **실행 순서**: 아래 단계는 위에서부터 순서대로 실행합니다. 뒤 단계는 앞 단계에서 만든 변수(`model`, `single_deletion_table`, `single_default`, `wt_growth` 등)를 그대로 사용하므로, 셀을 건너뛰면 `NameError`가 납니다.

## 단계 1. 모델을 불러오고 환경을 확인하기

**무엇을·왜.** 먼저 예제 모델을 불러오고 이후 단계에서 계속 쓸 라이브러리를 준비합니다. `load_model("textbook")`은 COBRApy에 내장된 *E. coli* 핵심 대사 모델(`e_coli_core`)을 불러옵니다. 이 모델은 반응·대사물·유전자 수가 작아 결손 분석을 빠르게 반복할 수 있어 학습에 적합합니다. 반응 수 같은 기본 크기를 먼저 확인해 두면, 뒤 단계에서 값이 달라졌을 때 원인을 추적하기 쉽습니다.

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

**예상 출력.** 기준 출력은 COBRApy 0.30.0, `e_coli_core`, GLPK, 반응 95개·대사물 72개·유전자 137개입니다. 두 번째 줄의 세 숫자가 확실한 기준값입니다.

```
0.30.0 e_coli_core optlang.glpk_interface
95 72 137
```

**확인 포인트.** 두 번째 줄이 `95 72 137`이면 성공입니다. 첫 줄의 버전이 `0.30.0`이 아니면 마지막 검산(단계 8)에서 값이 달라질 수 있으니, 버전을 [준비물](#준비물)의 기준에 맞춥니다.

**자주 나는 오류와 해결.**
- `ModuleNotFoundError: No module named 'cobra'`: 가상환경이 활성화되지 않았거나 패키지가 없습니다. 가상환경을 켠 뒤 [준비물](#준비물)의 설치 명령을 다시 실행합니다.
- 첫 줄의 solver 인터페이스 문자열은 optlang 버전에 따라 표기가 조금 다를 수 있습니다. GLPK를 쓰고 있고 두 번째 줄 숫자가 맞으면 문제가 없습니다.

## 단계 2. 단일 유전자 결손으로 상대 성장 계산하기

**무엇을·왜.** 유전자를 하나씩 껐을 때 성장률이 얼마나 줄어드는지를 계산합니다. 유전자 결손은 [GPR](../chapter-3/README.md) 규칙을 통해 반응의 경계값에 전달되고, 결손 뒤 성장은 [FBA](../chapter-4/README.md)로 다시 최적화합니다. 기준 성장률 $$\mu_0$$ 대비 결손 성장률 $$\mu_{-g}$$의 비를 상대 성장 $$r_g=\mu_{-g}/\mu_0$$라 합니다(이론은 [이 장 3절](03.md)). 결손 결과의 `ids` 열은 문자열이 아니라 집합이므로 명시적으로 gene ID를 추출합니다. 야생형이 최적 상태가 아니거나 목적값이 0에 가까우면 상대 성장을 계산하지 않습니다.

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

**예상 출력.** 이 환경에서는 기준 성장률이 약 0.873922 $$\mathrm{h^{-1}}$$이고 137개 유전자가 평가됩니다. 유한 최적해의 상대 성장 0.01 미만은 5개이고, 결손 뒤 `infeasible`인 유전자는 2개이므로 위 screen policy의 치사 후보는 7개입니다.

```
0.873922 137
7 2
```

**확인 포인트.** 첫 줄이 `0.873922 137`, 둘째 줄이 `7 2`이면 성공입니다. 첫 값은 야생형 성장률, 둘째 줄은 각각 치사 후보 수(7)와 결손 뒤 `infeasible`인 유전자 수(2)입니다.

{% hint style="warning" %}
**해석상의 주의** — `infeasible`을 성장 0으로 분류하는 정책과 0.01 임계값은 분석자가 명시해야 하며, 원 solver 상태를 지우지 않습니다.
{% endhint %}

**자주 나는 오류와 해결.**
- `NameError: name 'model' is not defined`: 단계 1을 먼저 실행하지 않았습니다. 위에서부터 순서대로 실행합니다.
- 결과가 프로세스마다 미세하게 흔들리면 `processes=1`이 지정되어 있는지 확인합니다(재현성을 위해 단일 프로세스로 고정합니다).

## 단계 3. 환경에 따른 조건부 필수성 비교하기

**무엇을·왜.** 같은 모델에서 산소 uptake만 닫아 무산소 조건을 만든 뒤, 같은 결손 분석을 다시 수행하여 호기·무산소 조건의 효과 차이를 봅니다. 어떤 유전자는 특정 환경에서만 필수가 되는데, 이를 조건부 필수성이라 합니다([이 장 3.1절](03.md)). 이 단계는 단계 2에서 정의한 `single_deletion_table` 함수와 `single_default` 표를 그대로 사용합니다. 모델 구조, 포도당 uptake, biomass와 solver는 그대로 유지하고 산소 교환만 바꿉니다.

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

**예상 출력.** 무산소 기준 성장률은 약 0.211663 $$\mathrm{h^{-1}}$$입니다. 이어서 `anaerobic_selectivity`가 큰 순으로 상위 3개 유전자가 표로 출력되며, 이 스냅샷에서는 맨 윗줄이 `b3956`입니다.

```
0.211663
```

**확인 포인트.** 첫 줄이 `0.211663`이고, 이어지는 표의 첫 행 `gene_id`가 `b3956`이면 성공입니다. `b3956` 결손은 이 스냅샷에서 호기 조건보다 무산소 조건에 훨씬 큰 영향을 줍니다.

{% hint style="warning" %}
**해석상의 주의** — 이 차이는 환경 조건부 의존성을 보여주지만 암-정상 선택성이나 약물 안전성을 뜻하지 않습니다.
{% endhint %}

**자주 나는 오류와 해결.**
- `KeyError: 'EX_o2_e'`: 산소 교환 반응 ID가 다른 모델을 불러왔을 수 있습니다. 단계 1의 `e_coli_core` 모델을 사용하는지 확인합니다.
- `NameError: name 'single_default' is not defined`: 단계 2를 먼저 실행하지 않았습니다.

## 단계 4. 이중 결손으로 합성 치사 후보 찾기

**무엇을·왜.** 두 유전자를 함께 껐을 때만 성장이 무너지는 조합, 곧 합성 치사 후보를 찾습니다([이 장 4절](04.md)). 아래 교육용 판정은 단일 상대 성장 0.5 초과(두 유전자 각각 단독으로는 성장을 크게 유지), 이중 상대 성장 0.05 미만(함께 끄면 성장 붕괴)을 사용합니다. `bliss_delta`는 이중 성장률에서 두 단일 성장률의 곱을 뺀 값으로, 두 결손의 상호작용을 요약합니다. 연구에서는 생물학적 endpoint와 측정오차에 맞추어 임계값을 사전 정의합니다.

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

**예상 출력.** 기준 스냅샷에서는 이 임계값과 `infeasible`=치사 정책으로 23개 쌍이 검출됩니다. 이어서 상위 5개 쌍이 표로 출력됩니다.

```
23
```

**확인 포인트.** 첫 줄이 `23`이면 성공입니다. 이 23개 가운데 10개는 이중 결손 LP가 `infeasible`이고 13개는 feasible하지만 성장률이 임계값보다 작습니다. `bliss_delta`가 음수이면 이중 성장률이 단일 성장률 곱보다 작다는 뜻입니다.

{% hint style="warning" %}
**해석상의 주의** — `bliss_delta`는 deterministic FBA 결과의 상호작용 요약이며 통계적 유의성이나 임상 SL을 증명하지 않습니다.
{% endhint %}

**자주 나는 오류와 해결.**
- 실행이 오래 걸리면 정상입니다. 이중 결손은 유전자 쌍을 모두 조합하므로 단일 결손보다 계산량이 큽니다. `processes=1`로 고정되어 있으니 그대로 기다립니다.
- 결과 개수가 23이 아니면 앞 단계의 `model`이 수정되었는지 확인합니다(단계 3에서 `model` 자체가 아니라 `anaerobic_model` 복사본만 바꾸었는지 점검합니다).

## 단계 5. 외부 필수성 자료의 평가 방향 검산하기

**무엇을·왜.** 모델 예측을 외부 필수성 자료와 견줄 때 쓰는 지표(Spearman 상관, ROC-AUC, PR-AUC)를 작은 합성 자료로 검산합니다([이 장 3.6절](03.md)). 이 단계는 앞 단계 결과에 의존하지 않고 독립적으로 실행할 수 있으며, `pandas`만 있으면 됩니다. [DepMap](https://depmap.org/portal/) 유형의 gene effect는 값이 더 음수일수록 강한 의존성이므로, 모델 효과와 방향을 맞추기 위해 부호를 뒤집습니다. 실제 분석에서는 DepMap release, cell line, gene identifier와 gene-effect 종류를 명시하고 모델 조정에 사용하지 않은 자료를 씁니다.

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

**예상 출력.** 이 합성 자료는 세 값이 모두 1이 되도록 구성되어 있습니다.

```
1.0 1.0 1.0
```

**확인 포인트.** 출력이 `1.0 1.0 1.0`이면 성공입니다. 세 지표가 각각 Spearman 상관, ROC-AUC, PR-AUC입니다.

{% hint style="warning" %}
**해석상의 주의** — 실제 자료의 PR-AUC 기준선은 양성 비율이며, 이 예제의 완전 분리를 성능 기대값으로 사용하지 않습니다.
{% endhint %}

**자주 나는 오류와 해결.**
- `ModuleNotFoundError: No module named 'scipy'` 또는 `'sklearn'`: 가상환경 안에서 `python -m pip install scipy scikit-learn`을 실행합니다.

## 단계 6. Flux-sampling AFR 계산 구조 재현하기

**무엇을·왜.** [ATP flux ratio(AFR)](../glossary.md)는 표본별 해당·OXPHOS ATP 생성 플럭스를 집계한 뒤 표본 평균의 비로 계산합니다([이 장 1.2절](01.md)). 이 단계는 실제 sampling 대신, 계산 구조만 보이도록 만든 합성 표본으로 절차를 재현합니다. 앞 단계 결과에 의존하지 않으며 `pandas`만 있으면 됩니다.

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

**예상 출력.** 합성 표본의 AFR은 1.9입니다.

```
1.9
```

**확인 포인트.** 출력이 `1.9`이면 성공입니다. 분모인 평균 OXPHOS ATP 플럭스가 0에 가까우면 `ZeroDivisionError`를 던져 잘못된 나눗셈을 막습니다.

{% hint style="warning" %}
**해석상의 주의** — 실제 모델에서는 ATP-producing reaction 집합, stoichiometric ATP yield, 방향, sampling 수렴과 배지를 원 연구 정의에 맞추어야 합니다.
{% endhint %}

## 단계 7. MTA 상태 변환 점수의 사후 계산하기

**무엇을·왜.** [MTA](../glossary.md)의 상태 변환 점수(TS)를 이미 얻은 flux에 적용하는 사후 계산만 재현합니다([이 장 6절](06.md)). 아래 함수는 MTA의 MIQP를 풀지 않으며, 기준 flux $$\mathbf v^{\mathrm{ref}}$$가 비영이고 결과 flux $$\mathbf v^{\mathrm{res}}$$가 부호를 넘지 않는 반응만 처리합니다. 목표 방향으로 충분히 변한 반응을 성공, 그렇지 못한 반응을 실패로 분류하고 TS 비율을 계산합니다. 원 MTA의 기준 0 가역 반응과 sign-crossing 판정은 구현하지 않으므로 입력에서 명시적으로 거부합니다. 이 단계는 `numpy`만 있으면 됩니다.

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

**예상 출력.** 반응 1은 forward 변화에 성공하고 반응 2는 backward 변화 기준을 충족하지 못합니다. 분자는 $$2.0-0.2=1.8$$, $$R_S$$ 변화의 합은 $$0.5+0.1=0.6$$이므로 TS는 3.0입니다.

```
3.0
```

**확인 포인트.** 출력이 `3.0`이면 성공입니다. 분모가 0이면 함수는 `NaN`을 반환하며, 임의의 큰 점수로 대체하지 않습니다.

{% hint style="warning" %}
**해석상의 주의** — 연구용 MTA 구현은 원 Supplementary Methods의 가역 반응 성공 판정을 사용해야 합니다.
{% endhint %}

**자주 나는 오류와 해결.**
- `ValueError: zero-reference reversible reactions require full MTA logic` 또는 `... sign-crossing ...`: 함수가 설계대로 입력을 거부한 것입니다. 이런 반응은 이 사후 계산이 다룰 수 없으므로 원 MTA 논리를 써야 합니다. 단계 8에서 이 거부가 정상 동작함을 검산합니다.

## 단계 8. 전체 결과 검산하기

**무엇을·왜.** 지금까지 만든 변수들이 기준값과 일치하는지 한 번에 확인합니다. 이 단계는 앞의 모든 단계(1~7)에서 만든 `model`, `wt_growth`, `anaerobic_growth`, `sl_pairs`, `afr`, `ts`, `transformation_score_sign_stable`를 사용하므로 반드시 마지막에 실행합니다. 아래 `assert`는 값이 어긋나면 즉시 오류를 내어, 어느 단계에서 결과가 달라졌는지 알려 줍니다. 마지막 반복문은 가역 반응 예외 두 경우가 실제로 `ValueError`로 거부되는지 검사합니다.

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

**예상 출력.** 모든 검산을 통과하면 마지막 줄이 출력됩니다.

```
all checks passed
```

**확인 포인트.** `all checks passed`가 출력되면 이 실습의 모든 값이 기준과 일치한 것입니다.

**자주 나는 오류와 해결.**
- `AssertionError`가 나면, 실패한 줄 위쪽 단계의 결과가 기준과 다른 것입니다. 패키지나 예제 모델 버전이 달라 assertion이 실패하면 기대값을 덮어쓰기 전에 모델 파일, 기본 배지, 목적함수와 solver 차이를 기록합니다.
- 특정 변수에서 `NameError`가 나면 해당 단계를 건너뛴 것이므로, 처음부터 순서대로 다시 실행합니다.

## 정리

이 실습에서는 다음을 했습니다.

- COBRApy로 `e_coli_core` 모델을 불러오고 반응 95개·대사물 72개·유전자 137개를 확인했습니다.
- 단일 유전자 결손으로 상대 성장을 계산하고 screen policy에 따라 치사 후보 7개를 판정했습니다.
- 산소 uptake를 닫아 무산소 조건을 만들고 조건부 필수성 차이를 비교했습니다.
- 이중 결손으로 합성 치사 후보 23개를 찾고 `bliss_delta`로 상호작용을 해석했습니다.
- 합성 자료로 ROC-AUC·PR-AUC·Spearman 상관을 검산하고, AFR과 MTA 상태 변환 점수의 계산 구조를 재현했습니다.

모든 계산은 명시한 모델·배지·목적함수·solver 아래의 결과이며, 인간 암 표적의 증명이 아니라는 점을 기억합니다.

## 스스로 해보기

아래 과제는 코드를 조금 바꿔 결과가 어떻게 달라지는지 관찰하는 연습입니다. 정답 코드는 바로 보여 주지 않으므로 직접 수정해 봅니다.

1. 단계 2의 치사 임계값 `0.01`을 `0.05`로 바꾸면 `lethal_by_policy.sum()`이 어떻게 달라지는지 확인해 봅니다. 임계값을 명시하는 일이 왜 중요한지 [이 장 3.1절](03.md)과 연결해 생각해 봅니다.
2. 단계 4의 `single_min_fraction`과 `double_max_fraction`을 조금씩 바꾸어 검출되는 쌍 수가 어떻게 변하는지 표로 정리해 봅니다.
3. 단계 6의 `flux_samples` 숫자를 바꾸어 AFR이 1보다 커지거나 작아지도록 만들어 보고, 어떤 경우에 해당 ATP 사용이 상대적으로 커지는지 설명해 봅니다.

이어서 무산소 조건이 아닌 다른 배지 변화나 이중 결손 정책을 시험하려면, 조건부 필수성은 [이 장 3절](03.md), 합성 치사는 [이 장 4절](04.md), MTA는 [이 장 6절](06.md)을 함께 읽습니다. 결손 뒤 flux 예측에 쓰는 [FBA](../chapter-4/README.md)와 [MOMA·ROOM](../chapter-8/README.md)의 차이도 참고할 수 있습니다.
