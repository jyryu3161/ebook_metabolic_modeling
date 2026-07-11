# 핵심 용어집 (Glossary)

대사모델링에서 반복적으로 등장하는 핵심 용어를 정리했습니다. 각 용어는 처음 상세히 정의되는 **관련 챕터**로 연결됩니다.

## A–F

| 용어 | 영문 | 정의 | 관련 챕터 |
|------|------|------|-----------|
| 적응 진화 | Adaptive Laboratory Evolution (ALE) | 선택압 아래 미생물을 여러 세대 배양해 성장·생산 표현형을 진화시키는 실험법 | [Ch8](chapter-8/README.md) |
| ATP 유지 에너지 | ATP maintenance; GAM/NGAM | GAM은 바이오매스 반응의 ATP 계수로 성장 비례 비용을, NGAM은 보통 ATPM 반응의 최소 flux(lower bound)로 성장 비의존 비용을 반영한다. 따라서 ATPM 자체를 GAM과 NGAM의 합으로 해석하지 않는다 | [Ch3](chapter-3/README.md) |
| 바이오매스 목적함수 | Biomass objective function | 세포 성장에 필요한 전구체·에너지 소비를 하나의 가상 반응으로 묶어 최적화 목표로 삼는 반응 | [Ch3](chapter-3/README.md) |
| 차단 반응 | Blocked reaction | 주어진 네트워크·bounds에서 어떤 정상상태 해에서도 0이 아닌 flux를 가질 수 없는 반응 | [Ch5](chapter-5/README.md) |
| 경계 반응 | Boundary reaction | 모델과 외부 경계를 잇는 exchange·demand·sink 반응의 총칭 | [Ch3](chapter-3/README.md) |
| 제약 기반 모델링 | Constraint-Based Modeling (CBM) | 효소 동역학 파라미터 없이 화학량론·열역학·용량 제약만으로 가능한 플럭스 공간을 정의하는 접근 | [Ch1](chapter-1/README.md) |
| 연속 배양 | Chemostat | 배지 유입과 배양액 유출을 같은 속도로 유지해 정상상태 성장률을 희석률로 제어하는 배양법 | [Ch1](chapter-1/README.md), [Ch8](chapter-8/README.md) |
| 맥락 특이 모델 | Context-specific model | 특정 조직·조건의 오믹스 증거를 반영한 모델; 반응을 제거해 추출할 수도 있고, 범용 네트워크를 유지한 채 bounds·가중치로 활성을 제한할 수도 있다 | [Ch6](chapter-6/README.md) |
| 구획 | Compartment | 세포질·미토콘드리아 등 반응이 일어나는 세포 내 공간 구분 | [Ch3](chapter-3/README.md) |
| 막다른 대사물 | Dead-end metabolite | 네트워크에서 생성만 되거나 소비만 되어 정상상태 질량수지를 만족할 수 없는 대사물. 흔히 누락 반응(gap)의 신호이며 관련 반응을 차단 반응(blocked reaction)으로 만든다 | [Ch2](chapter-2/README.md), [Ch5](chapter-5/README.md) |
| 요구 반응 | Demand reaction | 내부 대사산물을 비가역적으로 제거해 생산 가능 flux를 시험하는 경계 반응; 축적량 자체는 아님 | [Ch3](chapter-3/README.md) |
| 차등 발현 유전자 | Differentially Expressed Gene (DEG) | 조건 간 count 분포를 통계적으로 비교해 효과 크기와 보정 p-value 기준을 만족한 유전자 | [통계 보충](supplements/omics-statistics.md) |
| 동적 FBA | Dynamic FBA (dFBA) | 짧은 시간 구간마다 FBA를 풀고 외부 농도·생체량을 적분해 갱신하는 준동역학 접근 | [Ch4](chapter-4/README.md) |
| 효소 제약 모델 | Enzyme-constrained model (ecModel) | 효소량·$$k_{cat}$$·단백질 예산으로 반응 flux 용량을 제한한 GEM 확장 | [Ch6](chapter-6/README.md) |
| 교환 반응 | Exchange reaction | 모델 경계에서 대사물이 드나드는 가상 반응(영양분 흡수·부산물 분비) | [Ch3](chapter-3/README.md) |
| 유전자 필수성 | Gene essentiality | GPR 규칙을 평가한 유전자 결손 뒤, 정의한 배지·목적함수·생존 임계값에서 요구 기능을 유지하지 못하는 성질 | [Ch7](chapter-7/README.md), [Ch8](chapter-8/README.md) |
| 반응 필수성 | Reaction essentiality | 반응의 플럭스 경계를 직접 0으로 둔 뒤, 정의한 조건에서 요구 기능을 유지하지 못하는 성질. 유전자 필수성과 동의어가 아니다 | [Ch8](chapter-8/README.md), [Ch9](chapter-9/README.md) |
| 거짓발견률 | False Discovery Rate (FDR) | 유의하다고 선택한 항목 중 거짓 양성의 기대 비율; 보통 BH 절차로 제어 | [통계 보충](supplements/omics-statistics.md) |
| Flux Balance Analysis | FBA | 정상상태·제약 하에서 목적함수를 최대화하는 플럭스 분포를 선형계획법으로 구하는 방법 | [Ch4](chapter-4/README.md) |
| 플럭스(대사 통량) | Flux | 단위 생체량·시간당 반응 진행률; 농도와 다르며 보통 `mmol gDW⁻¹ h⁻¹`로 표현 | [Ch1](chapter-1/README.md), [Ch2](chapter-2/README.md) |
| 플럭스 원추 | Flux cone | $$Sv=0$$ 과 비가역성 제약이 정의하는 볼록 원추 형태의 해 공간 | [Ch4](chapter-4/README.md) |
| FSEOF | Flux Scanning based on Enforced Objective Flux | 산물 flux를 단계적으로 강제할 때 함께 증가하는 반응을 찾아 유전자 증폭 후보를 고르는 방법; 감소 flux를 억제·결손 후보로 해석하는 것은 후속 확장이다 | [Ch8](chapter-8/README.md) |
| Flux Variability Analysis | FVA | 목적값을 지정 비율 이상 유지하며 각 반응을 별도로 최소·최대화해 허용 범위를 계산하는 방법 | [Ch4](chapter-4/README.md) |

