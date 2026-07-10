# Chapter 2. 생화학 반응과 대사 네트워크의 수학적 표현

제약 기반 대사 모델은 반응식을 화학량론 행렬 $$\mathbf S$$로 표현한다. 행렬의 각 열은 하나의 반응, 각 행은 하나의 compartment-specific metabolite를 나타낸다. 이 표현을 사용하면 농도 변화는

$$
\frac{d\mathbf x}{dt}=\mathbf S\mathbf v
$$

로, 내부 대사산물의 pseudo-steady-state 조건은

$$
\mathbf S\mathbf v=\mathbf 0
$$

로 기술할 수 있다. 이 장은 반응식에서 $$\mathbf S$$를 구성하고, 행렬·이분 그래프·flux vector가 같은 네트워크를 어떻게 서로 보완하여 표현하는지 다룬다.

## 표기와 읽기 원칙

이 책은 한국어 용어를 먼저 쓰고, 처음 등장할 때 영어 원어와 약어를 함께 표기한다. 이후에는 같은 장 안에서 한 표기를 일관되게 사용한다.

- **플럭스**(flux; 대사 통량), **반응**(reaction), **대사물**(metabolite)은 각각 단위 시간당 반응 진행률, 화학량론적 변환, 구획을 포함한 화학종을 뜻한다.
- **경계조건**(bounds), **목적함수**(objective function), **솔버**(solver)는 생물학적 사실이 아니라 모델에 부여한 계산 조건이다.
- 조건·가정·절차는 번호 목록으로, 결과의 범위와 예외는 `해석상의 주의` 상자로 구분한다.

{% hint style="warning" %}
본문의 “예측”은 명시된 모델·배지·경계조건·목적함수 아래의 계산 결과다. 실험 관찰이나 인과적 효과와 혼용하지 않는다.
{% endhint %}

## 범위

이 장은 화학량론, 반응 방향성, flux bounds, matrix rank 및 null space를 다룬다. GPR, 세포 구획의 생물학적 의미, transport, boundary reaction 및 biomass formulation은 [Chapter 3](../chapter-3/README.md)에서 다룬다. FBA의 선형계획 정식화와 flux variability analysis는 [Chapter 4](../chapter-4/README.md)에서 다룬다.

## 표현의 흐름

```mermaid
flowchart LR
    R["반응식과 계수"] --> S["화학량론 행렬 S"]
    S --> G["부호·가중 이분 그래프"]
    S --> D["d x/dt = S v"]
    D --> SS["내부 대사산물의<br/>S v = 0"]
    SS --> F["Chapter 4<br/>feasible set과 FBA"]
```

*Figure 2.1: 반응식에서 정상상태 제약까지의 표현 변환. 행렬과 이분 그래프는 동일한 화학량론 정보를 다른 형식으로 나타낸다. 저자 작성.*

## 장 구성

| 절 | 주제 | 핵심 산출물 |
|:---|:---|:---|
| §1 | 반응·대사산물·flux | 부호와 단위가 명시된 reaction record |
| §2 | 화학량론 행렬 | $$\mathbf S$$의 행·열과 계수 |
| §3 | 이분 그래프 | 반응–대사산물 연결 구조 |
| §4 | 동역학·정상상태·선형대수 | rank, null space, conservation relation |
| Lab | COBRApy 조회와 행렬 검산 | `textbook` 모델의 $$\mathbf S$$ snapshot |

## 표기

| 기호 | 의미 |
|:---:|:---|
| $$m,n$$ | metabolite 수, reaction 수 |
| $$\mathbf S\in\mathbb R^{m\times n}$$ | stoichiometric matrix |
| $$\mathbf v\in\mathbb R^n$$ | flux vector |
| $$\mathbf x\in\mathbb R^m$$ | metabolite amount 또는 concentration vector |
| $$r=\operatorname{rank}(\mathbf S)$$ | 행렬 rank |
| $$\ell_j,u_j$$ | reaction $$j$$의 lower/upper bound |

Flux의 단위는 모델 convention에 따라 다르며, 이 교재의 COBRApy 예제에서는 일반적으로 $$\mathrm{mmol\,gDW^{-1}\,h^{-1}}$$를 사용한다.

## 대화형 도해: 핵심 가정과 결과 해석

{% hint style="info" %}
아래 도해는 **교육용 개념·모의 데이터**를 조작하여 이 장의 핵심 가정과 해석 범위를 확인하는 보조 자료이다. 실제 GEM 결과로 인용할 수 없으며, 실제 계산은 모델 버전·배지·목적함수·solver·허용오차를 고정한 실습 코드로 재현해야 한다.
{% endhint %}

{% embed url="https://cdn.jsdelivr.net/gh/jyryu3161/ebook_metabolic_modeling@main/interactive/index.html?chapter=2" %}

[새 창에서 대화형 도해 열기](https://cdn.jsdelivr.net/gh/jyryu3161/ebook_metabolic_modeling@main/interactive/index.html?chapter=2)

## 이 장을 읽는 방법

이 장의 핵심은 반응식을 행렬로 바꾸는 **표현의 번역**이다. 수식을 처음 볼 때에는 행렬 전체를 외우지 말고, 한 행은 “한 대사물의 수지”, 한 열은 “한 반응의 기여”라는 규칙부터 확인한다.

1. 반응식의 반응물은 음수, 생성물은 양수 계수로 적는다.
2. 구획이 다르면 같은 화학물질도 별도 대사물 종으로 취급한다.
3. 내부 대사물에 대해 $$\mathbf S\mathbf v=\mathbf0$$을 계산해 생성과 소비가 상쇄되는지 검산한다.

{% hint style="info" %}
$$\mathbf S\mathbf v=\mathbf0$$은 농도가 절대 변하지 않는다는 뜻이 아니라, 선택한 시간 척도에서 내부 대사물의 순축적을 0으로 근사한다는 뜻이다.
{% endhint %}

## 학습 목표

이 장을 마치면 다음을 수행할 수 있다.

1. 반응식의 소비·생성 계수를 $$\mathbf S$$의 한 열로 변환한다.
2. flux 부호와 bound가 저장된 반응식의 방향과 어떻게 연결되는지 설명한다.
3. compartment suffix가 다른 metabolite species를 구분하고 필요한 transport reaction을 식별한다.
4. $$\mathbf S\mathbf v$$를 계산하여 metabolite별 순생성률을 해석한다.
5. pseudo-steady-state 가정과 thermodynamic equilibrium을 구분한다.
6. rank–nullity theorem으로 $$\dim\ker(\mathbf S)=n-r$$를 계산하고, null-space basis·elementary flux mode·extreme ray를 구별한다.
7. COBRApy의 `textbook` 모델에서 $$\mathbf S$$의 크기, nonzero entry, rank 및 null-space dimension을 검산한다.

---
