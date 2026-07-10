# 마무리: 요약 · 스스로 점검 · 용어

## 한 장 요약

- 대사 네트워크는 **반응**과 **대사물**이라는 두 종류의 개체와 그 관계로 구성되며, 각 반응은 화학량론·방향성(가역성)·통량 범위·촉매 효소(GPR)라는 속성을 가진다.
- 반응의 방향성은 통량 하한/상한($$v^{lb}, v^{ub}$$)으로 코딩되며, 그 근거는 표준 깁스 자유 에너지 변화의 부호다.
- 대사물 ID의 구획 접미사(`_c`, `_e`, `_m` 등)는 같은 분자라도 위치가 다르면 서로 다른 노드로 다뤄야 함을 나타낸다.
- **화학량론 행렬 $$\mathbf{S} \in \mathbb{R}^{m\times n}$$**은 모든 반응의 화학량론 계수를 하나로 압축한 행렬이며, 2~3개 반응짜리 장난감 네트워크를 손으로 직접 구성해 봄으로써 그 구성 규칙을 확인했다.
- 실제 GEM에서 $$\mathbf{S}$$는 매우 희소한 구조를 가진다(*E. coli* core 모델은 5.26%). 이 희소성 이면에는 ATP, NADH 같은 소수의 허브 대사물이 존재한다.
- 대사 네트워크는 이 행렬과 동등하게 **이분 그래프**로도 표현할 수 있으며, 두 표현은 서로 다른 문제(위상 분석 vs. 선형대수/최적화)에 각각 유용하다.
- $$d\mathbf{x}/dt = \mathbf{S}\mathbf{v}$$에서 출발하여 **의사-정상 상태 가정**을 도입하면 $$\mathbf{S}\mathbf{v} = \mathbf{0}$$을 얻는다. 장난감 네트워크를 손으로 풀어 본 결과, 닫힌 네트워크(교환 반응 없음)는 오직 $$\mathbf{v}=\mathbf{0}$$만 허용하지만, 출입구를 열면(교환 반응 추가) 무한히 많은 정상 상태 해가 나타난다.
- 진짜 자유도는 naive한 $$n-m$$이 아니라 $$\mathbf{S}$$의 계수(rank) $$r$$을 반영한 $$n-r$$이다. $$\mathbf{S}$$의 네 가지 기본 부분공간(영공간, 왼쪽 영공간, 열공간, 행공간)은 각각 정상 상태 통량 공간과 보존 화기(예: ATP+ADP+AMP)라는 생물학적으로 의미 있는 구조에 대응하며, *E. coli* core 모델에서 이를 COBRApy로 직접 검증했다($$n-r=28$$, $$m-r=5$$).
- 이 무한한 해 집합에서 하나의 최적해를 골라내는 방법(목적함수, 선형계획법, 플럭스 원추)은 [Chapter 4](../chapter-4/README.md)에서, GPR·구획·바이오매스·교환 반응의 상세한 설계는 [Chapter 3](../chapter-3/README.md)에서 이어진다.

---

## 스스로 점검

1. **(개념)** 세포질의 피루브산(`pyr_c`)과 미토콘드리아의 피루브산(`pyr_m`)은 화학적으로 동일한 분자입니다. 그런데도 모델에서 서로 다른 대사물 노드로 취급하는 이유는 무엇일까요? *(힌트: 1.3절 — 대사물의 정체성은 화학종 자체가 아니라 그것이 관여하는 반응 집합으로 정의됩니다.)*

2. **(계산)** 반응 $$2\text{A} + \text{B} \rightarrow \text{C}$$ 하나만 있는 네트워크를 생각해 봅시다. 대사물 $$\{A, B, C\}$$를 행으로, 이 반응 하나를 열로 하는 $$3\times 1$$ 화학량론 행렬 $$\mathbf{S}$$를 직접 써 보세요. *(정답: $$\mathbf{S} = (-2, -1, +1)^\top$$)*

3. **(계산)** 4.3절 (B)의 열린 장난감 네트워크에서 $$v_1 = 4$$, $$v_3 = 2$$로 두면 $$v_0, v_2, v_4$$는 각각 얼마여야 $$\mathbf{S}\mathbf{v}=\mathbf{0}$$이 성립할까요? *(정답: $$v_0=6, v_2=4, v_4=6$$)*

4. **(개념)** 실제 게놈 규모 모델에서는 항상 $$n>m$$이 성립합니다. 이 부등식의 생물학적 의미는 무엇이며, 왜 이것이 곧바로 "무한히 많은 해"를 보장하지는 않는지(4.3절의 닫힌 네트워크 예시를 떠올리며) 설명해 보세요.

5. **(사고)** 만약 어떤 모델의 $$\mathbf{S}$$가 풀랭크(full row rank, 즉 $$r=m$$)라면, 이 모델에는 보존 화기가 존재할까요? 왜 그런지 4.5절의 왼쪽 영공간 정의를 이용해 설명해 보세요. *(힌트: 왼쪽 영공간의 차원은 $$m-r$$입니다.)*

