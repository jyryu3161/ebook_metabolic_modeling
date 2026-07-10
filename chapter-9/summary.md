# 마무리: 요약 · 스스로 점검 · 용어

## 한 장 요약

- 전통적 [FBA](../chapter-4/README.md) 기반 방법은 계산 확장성, 목적함수 의존, 비선형성 포착 불가, 큐레이션 병목의 한계를 가지며, AI/ML은 각각에 대응하는 방법론(서로게이트, 모델-자유 RL, GNN/딥러닝, LLM)으로 발전했다 — "정밀한 지도"(GEM)와 "베테랑의 직감"(ML)의 상생 관계다.
- Kim et al. (2026)의 MOMA-RF는 50개 유방암 세포주에서 민감도를 0.37→0.55, MCC를 0.27→0.33으로 높였지만 precision은 0.33→0.31로 낮아졌습니다. 이는 모든 지표의 일괄 향상이 아니라 recall-precision 절충입니다.
- GNN과 토폴로지 제약 신경망은 목적함수 의존성을 줄이거나 네트워크 구조를 학습에 넣을 수 있지만, 배지·샘플링·데이터 선택 의존성과 외부 검증의 필요성은 남습니다.
- 서로게이트의 가속 배수는 하드웨어·batch·solver·예측 horizon에 종속됩니다. 후보 선별 뒤 원 최적화로 재검산하고 제약 위반과 분포 밖 오차를 따로 측정해야 합니다.
- MARL의 12회·95% 결과는 기존 L-tryptophan 라이브러리를 이용한 가상/retrospective 벤치마크입니다. 실제 물리적 DBTL 폐쇄 루프 검증과 구분해야 합니다.
- Human2는 LLM이 전문가 검토 후보를 선별하고 GitHub Actions가 회귀검사를 수행하는 **인간 참여형 큐레이션** 사례입니다. generic Human2와 그로부터 파생한 organ/whole-body/dynamic models를 구분해야 합니다.
- Virtual Cell·디지털 트윈·자율 연구소는 현재 제한된 구성 요소와 특정 과제의 시연이 존재하는 장기 연구 의제입니다. end-to-end 자율 전세포 모델이 이미 완성된 것으로 서술해서는 안 됩니다.
- `e_coli_core`(95개 반응)만으로도 그래프 특징 추출 → RF 필수성 예측 → ROC 평가 → K-Means 클러스터링의 전체 파이프라인을 직접 실행하고 눈으로 확인할 수 있다.

## 스스로 점검

1. **개념**: FBA 기반 필수성 예측의 목적함수 의존성이 무엇이며, flux sampling이 이를 어떻게 줄이되 어떤 분석자 선택은 남기는지 설명하라.
   > *힌트*: 단일 biomass optimum에 묶이지 않지만 배지 경계·가역성·샘플링 방법과 학습 자료 선택에는 여전히 의존합니다.

2. **계산**: 어떤 분류기가 총 100개 반응(그중 10개가 실제 필수) 중 $$TP=8,\ FN=2,\ FP=6,\ TN=84$$로 예측했다. Accuracy, Recall, Precision, MCC를 계산하고, "모든 반응을 비필수로 예측"하는 전략의 Accuracy(90%)와 비교했을 때 어느 지표가 더 신뢰할 만한지 논하라.
   > *힌트*: Accuracy $$=\frac{8+84}{100}=92\%$$, Recall $$=\frac{8}{10}=0.8$$, Precision $$=\frac{8}{14}\approx0.571$$, MCC $$=\frac{8\times84-6\times2}{\sqrt{14\times10\times90\times92}}\approx0.61$$. 두 전략 모두 Accuracy는 90% 안팎으로 비슷해 보이지만 "모두 비필수" 전략은 Recall=0으로 아무 표적도 찾지 못한다 — MCC·Recall이 목적에 맞는 지표다.

3. **개념**: 초그래프(Hypergraph)가 일반 그래프보다 대사 반응 표현에 적합한 이유를 반응 하나를 예로 들어 설명하라.
   > *힌트*: §5.1의 6개 대사물이 참여하는 반응 예시를 참고하라. 일반 그래프의 엣지는 두 노드만 연결한다.

4. **분석**: 다음 세 상황 — (a) 발효기 실시간 제어, (b) 배지 조성의 gradient 기반 최적화, (c) 논문 제출 전 최종 검증 — 에 각각 가장 적합한 서로게이트/방법을 §6.3의 표에서 골라 이유와 함께 제시하라.

5. **비판적 사고**: 제약을 내장하지 않은 한 생성 실험에서 flux 표본이 화학량론 검사를 통과하지 못한 결과가 시사하는 바를 설명하고, 페널티·투영·정확한 최적화 층의 보장 수준을 비교하라.
   > *힌트*: §10.2와 §1.1의 "지도와 직감" 비유를 연결해 보라.

## 다음 장: 이론을 실행으로 검산하기

