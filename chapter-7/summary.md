# 마무리: 요약과 점검

## 한 장 요약

### 질병 대사의 모델 표현

- 대사 재프로그래밍은 같은 반응 네트워크의 flux·bounds 변화로도 나타날 수 있으며 반드시 topology 변화가 아니다.
- 발현 증가를 반응 상한 증가로, 이형접합 변이를 50% 용량으로 자동 변환하지 않는다. 사용한 통합 규칙과 민감도 범위를 명시한다.
- 목적함수는 생물학적 사실이 아니라 분석 가정이다. 정상 세포=ATP 최대화, 암세포=biomass 최대화라는 이분법은 성립하지 않는다.
- 정상상태 GEM은 온코대사물의 생산·소비·분비 flux를 분석할 수 있지만 세포 내 농도 축적과 시간 변화를 직접 예측하지 않는다.

### Warburg 효과와 AFR

Warburg 효과는 산소가 이용 가능한 조건에서도 높은 포도당 이용과 젖산 생성이 유지되는 현상이다. 이는 OXPHOS의 완전 상실 또는 모든 암의 공통 강도를 뜻하지 않는다.

원 Yizhak et al. 연구의 AFR은 허용 플럭스 분포를 표본화하여 해당·OXPHOS ATP 생성 flux의 평균을 비교한 지표이다.

$$
\mathrm{AFR}
=
\frac{\operatorname{mean}_s A_{\mathrm{gly}}^{(s)}}
{\operatorname{mean}_s A_{\mathrm{OXPHOS}}^{(s)}}.
$$

단일 FBA 최적해의 `PGK+PYK`를 ATP synthase flux로 나눈 값은 원 정의와 동일하지 않으며, AFR 1을 보편적 암 판정 경계로 사용할 수 없다.

### 맥락 특이적 모델과 필수성

암-정상 모델 비교에서는 같은 기저 reconstruction, 배지, biomass, 유지 에너지, 추출법과 solver tolerance를 맞춘다. 상대 결손 성장은

$$
r_g=\frac{\mu_{-g}}{\mu_0},
\qquad e_g=1-r_g
$$

로 계산한다. 암-정상 효과 차이 $$\Delta_g=e_g^C-e_g^N$$은 계산적 선택성 요약이지 임상 안전성 점수가 아니다. 여러 정상 조직, 대사 작업, 완전 KO와 부분 약물 억제의 차이를 평가한다.

결손 LP가 `infeasible`인 경우와 feasible하지만 최적 성장률이 0인 경우를 구분하여 저장한다. 필수성 screen에서 둘을 모두 치사로 분류할 수 있지만 그 정책을 명시하고 solver 상태를 원자료에서 지우지 않는다.

DepMap 비교에서는 release와 CERES·Chronos 점수 종류, gene/cell-line mapping, 라벨 정의와 점수 방향을 기록한다. PR-AUC의 무작위 기준선은 양성 비율이며 ROC-AUC 0.5와 다르다. 모델 조정에 사용한 자료를 최종 평가에 재사용하지 않는다.

### 합성 치사와 gMCS

두 단일 결손은 생존하고 이중 결손만 치명적인지를 사전 정의한 임계값에서 판정한다.

$$
r_a>\tau_s,\qquad r_b>\tau_s,\qquad r_{ab}\leq\tau_d.
$$

Bliss 생존 편차

$$
\delta_{ab}=r_{ab}-r_ar_b
$$

는 독립 기대치에서 벗어난 정도이다. 이는 합성 치사의 표현형 정의나 통계적 유의성과 동일하지 않다. gMCS는 지정한 대사 작업을 막는 포함관계상 최소 유전자 집합이며, 최소 독성·최소 용량 또는 유일한 표적 조합을 뜻하지 않는다.

### MTA와 rMTA

MTA는 source 전사체로 추정한 기준 flux $$\mathbf v^{\mathrm{ref}}$$와 source-target 차등발현에서 유도한 $$R_S,R_F,R_B$$를 사용한다. 후보별 MIQP proxy는 $$R_S$$ 변화를 줄이고 $$R_F,R_B$$의 목표 방향 변화를 늘린다. 최종 순위는 MIQP 목적값이 아니라 사후 TS이다.