## G–O

| 용어 | 영문 | 정의 | 관련 챕터 |
|------|------|------|-----------|
| Gap-filling | Gap-filling | 초안 모델의 대사 경로 단절을 메우기 위해 반응을 추가하는 과정 | [Ch5](chapter-5/README.md) |
| 근본·하위 간극 | Root / downstream gap | root gap은 특정 대사물의 생성 또는 소비 반응이 아예 없어 생기는 간극이고, downstream gap은 상류 root gap 때문에 파생되어 root를 채우면 함께 해소되는 간극이다 | [Ch5](chapter-5/README.md) |
| 유전자-단백질-반응 | Gene-Protein-Reaction (GPR) | 유전자→효소→반응의 논리(AND/OR) 관계 규칙 | [Ch3](chapter-3/README.md) |
| 게놈 규모 대사 모델 | Genome-scale Metabolic Model (GEM) | 한 생물의 게놈에서 도출한 전체 대사 반응 네트워크 모델 | [Ch1](chapter-1/README.md) |
| GeTPRA | Gene–Transcript–Protein–Reaction Association | 유전자에서 transcript isoform과 단백질을 거쳐 반응으로 연결한 확장 관계 | [Ch5](chapter-5/README.md) |
| GIMME | Gene Inactivity Moderated by Metabolism and Expression | 요구 기능을 유지하면서 저발현 반응 flux의 가중 불일치를 최소화하는 방법 | [Ch6](chapter-6/README.md) |
| iMAT | Integrative Metabolic Analysis Tool | 고발현 반응 활성과 저발현 반응 비활성의 일치 개수를 MILP로 최대화하는 방법 | [Ch6](chapter-6/README.md) |
| INIT / tINIT / ftINIT | — | 오믹스 증거로 active network를 추출하는 INIT 계열; tINIT은 task 보장을 강화하고 ftINIT은 계산을 가속 | [Ch5](chapter-5/README.md), [Ch6](chapter-6/README.md) |
| 동역학 모델 | Kinetic model | 각 반응의 속도식·파라미터로 농도 시간변화를 기술하는 모델 | [Ch1](chapter-1/README.md) |
| 선형 계획법 | Linear Programming (LP) | 선형 목적함수를 선형 제약 하에서 최적화하는 수학적 방법 | [Ch4](chapter-4/README.md) |
| 질량·전하 균형 | Mass/charge balance | 개별 반응의 양변에서 원소 수와 총전하가 보존되는 화학적 성질 | [Ch5](chapter-5/README.md) |
| MEMOTE | Metabolic Model Tests | 형식·주석·화학량론·biomass 등을 자동 회귀 테스트하는 GEM 품질관리 도구 | [Ch5](chapter-5/README.md) |
| 대사 과제 | Metabolic task | 요소 생성, 특정 전구체 합성처럼 모델이 수행해야 하는 생리 기능을 입출력과 조건으로 정의한 시험 | [Ch5](chapter-5/README.md) |
| 혼합정수선형계획법 | Mixed-Integer Linear Programming (MILP) | 연속 flux와 0/1 변수를 함께 포함하는 최적화; ROOM·tINIT·OptKnock 등에 사용 | [유전자 교란 보충](supplements/perturbation-analysis.md) |
| MOMA | Minimization of Metabolic Adjustment | 교란 후 mutant feasible space에서 기준 flux와의 제곱 유클리드 거리를 최소화하는 원래의 QP 방법 | [유전자 교란 보충](supplements/perturbation-analysis.md), [Ch8](chapter-8/README.md) |
| Monod 식 | Monod equation | 기질 농도에 따른 미생물 비성장속도의 포화 관계 $$\mu=\mu_{max}S/(K_S+S)$$ | 준비 A |
| MTA | Metabolic Transformation Algorithm | 질병 상태를 정상 상태로 되돌리는 반응 표적을 탐색하는 알고리즘 | [Ch7](chapter-7/README.md) |
| 영공간 | Null space | $$S\mathbf v=0$$을 만족하는 벡터의 집합; 정상상태 플럭스 자유도의 선형대수적 기반 | [Ch2](chapter-2/README.md), [Ch4](chapter-4/README.md) |
| 온코대사물 | Oncometabolite | 2-HG 등 암 대사 이상으로 축적되어 발암을 촉진하는 대사물 | [Ch7](chapter-7/README.md) |
| OptKnock | OptKnock | 안쪽의 세포 성장 최적화와 바깥쪽의 목적물 생산 최적화를 결합한 이중수준 문제로, 생산과 성장을 결합하는 결손 조합을 찾는 방법 | [Ch8](chapter-8/README.md) |
| 고아 반응 | Orphan reaction | 생화학적으로 성립하지만 촉매 유전자가 밝혀지지 않아 GPR이 비어 있는 실제 반응. 비효소적 자발 반응(관례상 s0001 배정)이나 누락 반응(gap)과 구분한다 | [Ch5](chapter-5/README.md) |
| OptForce | OptForce | 야생형과 목표 생산 상태의 flux 범위를 비교해 반드시 변해야 하는 반응(MUST set)을 찾고, 이를 강제할 조작 조합(FORCE set)을 설계하는 방법 | [Ch8](chapter-8/README.md) |