이 책의 이론 여정은 아홉 개 장에 걸쳐 하나의 길을 걸어왔다. [Chapter 1](../chapter-1/README.md)에서 대사라는 현상 자체의 복잡성에서 출발해, [Chapter 2](../chapter-2/README.md)에서 그 복잡성을 화학량론 행렬 $$\mathbf{S}$$와 $$\mathbf{S}\mathbf{v}=\mathbf{0}$$이라는 숫자와 방정식으로 옮겼다. [Chapter 3](../chapter-3/README.md)에서 GPR·구획·바이오매스 반응으로 그 뼈대에 생물학적 살을 입혔고, [Chapter 4](../chapter-4/README.md)에서 마침내 그 모델로 세포의 행동(FBA)을 예측했다. [Chapter 5](../chapter-5/README.md)는 그 모델 자체가 어떻게 만들어지고 검증되는지를, [Chapter 6](../chapter-6/README.md)은 범용 모델을 특정 맥락에 맞추는 법을, [Chapter 7](../chapter-7/README.md)과 [Chapter 8](../chapter-8/README.md)은 그렇게 완성된 모델을 질병 이해·약물 표적 발굴·세포공장 설계라는 실전 문제에 적용하는 법을 보여주었다.

그리고 이 장에서 우리는 그 모든 것 위에 머신러닝이 어떻게 포개어지는지 보았다 — 지도와 직감이 함께 일할 때 무엇이 가능해지는지를. `e_coli_core`라는 작은 모델 하나가 1장의 첫 `cobra.io.load_model("textbook")` 한 줄에서 시작해, 9장의 그래프 신경망·Random Forest·K-Means 클러스터링에 이르기까지 아홉 개 장 내내 우리 곁에 있었다는 사실이, 이 책이 전하고 싶었던 가장 중요한 메시지를 함축한다: **대사모델링은 하나의 고정된 기법이 아니라, 화학량론이라는 단단한 뼈대 위에 점점 더 많은 데이터와 방법론을 쌓아 올리는 살아있는 과정**이라는 것이다.

AI+GEM 분야는 빠르게 변하므로 연도별 수치 예측보다 모델·데이터·solver 버전을 고정하고 독립 자료로 재검증하는 습관이 중요합니다. 먼저 [Chapter 10의 완전 실행형 COBRApy 튜토리얼](../chapter-10/README.md)에서 FBA·pFBA·FVA·결손·MOMA·ROOM·작은 MILP·SBML 왕복을 같은 모델로 직접 검산하십시오. 그다음 [랜드마크 논문 가이드](../landmark-papers.md)에서 각 방법의 원 질문을 확인하고, 자신의 생물종·질병·공정에서 외부 검증이 가능한 작은 문제로 옮기는 것이 좋습니다.

## 핵심 용어 정리

| 용어(한글) | English | 정의 |
|:---|:---|:---|
| 지도학습 | Supervised Learning | 입력-정답 쌍으로부터 매핑 함수를 학습하는 ML 패러다임 |
| 랜덤 포레스트 | Random Forest | 다수 결정 트리를 앙상블하는 분류/회귀 알고리즘 |
| 매튜 상관계수 | Matthews Correlation Coefficient(MCC) | 클래스 불균형에 강건한 이진 분류 성능 지표 |
| 그래프 신경망 | Graph Neural Network(GNN) | 메시지 패싱으로 그래프 구조 데이터를 처리하는 신경망 |
| 그래프 어텐션 네트워크 | Graph Attention Network(GAT) | 이웃별 주의력 가중치를 학습하는 GNN 변형 |
| 관찰자 편향 | Observer Bias | 예측 결과가 연구자가 선택한 목적함수에 의존하는 문제 |
| 초그래프 | Hypergraph | 하나의 엣지가 임의 수의 노드를 연결할 수 있는 그래프의 일반화 |
| 서로게이트 모델 | Surrogate Model | 계산 비용이 높은 원본 함수(FBA 등)를 근사하는 빠른 모델 |
| 미분 가능 대사 최적화 계층 | Differentiable metabolic optimization layer | 최적화 또는 반복 mechanistic 계산을 학습 그래프에 넣어 역전파할 수 있게 한 계층; dynamic FBA와는 다른 개념 |
| 강화학습 | Reinforcement Learning(RL) | 에이전트가 보상을 최대화하는 행동을 학습하는 패러다임 |
| 다중 에이전트 강화학습 | Multi-Agent RL(MARL) | 여러 에이전트가 동시에 학습·상호작용하는 RL 설정 |
| 대형 언어 모델 | Large Language Model(LLM) | Transformer 기반 대규모 사전학습 언어 모델 |
| 환각 | Hallucination | LLM이 사실과 다른 그럴듯한 정보를 생성하는 현상 |
| Foundation Model | Foundation Model | 방대한 데이터로 사전학습되어 다양한 과제에 전이되는 대규모 모델 |
| 가상 세포 | Virtual Cell | 여러 생물학적 모델과 데이터를 연결해 세포 상태를 예측하려는 장기 연구 의제 |
| 디지털 트윈 | Digital Twin(DT) | 물리적 대상의 측정값으로 상태를 갱신하며 예측·제어를 지원하는 계산 모델 |
| 자율 연구소 | Self-Driving Laboratory(SDL) | 설계-실험-측정-학습 순환의 일부 또는 전부를 자동화하는 시스템; 자동화 범위를 명시해야 함 |
| 화학량론적 타당성 | Stoichiometric Feasibility | 예측된 플럭스가 질량 보존 제약 $$S \cdot v = 0$$을 만족하는 성질 |
| 불확실성 정량화 | Uncertainty Quantification | 예측값과 함께 신뢰도·분산 정보를 제공하는 것 |
| Design-Build-Test-Learn | DBTL | 대사공학의 반복적 실험 설계 프레임워크 |

