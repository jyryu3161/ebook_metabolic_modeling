# 실습: e_coli_core로 완성하는 특징추출 → RF → ROC → K-Means 파이프라인

> **실습:** 아래 코드는 §2~3에서 조각조각 만들어 온 것을 하나의 완결된 파이프라인으로 잇습니다. 1장에서 불러온 `e_coli_core`(95개 반응·72개 대사물·137개 유전자)만으로 그래프 특징 추출→필수성 레이블→Random Forest→ROC 평가→K-Means 대사상태 클러스터링까지 전부 실행할 수 있습니다. 더 큰 규모(iML1515)의 완전한 파이프라인과 5-fold 교차검증, Permutation Importance, Mann-Whitney U 검정 등 심화 내용은 합성 대사 네트워크 기반 특징 공학을 다루는 `raw_data/GEM_lecture_notes/gem9_w09_lab.ipynb` 노트북을 참고합니다.

## 이 실습에서 하는 일

이 실습에서는 대장균 소형 모델 `e_coli_core` 하나만으로, 대사 네트워크에서 특징을 뽑아 유전자·반응의 필수성을 예측하고 배양 조건별 대사 상태를 묶는 머신러닝 파이프라인을 처음부터 끝까지 직접 실행합니다. 새로운 이론을 배우는 것이 아니라, [§2](02.md)·[§3](03.md)에서 따로따로 만든 코드 조각들이 실제로는 하나의 매끄러운 흐름으로 이어진다는 것을 눈으로 확인하는 것이 목표입니다.

## 학습 목표

이 실습을 마치면 다음을 할 수 있습니다.

- COBRApy로 `e_coli_core`를 불러오고 NetworkX로 반응-반응 그래프를 만들어 연결 차수·매개 중심성 같은 위상 특징을 **추출한다**.
- 야생형 FBA와 반응 결손 계산으로 각 반응의 플럭스 특징과 필수성 레이블을 **생성한다**.
- scikit-learn의 Random Forest로 반응 필수성을 **학습**하고 ROC-AUC·MCC로 성능을 **평가한다**.
- 서로 다른 배양 조건의 FBA 플럭스 벡터를 K-Means로 **클러스터링**하고 그 결과를 발효·호흡 축과 견주어 **해석한다**.
- 각 단계가 이 장 어느 절의 개념을 재사용하는지 **연결한다**.

## 준비물

- **실행 환경**: [Chapter 11 §1](../chapter-11/01.md)의 가상환경(또는 [설치 가이드](../installation.md))을 먼저 준비하고 활성화합니다. 이 장의 숫자는 Python 3.10 이상·COBRApy 0.30.0 환경에서 얻은 값입니다. 원 강의자료에 solver 종류와 허용오차가 남아 있지 않으므로 이 두 항목은 결손이며, 아래 숫자를 그대로 재현하려면 [Chapter 10 §1](../chapter-10/02.md)의 preflight처럼 **solver를 먼저 명시적으로 고정하고 그 값을 기록**하십시오.

```python
from cobra import Configuration
configuration = Configuration()
configuration.solver = "glpk"   # solver 고정 — 아래 숫자와 함께 이 값을 기록
```

