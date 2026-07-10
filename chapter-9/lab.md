# 💡 실습: e_coli_core로 완성하는 특징추출 → RF → ROC → K-Means 파이프라인

> 💡 **실습:** 아래 코드는 §2~3에서 조각조각 만들어 온 것을 하나의 완결된 파이프라인으로 잇는다. 1장에서 불러온 `e_coli_core`(95개 반응·72개 대사물·137개 유전자)만으로 그래프 특징 추출→필수성 레이블→Random Forest→ROC 평가→K-Means 대사상태 클러스터링까지 전부 실행할 수 있다. 더 큰 규모(iML1515)의 완전한 파이프라인과 5-fold 교차검증, Permutation Importance, Mann-Whitney U 검정 등 심화 내용은 합성 대사 네트워크 기반 특징 공학을 다루는 `raw_data/GEM_lecture_notes/gem9_w09_lab.ipynb` 노트북을 참고한다.

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

`e_coli_core`는 반응이 95개뿐이라 학습 표본이 매우 적다 — §3.3에서 다룬 편향-분산 트레이드오프를 몸소 체험하기 좋은 조건이다. 표본이 적을수록 `max_depth`를 낮추고 `class_weight='balanced'`를 유지하는 것이 과적합을 막는 데 중요하다.

## 4단계 — 여러 배양 조건의 FBA 플럭스를 K-Means로 클러스터링

$$\mathbf{S}\mathbf{v}=\mathbf{0}$$을 그대로 둔 채 교환 반응(exchange reaction)의 하한만 바꾸면, 같은 `e_coli_core`로 산소·탄소원이 다른 여러 "대사 상태"의 플럭스 벡터를 만들 수 있다.

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

---
