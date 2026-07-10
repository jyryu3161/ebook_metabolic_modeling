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

---