$$
\mathrm{TS}=
\frac{
\sum_{i\in R_{\mathrm{success}}}|\Delta v_i|
-\sum_{i\in R_{\mathrm{unsuccess}}}|\Delta v_i|
}{
\sum_{i\in R_S}|\Delta v_i|
}.
$$

$$R_{\mathrm{success}}$$는 단순한 flux 차이 부호만으로 정하지 않는다. 원 MTA는 기준 flux가 0인 가역 반응과 기준 부호를 넘어서는 반응에 별도 판정을 적용한다. 분모가 0에 가까우면 TS가 불안정하며 alternative optimum과 flux scaling을 검사한다. rMTA는 best-case에 worst-case와 MOMA 기반 분석을 추가하지만 발현-flux 불일치, 기준 flux 비유일성과 약물 독성을 제거하지 않는다.

## 핵심 구분

| 혼동하기 쉬운 항목 | 구분 |
|:---|:---|
| Warburg 효과와 미토콘드리아 상실 | 호기성 해당이 높아도 TCA·OXPHOS가 유지될 수 있다. |
| 반응 추가와 flux 활성 | 신규 반응에 기질·소비·경계와 목적상 이점 또는 최소 flux 제약이 필요하다. |
| 유전자 필수성과 좋은 약물 표적 | 정상 조직 선택성, 부분 억제, 표적 외 효과와 노출이 추가로 필요하다. |
| Bliss 편차와 합성 치사 | 하나는 독립 기대치 편차, 다른 하나는 단일·이중 결손 표현형 정의이다. |
| Context-specific model과 MTA | 모델 추출법과 표적 상태 변환 순위화법은 서로 다른 단계이다. |
| MTA proxy와 TS | MIQP objective는 해를 찾는 proxy이고 TS는 그 해의 사후 순위 점수이다. |
| 계산 검증과 치료 검증 | 외부 데이터, 세포, 동물과 임상 근거는 단계별로 구분한다. |

*Table S.1. Chapter 7의 주요 개념 구분.*

## 스스로 점검

1. 같은 네트워크 topology에서 대사 재프로그래밍을 표현할 수 있는 bounds·환경 변화를 세 가지 제시하시오.
2. Warburg 효과가 OXPHOS 상실을 뜻하지 않는 이유와 이를 검증할 측정량을 설명하시오.
3. Flux sample이 주어졌을 때 AFR을 계산하고, 단일 최적해 기반 비와 다른 이유를 쓰시오.
4. `IDH1` hotspot 변이를 모델에 반영할 때 신규 반응, redox cofactor, 수송·exchange와 측정 제약을 설계하시오.
5. 암 모델과 정상 모델의 유전자 결손 효과를 공정하게 비교하기 위한 공통 조건을 작성하시오.
6. 대사 작업 비율과 biomass 성장 비율이 서로 다른 정보를 제공하는 사례를 구성하시오.
7. $$r_a=0.9$$, $$r_b=0.8$$, $$r_{ab}=0.1$$일 때 Bliss 편차를 계산하고, 사전 임계값 없이 SL을 확정할 수 없는 이유를 설명하시오.
8. 크기 2 gMCS가 항상 합성 치사 쌍이 되기 위해 필요한 단일 결손 조건을 쓰시오.
9. DepMap 점수로 모델을 조정하고 같은 cell line에서 성능을 보고할 때 발생하는 데이터 누출을 설명하시오.
10. MTA의 MIQP proxy와 TS의 역할을 구분하고 TS 분모가 0일 때의 처리 규칙을 제안하시오.
11. PRIME, tINIT 기반 HCC 분석과 MTA가 사용하는 입력·목적·출력을 비교하시오.
12. 계산 후보가 세포 실험에서 재현되지 않았을 때 구분할 모델·실험 원인을 제시하시오.

## 핵심 용어

