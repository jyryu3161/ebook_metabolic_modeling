# 💡 실습: COBRApy로 반응·대사물·S 행렬 탐색하기

> 아래 코드는 핵심 개념만 담은 발췌본입니다. 전체 실습(모델 로드, GPR 파싱, 구획·수송 반응 분석 등)은 `raw_data/GEM_lecture_notes/gem9_w02_lab.ipynb`와 `gem9_w03_lab.ipynb`에서 확인할 수 있습니다.

[Chapter 1](../chapter-1/README.md)에서 불러온 `e_coli_core`를 다시 사용합니다. 먼저 반응·대사물·유전자 수를 확인하고, 개별 반응 객체의 화학량론 정보를 직접 조회해 봅니다. 이 챕터의 대표 반응으로는 **PGI(phosphoglucose isomerase, 포스포글루코스 이성질화효소)**를 사용합니다.

```python
from cobra.io import load_model

# 1장에서 불러온 것과 동일한 E. coli core 모델 (COBRApy 내장 예제 모델)
model = load_model("textbook")

print(f"Model: {model.id}")
print(f"Reactions: {len(model.reactions)}")
print(f"Metabolites: {len(model.metabolites)}")
print(f"Genes: {len(model.genes)}")

# 기대 출력:
# Model: e_coli_core
# Reactions: 95
# Metabolites: 72
# Genes: 137

# 개별 반응 객체의 화학량론 조회 (대표 반응 PGI: G6P <=> F6P)
rxn = model.reactions.get_by_id("PGI")
print(rxn.name)
print(rxn.reaction)                       # 화학량론식 문자열
print(rxn.lower_bound, rxn.upper_bound)   # 통량 하한/상한
for met, coef in rxn.metabolites.items():
    print(f"  {met.id}: {coef:+.0f}")     # 대사물별 화학량론 계수

# 기대 출력:
# glucose-6-phosphate isomerase
# g6p_c <=> f6p_c
# -1000.0 1000.0
#   g6p_c: -1
#   f6p_c: +1
```

`rxn.lower_bound`가 음수라는 것은 `<=>` 표기 그대로 가역 반응이라는 뜻이며(1.2절), `rxn.metabolites`는 이 반응이 $$\mathbf{S}$$ 행렬에 기여하는 한 개의 열(column)을 그대로 보여줍니다(2.2절).

다음으로, 모델 전체의 화학량론 행렬 $$\mathbf{S}$$를 numpy 배열로 직접 꺼내 크기와 희소성(sparsity)을 확인합니다.

```python
from cobra.util.array import create_stoichiometric_matrix
import numpy as np

S = create_stoichiometric_matrix(model, array_type="dense")

print("S matrix shape (m x n):", S.shape)
print("Nonzero entries:", np.count_nonzero(S))
print(f"Sparsity (0이 아닌 비율): {np.count_nonzero(S) / S.size:.2%}")

# 기대 출력:
# S matrix shape (m x n): (72, 95)
# Nonzero entries: 360
# Sparsity (0이 아닌 비율): 5.26%
```

`S.shape`가 `(72, 95)`로 나온다는 것은 곧 $$m=72$$, $$n=95$$라는 뜻이며, 이는 2.4절 표에서 확인한 *E. coli* core 모델의 수치와 정확히 일치합니다.

마지막으로, 4.4~4.6절에서 손으로 논한 "진짜 자유도($$n-r$$)"와 "보존 화기 개수($$m-r$$)"를 실제 모델에서 직접 계산해 봅니다.

```python
# S 행렬의 계수(rank) 계산 — 4.4절 "n-m ≠ n-r" 논의의 실제 검증
r = np.linalg.matrix_rank(S)
m, n = S.shape

print(f"m = {m}, n = {n}, rank(S) = r = {r}")
print(f"naive 자유도 (n - m): {n - m}")
print(f"실제 영공간 차원  (n - r): {n - r}")
print(f"왼쪽 영공간 차원  (m - r), 즉 독립 보존 화기 개수: {m - r}")

# 기대 출력:
# m = 72, n = 95, rank(S) = r = 67
# naive 자유도 (n - m): 23
# 실제 영공간 차원  (n - r): 28
# 왼쪽 영공간 차원  (m - r), 즉 독립 보존 화기 개수: 5
```

$$n-r=28$$이 naive한 $$n-m=23$$보다 크다는 사실은, *E. coli* core 모델 안에도 4.6절에서 논한 것과 같은 보존 화기(예: 아데닌·피리딘 뉴클레오타이드 풀)가 최소 5개 숨어 있다는 증거입니다.

