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

---