- **필요한 패키지**: `cobra`, `numpy`, `pandas`, `matplotlib`에 더해 이 실습은 그래프 계산용 **[NetworkX](https://networkx.org/)**와 머신러닝용 **[scikit-learn](https://scikit-learn.org/)**을 추가로 사용합니다. 가상환경에 아직 없다면 아래처럼 설치합니다.

```bash
python -m pip install networkx scikit-learn
```

- **모델**: `e_coli_core`(COBRApy에서 `load_model("textbook")`으로 부르는 소형 모델)만 사용합니다. `load_model`은 캐시에 모델이 없으면 원격 저장소에서 내려받으므로 첫 실행에는 네트워크 연결이 필요할 수 있습니다.
- **셀 실행 순서**: 아래 네 단계는 앞 단계에서 만든 변수를 뒤 단계가 그대로 이어받습니다(예: 단계 1의 `G`·`degree`·`betweenness`, 단계 2의 `features`, 단계 3의 `X_test`·`y_test`). 따라서 반드시 **위에서 아래로 순서대로** 실행합니다. 중간부터 실행하면 `NameError`가 납니다.

## 실습의 전체 그림

이 실습이 지금까지 무엇을 짜맞추는 것인지 미리 지도를 그려보겠습니다. 아래 4단계는 각각 이 장의 특정 절에서 배운 개념을 정확히 재사용합니다 — 새로운 개념은 없습니다. 1단계는 [§2.2](02.md)의 그래프 특징 추출(연결 차수·매개 중심성), 2단계는 [§2.6](02.md)·[§3.4](03.md)의 필수성 레이블 만들기, 3단계는 [§2.1](02.md)·[§2.6](02.md)의 Random Forest 학습과 ROC/MCC 평가, 4단계는 [§2.3](02.md)의 K-Means 클러스터링을 그대로 따릅니다. 즉 이 실습의 목표는 새 이론을 배우는 것이 아니라, 흩어져 있던 코드 조각들이 실제로는 하나의 매끄러운 파이프라인으로 이어진다는 것을 눈으로 확인하는 데 있습니다.

```mermaid
flowchart LR
    S1["1단계<br/>그래프 특징 추출<br/>(§2.2)"] --> S2["2단계<br/>필수성 레이블 생성<br/>(§2.6, §3.4)"]
    S2 --> S3["3단계<br/>Random Forest 학습·평가<br/>(§2.1, §2.6)"]
    S3 --> S4["4단계<br/>K-Means 클러스터링<br/>(§2.3)"]
```

*그림 9.9. 제9장 교육용 실행 파이프라인. `e_coli_core` 반응 그래프에서 degree·betweenness·wild-type flux 특징을 만들고, 모델 계산으로 만든 필수성 레이블을 Random Forest로 분류한 뒤 ROC·MCC를 평가하며, 별도의 배양 조건별 flux 행렬은 PCA와 K-Means로 탐색합니다. 이 네 단계는 동일한 외부 benchmark의 성능 보고가 아니라 API와 평가 절차를 연결한 소표본 실습입니다. 출처: 저자 자체 제작; 계산 구현은 아래 [COBRApy](https://opencobra.github.io/cobrapy/)·[NetworkX](https://networkx.org/)·[scikit-learn](https://scikit-learn.org/) 코드이며 외부 그림을 재사용하지 않았습니다.*

## 단계 1. 모델을 불러오고 반응 그래프에서 위상 특징 뽑기

**무엇을·왜.** 먼저 `e_coli_core`를 불러오고, 대사물을 공유하는 두 반응을 잇는 **반응-반응 그래프**를 만듭니다. 이렇게 만든 그래프에서 각 반응의 **연결 차수(degree; 몇 개의 반응과 이어져 있는지)**와 **매개 중심성(betweenness centrality; 여러 경로의 길목에 얼마나 자주 놓이는지)**을 계산합니다. 이 두 값은 뒤 단계에서 머신러닝의 입력 특징이 됩니다. 왜 그래프로 바꾸는지, 손으로 먼저 세어보는 예제는 [§2.2](02.md)에 있습니다.

**코드.** 아래 코드는 (1) 모델을 불러와 크기를 확인하고, (2) 공통 대사물을 공유하는 반응 쌍을 엣지로 연결해 그래프 `G`를 만들고, (3) 모든 노드의 `degree`와 `betweenness`를 계산합니다.

```python
import cobra
import networkx as nx
import numpy as np
import pandas as pd

model = cobra.io.load_model("textbook")
print(f"반응 {len(model.reactions)}개, 대사물 {len(model.metabolites)}개, "
      f"유전자 {len(model.genes)}개")
# 기대 출력: 반응 95개, 대사물 72개, 유전자 137개

G = nx.Graph()
G.add_nodes_from(rxn.id for rxn in model.reactions)
met_to_rxns = {}
for rxn in model.reactions:
    for met in rxn.metabolites:
        met_to_rxns.setdefault(met.id, set()).add(rxn.id)
for rxn_ids in met_to_rxns.values():
    rxn_ids = list(rxn_ids)
    for i in range(len(rxn_ids)):
        for j in range(i + 1, len(rxn_ids)):
            if G.has_edge(rxn_ids[i], rxn_ids[j]):
                G[rxn_ids[i]][rxn_ids[j]]['weight'] += 1
            else:
                G.add_edge(rxn_ids[i], rxn_ids[j], weight=1)

degree = dict(G.degree())
betweenness = nx.betweenness_centrality(G)
print(f"그래프: 노드 {G.number_of_nodes()}개, 엣지 {G.number_of_edges()}개")
```

**예상 출력.** 첫 번째 줄은 모델의 크기를, 마지막 줄은 그래프의 크기를 보여줍니다.

```
반응 95개, 대사물 72개, 유전자 137개
그래프: 노드 95개, 엣지 …개
```

노드는 반응 개수와 같은 **정확히 95개**로 출력됩니다. 엣지 개수는 NetworkX가 세는 특정 정수로, 실행 환경에서 그대로 확인합니다.

**확인 포인트.** 첫 줄이 `반응 95개, 대사물 72개, 유전자 137개`로, 그래프 노드가 `95개`로 나오면 성공입니다. `degree`와 `betweenness`가 오류 없이 만들어졌으면 다음 단계로 넘어갑니다.

**자주 나는 오류와 해결.**
- `ModuleNotFoundError: No module named 'networkx'` — 준비물의 `pip install networkx scikit-learn`을 실행하지 않았거나 다른 가상환경에서 실행 중입니다. 가상환경을 활성화한 뒤 다시 설치합니다.
- 첫 실행에서 모델 다운로드가 멈추거나 실패하면 네트워크 연결을 확인합니다. `load_model("textbook")`은 캐시에 모델이 없으면 원격에서 내려받습니다.

## 단계 2. 야생형 플럭스와 반응 필수성 레이블 만들기

**무엇을·왜.** 이제 그래프 특징에 **플럭스 특징**을 더하고, 지도학습의 정답이 될 **필수성 레이블**을 만듭니다. 먼저 야생형(정상) 상태에서 FBA로 성장률과 각 반응의 플럭스(flux; `mmol gDW⁻¹ h⁻¹` 단위의 반응 진행률)를 구합니다. 그다음 반응을 하나씩 제거(`single_reaction_deletion`)해 성장률이 야생형의 1% 미만으로 떨어지거나 계산이 불가능해지면 그 반응을 **필수(essential)**로 표시합니다. 여기서 만드는 레이블은 실험으로 측정한 사실이 아니라 특정 모델·배지·목적함수로 계산한 **in silico label**임에 유의합니다. 관측 단위를 반응으로 잡는 이유와 유전자 필수성과의 차이는 [§3.4](03.md)에 정리되어 있습니다.

**코드.** 아래 코드는 (1) 야생형 성장률을 출력하고, (2) 각 반응을 결손해 성장률을 모은 뒤, (3) `degree`·`betweenness`·`wt_flux`·`essential` 네 열을 가진 특징 표 `features`를 완성합니다.

```python
wt = model.optimize()
print(f"야생형 성장률: {wt.objective_value:.4f} h^-1")
# 기대 출력: 야생형 성장률: 0.8739 h^-1

from cobra.flux_analysis import single_reaction_deletion

reaction_ko = single_reaction_deletion(model, processes=1)
ko_growth = {
    next(iter(ids)): float(growth)
    for ids, growth in zip(reaction_ko["ids"], reaction_ko["growth"])
}

rows = []
for rxn in model.reactions:
    rows.append({
        'reaction': rxn.id,
        'degree': degree[rxn.id],
        'betweenness': betweenness[rxn.id],
        'wt_flux': abs(wt.fluxes[rxn.id]),
        'essential': int(not np.isfinite(ko_growth[rxn.id])
                         or ko_growth[rxn.id] < 0.01 * wt.objective_value),
    })
features = pd.DataFrame(rows).set_index('reaction')
print(features['essential'].value_counts())
# 기대 출력: non-essential 77, essential 18
```

**예상 출력.** 야생형 성장률이 먼저 출력되고, 이어서 필수/비필수 반응의 개수가 나옵니다. `value_counts()`는 개수가 많은 값부터 정렬해 보여줍니다.

```
야생형 성장률: 0.8739 h^-1
```

```
0    77
1    18
```

여기서 `0`은 비필수 반응 **77개**, `1`은 필수 반응 **18개**를 뜻합니다. 즉 95개 반응 중 약 19%만 필수이며, 이 불균형이 다음 단계에서 왜 정확도(Accuracy)만으로 성능을 보면 안 되는지의 배경이 됩니다.

**확인 포인트.** 성장률이 `0.8739 h^-1`로, 필수 반응이 `18`개, 비필수 반응이 `77`개로 나오면 성공입니다. 이 세 숫자가 다르게 나오면 앞 단계 셀을 순서대로 다시 실행했는지 확인합니다. 성장률은 solver를 바꿔도 소수점 넷째 자리까지는 대체로 유지되지만, 필수/비필수 개수는 1% 임계값 근처에 걸친 반응에서 solver의 대안 최적해와 허용오차에 따라 한두 개 달라질 수 있습니다. 개수가 어긋나면 준비물에서 고정한 solver 설정을 먼저 확인하십시오.

**자주 나는 오류와 해결.**
- `NameError: name 'degree' is not defined` — 단계 1을 실행하지 않고 이 셀부터 실행한 경우입니다. 단계 1부터 순서대로 실행합니다.
- 결손 계산이 매우 느리거나 macOS에서 출력이 미세하게 흔들리면 `processes=1`(코드에 이미 지정됨)로 단일 프로세스 실행을 유지합니다.

## 단계 3. Random Forest 학습과 ROC/MCC 평가하기

**무엇을·왜.** 단계 2에서 만든 특징 표를 훈련·테스트로 나눈 뒤, **Random Forest(RF; 여러 결정 트리의 다수결 앙상블)**로 반응 필수성을 분류합니다. 그리고 [§2.6](02.md)에서 손으로 계산해 본 지표들 — 정밀도·재현율, MCC, ROC-AUC — 를 코드로 재현합니다. 표본이 매우 적으므로 `class_weight='balanced'`로 소수 클래스(필수)에 가중치를 주고, `max_depth`를 낮춰 과적합을 억제합니다.

**코드.** 아래 코드는 (1) 특징 `X`와 정답 `y`를 나누고, (2) `stratify=y`로 필수/비필수 비율을 유지한 채 30%를 테스트로 떼어 낸 뒤, (3) RF를 학습해 `classification_report`·MCC·AUC-ROC를 출력하고 ROC 곡선을 그립니다.

```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, auc, matthews_corrcoef, classification_report
import matplotlib.pyplot as plt

X = features.drop(columns='essential')
y = features['essential']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

rf = RandomForestClassifier(
    n_estimators=200, max_depth=8, min_samples_leaf=2,
    class_weight='balanced', random_state=42
)
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)
y_prob = rf.predict_proba(X_test)[:, 1]

print(classification_report(y_test, y_pred, target_names=['Non-essential', 'Essential']))
print(f"MCC: {matthews_corrcoef(y_test, y_pred):.3f}")

fpr, tpr, _ = roc_curve(y_test, y_prob)
print(f"AUC-ROC: {auc(fpr, tpr):.3f}")
plt.plot(fpr, tpr, label=f'RF (AUC={auc(fpr, tpr):.3f})')
plt.plot([0, 1], [0, 1], '--', color='gray')
plt.xlabel('False Positive Rate'); plt.ylabel('True Positive Rate')
plt.legend(); plt.title('Reaction Essentiality ROC Curve (e_coli_core)'); plt.show()
```

**예상 출력.** 다음과 같은 구성으로 출력됩니다 — 클래스별 정밀도·재현율·f1 점수를 담은 표, MCC 한 줄, AUC-ROC 한 줄, 그리고 ROC 곡선 그림입니다(각 칸의 구체적 숫자는 실행 환경에 따라 조금씩 달라질 수 있어 `…`로 표시합니다).

```
               precision    recall  f1-score   support

Non-essential       …         …         …          …
    Essential       …         …         …          …

     accuracy                           …          …
    macro avg       …         …         …          …
 weighted avg       …         …         …          …

MCC: …
AUC-ROC: …
```

**확인 포인트.** 오류 없이 `classification_report` 표, `MCC:` 값, `AUC-ROC:` 값이 차례로 출력되고 ROC 곡선 그림이 뜨면 성공입니다. 테스트 세트는 전체 95개 중 30%인 약 29개 반응입니다. ROC 곡선이 왼쪽 위 모서리에 가까울수록(대각선 위로 볼록할수록) 좋은 분류이며, AUC 값이 0.5(무작위)보다 크면 최소한 무작위보다는 낫다는 뜻입니다.

**자주 나는 오류와 해결.**
- `ModuleNotFoundError: No module named 'sklearn'` — scikit-learn을 설치하지 않았습니다. 준비물의 `pip install ... scikit-learn`을 실행합니다(설치 이름은 `scikit-learn`, import 이름은 `sklearn`입니다).
- 그림 창이 뜨지 않으면 Jupyter에서는 셀 맨 위에 `%matplotlib inline`을 한 번 실행하거나, 스크립트라면 `plt.show()`가 마지막 줄에 있는지 확인합니다.
- 표본이 워낙 작아 `random_state`를 바꾸면 지표가 크게 흔들립니다. 이는 오류가 아니라 아래에서 설명하는 소표본의 특성입니다.

`e_coli_core`는 반응이 95개뿐이라 학습 표본이 매우 적습니다 — [§3.5](03.md)에서 다룬 편향-분산 트레이드오프를 몸소 체험하기 좋은 조건입니다. 표본이 적을수록 `max_depth`를 낮추고 `class_weight='balanced'`를 유지하는 것이 과적합을 막는 데 중요합니다. 위 코드에서 `train_test_split(..., test_size=0.3, stratify=y)`는 [§2.5](02.md)에서 설명한 대로 전체 95개 반응 중 30%(약 29개)를 테스트 세트로 떼어 두고, `stratify=y`로 필수/비필수 비율을 훈련·테스트 양쪽 모두에서 원본과 같게(약 19% 필수) 유지합니다. 표본이 이렇게 작을 때는 단 한 번의 분할 결과가 운에 따라 크게 흔들릴 수 있으므로, 진지한 분석이라면 [§2.5](02.md)의 Stratified K-Fold로 여러 번 분할해 평균과 분산을 함께 보고하는 편이 안전합니다.

{% hint style="info" %}
**잠깐, 생각해보기:** 이 실습에서 `max_depth`를 3, 8, 20으로 각각 바꿔가며 훈련 정확도와 테스트 정확도를 비교해 봅니다. §3.5의 표에서 예상했듯 `max_depth=20`처럼 제한이 거의 없을 때 훈련 정확도는 100%에 가까워지지만 테스트 정확도는 오히려 낮아지는 과적합 패턴이 실제로 재현되는지 직접 확인해 보기를 권합니다.
{% endhint %}

## 단계 4. 여러 배양 조건의 FBA 플럭스를 K-Means로 클러스터링하기

**무엇을·왜.** 앞 세 단계가 "레이블이 있는 지도학습"이었다면, 이 단계는 정답 없이 구조를 찾는 **비지도학습**입니다. $$\mathbf{S}\mathbf{v}=\mathbf{0}$$을 그대로 둔 채 교환 반응(exchange reaction)의 하한만 바꾸면, 같은 `e_coli_core`로 산소·탄소원이 다른 여러 "대사 상태"의 플럭스 벡터를 만들 수 있습니다. [§2.3](02.md)의 손 계산 예제에서는 1차원 숫자 6개를 "1 근처"와 "8 근처" 두 그룹으로 나눴는데, 여기서는 그 "숫자"가 95차원 플럭스 벡터 6개(조건 6개)로 바뀔 뿐 K-Means의 원리는 완전히 같습니다 — 배정 단계에서 각 조건의 플럭스 벡터를 더 가까운 중심에 배정하고, 갱신 단계에서 각 그룹의 평균 벡터로 중심을 다시 계산하는 과정을 반복합니다. 아래 6개 조건은 크게 "산소가 있는 호기성 조건"(4개)과 "산소가 없는 혐기성 조건"(1개), 그리고 탄소원 자체가 다른 조건(아세테이트·숙신산)으로 나뉘어 있어, `n_clusters=2`로 두면 대사적으로 가장 크게 갈리는 발효 대 호흡 축을 따라 묶이는지 관찰하기 좋습니다.

**코드.** 아래 코드는 (1) 6개 배양 조건마다 교환 반응 하한을 바꿔 FBA를 풀어 플럭스 행렬을 만들고, (2) K-Means로 2개 군집으로 나눈 뒤, (3) PCA로 2차원에 투영해 각 조건이 어느 군집에 들어갔는지 출력하고 산점도로 그립니다. `with model:` 블록은 조건 변경을 그 블록 안에서만 적용하고 빠져나오면 원래 경계값으로 되돌립니다.

```python
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# 4장에서 배운 것처럼 교환 반응의 하한(lower_bound)만 바꿔 여러 조건을 만든다
conditions = {
    'aerobic_glucose':      {'EX_glc__D_e': -10, 'EX_o2_e': -20},
    'anaerobic_glucose':    {'EX_glc__D_e': -10, 'EX_o2_e': 0},
    'microaerobic_glucose': {'EX_glc__D_e': -10, 'EX_o2_e': -2},
    'aerobic_low_glucose':  {'EX_glc__D_e': -2,  'EX_o2_e': -20},
    'aerobic_acetate':      {'EX_glc__D_e': 0,   'EX_ac_e': -10, 'EX_o2_e': -20},
    'aerobic_succinate':    {'EX_glc__D_e': 0,   'EX_succ_e': -10, 'EX_o2_e': -20},
}

flux_rows, names = [], []
for name, bounds in conditions.items():
    with model:
        for ex_id, lb in bounds.items():
            model.reactions.get_by_id(ex_id).lower_bound = lb
        sol = model.optimize()
        flux_rows.append(sol.fluxes.values)
        names.append(name)

flux_matrix = np.array(flux_rows)  # (조건 수, 95)

kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
labels = kmeans.fit_predict(flux_matrix)

pca = PCA(n_components=2)
flux_2d = pca.fit_transform(flux_matrix)

for name, label in zip(names, labels):
    print(f"{name:>22s}  ->  cluster {label}")
# 기대 경향: 무산소(anaerobic_glucose)는 발효 대사 모드로,
#           나머지 호기 조건들과 다른 클러스터에 속할 가능성이 높다.

plt.scatter(flux_2d[:, 0], flux_2d[:, 1], c=labels, cmap='viridis', s=100)
for i, name in enumerate(names):
    plt.annotate(name, (flux_2d[i, 0], flux_2d[i, 1]))
plt.xlabel('PC1'); plt.ylabel('PC2')
plt.title('e_coli_core 배양 조건별 대사 상태 클러스터링'); plt.show()
```

**예상 출력.** 6개 조건 각각이 어느 군집(0 또는 1)에 배정됐는지 한 줄씩 출력되고, PC1-PC2 평면에 조건 이름이 붙은 산점도가 뜹니다. 출력 형식은 다음과 같습니다(군집 번호 0/1 자체는 임의로 매겨지므로 실행마다 뒤바뀔 수 있습니다).

```
       aerobic_glucose  ->  cluster ?
     anaerobic_glucose  ->  cluster ?
  microaerobic_glucose  ->  cluster ?
    aerobic_low_glucose  ->  cluster ?
       aerobic_acetate  ->  cluster ?
     aerobic_succinate  ->  cluster ?
```

**확인 포인트.** 6개 조건이 모두 출력되고 산점도가 뜨면 성공입니다. 코드 주석의 기대 경향처럼, 산소가 없는 `anaerobic_glucose`가 발효 대사 모드로 다른 호기성 조건들과 **다른 군집**에 속하는지 살펴봅니다. 군집 번호(0/1)의 절대값보다, 어떤 조건들이 **같은 군집으로 묶이는가**가 중요합니다.

**자주 나는 오류와 해결.**
- `KeyError: 'EX_ac_e'` 같은 오류 — 교환 반응 ID가 모델에 없을 때 납니다. `e_coli_core`에는 위 ID들이 모두 있으므로, 다른 모델을 불러오지 않았는지 단계 1의 `load_model("textbook")`을 확인합니다.
- 군집 배정이 실행마다 달라 보이면, `random_state=42`와 `n_init=10`(코드에 이미 지정됨)을 유지합니다. 표본이 6개뿐이라 초기화에 민감할 수 있습니다.

{% hint style="warning" %}
**해석상의 주의:** 이 4단계는 그래프 특징과 분류 평가를 익히는 교육용 파이프라인입니다. §3.2의 실제 MOMA-RF는 50개 유방암 세포주의 **MOMA flux vectors**를 특징으로 사용했고, FlowGAT/FluxGAT는 별도의 그래프 표현과 학습 설계를 사용했습니다. 문제 유형은 비슷하지만 입력과 검증 설계가 동일하지 않습니다.
{% endhint %}

## 정리

이 실습에서 다음을 했습니다.

- `e_coli_core` 하나로 그래프 특징 추출 → 필수성 레이블 생성 → Random Forest 학습·ROC/MCC 평가 → K-Means 클러스터링의 4단계 파이프라인을 처음부터 끝까지 실행했습니다.
- NetworkX로 반응-반응 그래프의 연결 차수·매개 중심성을, COBRApy로 야생형 플럭스(성장률 0.8739 h⁻¹)와 반응 결손 레이블(필수 18개, 비필수 77개)을 만들었습니다.
- scikit-learn의 Random Forest로 반응 필수성을 분류하고 ROC-AUC·MCC로 평가하며, 표본이 작을 때 과적합을 억제하는 방법을 확인했습니다.
- 서로 다른 배양 조건의 FBA 플럭스 벡터를 K-Means로 묶어, 발효 대 호흡 축을 따라 대사 상태가 갈리는지 관찰했습니다.
- 네 단계 모두 새 이론이 아니라 [§2](02.md)·[§3](03.md)에서 배운 도구의 재조합임을 확인했습니다.

## 스스로 해보기

아래 확장은 어느 것도 새 개념이 필요하지 않으며, 전부 이 장에서 이미 배운 도구의 재조합입니다. 정답 코드를 바로 참고하기 전에 먼저 스스로 시도해보길 권합니다.

1. **[§2.5](02.md)의 Stratified K-Fold 적용**: 단계 3의 단일 `train_test_split`을 5-fold 교차검증으로 바꿔, ROC-AUC와 MCC가 fold마다 얼마나 흔들리는지(표준편차) 확인해보십시오. 표본이 95개뿐이므로 분산이 꽤 클 수 있습니다.
2. **[§3.4](03.md)의 순열 중요도 계산**: `sklearn.inspection.permutation_importance`로 `degree`, `betweenness`, `wt_flux` 각각을 무작위로 섞었을 때 성능이 얼마나 떨어지는지 측정해, 기본 `feature_importances_`와 순위가 같은지 비교해보십시오.
3. **[§4](04.md)의 그래프 신경망으로 교체**: 단계 1에서 만든 `networkx` 그래프 `G`를 `torch_geometric.utils.from_networkx`로 변환한 뒤, §4.1의 `FlowGAT` 클래스에 `degree`·`wt_flux`를 노드 특징으로 넣어 학습해보고 RF와 성능을 비교해보십시오. 반응이 95개뿐이라 GNN이 RF보다 반드시 낫다고 기대하기는 어렵지만, §4의 코드를 실제로 손에 익히는 데는 좋은 연습이 됩니다.

이 심화 노트북(`raw_data/GEM_lecture_notes/gem9_w09_lab.ipynb`)에는 iML1515 규모로 확장한 같은 파이프라인과 Mann-Whitney U 검정을 이용한 특징 분포 비교가 함께 실려 있습니다. 이어지는 [Chapter 10](../chapter-10/README.md)은 이 장까지의 개념들을 하나의 실행 흐름으로 다시 검산하는 통합 실습입니다.

---
