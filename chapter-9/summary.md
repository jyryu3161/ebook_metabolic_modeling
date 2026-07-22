# 마무리: 요약 · 스스로 점검 · 용어

## 이 장의 수식 한눈에 보기

본격적인 요약에 앞서, 이 장에서 등장한 핵심 수식을 한 곳에 모은 표부터 정리한다. 각 식이 어느 절에서 왜 필요했는지 기억나지 않으면 해당 절을 다시 참고한다.

| 수식 | 절 | 한 줄 의미 |
|:---|:---:|:---|
| $$\theta^\star=\arg\min_\theta \frac{1}{n}\sum_i L(y_i,f_\theta(\mathbf{x}_i))$$ | §1.1.1 | "학습"이란 평균 손실을 최소화하는 파라미터 찾기 |
| $$P(Y=1\mid\mathbf{x})=\sigma(\mathbf{w}^T\mathbf{x}+b)$$ | §2.1 | 로지스틱 회귀: 가중합을 확률로 압축 |
| $$L=-[y\log\hat y+(1-y)\log(1-\hat y)]$$ | §2.1 | 교차 엔트로피(로그 손실): 자신 있게 틀릴수록 더 큰 벌점 |
| $$\mathbf{w}\leftarrow\mathbf{w}-\eta\,\partial\mathcal{L}/\partial\mathbf{w}$$ | §2.1 | 경사하강법: 손실이 줄어드는 방향으로 한 걸음 |
| $$\hat y=\mathbf{w}^T\mathbf{x}+b,\ \ \text{MSE}=\frac1n\sum(y_i-\hat y_i)^2$$ | §2.1 | 선형 회귀와 평균제곱오차 |
| $$\arg\min_{\mathbf C}\sum_k\sum_{\mathbf v\in C_k}\lVert \mathbf v-\boldsymbol\mu_k\rVert^2$$ | §2.3 | K-Means: 그룹 내 거리 제곱합을 최소화 |
| $$\text{MCC}=\dfrac{TP\cdot TN-FP\cdot FN}{\sqrt{(TP+FP)(TP+FN)(TN+FP)(TN+FN)}}$$ | §2.6 | 클래스 불균형에 강건한 단일 성능 지표 |
| $$\text{AUC}\approx\sum_k\frac{(FPR_{k+1}-FPR_k)(TPR_{k+1}+TPR_k)}{2}$$ | §2.6 | ROC 곡선 아래 면적을 사다리꼴로 근사 |
| $$\mathbf h_v^{(l+1)}=\text{UPDATE}(\mathbf h_v^{(l)},\text{AGGREGATE}(\{\mathbf h_u^{(l)}:u\in\mathcal N(v)\}))$$ | §4.1 | GNN 메시지 패싱: 이웃 정보를 모아 자신을 갱신 |
| $$\alpha_{vu}=\text{softmax}_u(\text{LeakyReLU}(\mathbf a^T[\mathbf W\mathbf h_v\|\mathbf W\mathbf h_u]))$$ | §4.1 | GAT: 이웃마다 다른 attention 가중치 |
| $$H=(V,\mathcal E),\ \mathcal E\subseteq 2^V$$ | §5.1 | 초그래프: 하나의 초엣지가 임의 개수의 노드를 연결 |
| $$Q(s,a)\leftarrow Q(s,a)+\alpha[r+\gamma\max_{a'}Q(s',a')-Q(s,a)]$$ | §7.1 | Q-Learning: TD 오차만큼 가치 추정을 갱신 |
| $$\text{Attention}(Q,K,V)=\text{softmax}(QK^T/\sqrt{d_k})V$$ | §8 | Self-Attention: 단어끼리 서로 얼마나 참고할지 계산 |
| $$v_i\leq k_{cat,i}\cdot[E_i]$$ | §9.3 | GECKO: 효소 용량이 플럭스의 상한을 제한 |

## 한 장 요약

- 전통적 [FBA](../chapter-4/README.md) 기반 방법은 계산 확장성, 목적함수 의존, 비선형성 포착 불가, 큐레이션 병목의 한계를 가지며, AI/ML은 각각에 대응하는 방법론(서로게이트, 모델-자유 RL, GNN/딥러닝, LLM)으로 발전했다 — "정밀한 지도"(GEM)와 "베테랑의 직감"(ML)의 상생 관계다. `e_coli_core`의 이중 결손 스크리닝만 해도 9,316번, iML1515 규모에서는 100만 번이 넘는 LP가 필요하다는 §1.1.2의 계산이 이 한계를 숫자로 보여준다.
- ML의 "학습"은 결국 손실함수를 정의하고 경사하강법으로 파라미터를 갱신하는 최적화 과정이다. 로지스틱 회귀·선형 회귀·K-Means·GNN·Q-Learning·Self-Attention은 이름은 다르지만 모두 이 골격(가중합 → 비선형 함수 → 손실 → 갱신) 위에 서 있으며, §2~9 곳곳의 손 계산 예제로 이 사실을 직접 확인했다.
- [Kim et al. (2026)](https://doi.org/10.3390/ijms27115059)의 MOMA-RF는 50개 유방암 세포주에서 민감도를 0.37→0.55, MCC를 0.27→0.33으로 높였지만 precision은 0.33→0.31로 낮아졌다. 이는 모든 지표의 일괄 향상이 아니라 recall-precision 절충이다.
- GNN과 토폴로지 제약 신경망은 목적함수 의존성을 줄이거나 네트워크 구조를 학습에 넣을 수 있지만, 배지·샘플링·데이터 선택 의존성과 외부 검증의 필요성은 남는다.
- 서로게이트의 가속 배수는 하드웨어·batch·solver·예측 horizon에 종속된다. 후보 선별 뒤 원 최적화로 재검산하고 제약 위반과 분포 밖 오차를 따로 측정해야 한다.
- MARL의 12회·95% 결과는 기존 L-tryptophan 라이브러리를 이용한 가상/retrospective 벤치마크이다. 실제 물리적 DBTL 폐쇄 루프 검증과 구분해야 한다.
- Human2는 LLM이 전문가 검토 후보를 선별하고 GitHub Actions가 회귀검사를 수행하는 **인간 참여형 큐레이션** 사례이다. generic Human2와 그로부터 파생한 organ/whole-body/dynamic models를 구분해야 한다.
- Virtual Cell·디지털 트윈·자율 연구소는 현재 제한된 구성 요소와 특정 과제의 시연이 존재하는 장기 연구 의제이다. end-to-end 자율 전세포 모델이 이미 완성된 것으로 서술해서는 안 된다.
- `e_coli_core`(95개 반응)만으로도 그래프 특징 추출 → RF 필수성 예측 → ROC 평가 → K-Means 클러스터링의 전체 파이프라인을 직접 실행하고 눈으로 확인할 수 있다.

## 스스로 점검

1. **개념**: FBA 기반 필수성 예측의 목적함수 의존성이 무엇이며, flux sampling이 이를 어떻게 줄이되 어떤 분석자 선택은 남기는지 설명하라.
   > *힌트*: 단일 biomass optimum에 묶이지 않지만 배지 경계·가역성·샘플링 방법과 학습 자료 선택에는 여전히 의존한다.

2. **계산**: 어떤 분류기가 총 100개 반응(그중 10개가 실제 필수) 중 $$TP=8,\ FN=2,\ FP=6,\ TN=84$$로 예측했다. Accuracy, Recall, Precision, MCC를 계산하고, "모든 반응을 비필수로 예측"하는 전략의 Accuracy(90%)와 비교했을 때 어느 지표가 더 신뢰할 만한지 논하라.
   > *힌트*: §2.6의 Accuracy·Recall·Precision·MCC 정의식에 주어진 네 값을 그대로 대입한다. 비교할 때는 "모든 반응을 비필수로 예측"하는 전략에서 $$TP$$가 얼마가 되는지부터 따져 보고, 그 값이 어느 지표를 0으로 만드는지 확인한다. 풀이는 아래 「답안」 절에 있다.

3. **개념**: 초그래프(Hypergraph)가 일반 그래프보다 대사 반응 표현에 적합한 이유를 반응 하나를 예로 들어 설명하라.
   > *힌트*: §5.1의 6개 대사물이 참여하는 반응 예시를 참고하라. 일반 그래프의 엣지는 두 노드만 연결한다.

4. **분석**: 다음 세 상황 — (a) 발효기 실시간 제어, (b) 배지 조성의 gradient 기반 최적화, (c) 논문 제출 전 최종 검증 — 에 각각 가장 적합한 서로게이트/방법을 §6.3의 표에서 골라 이유와 함께 제시하라.

5. **비판적 사고**: 제약을 내장하지 않은 한 생성 실험에서 flux 표본이 화학량론 검사를 통과하지 못한 결과가 시사하는 바를 설명하고, 페널티·투영·정확한 최적화 층의 보장 수준을 비교하라.
   > *힌트*: §10.2와 §1.1의 "지도와 직감" 비유를 연결해 보라.

6. **계산**: 현재 파라미터 $$w=1.0,\ b=0$$, 학습률 $$\eta=0.2$$인 로지스틱 회귀가 입력 $$x=1.5$$, 정답 $$y=0$$인 예제 하나를 만났다. $$z, \hat y=\sigma(z)$$, 오차, 그래디언트, 갱신된 $$w$$를 §2.1의 손 계산 예제와 같은 방식으로 계산하라.
   > *힌트*: §2.1의 손 계산 예제와 같은 순서로 $$z=wx+b$$ → $$\hat y=\sigma(z)$$ → 오차 $$\hat y-y$$ → 그래디언트 $$(\hat y-y)x$$ → 갱신식 $$w\leftarrow w-\eta\,\partial\mathcal{L}/\partial w$$를 차례로 적용한다. 정답이 0인데 예측이 0.5보다 큰 상황이므로, 계산에 앞서 $$w$$가 커질지 작아질지 부호를 먼저 예상한 뒤 결과와 대조한다. 풀이는 아래 「답안」 절에 있다.

7. **개념**: §4.1의 GNN 손 계산 예제에서 R1의 1층 갱신값이 3.5였다. 만약 R4(D→E)가 추가되어 R3의 이웃이 R1, R2, R4로 늘어난다면, R3의 1층 갱신값(R4의 초기 특징을 $$h_{R4}^{(0)}=0.6$$이라 하자)이 어떻게 달라지는지 §4.1의 갱신식으로 계산하라.
   > *힌트*: §4.1의 갱신식 $$h_v^{(1)}=\text{ReLU}\big(h_v^{(0)}+\text{mean}_{u\in\mathcal N(v)}h_u^{(0)}\big)$$를 쓴다. R3의 이웃 집합이 어떻게 바뀌는지 먼저 적고, 평균의 분모가 2에서 3으로 늘어난 점을 반영해 이웃 평균을 다시 계산한다. 새로 들어온 이웃의 초기 특징이 기존 두 이웃보다 작다는 점에 유의해 값이 오를지 내릴지 예상한 뒤 대조한다. 풀이는 아래 「답안」 절에 있다.

## 다음 장: 이론을 실행으로 검산하기

이 책의 이론 여정은 아홉 개 장에 걸쳐 하나의 길을 걸어왔다. [Chapter 1](../chapter-1/README.md)에서 대사라는 현상 자체의 복잡성에서 출발해, [Chapter 2](../chapter-2/README.md)에서 그 복잡성을 화학량론 행렬 $$\mathbf{S}$$와 $$\mathbf{S}\mathbf{v}=\mathbf{0}$$이라는 숫자와 방정식으로 옮겼다. [Chapter 3](../chapter-3/README.md)에서 GPR·구획·바이오매스 반응으로 그 뼈대에 생물학적 살을 입혔고, [Chapter 4](../chapter-4/README.md)에서 마침내 그 모델로 세포의 행동(FBA)을 예측했다. [Chapter 5](../chapter-5/README.md)는 그 모델 자체가 어떻게 만들어지고 검증되는지를, [Chapter 6](../chapter-6/README.md)은 범용 모델을 특정 맥락에 맞추는 법을, [Chapter 7](../chapter-7/README.md)과 [Chapter 8](../chapter-8/README.md)은 그렇게 완성된 모델을 질병 이해·약물 표적 발굴·세포공장 설계라는 실전 문제에 적용하는 법을 보여주었다.

그리고 이 장에서 우리는 그 모든 것 위에 머신러닝이 어떻게 포개어지는지 보았다 — 지도와 직감이 함께 일할 때 무엇이 가능해지는지를. `e_coli_core`라는 작은 모델 하나가 1장의 첫 `cobra.io.load_model("textbook")` 한 줄에서 시작해, 9장의 그래프 신경망·Random Forest·K-Means 클러스터링에 이르기까지 아홉 개 장 내내 우리 곁에 있었다는 사실이, 이 책이 전하고 싶었던 가장 중요한 메시지를 함축한다: **대사모델링은 하나의 고정된 기법이 아니라, 화학량론이라는 단단한 뼈대 위에 점점 더 많은 데이터와 방법론을 쌓아 올리는 살아있는 과정**이라는 것이다.

AI+GEM 분야는 빠르게 변하므로 연도별 수치 예측보다 모델·데이터·solver 버전을 고정하고 독립 자료로 재검증하는 습관이 중요하다. 먼저 [Chapter 10의 완전 실행형 COBRApy 튜토리얼](../chapter-10/README.md)에서 FBA·pFBA·FVA·결손·MOMA·ROOM·작은 MILP·SBML 왕복을 같은 모델로 직접 검산한다. 그다음 [랜드마크 논문 가이드](../landmark-papers.md)에서 각 방법의 원 질문을 확인하고, 자신의 생물종·질병·공정에서 외부 검증이 가능한 작은 문제로 옮기는 것이 좋다.

## 핵심 용어 정리

| 용어(한글) | English | 정의 |
|:---|:---|:---|
| 지도학습 | Supervised Learning | 입력-정답 쌍으로부터 매핑 함수를 학습하는 ML 패러다임 |
| 손실함수 | Loss Function | 예측이 정답과 얼마나 다른지 재는 함수(교차 엔트로피, MSE 등) |
| 경사하강법 | Gradient Descent | 손실이 감소하는 방향으로 파라미터를 반복적으로 갱신하는 최적화 방법 |
| 학습률 | Learning Rate | 경사하강법에서 한 걸음의 보폭을 정하는 하이퍼파라미터 |
| 하이퍼파라미터 | Hyperparameter | 학습 전에 사람이 미리 정해야 하는 설정값(트리 깊이, 트리 개수 등) |
| 편향-분산 트레이드오프 | Bias-Variance Tradeoff | 모델이 너무 단순(과소적합)한 것과 너무 복잡(과적합)한 것 사이의 균형 문제 |
| 데이터 유출 | Data Leakage | 훈련·테스트 데이터가 부적절하게 섞여 성능이 부풀려지는 문제 |
| 보정(캘리브레이션) | Calibration | 모델이 출력한 확률이 실제 관측 빈도와 일치하는 정도 |
| 랜덤 포레스트 | Random Forest | 다수 결정 트리를 앙상블하는 분류/회귀 알고리즘 |
| 매튜 상관계수 | Matthews Correlation Coefficient(MCC) | 클래스 불균형에 강건한 이진 분류 성능 지표 |
| 그래프 신경망 | Graph Neural Network(GNN) | 메시지 패싱으로 그래프 구조 데이터를 처리하는 신경망 |
| 그래프 어텐션 네트워크 | Graph Attention Network(GAT) | 이웃별 주의력 가중치를 학습하는 GNN 변형 |
| 관찰자 편향 | Observer Bias | 예측 결과가 연구자가 선택한 목적함수에 의존하는 문제 |
| 초그래프 | Hypergraph | 하나의 엣지가 임의 수의 노드를 연결할 수 있는 그래프의 일반화 |
| 접속 행렬 | Incidence Matrix | 초그래프를 대사물(행)×반응(열)의 0/1 행렬로 표현한 것 |
| 시간차 오차 | Temporal-Difference(TD) Error | Q-Learning에서 "예상보다 실제 결과가 얼마나 좋았는가"를 재는 값 |
| Self-Attention | Self-Attention | 문장(또는 시퀀스) 내 각 토큰이 다른 모든 토큰을 참고하는 정도를 학습하는 메커니즘 |
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

## 답안

본문의 `잠깐, 생각해보기`와 위 「스스로 점검」의 풀이를 모았다. 질문을 먼저 스스로 풀어 본 뒤 대조한다.

### 잠깐, 생각해보기

**§2.1 학습률의 크기.** 학습률 $$\eta$$가 너무 크면 손실이 감소하는 방향은 맞더라도 한 걸음이 너무 커서 최솟값을 지나쳐 반대편으로 넘어가 버리고, 심하면 손실이 오히려 발산한다. 반대로 $$\eta$$가 너무 작으면 한 걸음이 너무 작아 수렴에 매우 오랜 시간이 걸린다. 실무에서는 $$\eta=0.01\sim0.1$$ 근처에서 시작해 학습 곡선을 보며 조정하는 경우가 많다.

**§3.2 MOMA-RF를 개선이라 부르는 근거.** 민감도와 MCC는 증가했지만 precision은 감소했다. 따라서 단일 숫자로 “우월”하다고 말하지 말고, 표적 누락과 거짓양성의 비용을 함께 보고 용도에 맞는 지표를 선택해야 한다.

**§3.5 표본 크기와 트리 깊이.** 일반적으로 데이터가 많을수록 분산이 줄어드는 경향이 있어(암기할 잡음 대비 진짜 패턴의 비율이 높아지므로) 더 복잡한 모델을 써도 과적합 위험이 상대적으로 낮아진다. 따라서 iML1515 쪽이 깊은 트리를 상대적으로 안전하게 쓸 수 있다. 반대로 `e_coli_core`처럼 표본이 작을 때는 `max_depth`를 낮게, `class_weight='balanced'`를 유지하고, 가능하면 §2.5의 K-Fold 교차검증으로 여러 분할의 평균 성능을 확인하는 것이 안전하다.

**§4.2 FlowGAT와 FluxGAT의 입력 차이.** FlowGAT의 질량 흐름 그래프는 한 wild-type FBA 해의 flux를 쓰지만, FluxGAT는 bounds와 $$\mathbf{S}\mathbf{v}=\mathbf{0}$$이 정한 feasible space에서 여러 flux를 샘플링한다. 이는 목적함수 선택 의존성을 줄이는 대안이지, 가능한 모든 해를 열거하거나 배지·bounds·sampling 수렴·학습 label의 편향을 없애는 방법은 아니다.

**§5.2 인공 갭 복원율의 해석 범위.** 훈련 모델의 큐레이션 편향, synthetic negative 생성법, 후보 reaction pool이 평가 난이도를 결정한다. 따라서 인공 갭 복원 성능을 자연계 미지 반응 발견 성능으로 옮겨 읽을 수 없으며, 내부 복원율과 독립 phenotype·유전자·생화학 검증을 분리해서 읽어야 한다.

**실습 단계 3 `max_depth` 실험.** §3.5의 표에서 예상한 대로, `max_depth=20`처럼 제한이 거의 없을 때 훈련 정확도는 100%에 가까워지지만 테스트 정확도는 오히려 낮아지는 과적합 패턴이 나타난다. 다만 `e_coli_core`는 표본이 95개뿐이라 분할 난수에 따라 흔들릴 수 있으므로, 한 번의 분할이 아니라 여러 분할의 평균으로 확인한다.

### 스스로 점검

**2번 — 혼동 행렬 지표 계산.** $$\text{Accuracy}=\frac{8+84}{100}=92\%$$, $$\text{Recall}=\frac{8}{10}=0.8$$, $$\text{Precision}=\frac{8}{14}\approx0.571$$, $$\text{MCC}=\frac{8\times84-6\times2}{\sqrt{14\times10\times90\times92}}\approx0.61$$이다. 두 전략 모두 Accuracy는 90% 안팎으로 비슷해 보이지만 "모두 비필수" 전략은 $$TP=0$$이므로 Recall도 0이 되어 아무 표적도 찾지 못한다. 따라서 이 문제에서는 MCC와 Recall이 목적에 맞는 지표다.

**6번 — 로지스틱 회귀 한 걸음.** $$z=1.0\times1.5+0=1.5$$, $$\hat y=\sigma(1.5)\approx0.818$$, 오차 $$=\hat y-y=0.818$$, 그래디언트 $$=0.818\times1.5=1.227$$, $$w\leftarrow1.0-0.2\times1.227\approx0.755$$이다. 정답이 0인데 모델이 0.818로 자신 있게 틀렸으므로 $$w$$가 감소하는 방향(그래디언트의 반대 방향)으로 크게 조정된다.

**7번 — 이웃이 늘어난 GNN 갱신값.** 새 이웃 평균은 $$\frac{h_{R1}^{(0)}+h_{R2}^{(0)}+h_{R4}^{(0)}}{3}=\frac{1.0+2.0+0.6}{3}=1.2$$이므로 $$h_{R3}^{(1)}=\text{ReLU}(3.0+1.2)=4.2$$다. 원래(이웃 R1, R2만) 4.5였던 값이 4.2로 낮아진다 — 이웃이 늘어나면 평균이 새 이웃의 값 쪽으로 끌려가기 때문이다.

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
16. Tazza G, Moro F, Ruggeri D, Teusink B, Vidács L (2025). ["MINN: A metabolic-informed neural network for integrating omics data into genome-scale metabolic modeling."](https://doi.org/10.1016/j.csbj.2025.08.004) *Computational and Structural Biotechnology Journal* 27:3609–3617.
17. Nair NK, D'Souza A (2026). ["An Integrative Genome-Scale Metabolic Modeling and Machine Learning Framework for Predicting and Optimizing Single-Cell Protein Production in *Saccharomyces cerevisiae*."](https://doi.org/10.48550/arXiv.2603.25561) arXiv:2603.25561 (사전출판물). — §10.2의 GAN flux 생성 0/100 결과.
18. COBRApy: https://github.com/opencobra/cobrapy · DepMap: https://depmap.org/portal/ · MEMOTE: https://github.com/opencobra/memote
19. GECKO 3.0: https://github.com/SysBioChalmers/GECKO · ECMpy 2.0: https://github.com/synbio-eecmp/ECMpy
20. Palsson, B.O. (2015). *Systems Biology: Constraint-based Reconstruction and Analysis*, 2nd ed. Cambridge University Press.
21. Lewis, N.E. et al. (2012). "Constraining the metabolic genotype-phenotype relationship using a phylogeny of in silico methods." *Nature Reviews Microbiology*, 10(4), 291-305.

> 본 장의 원 강의자료(9주차, `gem9_w09/week9_ebook.md`)는 2025년 7월 작성되었으며, 인용된 연구는 2023-2026년 사이 발표분을 중심으로 한다. AI+GEM 분야는 빠르게 발전하므로 최신 문헌을 지속적으로 추적할 것을 권장한다.