| 용어 | 정의 |
|:---|:---|
| Metabolic reprogramming | 유전·환경·세포 상태에 따른 기질 이용과 대사 flux의 재편 |
| [Warburg effect](../glossary.md) | 산소 이용 가능 조건에서도 높은 해당·젖산 생성이 유지되는 현상 |
| AFR | 표본화한 해당 ATP 생성과 OXPHOS ATP 생성 평균의 비 |
| [Oncometabolite](../glossary.md) | 비정상적 생성·축적이 종양 관련 조절에 관여하는 대사물 |
| [Context-specific GEM](../glossary.md) | 특정 조직·세포·조건의 자료와 기능 요구를 반영해 제한한 GEM |
| Conditional essentiality | 지정 모델·배지·목적에서 결손이 기능을 잃게 하는 성질 |
| [Synthetic lethality](../glossary.md) | 각 단일 교란은 허용되지만 결합 교란은 치명적인 상호작용 |
| Bliss independence | 두 단일 생존율의 곱을 독립 이중 효과로 사용하는 기준선 |
| gMCS | 지정 대사 작업을 막는 포함관계상 최소 유전자 집합 |
| [MTA](../glossary.md) | Source 기준 flux와 source-target 발현 방향으로 교란을 순위화하는 방법 |
| TS | MTA 해에서 목표 변화와 비목표 변화를 비교하는 사후 비율 |
| rMTA | Best/worst/MOMA 기반 분석을 결합한 MTA 확장 |

*Table S.2. Chapter 7의 핵심 용어.*

이 장에서 언급한 [FBA](../chapter-4/README.md), [MOMA·ROOM](../chapter-8/README.md) 등 섭동 예측 방법의 원 논문이 실제로 무엇을 결론 내렸는지, 그리고 흔한 오독은 무엇인지는 [대표 논문 가이드](../landmark-papers.md)에 정리되어 있다.

## 다음 장

[Chapter 8](../chapter-8/README.md)에서는 유전자 교란을 생산 균주 설계와 microbial community 분석에 확장한다. 질병 표적과 산업 균주 설계는 같은 화학량론·GPR 도구를 사용하지만 목적함수, 선택성 기준과 검증 endpoint가 다르다.

## 참고문헌

1. [Vander Heiden MG, Cantley LC, Thompson CB. Understanding the Warburg effect. *Science*. 2009.](https://doi.org/10.1126/science.1160809)
2. [Yizhak K et al. A computational study of the Warburg effect identifies metabolic targets inhibiting cancer migration. *Molecular Systems Biology*. 2014.](https://doi.org/10.15252/msb.20134993)
3. [Dang L et al. Cancer-associated IDH1 mutations produce 2-hydroxyglutarate. *Nature*. 2009.](https://doi.org/10.1038/nature08617)
4. [Folger O et al. Predicting selective drug targets in cancer through metabolic networks. *Molecular Systems Biology*. 2011.](https://doi.org/10.1038/msb.2011.35)
5. [Agren R et al. Identification of anticancer drugs for hepatocellular carcinoma through personalized genome-scale metabolic modeling. *Molecular Systems Biology*. 2014.](https://doi.org/10.1002/msb.145122)
6. [Meyers RM et al. Computational correction of copy-number effect improves specificity of CRISPR-Cas9 essentiality screens in cancer cells. *Nature Genetics*. 2017.](https://doi.org/10.1038/ng.3984)
7. [Farmer H et al. Targeting the DNA repair defect in BRCA mutant cells as a therapeutic strategy. *Nature*. 2005.](https://doi.org/10.1038/nature03445)
8. [Muller FL et al. Passenger deletions generate therapeutic vulnerabilities in cancer. *Nature*. 2012.](https://doi.org/10.1038/nature11331)
9. [Apaolaza I et al. An in-silico approach to predict and exploit synthetic lethality in cancer metabolism. *Nature Communications*. 2017.](https://doi.org/10.1038/s41467-017-00555-y)
10. [Yizhak K et al. Model-based identification of drug targets that revert disrupted metabolism and its application to ageing. *Nature Communications*. 2013.](https://doi.org/10.1038/ncomms3632)
11. [Valcárcel LV et al. rMTA: robust metabolic transformation analysis. *Bioinformatics*. 2019.](https://doi.org/10.1093/bioinformatics/btz231)