## 손으로 계산한 것을 코드로 검산하기

2.3절과 4.3절에서 손으로 만들고 풀었던 장난감 네트워크를 그대로 numpy로 옮겨, 손 계산과 코드가 정확히 일치하는지 확인해 봅시다. 먼저 닫힌 네트워크에서 4.1절의 예시($$v_1=v_2=v_3=1$$일 때 $$d\mathbf{x}/dt=(-2,0,+2)$$)를 검증합니다.

```python
import numpy as np

# 2.3절 닫힌 장난감 네트워크: 행=[A,B,C], 열=[R1,R2,R3]
S_closed = np.array([
    [-1,  0, -1],
    [ 1, -1,  0],
    [ 0,  1,  1],
])

v = np.array([1, 1, 1])          # 4.1절에서 사용한 임의의 통량
dxdt = S_closed @ v
print("dx/dt =", dxdt)

# 기대 출력:
# dx/dt = [-2  0  2]
```

이어서 4.3절 (B)의 열린 네트워크(교환 반응 $$R_0, R_4$$ 추가)에서, 손으로 검산했던 $$v_1=3, v_3=5 \Rightarrow (v_0,v_2,v_4)=(8,3,8)$$이 실제로 $$\mathbf{S}\mathbf{v}=\mathbf{0}$$을 만족하는지 확인합니다.

```python
# 4.3절 (B) 열린 네트워크: 열 순서 = [R0, R1, R2, R3, R4]
S_open = np.array([
    [ 1, -1,  0, -1,  0],   # A
    [ 0,  1, -1,  0,  0],   # B
    [ 0,  0,  1,  1, -1],   # C
])

v_open = np.array([8, 3, 3, 5, 8])   # v0, v1, v2, v3, v4
print("S_open @ v_open =", S_open @ v_open)

# 기대 출력:
# S_open @ v_open = [0 0 0]
```

`[0 0 0]`이 그대로 나온다는 것은, 4.3절에서 손으로 검산했던 결과가 코드로도 정확히 재현된다는 뜻입니다. 이런 식으로 "손 계산 → 코드 검증"을 습관화하면, 이후 수백~수천 차원의 실제 GEM을 다룰 때도 결과를 신뢰할 수 있는 감각이 생깁니다.

## 실제 모델에서 영공간·왼쪽 영공간 기저를 직접 구하기

마지막으로, 4.5절에서 배운 영공간·왼쪽 영공간의 **차원**뿐 아니라 실제 **기저 벡터**까지 `scipy`로 계산해, 그 개수가 앞서 구한 차원과 일치하는지 확인합니다.

```python
from scipy.linalg import null_space

# 영공간 기저: S v = 0 을 만족하는 벡터들의 기저 (열 개수 = n - r)
ns = null_space(S)
print("영공간 기저 벡터 개수 (n - r):", ns.shape[1])

# 왼쪽 영공간 기저: S^T p = 0, 즉 p^T S = 0 을 만족하는 벡터들의 기저 (열 개수 = m - r)
lns = null_space(S.T)
print("왼쪽 영공간 기저 벡터 개수 (m - r), 즉 독립 보존 화기 개수:", lns.shape[1])

# 기대 출력:
# 영공간 기저 벡터 개수 (n - r): 28
# 왼쪽 영공간 기저 벡터 개수 (m - r), 즉 독립 보존 화기 개수: 5
```

`ns.shape[1]`이 28, `lns.shape[1]`이 5로 나온다는 것은, 앞서 `np.linalg.matrix_rank`로 계산한 $$n-r=28$$, $$m-r=5$$와 정확히 일치합니다 — 랭크로부터 유도한 "차원"과 `scipy`가 실제로 구성해준 "기저 벡터 개수"가 서로 다른 방법으로 계산했음에도 같은 값에 도달한다는 것은, 4.5절의 이론이 코드에서도 그대로 성립함을 보여주는 좋은 교차 검증입니다. 이 기저 벡터들을 직접 열어보면(`ns[:, 0]` 등) 4.5절에서 손으로 구한 $$\mathbf{u}_1, \mathbf{u}_2$$처럼 특정 반응 경로에 대응하는 패턴을 확인할 수 있습니다 — 다만 실제 GEM에서는 기저 벡터 하나가 항상 깔끔한 하나의 "경로"에 대응하지는 않으며, 여러 경로가 섞인 형태로 나올 수도 있다는 점에 유의하십시오.

---
