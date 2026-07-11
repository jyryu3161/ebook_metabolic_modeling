# 마무리: 요약 · 연습문제 · 용어

## 한 장 요약

- [화학량론 행렬](../glossary.md) $$\mathbf{S}\in\mathbb{R}^{m\times n}$$의 행은 구획이 지정된 대사물, 열은 반응에 대응한다. 원소 $$S_{ij}$$는 반응 $$j$$에서 대사물 $$i$$의 순 화학량론 몰비이며, 소비는 음수, 생성은 양수로 기록한다.
- 반응 방향성과 용량은 $$\mathbf{S}$$가 아니라 bounds $$\mathbf{l}\leq\mathbf{v}\leq\mathbf{u}$$에 기록한다. 통량 $$v_j$$는 단위 시간·단위 생물량당 반응 진행률이며, $$\mathbf{S}\mathbf{v}$$는 같은 단위의 대사물 순생성률이다. 별도의 부피 변환 없이 농도 변화율로 해석할 수 없다.
- COBRA 계열 교환 반응이 $$X_e\rightleftharpoons\varnothing$$, $$S_{X,\mathrm{EX}}=-1$$로 저장되어 있으면 음의 교환 통량은 흡수, 양의 교환 통량은 분비를 뜻한다. 모델마다 저장 방향이 다를 수 있으므로 반응식·계수·bounds를 함께 확인한다.
- 부호·가중 이분 그래프는 $$\mathbf{S}$$의 비영 원소와 계수 크기를 보존할 수 있다. 무가중 이분 그래프는 참여 관계만 보존하며, 대사물 또는 반응 투영 그래프는 다자 반응을 쌍별 간선으로 축약한다.
- 행렬 비영 비율 $$\operatorname{nnz}(\mathbf{S})/(mn)$$, 이분 incidence 그래프 밀도 $$|E|/(mn)$$, 투영 그래프 밀도는 정의가 서로 다르다. 그래프 경로는 위상적 연결 가능성을 나타낼 뿐 정상상태·bounds·열역학을 만족하는 통량 경로를 보장하지 않는다.
- [의사-정상상태](../glossary.md) 가정은 세포 내 중간대사물의 순축적이 관심 시간척도에서 작다고 보는 근사이다. 표준 FBA는 이 근사를 정확한 계산 제약 $$\mathbf{S}\mathbf{v}=0$$으로 부과한다. 정상상태는 화학평형이 아니며 총생성률과 총소비률은 비영일 수 있다.
- 대사물 풀 $$q_i$$와 정상상태 gross turnover flux $$J_i=J_i^+=J_i^-$$에 대한 회전시간은 $$\tau_i=q_i/J_i$$이다. 정상상태에서 0이 되는 순생성률 $$(\mathbf{S}\mathbf{v})_i$$를 분모로 사용하지 않는다.
- $$r=\operatorname{rank}(\mathbf{S})$$이면 $$\dim\ker(\mathbf{S})=n-r$$이다. 이는 정상상태 등식계의 nullity이며, bounds까지 적용한 가능 영역의 차원이나 생물학적 경로 수가 아니다. $$n>m$$은 GEM의 필수 조건이 아니다.
- [null-space basis](../glossary.md)는 비유일한 선형대수 좌표계이다. 비가역성까지 만족하는 support-minimal 경로는 elementary flux mode(EFM), pointed flux cone의 최소 생성 방향은 extreme ray로 구분한다. 유한한 비영 bounds가 포함된 FBA 가능 영역은 일반적으로 원추가 아니라 flux polyhedron이다.
- 교환 반응이 없는 비가역·비순환 toy network에서는 0 통량만 남을 수 있지만, 가역 반응이나 내부 순환을 가진 닫힌 네트워크에는 비영 정상상태 순환이 존재할 수 있다. 닫힘 여부만으로 통량을 판정할 수 없다.

---

## 연습문제

1. **정의 확인**: 반응 $$2A+B\rightarrow3C$$를 행 순서 $$(A,B,C)$$로 표현한 화학량론 열을 작성하고 각 계수의 단위를 설명하시오.

2. **단위 분석**: $$v_j$$의 단위가 $$\mathrm{mmol\,gDW^{-1}\,h^{-1}}$$이고 $$S_{ij}=-2$$일 때, 반응 $$j$$가 대사물 $$i$$의 순생성률에 기여하는 값과 단위를 계산하시오. 이 값을 곧바로 $$\mathrm{mmol\,L^{-1}\,h^{-1}}$$로 해석할 수 없는 이유를 설명하시오.

3. **교환 부호**: `EX_glc__D_e`가 `glc__D_e <=>`, 계수 $$-1$$, bounds $$(-10,1000)$$으로 저장되어 있다. 흡수·분비 방향과 각 방향의 최대 허용량을 구분하시오.

4. **그래프 표현 비교**: 하나의 반응 $$A+2B\rightarrow C+D$$를 부호·가중 이분 그래프와 대사물 투영 그래프로 각각 표현하시오. 두 표현이 보존하거나 잃는 정보를 비교하시오.

5. **정상상태와 평형**: $$J_i^+=J_i^-=20\ \mathrm{mmol\,gDW^{-1}\,h^{-1}}$$인 대사물에 대해 순생성률을 계산하고, 이 상태가 화학평형을 의미하지 않는 이유를 설명하시오.

6. **회전시간**: 특정 대사물 풀 크기가 $$0.20\ \mathrm{mmol\,gDW^{-1}}$$이고 정상상태 gross inflow가 $$20\ \mathrm{mmol\,gDW^{-1}\,h^{-1}}$$이다. 회전시간을 시간과 초 단위로 계산하시오.

