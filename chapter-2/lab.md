# 실습: COBRApy로 반응·대사산물·화학량론 행렬 검사하기

이 실습은 [COBRApy](https://opencobra.github.io/cobrapy/) `textbook` 모델에서 reaction·metabolite 객체와 화학량론 행렬 $$\mathbf S$$를 조회하고, [rank](../glossary.md)와 [영공간](../glossary.md)(null space)의 차원을 검산합니다. 전체 notebook은 `raw_data/GEM_lecture_notes/gem9_w02_lab.ipynb`와 `gem9_w03_lab.ipynb`에 있습니다.

## 이 실습에서 하는 일

COBRApy에 내장된 *E. coli* core 모델(`textbook`)을 불러와, 이 장에서 배운 개념이 실제 코드에서 어떻게 나타나는지 직접 확인합니다. 반응 하나의 화학량론 계수를 읽는 것에서 시작해, 모델 전체의 $$\mathbf S$$ 행렬을 꺼내고, 마지막에는 작은 장난감(toy) 네트워크로 정상상태 제약 $$\mathbf S\mathbf v=0$$을 손으로 검산합니다.

## 학습 목표

이 실습을 마치면 다음을 수행할 수 있습니다.

1. COBRApy `textbook` 모델을 불러와 반응·대사물·유전자 수를 확인합니다.
2. 개별 반응 객체에서 화학량론 계수와 flux bound를 조회합니다.
3. 화학량론 행렬 $$\mathbf S$$를 numpy 배열로 꺼내 크기와 희소성(sparsity)을 계산합니다.
4. rank로 영공간·왼쪽 영공간의 차원을 계산하고, 단순한 $$n-m$$과 구분합니다.
5. 장난감 네트워크에서 $$\mathbf S\mathbf v$$를 계산해 정상상태 제약을 수치로 검산합니다.
6. `scipy`로 구한 영공간 기저 벡터의 개수가 앞서 계산한 차원과 일치하는지 확인합니다.

## 준비물

- **실행 환경**: 이 실습은 파이썬으로 진행합니다. [Chapter 11 §1](../chapter-11/01.md)의 격리된 가상환경(`.venv-gem`)을 그대로 사용하거나, [설치 가이드](../installation.md)를 따라 환경을 먼저 준비합니다.
- **필요한 패키지**: `cobra==0.30.0`(모델 조회), `numpy`(행렬 계산), `scipy`(영공간 기저 계산). 세 가지 모두 위 가상환경에 이미 포함되어 있습니다.
- **모델**: COBRApy에 내장된 `textbook` 예제(모델 ID는 `e_coli_core`)를 사용합니다. 별도의 파일을 내려받을 필요 없이 `load_model("textbook")`로 불러옵니다.
- **선행 셀**: 단계 3 이후는 앞 단계에서 만든 변수(`model`, `S`)를 재사용합니다. 노트북을 위에서 아래로 순서대로 실행합니다.

이 장의 모든 숫자는 위 버전 조합에서 얻은 값입니다. 버전이 다르면 rank 같은 수치가 미세하게 달라질 수 있습니다.

### 단계 1. textbook 모델 불러오기와 규모 확인하기

먼저 COBRApy에 내장된 *E. coli* core 모델을 불러오고, 이 모델이 몇 개의 반응·대사물·유전자로 이루어졌는지 확인합니다. `load_model("textbook")`은 인터넷 연결 없이 패키지 안에 들어 있는 예제 모델을 바로 반환합니다.

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
```

**예상 출력**

```
Model: e_coli_core
Reactions: 95
Metabolites: 72
Genes: 137
```

**확인 포인트**: 모델 ID가 `e_coli_core`이고 반응 95개, 대사물 72개, 유전자 137개로 출력되면 성공입니다. 이 대사물 수 72와 반응 수 95는 뒤에서 만들 $$\mathbf S$$ 행렬의 행·열 개수와 정확히 같아야 합니다.

**자주 나는 오류와 해결**

- `ModuleNotFoundError: No module named 'cobra'`: 가상환경이 활성화되지 않았거나 COBRApy가 설치되지 않은 경우입니다. [Chapter 11 §1](../chapter-11/01.md)의 `source .venv-gem/bin/activate`로 환경을 켠 뒤 다시 실행합니다.
- 모델 다운로드를 시도하며 멈추는 경우: `"textbook"`은 내장 모델이므로 네트워크가 필요 없습니다. 철자를 그대로(`textbook`) 입력했는지 확인합니다.

### 단계 2. PGI 반응 객체에서 화학량론 열 읽기

다음으로 반응 하나를 골라 그 안을 들여다봅니다. 대표로 PGI(glucose-6-phosphate isomerase) 반응을 조회합니다. 여기서 [플럭스](../glossary.md)(flux)는 반응 $$j$$의 진행 속도이며, 이 교재의 COBRApy 예제에서는 단위가 $$\mathrm{mmol\,gDW^{-1}\,h^{-1}}$$인 값입니다. `lower_bound`와 `upper_bound`는 이 flux가 움직일 수 있는 범위(하한·상한)를 뜻합니다. 반응 객체의 화학량론 개념은 [1.2절](01.md), 이 값이 $$\mathbf S$$의 한 열이 되는 원리는 [2.2절](02.md)에서 설명합니다.

```python
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

**예상 출력**

```
glucose-6-phosphate isomerase
g6p_c <=> f6p_c
-1000.0 1000.0
  g6p_c: -1
  f6p_c: +1
```

**확인 포인트**: 반응식이 `g6p_c <=> f6p_c`로, 계수가 `g6p_c: -1`, `f6p_c: +1`로 나오면 성공입니다. 음수 계수는 소비되는 기질, 양수 계수는 생성되는 산물을 뜻합니다.

`rxn.lower_bound`가 음수(`-1000.0`)라는 것은 `<=>` 표기 그대로 가역 반응이라는 뜻이며([1.2절](01.md)), `rxn.metabolites`는 이 반응이 $$\mathbf{S}$$ 행렬에 기여하는 한 개의 열(column)을 그대로 보여줍니다([2.2절](02.md)).

**자주 나는 오류와 해결**

- `KeyError` 또는 반응을 찾지 못하는 경우: 반응 ID는 대소문자를 구분합니다. `"PGI"`처럼 정확히 입력합니다.
- `NameError: name 'model' is not defined`: 단계 1을 먼저 실행하지 않은 경우입니다. 노트북을 위에서부터 순서대로 실행합니다.

### 단계 3. 화학량론 행렬 S를 꺼내 희소성 확인하기

이제 반응 하나가 아니라 모델 **전체**의 [화학량론 행렬](../glossary.md) $$\mathbf S$$를 numpy 배열로 꺼냅니다. `create_stoichiometric_matrix`는 각 열이 하나의 반응, 각 행이 하나의 대사물인 $$m\times n$$ 행렬을 만들어 줍니다. 대부분의 반응은 소수의 대사물만 포함하므로, 이 행렬은 0이 많은 희소(sparse) 행렬입니다([2.4절](02.md)).

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

**예상 출력**

```
S matrix shape (m x n): (72, 95)
Nonzero entries: 360
Sparsity (0이 아닌 비율): 5.26%
```

**확인 포인트**: `S.shape`가 `(72, 95)`로, 비영 원소가 360개, 채움 비율이 `5.26%`로 나오면 성공입니다.

`S.shape`가 `(72, 95)`로 나온다는 것은 곧 $$m=72$$, $$n=95$$라는 뜻이며, 이는 [2.4절](02.md) 표에서 확인한 *E. coli* core 모델의 수치와 정확히 일치합니다.

**자주 나는 오류와 해결**

- `NameError: name 'model' is not defined`: 단계 1을 실행하지 않았기 때문입니다. 앞 단계를 먼저 실행합니다.
- `NameError: name 'np' is not defined`: 이 셀 안에서 `import numpy as np`가 실행되었는지 확인합니다. 이 블록은 그 import를 포함하고 있으므로 블록 전체를 실행합니다.

### 단계 4. rank로 영공간·왼쪽 영공간 차원 계산하기

같은 $$\mathbf S$$에서 [rank](../glossary.md)(계수) $$r$$를 구해, 영공간 차원 $$n-r$$과 왼쪽 영공간 차원 $$m-r$$을 계산합니다. 이 단계는 [4.4절](04.md)의 "$$n-m$$과 $$n-r$$은 다르다"는 논의를 실제 숫자로 확인하는 검산입니다. $$m-r$$은 수학적 왼쪽 영공간의 차원이며, 물리적으로 해석 가능한 보존 모이어티(conserved moiety) 수와 자동으로 같지는 않습니다.

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

**예상 출력**

```
m = 72, n = 95, rank(S) = r = 67
naive 자유도 (n - m): 23
실제 영공간 차원  (n - r): 28
왼쪽 영공간 차원 (m - r): 5
```

**확인 포인트**: `rank(S) = r = 67`, `n - r = 28`, `m - r = 5`로 나오면 성공입니다. $$n-r=28$$이 단순한 $$n-m=23$$보다 크다는 것은 $$\mathbf S$$의 행이 선형 독립이 아님을 뜻합니다.

{% hint style="warning" %}
**해석상의 주의**: 물리적으로 해석 가능한 보존 pool을 식별하려면 왼쪽 영공간 벡터의 비음수성, 원자 조성, biomass·exchange·분해 반응을 추가로 검토해야 합니다. $$m-r=5$$라는 숫자 자체가 곧 "보존 모이어티 5개"를 뜻하지는 않습니다.
{% endhint %}

**자주 나는 오류와 해결**

- `NameError: name 'S' is not defined`: 단계 3을 실행하지 않은 경우입니다. $$\mathbf S$$를 먼저 만든 뒤 이 셀을 실행합니다.
- rank 값이 67이 아닌 경우: COBRApy·numpy 버전이 준비물에 명시한 버전과 다를 수 있습니다. 수치 rank는 허용오차에 민감하므로 [Chapter 11 §1](../chapter-11/01.md)의 버전을 사용합니다.

### 단계 5. 닫힌 장난감 네트워크의 dx/dt 계산하기

큰 모델에서 눈을 돌려, 손으로 확인할 수 있는 아주 작은 네트워크로 $$\mathbf S\mathbf v$$의 의미를 검산합니다. [2.3절](02.md)의 닫힌(closed) 장난감 네트워크(반응 3개, 대사물 A·B·C)에서 모든 flux를 $$v_1=v_2=v_3=1$$로 두었을 때, 각 대사물의 순생성률 $$d\mathbf x/dt=\mathbf S\mathbf v$$를 계산합니다.

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

**예상 출력**

```
dx/dt = [-2  0  2]
```

**확인 포인트**: 출력이 `dx/dt = [-2  0  2]`이면 성공입니다. A는 두 반응에서 소비되어 $$-2$$, B는 생성과 소비가 상쇄되어 $$0$$, C는 두 반응에서 생성되어 $$+2$$가 됩니다. B의 값이 0이라는 것은 이 flux 조합에서 B만 순축적이 없다는 뜻입니다.

**자주 나는 오류와 해결**

- `@`(행렬 곱) 자리에 `*`를 쓰면 원소별 곱이 되어 다른 결과가 나옵니다. 행렬-벡터 곱에는 `@`를 사용합니다.

### 단계 6. 열린 장난감 네트워크의 정상상태 검산하기

이번에는 교환 반응 $$R_0,R_4$$가 추가된 열린(open) 네트워크에서, 특정 flux 벡터가 정상상태 제약 $$\mathbf S\mathbf v=0$$을 만족하는지 확인합니다([4.3절](04.md)). $$v_1=3$$, $$v_3=5$$이고 물질수지가 강제하는 $$(v_0,v_2,v_4)=(8,3,8)$$을 대입합니다.

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

**예상 출력**

```
S_open @ v_open = [0 0 0]
```

**확인 포인트**: 출력이 `[0 0 0]`이면 해당 flux vector가 이 toy network의 정상상태 제약을 만족한다는 뜻이며, 성공입니다. 세 대사물 모두 순생성률이 0이 되어야 정상상태입니다.

**자주 나는 오류와 해결**

- `v_open`의 순서가 헷갈릴 수 있습니다. 열 순서는 $$(R_0,R_1,R_2,R_3,R_4)$$이므로 `v_open`의 성분도 같은 순서 $$(v_0,v_1,v_2,v_3,v_4)$$로 입력합니다.

### 단계 7. scipy로 영공간·왼쪽 영공간 기저 구하기

마지막으로 단계 4에서 구한 **차원**뿐 아니라 실제 **기저 벡터**까지 `scipy`로 계산해, 그 개수가 앞서 구한 $$n-r$$·$$m-r$$과 일치하는지 확인합니다([4.5절](04.md)). `null_space(S)`는 $$\mathbf S\mathbf v=0$$을 만족하는 벡터들의 기저를, `null_space(S.T)`는 왼쪽 영공간의 기저를 열로 반환합니다.

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

**예상 출력**

```
영공간 기저 벡터 개수 (n - r): 28
왼쪽 영공간 기저 벡터 개수 (m - r): 5
```

**확인 포인트**: 영공간 기저 개수가 `28`, 왼쪽 영공간 기저 개수가 `5`로 나오면 성공입니다. 이 두 값은 단계 4에서 rank로 구한 $$n-r=28$$, $$m-r=5$$와 각각 정확히 일치해야 합니다.

{% hint style="warning" %}
**해석상의 주의**: 수치적 [영공간](../glossary.md) 기저(numerical null-space basis)는 유일하지 않습니다. 기저 벡터 하나를 독립적인 생물학적 pathway나 보존 pool로 해석해서는 안 됩니다.
{% endhint %}

**자주 나는 오류와 해결**

- `ModuleNotFoundError: No module named 'scipy'`: 가상환경에 `scipy`가 없는 경우입니다. [설치 가이드](../installation.md)의 환경을 사용하거나 `python -m pip install scipy`로 설치합니다.
- `NameError: name 'S' is not defined`: 단계 3에서 만든 $$\mathbf S$$가 필요합니다. 앞 단계를 먼저 실행합니다.

## 정리

이 실습에서는 다음을 직접 확인했습니다.

- COBRApy `textbook` 모델을 불러와 반응 95개·대사물 72개·유전자 137개를 확인했습니다.
- PGI 반응 객체에서 화학량론 계수(`g6p_c: -1`, `f6p_c: +1`)와 flux bound를 읽었고, 이것이 $$\mathbf S$$의 한 열임을 확인했습니다.
- 모델 전체의 $$\mathbf S$$를 꺼내 크기 `(72, 95)`, 비영 원소 360개, 채움 비율 5.26%를 계산했습니다.
- rank $$r=67$$에서 영공간 차원 $$n-r=28$$, 왼쪽 영공간 차원 $$m-r=5$$를 구하고, 단순한 $$n-m=23$$과 다름을 확인했습니다.
- 두 장난감 네트워크로 $$\mathbf S\mathbf v$$를 계산해 정상상태 제약을 손으로 검산하고, `scipy`로 구한 기저 개수가 차원과 일치함을 확인했습니다.

## 스스로 해보기

1. 단계 2에서 `"PGI"` 대신 다른 반응 ID(예: `"PFK"`, `"PYK"`)를 넣어 화학량론 열과 bound를 조회해 봅니다. 이어서 교환 반응 `"EX_glc__D_e"`를 조회하면 열에 계수가 몇 개 나타나는지 확인하고, 그 이유를 [2.5절](02.md)과 연결해 생각해 봅니다.
2. 단계 5의 닫힌 네트워크에서 통량을 `v = np.array([2, 2, 2])`로 바꾸면 `dx/dt`가 어떻게 변할지 먼저 예측한 뒤, 실행해 예측과 비교해 봅니다.
3. 단계 6의 `v_open`에서 한 성분만 1만큼 바꾸면 `S_open @ v_open`이 더 이상 `[0 0 0]`이 아님을 확인하고, 정상상태를 회복하려면 어떤 성분들을 함께 조정해야 하는지 물질수지 식으로 따져 봅니다.

다음 단계로는 여기서 확인한 $$\mathbf S$$와 정상상태 제약 위에서 목적함수를 최적화하는 [FBA](../chapter-4/README.md)를 [Chapter 4](../chapter-4/README.md)에서 다룹니다. 영공간·왼쪽 영공간의 개념적 배경은 [4.5절](04.md)과 [4.6절](04.md)에서 더 볼 수 있습니다.

---
