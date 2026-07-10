# 💡 실습: COBRApy로 FBA · FVA · pFBA 수행하기

> 아래 스니펫들은 핵심 흐름만 보여줍니다. 전체 실행 가능한 예제(모델 불러오기부터 그림자 가격 시각화, 혐기 조건 비교, 연습 문제까지)는 `gem9_w03_lab.ipynb` 노트북을 참고하세요. 이 실습은 [Chapter 1](../chapter-1/README.md)~[Chapter 3](../chapter-3/README.md)에서 계속 사용해 온 `e_coli_core`를 그대로 이어서 사용합니다.

**1) 기본 FBA 실행**

```python
import cobra
from cobra.io import load_model

model = load_model("textbook")
solution = model.optimize()
print(f"{solution.status}, μ = {solution.objective_value:.4f} h^-1")
# optimal, μ = 0.8739 h^-1
```

**2) 목적 함수를 바꿔 부산물 최대화 확인**

```python
with model:
    model.objective = model.reactions.EX_ac_e   # 아세테이트 분비 최대화
    ac_solution = model.optimize()
    print(f"최대 아세테이트 분비율: {ac_solution.objective_value:.2f} mmol/gDW/h")
```

**3) 호기 vs 혐기 비교**

```python
with model:
    model.reactions.EX_o2_e.lower_bound = 0
    anaerobic = model.optimize()
    print(f"혐기 성장률: {anaerobic.objective_value:.4f} h^-1  (호기 대비 크게 감소)")
```

**4) FVA로 반응 유연성 진단**

```python
from cobra.flux_analysis import flux_variability_analysis

fva = flux_variability_analysis(model, fraction_of_optimum=0.9, processes=1)
fva['range'] = fva['maximum'] - fva['minimum']
print(fva.sort_values('range', ascending=False).head(5))
```

**5) pFBA 대표 해와 물질수지 쌍대값 확인**

```python
from cobra.flux_analysis import pfba

pfba_solution = pfba(model)
print(f"pFBA 총 |flux| 합: {pfba_solution.fluxes.abs().sum():.1f}")

largest_duals = solution.shadow_prices.abs().sort_values(ascending=False).head(5)
print(solution.shadow_prices[largest_duals.index])
# 부호만으로 제한 영양소를 판정하지 말고 §5.2처럼 exchange bound 민감도를 확인한다.
```

**6) 3~5절에서 손으로 푼 토이 LP를 `scipy.optimize.linprog`로 검증**

이 장 전체에서 반복해서 손으로 풀었던 3.1절의 장난감 LP($$\max\ 0.5v_1+0.8v_2$$)를 코드로도 풀어, 3.3절의 답 $$(2,8)$$·4.4절의 심플렉스 경로·5.6절의 쌍대값이 모두 일관됨을 확인합니다. `linprog`는 기본적으로 **최소화** 문제를 풀므로 목적 함수의 부호를 뒤집어 넣습니다.

```python
from scipy.optimize import linprog

# max 0.5 v1 + 0.8 v2  ==  min -0.5 v1 - 0.8 v2
c = [-0.5, -0.8]
A_ub = [[1, 1], [1, 0], [0, 1]]   # v1+v2<=10, v1<=6, v2<=8
b_ub = [10, 6, 8]
bounds = [(0, None), (0, None)]

result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
print(f"v1*={result.x[0]:.4f}, v2*={result.x[1]:.4f}, Z*={-result.fun:.4f}")
# 기대 출력: v1*=2.0000, v2*=8.0000, Z*=7.4000  (3.3절의 손 계산과 정확히 일치)

# highs 솔버는 부등식 제약의 쌍대값(shadow price)도 함께 보고한다.
print("쌍대값(y1, y2, y3):", -result.ineqlin.marginals)
# 기대 출력에 가까운 값: [0.5, 0.0, 0.3]  (5.6절에서 상보 여유성으로 손 계산한 값과 일치)
```

**7) 성장률 강건성 곡선 그리기 (5.4절)**

```python
import numpy as np
import matplotlib.pyplot as plt

o2_range = np.linspace(0, 25, 26)
mu = []
with model:
    model.reactions.EX_glc__D_e.lower_bound = -10   # 포도당은 충분히 공급
    for o2 in o2_range:
        with model:
            model.reactions.EX_o2_e.lower_bound = -o2
            mu.append(model.slim_optimize(error_value=0.0))

plt.plot(o2_range, mu, marker="o")
plt.xlabel("산소 흡수 상한 (mmol/gDW/h)")
plt.ylabel("성장률 μ (h$^{-1}$)")
plt.title("산소 강건성 곡선 — e_coli_core")
# 산소가 부족한 구간에서는 μ가 급격히 증가하다가, 어느 지점 이후로는
# 포도당 10이 병목이 되어 증가폭이 완만해지는 5.4절의 곡선 형태를 재현한다.
```

**연습 문제**

1. 6)번 코드에서 포도당 상한을 3.6절처럼 $$14$$로 바꾸면(`A_ub`의 첫 번째 원소를 14로), `linprog`가 반환하는 $$(v_1^*,v_2^*)$$와 쌍대값이 3.6절의 손 계산과 일치하는지 확인하라.
2. 7)번 코드를 응용해, 이번에는 산소는 고정하고(`EX_o2_e.lower_bound = -20`) 포도당 흡수 상한을 0~20까지 스캔하는 강건성 곡선을 그려 5.4절 그림 4.2와 비교하라.

---
