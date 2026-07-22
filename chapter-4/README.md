# Chapter 4. Flux Balance Analysis (FBA)

> [Chapter 2](../chapter-2/README.md)~[Chapter 3](../chapter-3/README.md)에서 만든 모델([화학량론 행렬](../glossary.md) $$\mathbf{S}$$, 플럭스 범위, 바이오매스 목적함수)에는 사실 무한히 많은 플럭스 해가 존재한다. 이 장에서는 그중 목적 함수를 최적화하는 해를 [선형 계획법](../glossary.md)(Linear Programming, LP)으로 찾는 방법 — **[Flux Balance Analysis(FBA, 플럭스 균형 분석)](../landmark-papers.md)** — 을 손 계산과 코드로 직접 익힌다. 최적 목적값은 하나여도 그 값을 만드는 플럭스 분포는 여러 개일 수 있다.

---

## 표기와 읽기 원칙

이 책은 한국어 용어를 먼저 쓰고, 처음 등장할 때 영어 원어와 약어를 함께 표기한다. 이후에는 같은 장 안에서 한 표기를 일관되게 사용한다.

- **플럭스**(flux; 대사 통량)는 단위 시간당 반응이 진행되는 정도, **반응**(reaction)은 화학량론에 따른 대사물의 변환, **대사물**(metabolite)은 반응에 참여하는 물질(포도당·피루브산 등, 구획이 다르면 다른 화학종으로 센다)을 뜻한다.
- **경계조건**(bounds), **목적함수**(objective function), **솔버**(solver)는 생물학적 사실이 아니라 우리가 모델에 부여한 계산 조건이다.
- 조건·가정·절차는 번호 목록으로, 결과의 범위와 예외는 `해석상의 주의` 상자로 구분한다.

{% hint style="warning" %}
본문의 “예측”은 명시된 모델·배지·경계조건·목적함수 아래의 계산 결과다. 실험 관찰이나 인과적 효과와 혼용하지 않는다.
{% endhint %}

## 이 장을 시작하며

**질문 하나에서 출발한다.** [Chapter 2](../chapter-2/README.md)에서 우리는 대장균 코어 모델 `e_coli_core`(대사물 72개, 반응 95개)의 화학량론 행렬 $$\mathbf{S}$$를 만들었고, 정상상태 방정식 $$\mathbf{S}\mathbf{v}=\mathbf{0}$$을 배웠다. [Chapter 3](../chapter-3/README.md)에서는 여기에 GPR 규칙, 구획, 그리고 "세포가 무엇을 위해 존재하는가"를 인코딩한 바이오매스 반응까지 붙였다. 이제 이 완성된 모델에게 "대장균은 포도당 최소배지에서 얼마나 빨리 자랄까?"라고 물을 때 컴퓨터가 답을 계산하는 방법이 이 장의 출발점이다.

바로 여기서 곤란한 사실이 등장한다. $$\mathbf{S}\mathbf{v}=\mathbf{0}$$과 플럭스 범위 제약만으로는 답이 **하나로 정해지지 않는다.** `e_coli_core`에는 독립 물질수지식보다 반응 변수가 많아, 이 제약을 만족하는 플럭스 벡터 $$\mathbf{v}$$가 무한히 많이 존재한다. Chapter 2~3에서 정성 들여 만든 모델 안에는 사실 무한히 많은 "가능한 세포"가 숨어 있는 셈이다. 그렇다면 생물학적으로 의미 있는 최적 집합을 좁히는 기준이 필요하다.

이 질문에 답하는 계산 기법이 바로 이 장의 주제, **FBA(Flux Balance Analysis)**이다. FBA는 "세포는 특정 목적(대개는 빠른 성장)을 최대화하도록 진화했다"는 가정을 하나 더 얹어 최적 목적값과 그 값을 달성하는 플럭스 해를 계산한다. 솔버는 한 벡터를 반환하지만 대안 최적해가 존재할 수 있다. 이 장을 마치면 계산 원리를 손으로 검산하고 COBRApy로 실행할 수 있다.

이 책은 이미 배포된 교육용 `e_coli_core`를 먼저 분석 대상으로 사용해 FBA의 계산 논리를 익힌 뒤, 다음 장에서 그러한 모델이 어떤 근거와 품질 관리 과정을 거쳐 만들어지는지 역으로 해설한다. 따라서 이 장의 모델 조작은 재구축의 완결이 아니라, 사전 구축된 모델을 이용한 분석 훈련이다.