7. **rank-nullity와 bounds**: $$m=4$$, $$n=7$$, $$r=3$$인 모델의 영공간 차원을 계산하시오. 이어서 두 반응의 bounds가 $$l_j=u_j=0$$으로 고정되었을 때 이 값이 가능 영역의 차원과 반드시 같지 않은 이유를 설명하시오.

8. **가정 비판**: 교환 반응이 없는 네트워크에서 비영 정상상태 통량이 가능한 반례를 가역 반응 또는 내부 순환을 사용하여 구성하시오. 해당 통량이 생리학적으로 타당하려면 추가로 어떤 조건을 검토해야 하는가?

9. **경로 개념**: null-space basis, extreme ray, EFM을 정의하고, 임의의 null-space basis 벡터를 대사 경로로 해석하면 안 되는 이유를 서술하시오.

---

## 이 장의 표기법

| 기호 | 정의 | 단위 또는 차원 |
|:---:|:---|:---|
| $$\mathbf{S}$$ | 화학량론 행렬 | $$m\times n$$, 계수는 몰비 |
| $$m,n$$ | 대사물 수, 반응 수 | 무차원 개수 |
| $$\mathbf{v},v_j$$ | 특정 반응 통량 | 보통 $$\mathrm{mmol\,gDW^{-1}\,h^{-1}}$$ |
| $$\mathbf{l},\mathbf{u}$$ | 통량 하한·상한 | $$\mathbf{v}$$와 동일 |
| $$\mathbf{n}$$ | 절대 대사물 물질량 | $$\mathrm{mmol}$$ |
| $$\mathbf{q}=\mathbf{n}/X$$ | 생물량 정규화 대사물 풀 | $$\mathrm{mmol\,gDW^{-1}}$$ |
| $$J_i^+,J_i^-$$ | 대사물 $$i$$의 gross 생성·소비 통량 | $$\mathrm{mmol\,gDW^{-1}\,h^{-1}}$$ |
| $$\tau_i=q_i/J_i$$ | 회전시간 | 시간 |
| $$r$$ | $$\operatorname{rank}(\mathbf{S})$$ | 무차원 |
| $$n-r$$ | $$\ker(\mathbf{S})$$의 차원 | 정상상태 등식계의 nullity |
| $$m-r$$ | $$\ker(\mathbf{S}^\top)$$의 차원 | 왼쪽 영공간의 차원 |

## 다음 장

[Chapter 3](../chapter-3/README.md)에서는 화학량론 외에 [GPR](../chapter-3/README.md), 구획, 경계 반응, 바이오매스 반응, 목적함수와 같은 모델 구조를 구분한다. 이 정보들은 $$\mathbf{S}$$의 일부이거나 별도 속성으로 저장되며, [Chapter 4](../chapter-4/README.md)에서 bounds 및 목적함수와 결합되어 선형계획 문제를 구성한다.

---

## 핵심 용어

| 용어 | 정의 |
|:---|:---|
| [화학량론 행렬](../glossary.md) | 반응별 순 화학량론 몰비를 대사물×반응 배열로 기록한 행렬 |
| 비영 비율 | $$\operatorname{nnz}(\mathbf{S})/(mn)$$ |
| 부호·가중 이분 그래프 | 대사물과 반응을 서로 다른 노드 집합으로 두고 계수의 부호·크기를 간선에 기록한 그래프 |
| 투영 그래프 | 이분 그래프에서 한 종류의 노드만 남겨 쌍별 관계로 축약한 그래프 |
| [의사-정상상태](../glossary.md) | 관심 시간척도에서 세포 내 중간대사물의 순축적을 무시하는 근사 |
| 회전시간 | 대사물 pool size를 정상상태 gross inflow 또는 gross outflow로 나눈 시간 |
| [영공간](../glossary.md) | $$\{\mathbf{v}:\mathbf{S}\mathbf{v}=0\}$$ |
| 보존량 후보 | 왼쪽 영공간의 비음수이며 화학적으로 해석 가능한 벡터가 나타내는 보존 pool |
| [플럭스 원추](../glossary.md) | 정상상태 등식과 동차 비가역성 제약의 교집합 |
| flux polyhedron | 정상상태 등식과 일반적인 유한 bounds의 교집합 |
| EFM | 플럭스 원추의 비영 support-minimal 통량 벡터 |
| EFV | 일반 flux polyhedron으로 확장된 elementary flux vector |

---

## 참고문헌

1. Orth JD, Thiele I, Palsson BØ. What is flux balance analysis? *Nature Biotechnology*. 2010;28:245–248. [DOI: 10.1038/nbt.1614](https://doi.org/10.1038/nbt.1614), [PMC3108565](https://pmc.ncbi.nlm.nih.gov/articles/PMC3108565/)
2. Jang C, Chen L, Rabinowitz JD. Metabolomics and isotope tracing. *Cell*. 2018;173:822–837. [DOI: 10.1016/j.cell.2018.03.055](https://doi.org/10.1016/j.cell.2018.03.055), [PMC6034115](https://pmc.ncbi.nlm.nih.gov/articles/PMC6034115/)
3. Klamt S, Regensburger G, Gerstl MP, et al. From elementary flux modes to elementary flux vectors. *PLoS Computational Biology*. 2017;13:e1005409. [DOI: 10.1371/journal.pcbi.1005409](https://doi.org/10.1371/journal.pcbi.1005409)
4. Poupin N, Corvez A, Mariadassou M, et al. Combining graph and flux-based structures to decipher phenotypic essential metabolites within metabolic networks. *BMC Systems Biology*. 2017;11:94. [PMC5641430](https://pmc.ncbi.nlm.nih.gov/articles/PMC5641430/)

---
