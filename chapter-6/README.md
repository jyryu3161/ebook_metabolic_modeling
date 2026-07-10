# Chapter 6. 오믹스 데이터와 맥락 특이적 대사 모델

범용 게놈 규모 대사 모델(Genome-Scale Metabolic Model, GEM)은 한 생물 또는 여러 인체 조직에서 알려진 대사 능력의 합집합을 나타냅니다. 특정 세포가 어느 반응에 실제로 flux를 갖는지는 전사체만으로 직접 관찰되지 않으며, 화학량론·배지·조절·효소량과 목적 가설에도 의존합니다. **맥락 특이적 모델(context-specific model)**은 오믹스 증거와 기능 제약을 이용해 범용 GEM의 실행가능 공간을 줄이거나 서브네트워크를 추출한 계산 모델입니다. 따라서 실제 활성 네트워크의 직접 측정값이 아니라 검증해야 하는 가설입니다.

이 장은 유전자 수준의 전사체·단백질체·대사체 증거를 반응 수준의 점수와 제약으로 변환하는 절차를 다룹니다. GIMME, iMAT, E-Flux, tINIT와 FASTCORE 계열의 목적함수와 가정을 비교하고, RNA-seq 정규화와 `e_coli_core` 실습을 통해 결과가 임계값과 경계조건에 얼마나 의존하는지 검토합니다. 모델 재구축과 품질관리는 [Chapter 5](../chapter-5/README.md), FBA/FVA는 [Chapter 4](../chapter-4/README.md), 질병 모델의 표적 예측은 [Chapter 7](../chapter-7/README.md)에서 다룹니다.

{% hint style="info" %}
count 분포, 정규화, t-test, 다중검정과 FDR이 낯설다면 [오믹스 데이터 분석과 기초 통계](../supplements/omics-statistics.md)를 먼저 읽으십시오. 통계적 유의성과 생물학적 효과 크기를 구분한 뒤 모델 통합으로 넘어갑니다.
{% endhint %}

## 분석 범위

1. 범용 GEM과 맥락 특이적 모델의 차이 및 검증 대상
2. GPR의 부울 구조와 연속 반응 점수로의 휴리스틱 변환
3. 발현 이산화, zFPKM과 임계값 민감도
4. GIMME·iMAT·E-Flux·tINIT·FASTCORE의 최적화 정식화
5. RNA-seq 전처리와 generic/context 모델의 동일 조건 유전자 결손 비교
6. 효소·열역학 제약과 다중 오믹스 통합의 한계

---
## 대화형 도해: 핵심 가정과 결과 해석

{% hint style="info" %}
아래 도해는 **교육용 개념·모의 데이터**를 조작하여 이 장의 핵심 가정과 해석 범위를 확인하는 보조 자료이다. 실제 GEM 결과로 인용할 수 없으며, 실제 계산은 모델 버전·배지·목적함수·solver·허용오차를 고정한 실습 코드로 재현해야 한다.
{% endhint %}

{% embed url="https://cdn.jsdelivr.net/gh/jyryu3161/ebook_metabolic_modeling@main/interactive/index.html?chapter=6" %}

[새 창에서 대화형 도해 열기](https://cdn.jsdelivr.net/gh/jyryu3161/ebook_metabolic_modeling@main/interactive/index.html?chapter=6)

## 학습 목표

이 장을 마치면 다음을 할 수 있습니다.

1. 범용 GEM과 맥락 특이적 모델의 차이를 정의하고, 발현 증거가 flux의 직접 측정값이 아닌 이유를 설명할 수 있다.
2. **GPR(Gene-Protein-Reaction)**의 부울 AND/OR와 연속 발현값에 적용하는 min/max 휴리스틱을 구분하고 **반응 활성 점수(Reaction Activity Score, RAS)**를 계산할 수 있다.
3. 발현 **임계값(threshold)** 전략을 비교하고, 일반 z-score와 half-Gaussian 적합에 기반한 zFPKM을 구분할 수 있다.
4. **GIMME, iMAT, E-Flux, tINIT**의 수학적 정형화(목적함수·제약·최적화 유형)를 비교하고, 상황에 맞는 방법을 선택할 수 있다.
5. Raw counts로부터 **TPM**을 계산하고, `e_coli_core`에 발현 기반 제약을 적용한 뒤 generic/context 모델의 유전자 결손 결과를 같은 기준으로 비교할 수 있다.
6. 단백질체 통합(**GECKO 효소 제약**)과 대사체 통합(열역학·검출 기반 제약)의 단위와 가정을 설명할 수 있다.
7. 다중 오믹스 통합의 오차원과 독립 검증 요건을 비판적으로 평가할 수 있다.

---
