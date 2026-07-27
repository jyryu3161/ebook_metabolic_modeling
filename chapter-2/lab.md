# 실습: COBRApy로 반응·대사물·화학량론 행렬 검사하기

이 실습은 [COBRApy](https://opencobra.github.io/cobrapy/) `textbook` 모델에서 reaction·metabolite 객체와 화학량론 행렬 $$\mathbf S$$를 조회하고, 대사물별 생성·소비가 맞는지 검산합니다. 전체 notebook은 `raw_data/GEM_lecture_notes/gem9_w02_lab.ipynb`와 `gem9_w03_lab.ipynb`에 있습니다.

## 이 실습에서 하는 일

COBRApy에 내장된 *E. coli* core 모델(`textbook`)을 불러와, 이 장에서 배운 개념이 실제 코드에서 어떻게 나타나는지 직접 확인합니다. 반응 하나의 화학량론 계수를 읽는 것에서 시작해, 모델 전체의 $$\mathbf S$$ 행렬을 꺼내고, 마지막에는 작은 장난감(toy) 네트워크로 정상상태 제약 $$\mathbf S\mathbf v=0$$을 손으로 검산합니다.

## 학습 목표

이 실습을 마치면 다음을 수행할 수 있습니다.

1. COBRApy `textbook` 모델을 불러와 반응·대사물·유전자 수를 확인합니다.
2. 개별 반응 객체에서 화학량론 계수와 플럭스 bound를 조회합니다.
3. 화학량론 행렬 $$\mathbf S$$를 numpy 배열로 꺼내 크기와 0이 아닌 계수의 비율을 계산합니다.
4. 장난감 네트워크에서 대사물별 생성 기여와 소비 기여를 계산합니다.
5. $$\mathbf S\mathbf v$$의 각 성분이 0인지 확인하여 의사-정상상태 물질수지를 검산합니다.

## 준비물

- **실행 환경**: 이 실습은 파이썬으로 진행합니다. [Chapter 11 §1](../chapter-11/01.md)의 격리된 가상환경(`.venv-gem`)을 그대로 사용하거나, [설치 가이드](../installation.md)를 따라 환경을 먼저 준비합니다.
- **필요한 패키지**: `cobra==0.30.0`(모델 조회)와 `numpy`(표 계산)를 사용합니다. 두 패키지는 위 가상환경에 이미 포함되어 있습니다.
- **모델**: COBRApy에 내장된 `textbook` 예제(모델 ID는 `e_coli_core`)를 사용합니다. 별도의 파일을 내려받을 필요 없이 `load_model("textbook")`로 불러옵니다.
- **선행 셀**: 단계 3 이후는 앞 단계에서 만든 변수(`model`, `S`)를 재사용합니다. 노트북을 위에서 아래로 순서대로 실행합니다.

이 장의 모든 숫자는 위 버전 조합에서 얻은 값입니다. 버전이나 모델 파일이 다르면 객체 수와 행렬의 0이 아닌 계수 수가 달라질 수 있습니다.

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

**확인 포인트**: 기록한 환경에서 모델 ID와 세 객체 수를 출력으로 확인합니다. 대사물 수와 반응 수는 이어서 만든 $$\mathbf S$$ 행렬의 행·열 개수와 같아야 합니다. 수치가 다르면 패키지 버전, 모델 파일, 로더와 집계 규약을 기록한 뒤 다음 단계의 예시 출력값을 그대로 사용하지 않습니다.

**자주 나는 오류와 해결**

- `ModuleNotFoundError: No module named 'cobra'`: 가상환경이 활성화되지 않았거나 COBRApy가 설치되지 않은 경우입니다. [Chapter 11 §1](../chapter-11/01.md)의 `source .venv-gem/bin/activate`로 환경을 켠 뒤 다시 실행합니다.
- 모델 다운로드를 시도하며 멈추는 경우: `"textbook"`은 내장 모델이므로 네트워크가 필요 없습니다. 철자를 그대로(`textbook`) 입력했는지 확인합니다.

### 단계 2. PGI 반응 객체에서 화학량론 열 읽기

다음으로 반응 하나를 골라 그 안을 들여다봅니다. 대표로 PGI(glucose-6-phosphate isomerase) 반응을 조회합니다. 여기서 [플럭스](../glossary.md)(flux)는 반응 $$j$$의 진행 속도이며, 이 교재의 COBRApy 예제에서는 단위가 $$\mathrm{mmol\,gDW^{-1}\,h^{-1}}$$인 값입니다. `lower_bound`와 `upper_bound`는 이 플럭스가 움직일 수 있는 범위(하한·상한)를 뜻합니다. 반응 객체의 화학량론 개념은 [1.2절](01.md), 이 값이 $$\mathbf S$$의 한 열이 되는 원리는 [2.2절](02.md)에서 설명합니다.

```python
# 개별 반응 객체의 화학량론 조회 (대표 반응 PGI: G6P <=> F6P)
rxn = model.reactions.get_by_id("PGI")
print(rxn.name)
print(rxn.reaction)                       # 화학량론식 문자열
print(rxn.lower_bound, rxn.upper_bound)   # 플럭스 하한/상한
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

### 단계 3. 화학량론 행렬 S의 크기와 채움 비율 확인하기

이제 반응 하나가 아니라 모델 **전체**의 [화학량론 행렬](../glossary.md) $$\mathbf S$$를 numpy 배열로 꺼냅니다. `create_stoichiometric_matrix`는 각 열이 하나의 반응, 각 행이 하나의 대사물인 $$m\times n$$ 행렬을 만들어 줍니다. 대부분의 반응은 소수의 대사물만 포함하므로, 이 행렬은 0이 많은 희소(sparse) 행렬입니다([2.4절](02.md)).

```python
from cobra.util.array import create_stoichiometric_matrix
import numpy as np

S = create_stoichiometric_matrix(model, array_type="dense")

print("S matrix shape (m x n):", S.shape)
print("Nonzero entries:", np.count_nonzero(S))
print(f"Nonzero ratio: {np.count_nonzero(S) / S.size:.2%}")

# 기대 출력:
# S matrix shape (m x n): (72, 95)
# Nonzero entries: 360
# Nonzero ratio: 5.26%
```

**예상 출력**

```
S matrix shape (m x n): (72, 95)
Nonzero entries: 360
Nonzero ratio: 5.26%
```

**확인 포인트**: `S.shape`, 비영 원소 수, 채움 비율을 함께 기록합니다. 이 값들은 단계 1의 실제 대사물·반응 수와 일관되어야 하며, 고정한 환경의 예시 출력 `(72, 95)`, 360, `5.26%`와 다르면 버전·모델 파일·추출 규약을 먼저 확인합니다.

`S.shape`가 `(72, 95)`로 나온다는 것은 곧 $$m=72$$, $$n=95$$라는 뜻이며, 이는 [2.4절](02.md) 표에서 확인한 *E. coli* core 모델의 수치와 정확히 일치합니다.

**자주 나는 오류와 해결**

- `NameError: name 'model' is not defined`: 단계 1을 실행하지 않았기 때문입니다. 앞 단계를 먼저 실행합니다.
- `NameError: name 'np' is not defined`: 이 셀 안에서 `import numpy as np`가 실행되었는지 확인합니다. 이 블록은 그 import를 포함하고 있으므로 블록 전체를 실행합니다.

### 단계 4. 닫힌 장난감 네트워크의 순생성률 계산하기

큰 모델에서 눈을 돌려, 손으로 확인할 수 있는 작은 네트워크로 $$\mathbf S\mathbf v$$의 의미를 검산합니다. [2.3절](02.md)의 닫힌 장난감 네트워크(반응 3개, 대사물 A·B·C)에서 모든 플럭스를 $$v_1=v_2=v_3=1$$로 두고, 각 대사물의 생성 기여와 소비 기여를 더합니다.

```python
import numpy as np

# 2.3절 닫힌 장난감 네트워크: 행=[A,B,C], 열=[R1,R2,R3]
S_closed = np.array([
    [-1,  0, -1],
    [ 1, -1,  0],
    [ 0,  1,  1],
])

v = np.array([1, 1, 1])          # 열 순서 [R1, R2, R3]의 임의 플럭스
dxdt = S_closed @ v
for metabolite, net_rate in zip(["A", "B", "C"], dxdt):
    print(f"{metabolite} 순생성률: {net_rate:+d}")

# 기대 출력:
# A 순생성률: -2
# B 순생성률: +0
# C 순생성률: +2
```

**예상 출력**

```
A 순생성률: -2
B 순생성률: +0
C 순생성률: +2
```

**확인 포인트**: A는 두 반응에서 소비되어 $$-2$$, B는 생성과 소비가 상쇄되어 $$0$$, C는 두 반응에서 생성되어 $$+2$$가 됩니다. B의 값이 0이라는 것은 이 플럭스 조합에서 B만 생성과 소비가 맞는다는 뜻입니다. 세 대사물 모두 0이어야 전체 네트워크가 의사-정상상태 제약을 만족합니다.

**자주 나는 오류와 해결**

- `@`(행렬 곱) 자리에 `*`를 쓰면 원소별 곱이 되어 다른 결과가 나옵니다. 행렬-벡터 곱에는 `@`를 사용합니다.

### 단계 5. 열린 장난감 네트워크의 정상상태 검산하기

이번에는 교환 반응 $$R_0,R_4$$가 추가된 열린(open) 네트워크에서, 특정 플럭스 벡터가 정상상태 제약 $$\mathbf S\mathbf v=0$$을 만족하는지 확인합니다([4.3절](04.md)). $$v_1=3$$, $$v_3=5$$이고 물질수지가 강제하는 $$(v_0,v_2,v_4)=(8,3,8)$$을 대입합니다.

```python
# 4.3절 열린 네트워크: 열 순서 = [R0, R1, R2, R3, R4]
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

**확인 포인트**: 출력이 `[0 0 0]`이면 해당 플럭스 벡터가 이 toy network의 정상상태 제약을 만족한다는 뜻이며, 성공입니다. 세 대사물 모두 순생성률이 0이 되어야 정상상태입니다.

**자주 나는 오류와 해결**

- `v_open`의 순서가 헷갈릴 수 있습니다. 열 순서는 $$(R_0,R_1,R_2,R_3,R_4)$$이므로 `v_open`의 성분도 같은 순서 $$(v_0,v_1,v_2,v_3,v_4)$$로 입력합니다.

## 정리

이 실습에서는 다음을 직접 확인했습니다.

- COBRApy `textbook` 모델을 불러와 반응 95개·대사물 72개·유전자 137개를 확인했습니다.
- PGI 반응 객체에서 화학량론 계수(`g6p_c: -1`, `f6p_c: +1`)와 플럭스 bound를 읽었고, 이것이 $$\mathbf S$$의 한 열임을 확인했습니다.
- 모델 전체의 $$\mathbf S$$를 꺼내 크기 `(72, 95)`, 비영 원소 360개, 채움 비율 5.26%를 계산했습니다.
- 닫힌 장난감 네트워크에서 대사물별 순생성률을 계산해 어떤 행에서 생성과 소비가 맞지 않는지 확인했습니다.
- 열린 장난감 네트워크에서 세 대사물의 생성·소비가 모두 맞아 $$\mathbf S\mathbf v=\mathbf0$$이 되는 플럭스 조합을 검산했습니다.

## 스스로 해보기

1. 단계 2에서 `"PGI"` 대신 다른 반응 ID(예: `"PFK"`, `"PYK"`)를 넣어 화학량론 열과 bound를 조회해 봅니다. 이어서 교환 반응 `"EX_glc__D_e"`를 조회하면 열에 계수가 몇 개 나타나는지 확인하고, 그 이유를 [2.5절](02.md)과 연결해 생각해 봅니다.
2. 단계 4의 닫힌 네트워크에서 플럭스를 `v = np.array([2, 2, 2])`로 바꾸면 각 대사물의 순생성률이 어떻게 변할지 먼저 예측한 뒤, 실행해 비교해 봅니다.
3. 단계 5의 `v_open`에서 한 성분만 1만큼 바꾸면 `S_open @ v_open`이 더 이상 `[0 0 0]`이 아님을 확인하고, 어느 대사물의 생성·소비가 맞지 않는지 행별로 설명해 봅니다.

다음 단계로는 여기서 확인한 $$\mathbf S$$와 정상상태 제약 위에서 목적함수를 최적화하는 [FBA](../chapter-4/README.md)를 [Chapter 4](../chapter-4/README.md)에서 다룹니다. 물질수지의 적용 범위와 검산 순서는 [4.5절](04.md)과 [4.6절](04.md)에서 다시 확인할 수 있습니다.

---