## 참고문헌

1. Kim BK, Gu C, Farh MEA, Ryu JY (2026). "Integrating Genome-Scale Metabolic Modeling with Machine Learning Improves Gene Essentiality Prediction in Triple-Negative Breast Cancer." *International Journal of Molecular Sciences* 27(11):5059. DOI: 10.3390/ijms27115059.
2. Hasibi R, Michoel T, Oyarzún DA (2024). ["Integration of graph neural networks and genome-scale metabolic models for predicting gene essentiality."](https://doi.org/10.1038/s41540-024-00348-2) *npj Systems Biology and Applications* 10:24.
3. Chen C, Liao C, Liu Y-Y (2023). ["Teasing out missing reactions in genome-scale metabolic networks through hypergraph learning."](https://doi.org/10.1038/s41467-023-38110-7) *Nature Communications* 14:2375.
4. Liu X et al. (2024). ["A generalizable framework for unlocking missing reactions in genome-scale metabolic networks using deep learning."](https://arxiv.org/abs/2409.13259) arXiv:2409.13259 (CLOSEgaps preprint).
5. Zhao Y et al. (2026). ["A multi-way SMILES-based hypergraph inference network for metabolic model reconstruction."](https://doi.org/10.1038/s42003-026-09761-1) *Communications Biology* 9:531.
6. Sabzevari M, Szedmak S, Penttilä M, Jouhten P, Rousu J (2022). ["Strain design optimization using reinforcement learning."](https://doi.org/10.1371/journal.pcbi.1010177) *PLoS Computational Biology* 18:e1010177.
7. Luo J, Wang H, Moyer D, et al. (2026). "Reconstruction of human metabolic models with large language models." *PNAS* 123(15):e2516511123. DOI: 10.1073/pnas.2516511123.
8. Li X et al. (2026). ["Leveraging large language models for metabolic engineering design."](https://doi.org/10.1016/j.tibtech.2026.03.026) *Trends in Biotechnology*. — D2Cell.
9. DeepMind (2024). "AlphaFold 3: Predicting the structure and interactions of all of life's molecules." *Nature*.
10. EvolutionaryScale (2024). "ESM-3: Simulating 500 million years of evolution with a language model."
11. Tschauner et al. (2023). "Model predictive control of a fermenter using dynamic flux balance analysis coupled with convolutional neural networks." *Computers & Chemical Engineering*.
12. Aghaee M, Krau S, Tamer M, Budman H (2024). ["Graph Neural Network Representation of State Space Models of Metabolic Pathways."](https://doi.org/10.1016/j.ifacol.2024.08.380) *IFAC-PapersOnLine* 58:464–469.
13. Sharma K, Marucci L, Abdallah ZS (2026). ["Flux sampling and graph neural networks for improved gene essentiality prediction in mammalian genome-scale metabolic models."](https://doi.org/10.1038/s41540-026-00738-8) *npj Systems Biology and Applications*.
14. Huang Y, Liang X, Lin T, Liu J (2025). ["Multi-HGNN: Multi-modal hypergraph neural networks for predicting missing reactions in metabolic networks."](https://doi.org/10.1016/j.ins.2025.121960) *Information Sciences* 704:121960.
15. Faure L, Mollet B, Liebermeister W, et al. (2023). ["A neural-mechanistic hybrid approach improving the predictive power of genome-scale metabolic models."](https://doi.org/10.1038/s41467-023-40380-0) *Nature Communications* 14:4669. — AMN.
16. COBRApy: https://github.com/opencobra/cobrapy · DepMap: https://depmap.org/portal/ · MEMOTE: https://github.com/opencobra/memote
17. GECKO 3.0: https://github.com/SysBioChalmers/GECKO · ECMpy 2.0: https://github.com/synbio-eecmp/ECMpy
18. Palsson, B.O. (2015). *Systems Biology: Constraint-based Reconstruction and Analysis*, 2nd ed. Cambridge University Press.
19. Lewis, N.E. et al. (2012). "Constraining the metabolic genotype-phenotype relationship using a phylogeny of in silico methods." *Nature Reviews Microbiology*, 10(4), 291-305.

> 본 장의 원 강의자료(9주차, `gem9_w09/week9_ebook.md`)는 2025년 7월 작성되었으며, 인용된 연구는 2023-2026년 사이 발표분을 중심으로 한다. AI+GEM 분야는 빠르게 발전하므로 최신 문헌을 지속적으로 추적할 것을 권장한다.
