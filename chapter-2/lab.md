# 실습: COBRApy로 반응·대사산물·화학량론 행렬 검사하기

이 실습은 COBRApy `textbook` 모델에서 reaction·metabolite 객체와 $$\mathbf S$$를 조회하고, rank와 null-space dimension을 검산한다. 전체 notebook은 `raw_data/GEM_lecture_notes/gem9_w02_lab.ipynb`와 `gem9_w03_lab.ipynb`에 있다.

COBRApy `textbook` 모델을 사용해 reaction·metabolite·gene 수와 PGI reaction의 화학량론을 조회한다.

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

마지막으로 $$n-r$$과 왼쪽 영공간 차원 $$m-r$$을 계산한다. $$m-r$$은 수학적 왼쪽 영공간의 차원이며, 물리적으로 해석 가능한 보존 모이어티 수와 자동으로 같지는 않다.

```python
# S 행렬의 계수(rank) 계산 — 4.4절 "n-m ≠ n-r" 논의의 실제 검증
r = np.linalg.matrix_rank(S)
m, n = S.shape

print(f"m = {m}, n = {n}, rank(S) = r = {r}")
print(f"naive 자유도 (n - m): {n - m}")
print(f"실제 영공간 차원  (n - r): {n - r}")
print(f"왼쪽 영공간 차원 (m - r): {m - r}")

# 기대 출력:
# m = 72, n = 95, rank(S) = r = 67
# naive 자유도 (n - m): 23
# 실제 영공간 차원  (n - r): 28
# 왼쪽 영공간 차원 (m - r): 5
```

$$n-r=28$$이 단순한 $$n-m=23$$보다 크다는 것은 $$\mathbf S$$의 행이 선형 독립이 아님을 뜻한다. 물리적으로 해석 가능한 보존 pool을 식별하려면 왼쪽 영공간 벡터의 비음수성, 원자 조성 및 biomass·exchange·분해 반응을 추가로 검토한다.

## 장난감 네트워크의 수치 검산

다음 장난감 네트워크는 $$\mathbf S\mathbf v$$ 계산과 정상상태 제약을 수치로 검산한다. 먼저 닫힌 네트워크에서 $$v_1=v_2=v_3=1$$일 때 $$d\mathbf x/dt=(-2,0,+2)$$를 계산한다.

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

이어서 교환 반응 $$R_0,R_4$$가 있는 열린 네트워크에서 $$v_1=3$$, $$v_3=5$$, $$(v_0,v_2,v_4)=(8,3,8)$$이 $$\mathbf S\mathbf v=0$$을 만족하는지 확인한다.

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

출력이 `[0 0 0]`이면 해당 flux vector가 이 toy network의 정상상태 제약을 만족한다.

## 실제 모델의 영공간과 왼쪽 영공간

마지막으로, 4.5절에서 배운 영공간·왼쪽 영공간의 **차원**뿐 아니라 실제 **기저 벡터**까지 `scipy`로 계산해, 그 개수가 앞서 구한 차원과 일치하는지 확인합니다.

```python
from scipy.linalg import null_space

# 영공간 기저: S v = 0 을 만족하는 벡터들의 기저 (열 개수 = n - r)
ns = null_space(S)
print("영공간 기저 벡터 개수 (n - r):", ns.shape[1])

# 왼쪽 영공간 기저: S^T p = 0, 즉 p^T S = 0 을 만족하는 벡터들의 기저 (열 개수 = m - r)
lns = null_space(S.T)
print("왼쪽 영공간 기저 벡터 개수 (m - r):", lns.shape[1])

# 기대 출력:
# 영공간 기저 벡터 개수 (n - r): 28
# 왼쪽 영공간 기저 벡터 개수 (m - r): 5
```

`ns.shape[1]`과 `lns.shape[1]`은 rank에서 계산한 $$n-r$$과 $$m-r$$에 각각 일치해야 한다. Numerical null-space basis는 유일하지 않으며, basis vector 하나를 독립적인 생물학적 pathway나 보존 pool로 해석해서는 안 된다.

---
