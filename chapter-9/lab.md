# 실습: 계산 유전자 필수성 레이블로 분류 절차 익히기

> 이 실습은 [§1](01.md)–[§3](03.md)의 핵심만 연결합니다. `e_coli_core`에서 유전자별 특징과 **계산 레이블**을 만들고, 층화 교차검증으로 랜덤 포레스트를 평가합니다. 실험 레이블을 사용하지 않으므로 결과를 실험적 유전자 필수성 성능으로 해석하지 않습니다.

## 학습 목표

이 실습을 마치면 다음을 할 수 있습니다.

- GEM·배지·목적함수·솔버와 필수성 임계값을 기록합니다.
- 야생형 상태에서 얻은 유전자별 특징과 결손 뒤 성장으로 만든 계산 레이블을 구분합니다.
- 클래스 불균형을 확인하고 층화 교차검증을 수행합니다.
- 혼동 행렬·정밀도·재현율·MCC를 함께 해석합니다.
- 계산 레이블 평가와 실험 레이블 외부 검증의 차이를 설명합니다.

## 준비

[설치 가이드](../installation.md)의 Python 3.10 이상·COBRApy 0.30.0 환경을 사용합니다. 이 실습에는 `numpy`, `pandas`, `scikit-learn`이 추가로 필요합니다.

```bash
python -m pip install "cobra==0.30.0" numpy pandas scikit-learn
```

아래 코드는 COBRApy의 `textbook` 모델, 모델의 기본 배지, 바이오매스 목적함수와 GLPK를 사용합니다. 설치된 GLPK 세부 버전과 허용오차도 실행 기록에 남깁니다.

## 1단계. 계산 조건 고정하기

먼저 모델과 솔버를 불러오고 기준 성장을 계산합니다.

```python
import cobra
import numpy as np
import pandas as pd
import swiglpk
from cobra import Configuration

configuration = Configuration()
configuration.solver = "glpk"
configuration.processes = 1

model = cobra.io.load_model("textbook")
wt = model.optimize()

print("model:", model.id)
print("reactions:", len(model.reactions))
print("metabolites:", len(model.metabolites))
print("genes:", len(model.genes))
print("solver interface:", model.solver.interface.__name__)
print("GLPK version:", swiglpk.glp_version())
print("tolerance:", configuration.tolerance)
print(f"wild-type growth: {wt.objective_value:.4f} h^-1")
```

COBRApy 0.30.0의 기준 환경에서는 반응 95개, 대사물 72개, 유전자 137개와 약 0.874 h$$^{-1}$$의 기준 성장값이 출력됩니다. 이 수치는 대장균의 고정된 생물학적 성장률이 아니라 해당 모델·배지·목적함수·솔버 조건의 계산 결과입니다.

{% hint style="warning" %}
출력이 다르면 먼저 모델 ID, COBRApy 버전, 배지 경계, 목적함수와 솔버를 비교합니다. 원하는 수치에 맞추기 위해 임의로 경계를 바꾸지 않습니다.
{% endhint %}

## 2단계. 특징과 계산 레이블 만들기

각 유전자를 하나의 표본으로 사용합니다. 특징은 결손 전에 알 수 있는 정보만 사용합니다.

- `reaction_count`: 그 유전자가 연결된 반응 수
- `mean_abs_wt_flux`: 연결 반응의 야생형 절대 플럭스 평균
- `max_abs_wt_flux`: 연결 반응의 야생형 절대 플럭스 최댓값

레이블은 유전자를 제거한 뒤 계산한 성장값이 기준 성장값의 1% 미만인지로 정합니다. 결손 성장값은 레이블을 만드는 데 사용하므로 특징에 넣지 않습니다.

```python
from cobra.flux_analysis import single_gene_deletion

deletion = single_gene_deletion(model, processes=1)
ko_growth = {
    next(iter(ids)): float(growth)
    for ids, growth in zip(deletion["ids"], deletion["growth"])
}

threshold_fraction = 0.01
rows = []

for gene in model.genes:
    reaction_ids = [reaction.id for reaction in gene.reactions]
    wt_fluxes = [abs(float(wt.fluxes[reaction_id]))
                 for reaction_id in reaction_ids]
    growth = ko_growth[gene.id]

    rows.append({
        "gene_id": gene.id,
        "reaction_count": len(reaction_ids),
        "mean_abs_wt_flux": float(np.mean(wt_fluxes)) if wt_fluxes else 0.0,
        "max_abs_wt_flux": float(np.max(wt_fluxes)) if wt_fluxes else 0.0,
        "computed_essential": int(
            not np.isfinite(growth)
            or growth < threshold_fraction * wt.objective_value
        ),
    })

data = pd.DataFrame(rows).set_index("gene_id")
print(data.head())
print(data["computed_essential"].value_counts().sort_index())
```

기준 환경에서는 필수 계산 레이블이 소수이므로 클래스 불균형이 나타납니다. 기존 기준 실행에서는 137개 유전자 가운데 필수 7개가 보고되었지만, 실행 결과와 함께 모델·솔버·허용오차를 기록하고 실제 출력값을 사용합니다.