이 장은 반응 3개짜리 교육용 장난감 네트워크를 반복해 손으로 푼다. 가능 영역(3절), 심플렉스 타블로(4절), 쌍대 문제(5절), pFBA(8절)를 같은 수치로 연결해 검산한다. 선형계획의 기본 정식화는 `e_coli_core`와 더 큰 모델에도 적용되지만, 실제 해석에는 모델 릴리스, bounds, 목적함수, solver 허용오차와 생물학적 가정을 추가로 확인해야 한다.

---
## 대화형 도해: 핵심 가정과 결과 해석

{% hint style="info" %}
아래 도해는 **교육용 개념·모의 데이터**를 조작하여 이 장의 핵심 가정과 해석 범위를 확인하는 보조 자료이다. 실제 GEM 결과로 인용할 수 없으며, 실제 계산은 모델 버전·배지·목적함수·solver·허용오차를 고정한 실습 코드로 재현해야 한다.
{% endhint %}

{% embed url="https://jyryu3161.github.io/ebook_metabolic_modeling/interactive/index.html?chapter=4" %}

[새 창에서 대화형 도해 열기](https://jyryu3161.github.io/ebook_metabolic_modeling/interactive/index.html?chapter=4)

대화형 조작은 GitBook 지면이 아니라 위 링크(또는 Jupyter)에서 작동한다. 아래는 이 장 3절에서 손으로 다시 유도할 장난감 LP의 가능 영역을 미리 보여주는 정적 그림이다.

![장난감 LP의 가능 오각형과 선형 목적함수 등고선, 유일 최적점 및 대안 최적해가 놓이는 최적 변](../.gitbook/assets/lp-feasible-region.png)

## 이 장을 읽는 방법

플럭스 균형 분석(Flux Balance Analysis, FBA)은 세 가지를 함께 읽어야 한다. **물질수지**, **플럭스 경계**, **목적함수**다. 어느 하나라도 바뀌면 답도 달라질 수 있다.

1. 먼저 $$\mathbf S\mathbf v=\mathbf0$$으로 가능한 상태를 제한한다.
2. 다음으로 배지·방향성·용량을 플럭스 경계로 적용한다.
3. 마지막으로 목적함수를 최대화하거나 최소화해 가능한 해 가운데 하나를 고른다.

{% hint style="info" %}
`optimal`은 주어진 수치 허용오차 안에서 최적해를 찾았다는 solver 상태다. 생물학적 가설이 검증되었다는 뜻은 아니다.
{% endhint %}

## 학습 목표

이 장을 마치면 다음을 할 수 있다.

1. FBA의 세 가지 기본 가정(의사정상상태, 플럭스 제약, 최적화 원리)을 설명하고, 이들이 결합되어 선형 계획법(LP) 문제가 되는 과정을 서술할 수 있다.
2. FBA를 $$\max \mathbf{c}^\mathsf{T}\mathbf{v}$$ subject to $$\mathbf{S}\mathbf{v}=\mathbf{0}$$, $$\mathbf{v}^{lb} \le \mathbf{v} \le \mathbf{v}^{ub}$$ 형태로 정확히 작성할 수 있다.
3. 작은 장난감 네트워크에서 가능 영역을 손으로 그리고, 비어 있지 않은 bounded polytope에서는 적어도 하나의 최적 꼭짓점이 존재한다는 사실을 검증할 수 있다.
4. [플럭스 원추](../glossary.md)(Flux Cone)와 플럭스 폴리토프(Flux Polytope)의 기하학적 의미를 설명할 수 있다.
5. 경사하강법과 LP의 문제 구조를 구분하고, 심플렉스법(Simplex Method)과 내점법(Interior-Point Method)의 원리·차이를 비교하며, [COBRApy](https://opencobra.github.io/cobrapy/)에서 솔버를 설정할 수 있다.
6. 쌍대 문제(Dual Problem)로부터 [그림자 가격](../glossary.md)(Shadow Price)과 환원비용(Reduced Cost)을 손으로 계산·해석하고, 강건성 분석·표현형 상 평면(PhPP)과 연결할 수 있다.
7. COBRApy로 [`e_coli_core`](http://bigg.ucsd.edu/models/e_coli_core)에 FBA를 실행하고, 목적함수와 배지 조건(호기/혐기)을 바꿔가며 결과를 해석할 수 있다.
8. [pFBA](../glossary.md)와 [FVA](../glossary.md)를 실행하여 [대안 최적해](../glossary.md)(Alternate Optima)를 진단하고, 반응을 유연함/목표 유지에 필요함/차단됨으로 구분할 수 있다.
9. FBA의 구조적 한계(열역학, 동역학, 조절, overflow 대사 등)를 인지하고, 대안 기법이 어느 장으로 이어지는지 설명할 수 있다.

---
