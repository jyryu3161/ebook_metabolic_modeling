# 💡 실습: e_coli_core로 완성하는 특징추출 → RF → ROC → K-Means 파이프라인

> 💡 **실습:** 아래 코드는 §2~3에서 조각조각 만들어 온 것을 하나의 완결된 파이프라인으로 잇는다. 1장에서 불러온 `e_coli_core`(95개 반응·72개 대사물·137개 유전자)만으로 그래프 특징 추출→필수성 레이블→Random Forest→ROC 평가→K-Means 대사상태 클러스터링까지 전부 실행할 수 있다. 더 큰 규모(iML1515)의 완전한 파이프라인과 5-fold 교차검증, Permutation Importance, Mann-Whitney U 검정 등 심화 내용은 합성 대사 네트워크 기반 특징 공학을 다루는 `raw_data/GEM_lecture_notes/gem9_w09_lab.ipynb` 노트북을 참고한다.

이 실습이 지금까지 무엇을 짜맞추는 것인지 미리 지도를 그려보자. 아래 4단계는 각각 이 장의 특정 절에서 배운 개념을 정확히 재사용한다 — 새로운 개념은 없다. 1단계는 [§2.2](02.md)의 그래프 특징 추출(연결 차수·매개 중심성), 2단계는 [§2.6](02.md)·[§3.4](03.md)의 필수성 레이블 만들기, 3단계는 [§2.1](02.md)·[§2.6](02.md)의 Random Forest 학습과 ROC/MCC 평가, 4단계는 [§2.3](02.md)의 K-Means 클러스터링을 그대로 따른다. 즉 이 실습의 목표는 새 이론을 배우는 것이 아니라, 흩어져 있던 코드 조각들이 실제로는 하나의 매끄러운 파이프라인으로 이어진다는 것을 눈으로 확인하는 데 있다.

```mermaid
flowchart LR
    S1["1단계<br/>그래프 특징 추출<br/>(§2.2)"] --> S2["2단계<br/>필수성 레이블 생성<br/>(§2.6, §3.4)"]
    S2 --> S3["3단계<br/>Random Forest 학습·평가<br/>(§2.1, §2.6)"]
    S3 --> S4["4단계<br/>K-Means 클러스터링<br/>(§2.3)"]
```