이 표에는 실험 측정값이 없습니다. `computed_essential`은 `e_coli_core`의 구조와 1% 임계값을 재현하는 계산 레이블입니다.

## 3단계. 층화 교차검증으로 분류하기

필수 유전자 수가 적으므로 한 번의 훈련·테스트 분할은 결과가 크게 흔들릴 수 있습니다. 3-fold 층화 교차검증을 사용해 각 유전자가 자신을 학습하지 않은 모델에서 한 번씩 평가되도록 합니다.

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    matthews_corrcoef,
    precision_score,
    recall_score,
)

X = data[["reaction_count", "mean_abs_wt_flux", "max_abs_wt_flux"]]
y = data["computed_essential"]

cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
classifier = RandomForestClassifier(
    n_estimators=200,
    max_depth=4,
    min_samples_leaf=2,
    class_weight="balanced",
    random_state=42,
)

prediction = cross_val_predict(classifier, X, y, cv=cv, method="predict")

tn, fp, fn, tp = confusion_matrix(y, prediction, labels=[0, 1]).ravel()
print({"TN": tn, "FP": fp, "FN": fn, "TP": tp})
print("accuracy:", accuracy_score(y, prediction))
print("precision:", precision_score(y, prediction, zero_division=0))
print("recall:", recall_score(y, prediction, zero_division=0))
print("MCC:", matthews_corrcoef(y, prediction))
```

구체적 점수는 라이브러리 버전과 계산 결과에 따라 달라질 수 있습니다. 다음 순서로 해석합니다.

1. 혼동 행렬에서 필수 유전자를 몇 개 놓쳤는지 `FN`으로 확인합니다.
2. 필수라고 제시한 후보 가운데 몇 개가 맞았는지 정밀도로 확인합니다.
3. 실제 필수 가운데 몇 개를 찾았는지 재현율로 확인합니다.
4. 다수 범주를 반복한 결과가 아닌지 MCC로 확인합니다.
5. 정확도가 높더라도 재현율과 MCC가 낮으면 유용한 필수성 분류기로 간주하지 않습니다.

### 다수 범주 기준선과 비교

모든 유전자를 비필수로 예측한 기준선도 함께 계산합니다.

```python
baseline = np.zeros_like(y)
print("baseline accuracy:", accuracy_score(y, baseline))
print("baseline recall:", recall_score(y, baseline, zero_division=0))
print("baseline MCC:", matthews_corrcoef(y, baseline))
```

필수 유전자가 적기 때문에 기준선 정확도는 높게 보일 수 있지만 재현율은 0입니다. 이 비교는 [§2](02.md)의 클래스 불균형 예시를 실제 계산 레이블에서 확인하는 절차입니다.

## 4단계. 이 결과가 말하지 않는 것 기록하기

실습 결과표 아래에 다음 제한을 그대로 기록합니다.

| 항목 | 이 실습의 상태 |
|:---|:---|
| 레이블 출처 | GEM 단일 유전자 결손 계산 |
| 계산 조건 | `textbook` 모델, 기본 배지, 바이오매스 목적함수, GLPK, 1% 임계값 |
| 특징 출처 | 같은 GEM의 GPR 연결과 야생형 FBA |
| 분할 | 한 모델 안의 유전자를 층화한 3-fold |
| 외부 실험 검증 | 수행하지 않음 |
| 허용되는 결론 | 계산 레이블을 재현하는 입문 분류 절차 평가 |
| 허용되지 않는 결론 | 새로운 생물종·세포주에서의 실험 필수성 성능 주장 |

실험 레이블을 추가하는 후속 연구에서는 `gene_id`만 맞추는 것으로 충분하지 않습니다. 균주·세포주·배지·교란법·측정 시점·점수 방향·임계값을 함께 맞추고, 세포주나 생물종 전체를 평가 fold로 남겨야 합니다.

## 스스로 해보기

1. 1% 임계값을 5%와 10%로 바꾸고 계산 레이블 수가 어떻게 달라지는지 기록합니다. 임계값마다 새 레이블을 만들되 가장 높은 점수를 내는 임계값을 테스트 결과로 선택하지 않습니다.
2. `reaction_count` 하나만 사용한 결과와 세 특징을 사용한 결과를 비교합니다. 특징이 늘었다는 사실만으로 외부 일반화가 좋아졌다고 결론 내리지 않습니다.
3. 같은 코드에 실험 레이블 열이 있다고 가정하고, 계산 레이블 평가 표와 실험 레이블 평가 표에 각각 어떤 조건 정보를 붙여야 하는지 작성합니다.

## 정리

이 실습에서는 GEM 조건을 고정하고, 결손 전 특징과 결손 뒤 계산 레이블을 분리해 표를 만들었습니다. 층화 교차검증과 혼동 행렬·정밀도·재현율·MCC로 작은 불균형 자료를 평가했습니다. 가장 중요한 결과는 점수 자체가 아니라 이 점수가 특정 GEM의 계산 규칙 재현을 평가하며 독립 실험 검증은 수행하지 않았다는 기록입니다.

---