## P–Z

| 용어 | 영문 | 정의 | 관련 챕터 |
|------|------|------|-----------|
| 대안 최적해 | Alternate optima | 같은 최적 목적값을 내지만 내부 flux 분포가 다른 여러 해 | [Ch4](chapter-4/README.md) |
| pFBA | parsimonious FBA | 주 목적 최적값을 유지한 채 $$\sum_j|v_j|$$를 최소화하는 사전식 2단계 최적화 | [Ch4](chapter-4/README.md), [논문 가이드](landmark-papers.md) |
| 표현형 위상 평면 | Phenotype Phase Plane (PhPP) | 두 교환 플럭스에 따른 최적 성장의 지형을 시각화한 분석 | [Ch8](chapter-8/README.md) |
| 생산 포락선 | Production envelope | 성장률 대비 목적물 생산의 가능 영역을 나타낸 곡선 | [Ch8](chapter-8/README.md) |
| 이차계획법 | Quadratic Programming (QP) | 목적함수에 제곱항을 포함하는 최적화; 원래 MOMA에는 QP solver가 필요 | [유전자 교란 보충](supplements/perturbation-analysis.md) |
| 행렬 계수 | Matrix rank | 화학량론 행렬의 선형 독립 행/열 수; 단순히 대사물 수와 같지 않음 | [Ch2](chapter-2/README.md), [Ch4](chapter-4/README.md) |
| 반응 활성 점수 | Reaction Activity Score (RAS) | GPR의 AND/OR 논리를 이용해 유전자 발현을 반응 수준 증거로 집약한 점수 | [Ch6](chapter-6/README.md) |
| Recon / Human-GEM | — | 대표적 인체 게놈 규모 대사 모델 계열 | [Ch5](chapter-5/README.md) |
| 재구축과 모델 | Reconstruction / model | 증거 기반 대사 지식베이스가 reconstruction이고, 여기에 bounds·objective를 붙인 계산 인스턴스가 model | [Ch5](chapter-5/README.md) |
| ROOM | Regulatory On/Off Minimization | 교란 전 기준 flux가 정한 허용 구간을 벗어나는 큰 flux 변화의 개수를 최소화해 교란 뒤 상태를 예측하는 방법; 특정 시간척도를 자동 지정하지 않는다 | [유전자 교란 보충](supplements/perturbation-analysis.md), [Ch8](chapter-8/README.md) |
| SBML FBC | Systems Biology Markup Language, Flux Balance Constraints | GEM의 반응·GPR·bounds·objective를 교환하는 표준 XML package | [SBML 보충](supplements/sbml-practical.md) |
| 그림자 가격 | Shadow price | 제약식 우변(RHS)을 미소하게 바꿀 때 최적 목적값이 변하는 한계율인 쌍대값; 부호는 목적함수 방향, 제약식 표기와 solver convention에 따라 달라진다 | [Ch4](chapter-4/README.md) |
| 싱크 반응 | Sink reaction | 내부 대사산물을 가역적으로 공급·제거하는 경계 반응; 근거 없는 사용은 gap을 숨길 수 있음 | [Ch3](chapter-3/README.md) |
| 화학량론적 일관성 | Stoichiometric consistency | 내부 대사산물에 양의 질량을 부여해 모든 내부 반응이 보존되도록 할 수 있는 네트워크 성질 | [Ch5](chapter-5/README.md) |
| 화학량론 행렬 | Stoichiometric matrix (S) | 반응별 대사물 계수를 담아 네트워크를 표현하는 (대사물×반응) 행렬 | [Ch2](chapter-2/README.md) |
| 화학량론적 균형 순환 | Stoichiometrically balanced cycle (SBC); Type III pathway | 모든 교환 반응을 닫은 닫힌계에서도 flux를 나르는 내부 반응 순환. 열역학·조절 제약 부족으로 생긴 재구축 인공산물로, 외부 공급 없이 ATP·redox를 재생할 수 있다. 에너지를 소비하는 futile cycle과 구별한다 | [Ch4](chapter-4/README.md), [Ch5](chapter-5/README.md) |
| 의사-정상상태 | Pseudo-steady state | intracellular pool의 시간 변화가 관찰 시간척도에서 작다고 두어 $$S\mathbf v=0$$을 적용하는 가정 | [Ch2](chapter-2/README.md) |
| 합성생물학 | Synthetic biology | 표준화된 생물학적 부품과 설계–제작–시험–학습 주기로 원하는 기능을 구현하는 공학 분야 | [Ch8](chapter-8/README.md) |
| 합성 치사 | Synthetic lethality | 단독으로는 무해하나 함께 제거하면 치사가 되는 유전자 쌍 | [Ch7](chapter-7/README.md) |
| TPM | Transcripts Per Million | 유전자 길이로 보정한 상대 발현 비율; 표본 내 조성값이므로 절대 분자 수나 직접 flux가 아님 | [통계 보충](supplements/omics-statistics.md), [Ch6](chapter-6/README.md) |
| 열역학 기반 flux 분석 | Thermodynamics-based Flux Analysis (TFA) | 농도 범위와 반응 Gibbs 에너지로 방향성을 추가 제약하는 방법 | [Ch6](chapter-6/README.md) |
| 수송 반응 | Transport reaction | 구획 간 대사물 이동을 표현하는 반응 | [Ch3](chapter-3/README.md) |
| Warburg 효과 | Warburg effect | 산소가 있어도 해당과정에 의존하는 암세포의 호기성 글리콜라이시스 | [Ch7](chapter-7/README.md) |

---

> 이 용어집은 각 챕터의 "핵심 용어 정리"를 통합한 것입니다. 더 자세한 정의와 맥락은 관련 챕터를 참고하세요.