*그림 9.9. 제9장 교육용 실행 파이프라인. `e_coli_core` 반응 그래프에서 degree·betweenness·wild-type flux 특징을 만들고, 모델 계산으로 만든 필수성 레이블을 Random Forest로 분류한 뒤 ROC·MCC를 평가하며, 별도의 배양 조건별 flux 행렬은 PCA와 K-Means로 탐색합니다. 이 네 단계는 동일한 외부 benchmark의 성능 보고가 아니라 API와 평가 절차를 연결한 소표본 실습입니다. 출처: 저자 자체 제작; 계산 구현은 아래 [COBRApy](https://opencobra.github.io/cobrapy/)·[NetworkX](https://networkx.org/)·[scikit-learn](https://scikit-learn.org/) 코드이며 외부 그림을 재사용하지 않았습니다.*

## 1단계 — 모델 로드와 그래프 특징 추출

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

## 2단계 — 플럭스 특징과 필수성 레이블

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

## 3단계 — Random Forest 학습과 ROC 평가

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

`e_coli_core`는 반응이 95개뿐이라 학습 표본이 매우 적다 — [§3.5](03.md)에서 다룬 편향-분산 트레이드오프를 몸소 체험하기 좋은 조건이다. 표본이 적을수록 `max_depth`를 낮추고 `class_weight='balanced'`를 유지하는 것이 과적합을 막는 데 중요하다. 위 코드에서 `train_test_split(..., test_size=0.3, stratify=y)`는 [§2.5](02.md)에서 설명한 대로 전체 95개 반응 중 30%(약 29개)를 테스트 세트로 떼어 두고, `stratify=y`로 필수/비필수 비율을 훈련·테스트 양쪽 모두에서 원본과 같게(약 19% 필수) 유지한다. 표본이 이렇게 작을 때는 단 한 번의 분할 결과가 운에 따라 크게 흔들릴 수 있으므로, 진지한 분석이라면 [§2.5](02.md)의 Stratified K-Fold로 여러 번 분할해 평균과 분산을 함께 보고하는 편이 안전하다.

{% hint style="info" %}
💡 **잠깐, 생각해보기:** 이 실습에서 `max_depth`를 3, 8, 20으로 각각 바꿔가며 훈련 정확도와 테스트 정확도를 비교해보자. §3.5의 표에서 예상했듯 `max_depth=20`처럼 제한이 거의 없을 때 훈련 정확도는 100%에 가까워지지만 테스트 정확도는 오히려 낮아지는 과적합 패턴이 실제로 재현되는지 직접 확인해보길 권한다.
{% endhint %}

## 4단계 — 여러 배양 조건의 FBA 플럭스를 K-Means로 클러스터링

$$\mathbf{S}\mathbf{v}=\mathbf{0}$$을 그대로 둔 채 교환 반응(exchange reaction)의 하한만 바꾸면, 같은 `e_coli_core`로 산소·탄소원이 다른 여러 "대사 상태"의 플럭스 벡터를 만들 수 있다. [§2.3](02.md)의 손 계산 예제에서는 1차원 숫자 6개를 "1 근처"와 "8 근처" 두 그룹으로 나눴는데, 여기서는 그 "숫자"가 95차원 플럭스 벡터 6개(조건 6개)로 바뀔 뿐 K-Means의 원리는 완전히 같다 — 배정 단계에서 각 조건의 플럭스 벡터를 더 가까운 중심에 배정하고, 갱신 단계에서 각 그룹의 평균 벡터로 중심을 다시 계산하는 과정을 반복한다. 아래 6개 조건은 크게 "산소가 있는 호기성 조건"(4개)과 "산소가 없는 혐기성 조건"(1개), 그리고 탄소원 자체가 다른 조건(아세테이트·숙신산)으로 나뉘어 있어, `n_clusters=2`로 두면 대사적으로 가장 크게 갈리는 발효 대 호흡 축을 따라 묶이는지 관찰하기 좋다.

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

이 4단계는 그래프 특징과 분류 평가를 익히는 교육용 파이프라인입니다. §3.2의 실제 MOMA-RF는 50개 유방암 세포주의 **MOMA flux vectors**를 특징으로 사용했고, FlowGAT/FluxGAT는 별도의 그래프 표현과 학습 설계를 사용했습니다. 문제 유형은 비슷하지만 입력과 검증 설계가 동일하지 않습니다.

### 더 해보고 싶다면: 심화 방향 세 가지

이 4단계를 모두 실행해봤다면, 다음 확장을 스스로 시도해보길 권한다. 어느 것도 새 개념이 필요하지 않으며, 전부 이 장에서 이미 배운 도구의 재조합이다.

1. **§2.5의 Stratified K-Fold 적용**: 3단계의 단일 `train_test_split`을 5-fold 교차검증으로 바꿔, ROC-AUC와 MCC가 fold마다 얼마나 흔들리는지(표준편차) 확인해보자. 표본이 95개뿐이므로 분산이 꽤 클 수 있다.
2. **§3.4의 순열 중요도 계산**: `sklearn.inspection.permutation_importance`로 `degree`, `betweenness`, `wt_flux` 각각을 무작위로 섞었을 때 성능이 얼마나 떨어지는지 측정해, 기본 `feature_importances_`와 순위가 같은지 비교해보자.
3. **§4의 그래프 신경망으로 교체**: 1단계에서 만든 `networkx` 그래프 `G`를 `torch_geometric.utils.from_networkx`로 변환한 뒤, §4.1의 `FlowGAT` 클래스에 `degree`·`wt_flux`를 노드 특징으로 넣어 학습해보고 RF와 성능을 비교해보자. 반응이 95개뿐이라 GNN이 RF보다 반드시 낫다고 기대하기는 어렵지만, §4의 코드를 실제로 손에 익히는 데는 좋은 연습이 된다.

이 심화 노트북(`raw_data/GEM_lecture_notes/gem9_w09_lab.ipynb`)에는 iML1515 규모로 확장한 같은 파이프라인과 Mann-Whitney U 검정을 이용한 특징 분포 비교가 함께 실려 있다.

---