---

## 다음 장 예고

이 장에서 우리는 반응과 대사물이라는 두 개체를 화학량론 행렬 $$\mathbf{S}$$로 압축하고, $$\mathbf{S}\mathbf{v}=\mathbf{0}$$이라는 질량 보존 제약이 대사 네트워크에 어떤 자유도를 남기는지 손으로 직접 확인했습니다. 이제 우리는 네트워크의 "뼈대"를 갖췄습니다.

하지만 아직 빠진 것이 있습니다 — $$\mathbf{S}$$의 각 열(반응)이 **어떤 유전자·효소**에 의해 촉매되는지, 그 반응이 세포의 **어느 구획**에서 일어나는지, 그리고 세포와 환경의 **경계**는 어떻게 설정되는지에 대한 정보입니다. 이 정보들이 채워져야 비로소 $$\mathbf{S}$$가 "이름 없는 골격"에서 살아있는 세포의 완전한 모델로 거듭납니다. 다음 [Chapter 3. GEM의 구조](../chapter-3/README.md)에서는 GPR(Gene-Protein-Reaction) 규칙, 세포 구획과 수송 반응, 교환·생물량 반응의 설계를 다루며 이 골격에 생물학적 정체성을 입힙니다.

---

## 핵심 용어 정리

| 용어 (English) | 정의 |
|:---|:---|
| 반응 (Reaction) | 대사물을 변환하는 기본 단위. 화학량론·방향성·통량 범위·GPR로 구성됨 |
| 대사물 (Metabolite) | 반응에서 소비·생성되는 화학 종. ID에 구획 접미사가 붙음 |
| 가역성 (Reversibility) | 반응이 양방향으로 진행 가능한지 여부. $$v^{lb}<0<v^{ub}$$로 코딩 |
| 구획 (Compartment) | 대사물·반응이 위치하는 세포 내 구역 (`_c`, `_e`, `_m` 등) |
| 화학량론 행렬 (Stoichiometric Matrix, S) | $$m \times n$$ 크기로 모든 반응의 화학량론 계수를 인코딩한 행렬 |
| 희소성 (Sparsity) | 행렬에서 0이 아닌 항목의 비율이 매우 낮은 성질. *E. coli* core 모델은 5.26% |
| 허브 대사물 (Hub Metabolite) | ATP, NADH, H$$_2$$O 등 수백 개 반응에 관여하는 소수의 고연결 대사물 |
| 이분 그래프 (Bipartite Graph) | 대사물 노드와 반응 노드 두 집합으로만 구성되고, 같은 집합 내 간선이 없는 그래프 |
| 정상 상태 가정 (Pseudo-Steady-State Assumption, PSSA) | 내부 대사물 농도가 관심 시간 척도에서 변하지 않는다는 가정, $$d\mathbf{x}/dt=\mathbf{0}$$ |
| 자유도 (Degrees of Freedom) | 정상 상태 제약만으로 유일해가 결정되지 않는 미지수의 여유분. 진짜 값은 $$n-r$$ ($$r$$=계수) |
| 계수 (Rank) | 행렬의 독립적인 행(또는 열)의 개수 $$r$$. 실제 GEM에서는 보통 $$r<m$$ |
| 영공간 (Null Space) | $$\{\mathbf{v}: \mathbf{S}\mathbf{v}=\mathbf{0}\}$$, 차원 $$n-r$$. 가능한 모든 정상 상태 통량 분포의 공간 |
| 왼쪽 영공간 (Left Null Space) | $$\{\mathbf{p}: \mathbf{p}^\top\mathbf{S}=\mathbf{0}\}$$, 차원 $$m-r$$. 보존 화기의 공간 |
| 보존 화기 (Conserved Moiety) | 왼쪽 영공간에서 유래하는, 총합이 항상 일정한 대사물 풀 (예: ATP+ADP+AMP) |

---

## 참고문헌 / 더 읽을거리

- Monk, J. M. et al. (2017). *iML1515, a knowledgebase that computes Escherichia coli traits.* Nature Biotechnology, 35(10), 904–908.
- Orth, J. D., Thiele, I., & Palsson, B. Ø. (2010). *What is flux balance analysis?* Nature Biotechnology, 28(3), 245–248.
- Palsson, B. Ø. (2015). *Systems Biology: Constraint-based Reconstruction and Analysis.* Cambridge University Press.
- Ravasz, E. et al. (2002). *Hierarchical organization of modularity in metabolic networks.* Science, 297(5586), 1551–1555.
- Ebrahim, A. et al. (2013). *COBRApy: COnstraints-Based Reconstruction and Analysis for Python.* BMC Systems Biology, 7, 74.
- 본 챕터의 실습 코드 전체: `raw_data/GEM_lecture_notes/gem9_w02_lab.ipynb`, `gem9_w03_lab.ipynb`
