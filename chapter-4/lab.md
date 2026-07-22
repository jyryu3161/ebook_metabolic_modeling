# 실습: COBRApy로 FBA · FVA · pFBA 수행하기

> 아래 스니펫들은 핵심 흐름만 보여줍니다. 전체 실행 가능한 예제(모델 불러오기부터 [그림자 가격](../glossary.md) 시각화, 혐기 조건 비교, 연습 문제까지)는 `raw_data/GEM_lecture_notes/gem9_w03_lab.ipynb` 노트북을 참고하세요. 이 실습은 [Chapter 1](../chapter-1/README.md)~[Chapter 3](../chapter-3/README.md)에서 계속 사용해 온 [`e_coli_core`](http://bigg.ucsd.edu/models/e_coli_core)를 그대로 이어서 사용합니다.

## 이 실습에서 하는 일

앞 절들에서 손으로 풀었던 [Flux Balance Analysis](../landmark-papers.md)(FBA, 플럭스 균형 분석)를 이번에는 [COBRApy](https://opencobra.github.io/cobrapy/)로 직접 실행합니다. 대장균 코어 모델 `e_coli_core`의 성장률을 계산하고, 목적 함수와 배지 조건을 바꿔 결과가 어떻게 달라지는지 관찰합니다. 마지막으로 3~5절에서 손으로 푼 장난감 LP를 코드로 다시 풀어, 손 계산과 컴퓨터 계산이 같은 답을 내는지 확인합니다.

여기서 **플럭스(flux)**는 단위 시간당 반응이 진행하는 속도이며, 단위는 `mmol gDW⁻¹ h⁻¹`(건조 세포량 1그램이 1시간 동안 처리하는 밀리몰 수)입니다. 성장률 μ의 단위는 `h⁻¹`입니다.

## 학습 목표

이 실습을 마치면 다음을 할 수 있습니다.

1. COBRApy로 `e_coli_core`를 불러와 기본 FBA를 **실행**하고 성장률을 확인한다.
2. 목적 함수를 바이오매스에서 부산물 분비로 **바꾸어** 최적값이 달라지는 것을 관찰한다.
3. 호기와 혐기 조건의 성장률을 **비교**하고 그 차이를 해석한다.
4. FVA와 pFBA를 **실행**하여 반응의 유연성과 대표 해를 진단한다.
5. 손으로 푼 장난감 LP를 `scipy.optimize.linprog`로 **검증**하고 쌍대값이 일치함을 확인한다.

## 준비물

- **실행 환경**: Python과 COBRApy가 설치된 가상환경. 아직 준비하지 않았다면 [Chapter 11의 1절](../chapter-11/01.md) 또는 [설치 가이드](../installation.md)를 먼저 따라 환경과 솔버(solver)를 갖추십시오. 솔버는 LP 문제를 실제로 푸는 계산 엔진으로, COBRApy 설치 시 함께 들어오는 GLPK로도 이 실습을 모두 실행할 수 있습니다.
- **필요한 패키지**: `cobra`(COBRApy), `scipy`, `numpy`, `matplotlib`. 이 중 하나라도 없으면 아래 각 단계의 "자주 나는 오류" 안내를 참고해 설치합니다.
- **모델**: `e_coli_core`(BiGG의 `textbook` 모델). 별도로 파일을 내려받을 필요 없이 `load_model("textbook")` 한 줄이 자동으로 불러옵니다.
- **선행 지식**: 이 장 3~5절과 8~9절의 손 계산. 코드가 재현하는 숫자들이 그 절들에서 나온 값과 같기 때문에, 해당 절을 먼저 읽어 두면 각 출력의 의미가 분명해집니다.

{% hint style="info" %}
아래 단계는 **위에서부터 순서대로** 실행해야 합니다. 특히 단계 1에서 만든 `model`과 `solution` 변수를 뒤 단계들이 계속 사용하므로, 새 세션을 시작했다면 단계 1부터 다시 실행하십시오.
{% endhint %}

---

## 실습 단계별 따라 하기

### 단계 1. 모델을 불러오고 기본 FBA로 성장률 계산하기

**무엇을·왜.** 먼저 `e_coli_core` 모델을 메모리에 불러오고, `model.optimize()`로 FBA를 한 번 실행합니다. FBA는 물질수지 $$\mathbf{S}\mathbf{v}=\mathbf{0}$$과 플럭스 범위를 만족하는 무한히 많은 해 중에서 목적 함수(기본값은 바이오매스 = 성장률)를 최대화하는 해 하나를 골라 줍니다. 실행 원리는 [6절](06.md)에서 자세히 다룹니다.

```python
import cobra
from cobra.io import load_model

model = load_model("textbook")
solution = model.optimize()
print(f"{solution.status}, μ = {solution.objective_value:.4f} h^-1")
# optimal, μ = 0.8739 h^-1
```

**예상 출력.**

```
optimal, μ = 0.8739 h^-1
```

**확인 포인트.** 출력의 상태가 `optimal`이면 솔버가 최적해를 찾았다는 뜻이며 성공입니다. 성장률 μ가 약 `0.8739`이면 정상입니다. 이 값은 `textbook` 모델의 기본 배지·bounds와 바이오매스 목적함수를 이 solver로 풀었을 때의 계산값이며, 실험 성장률과 비교하려면 균주·배지·산소·유지에너지·측정 방법을 맞춘 별도 benchmark가 필요합니다([6.2절](06.md)). `optimal`은 어디까지나 "주어진 허용오차 안에서 최적해를 찾았다"는 솔버 상태이며, 생물학적 가설이 검증되었다는 뜻은 아닙니다.

**자주 나는 오류와 해결.**
- `ModuleNotFoundError: No module named 'cobra'` — COBRApy가 설치되지 않았습니다. 가상환경을 활성화한 뒤 `pip install cobra`로 설치합니다.
- 모델 다운로드 관련 오류가 난다면, `load_model("textbook")`이 처음 호출될 때 모델을 내려받으므로 네트워크 연결을 확인합니다.
- 뒤 단계에서 `NameError: name 'model' is not defined`가 보이면 모델을 만드는 셀이 실행되었는지 확인합니다. 노트북을 처음부터 순서대로 실행하거나 필요한 초기화 셀을 다시 실행합니다.

### 단계 2. 목적 함수를 바꿔 부산물 분비 최대화하기

**무엇을·왜.** 목적 함수는 생물학적 사실이 아니라 사용자가 정하는 계산 설정입니다([7절](07.md)). 이 단계에서는 목적 함수를 성장(바이오매스)에서 아세테이트 분비(`EX_ac_e`)로 바꾸어, 같은 모델이라도 무엇을 최대화하느냐에 따라 답이 달라진다는 것을 확인합니다. `with model:` 블록은 그 안에서 바꾼 설정을 블록을 벗어날 때 자동으로 되돌려 주므로, 원래 목적 함수(바이오매스)가 안전하게 복원됩니다.

```python
with model:
    model.objective = model.reactions.EX_ac_e   # 아세테이트 분비 최대화
    ac_solution = model.optimize()
    print(f"최대 아세테이트 분비율: {ac_solution.objective_value:.2f} mmol/gDW/h")
```

**예상 출력.** `최대 아세테이트 분비율:` 뒤에 양의 값이 `mmol/gDW/h` 단위로 출력됩니다. 이 값은 "세포가 성장을 포기하고 아세테이트만 최대로 내보낼 때"의 분비율이므로, 성장을 최대화한 단계 1과는 전혀 다른 플럭스 분포에서 얻어집니다.

**확인 포인트.** 오류 없이 양의 분비율 하나가 출력되면 성공입니다. 블록을 벗어난 뒤 `model.optimize().objective_value`를 다시 확인하면 단계 1의 성장률(약 `0.8739`)로 돌아와 있어야 합니다 — 이것이 `with model:` 블록이 설정을 되돌렸다는 증거입니다.

**자주 나는 오류와 해결.**
- `model`이 정의되지 않았다는 오류는 단계 1을 실행하지 않은 것입니다.
- 들여쓰기(indent)를 빠뜨리면 `IndentationError`가 납니다. `with model:` 아래 세 줄은 모두 같은 깊이로 들여써야 합니다.

### 단계 3. 호기와 혐기 조건 비교하기

**무엇을·왜.** 배지 조건을 바꾸면 표현형도 바뀝니다. 산소 흡수 반응의 하한을 0으로 두면(`EX_o2_e.lower_bound = 0`) 세포는 산소를 전혀 쓸 수 없는 혐기(anaerobic) 조건이 됩니다. 산소 없이는 ATP 생성 효율이 크게 떨어지므로 성장률도 크게 감소합니다. 흡수 반응의 하한이 음수인 이유와 배지 설정은 [6.4절](06.md)에서 설명합니다.

```python
with model:
    model.reactions.EX_o2_e.lower_bound = 0
    anaerobic = model.optimize()
    print(f"혐기 성장률: {anaerobic.objective_value:.4f} h^-1  (호기 대비 크게 감소)")
```

**예상 출력.** 혐기 성장률이 출력됩니다. [6.4절](06.md)에서 설명하듯 이 값은 호기 성장률(약 `0.8739`)의 1/3~1/4 수준, 즉 약 `0.2 h⁻¹` 부근으로 크게 감소합니다.

**확인 포인트.** 혐기 성장률이 단계 1의 호기 성장률보다 뚜렷하게 작으면 성공입니다. 성장률이 0이거나 음수, 혹은 `nan`이 나온다면 배지 설정이 잘못된 것이므로 산소 이외의 다른 흡수 반응을 건드리지 않았는지 확인합니다.

**자주 나는 오류와 해결.**
- 반응 ID를 `EX_O2_e`(대문자 O)로 잘못 쓰면 `KeyError`가 납니다. 정확한 ID는 소문자 `EX_o2_e`입니다.

### 단계 4. FVA로 반응 유연성 진단하기

**무엇을·왜.** FBA는 최적해 하나만 돌려주지만, 같은 최적 성장률을 내는 플럭스 분포는 여러 개일 수 있습니다([3.4절](03.md)). **FVA(Flux Variability Analysis, 플럭스 가변성 분석)**는 각 반응이 최적값의 일정 비율 이상을 유지하는 조건에서 가질 수 있는 최솟값과 최댓값을 계산해, 이 비유일성을 정량화합니다([9절](09.md)). `fraction_of_optimum=0.9`는 최적 성장률의 90%까지 허용한다는 뜻이고, `processes=1`은 병렬 없이 한 프로세스로 실행한다는 뜻입니다.

```python
from cobra.flux_analysis import flux_variability_analysis

fva = flux_variability_analysis(model, fraction_of_optimum=0.9, processes=1)
fva['range'] = fva['maximum'] - fva['minimum']
print(fva.sort_values('range', ascending=False).head(5))
```

**예상 출력.** 반응별 `minimum`, `maximum`, 그리고 방금 추가한 `range`(= 최댓값 − 최솟값) 열을 가진 표가 출력됩니다. `range`가 큰 순으로 상위 5개 반응이 나오며, `PGI` 같은 유연한 반응이 위쪽에 나타납니다. 참고로 [9.1절](09.md)의 예시에서 `EX_glc__D_e`의 구간은 `[-10.0000, -9.0466]`, `PGI`의 구간은 `[-14.2990, 9.8388]`입니다.

**확인 포인트.** `minimum`, `maximum`, `range` 세 열을 가진 표가 오류 없이 출력되고, 상위 반응의 `range`가 0보다 크면 성공입니다. `range`가 큰 반응일수록 최적 성장을 유지하면서도 플럭스가 넓게 움직일 수 있는 "유연한" 반응입니다.

**자주 나는 오류와 해결.**
- FVA는 반응마다 최소·최대 두 번의 LP를 풀어 시간이 걸릴 수 있습니다. `e_coli_core`는 작아 수 초 안에 끝나지만, 멈춘 것처럼 보여도 기다립니다.
- 표가 잘려 보이면 `pandas`의 출력 폭 설정 때문이며 계산 자체는 정상입니다.

### 단계 5. pFBA 대표 해와 물질수지 그림자 가격 확인하기

**무엇을·왜.** **pFBA(Parsimonious FBA, 절약형 FBA)**는 최적 성장률을 유지하는 해 중 총 플럭스 합 $$\sum_j |v_j|$$이 최소인 해를 골라, 아무 이득 없이 도는 무익한 순환을 제거한 "대표 해"를 줍니다([8절](08.md)). 이어서 단계 1의 `solution`에 담긴 **그림자 가격(shadow price)** — 물질수지 제약을 한 단위 완화할 때 목적값이 얼마나 변하는지를 나타내는 민감도 — 중 절댓값이 큰 상위 5개를 살펴봅니다.

```python
from cobra.flux_analysis import pfba

pfba_solution = pfba(model)
print(f"pFBA 총 |flux| 합: {pfba_solution.fluxes.abs().sum():.1f}")

largest_duals = solution.shadow_prices.abs().sort_values(ascending=False).head(5)
print(solution.shadow_prices[largest_duals.index])
# 부호만으로 제한 영양소를 판정하지 말고 §5.2처럼 exchange bound 민감도를 확인한다.
```

**예상 출력.** 첫 줄의 pFBA 총 `|flux|` 합은 약 `518.4`입니다([8.2절](08.md)). 둘째 출력은 그림자 가격의 절댓값이 큰 상위 5개 대사물과 그 값(부호 포함)입니다.

**확인 포인트.** pFBA 총 `|flux|` 합이 약 `518.4`로 출력되고, 이어서 대사물 5개의 그림자 가격이 표시되면 성공입니다.

{% hint style="warning" %}
**해석상의 주의:** 그림자 가격의 **부호는 목적함수 방향·등식 작성 방향·솔버 관례**에 따라 달라지므로, "음수 = 제한 영양소"처럼 부호만으로 영양 제한을 판정하면 안 됩니다. 어떤 영양소가 성장을 제한하는지 알고 싶다면 [5.2절](05.md)처럼 해당 exchange 반응의 bound를 조금 바꿔 목적값의 변화를 직접 확인하십시오. 코드 마지막 줄의 주석이 바로 이 점을 상기시킵니다.
{% endhint %}

**자주 나는 오류와 해결.**
- `pfba`를 불러올 때 `ImportError`가 나면 COBRApy 버전이 오래된 것입니다. `pip install -U cobra`로 갱신합니다.
- `solution`이 정의되지 않았다는 오류는 단계 1을 건너뛴 것입니다. 그림자 가격은 단계 1에서 만든 `solution` 객체에서 읽습니다.

### 단계 6. 손으로 푼 토이 LP를 `scipy.optimize.linprog`로 검증하기

**무엇을·왜.** 이 장 전체에서 반복해서 손으로 풀었던 [3.1절](03.md)의 장난감 LP($$\max\ 0.5v_1+0.8v_2$$)를 코드로도 풀어, [3.3절](03.md)의 답 $$(2,8)$$·[4.4절](04.md)의 심플렉스 경로·[5.6절](05.md)의 쌍대값이 모두 일관됨을 확인합니다. [`scipy.optimize.linprog`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html)는 기본적으로 **최소화** 문제를 풀므로 목적 함수의 부호를 뒤집어 넣습니다.

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

**예상 출력.**

```
v1*=2.0000, v2*=8.0000, Z*=7.4000
쌍대값(y1, y2, y3): [0.5 0. 0.3]
```

**확인 포인트.** $$v_1^*=2,\ v_2^*=8,\ Z^*=7.4$$가 [3.3절](03.md)의 손 계산과 정확히 일치하고, 쌍대값이 $$(0.5,\ 0,\ 0.3)$$에 가까우면 성공입니다. 이 세 쌍대값은 [5.6절](05.md)에서 상보 여유성으로 유도한 $$y_1=0.5,\ y_2=0,\ y_3=0.3$$과 같습니다 — 손 계산, 심플렉스 타블로, 쌍대 LP, 그리고 이 코드가 모두 같은 값을 가리킵니다.

**자주 나는 오류와 해결.**
- `ModuleNotFoundError: No module named 'scipy'` — `pip install scipy`로 설치합니다.
- `AttributeError: ... 'ineqlin'`이 나면 SciPy 버전이 오래된 것입니다. 부등식 쌍대값(`ineqlin.marginals`)은 `method="highs"`와 비교적 최신 SciPy에서 제공되므로 `pip install -U scipy`로 갱신합니다.

### 단계 7. 성장률 강건성 곡선 그리기

**무엇을·왜.** 마지막으로 산소 흡수 상한을 0부터 25까지 조금씩 바꿔 가며 성장률이 어떻게 변하는지 곡선으로 그립니다([5.4절](05.md)). 포도당은 충분히 공급한 채(하한 −10) 산소만 바꾸므로, 산소가 부족한 구간과 포도당이 병목이 되는 구간의 기울기 차이를 눈으로 볼 수 있습니다. `slim_optimize`는 목적값만 빠르게 계산하는 함수이며, `error_value=0.0`은 실행 불가능한 경우 0을 반환하라는 뜻입니다.

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

**예상 출력.** 숫자 출력 대신 그래프 하나가 그려집니다. x축은 산소 흡수 상한, y축은 성장률 μ이며, 산소가 적은 구간에서는 μ가 가파르게 오르다가 어느 지점 이후로는 포도당 공급(10)이 병목이 되어 증가폭이 완만해지는 꺾인 곡선 모양이 나타납니다.

**확인 포인트.** 산소가 늘수록 성장률이 증가하다가 완만해지는 우상향 곡선이 그려지면 성공입니다. 시작점(산소 상한 0)에서 μ가 낮고 오른쪽으로 갈수록 높아지는 형태여야 합니다.

**자주 나는 오류와 해결.**
- `ModuleNotFoundError: No module named 'matplotlib'` — `pip install matplotlib`로 설치합니다.
- 스크립트(`.py`)로 실행했는데 창이 뜨지 않으면, 코드 끝에 `plt.show()`를 한 줄 추가합니다. Jupyter 노트북에서는 자동으로 그려집니다.

---

## 정리

이 실습에서 한 일을 되짚어 봅니다.

- `e_coli_core`를 불러와 기본 FBA를 실행하고, 호기 성장률 약 `0.8739 h⁻¹`을 확인했습니다(단계 1).
- 목적 함수를 부산물 분비로 바꾸고(단계 2), 산소를 차단해 혐기 성장률이 크게 감소하는 것을 관찰했습니다(단계 3).
- FVA로 반응별 플럭스 가변 범위를(단계 4), pFBA로 총 플럭스가 최소인 대표 해(약 `518.4`)와 그림자 가격을(단계 5) 진단했습니다.
- 손으로 푼 장난감 LP를 `linprog`로 풀어 최적해 $$(2,8)$$과 쌍대값 $$(0.5,\ 0,\ 0.3)$$이 손 계산과 정확히 일치함을 검증했고(단계 6), 산소 강건성 곡선을 그려 배지 조건에 따른 성장률 변화를 시각화했습니다(단계 7).

작은 장난감 예제에서 확인한 원리(단계 6)가 그대로 95차원 `e_coli_core`의 계산(단계 1~5)에 적용된다는 점이 이 실습의 핵심입니다 — 차원만 커질 뿐 이론은 바뀌지 않습니다.

## 스스로 해보기

코드를 조금 바꿔 보며 결과가 어떻게 달라지는지 직접 확인해 보십시오. 정답 코드를 바로 보지 말고 먼저 예측한 뒤 실행해 비교하는 것이 좋습니다.

1. 단계 6의 코드에서 포도당 상한을 [3.6절](03.md)처럼 $$14$$로 바꾸면(`A_ub`의 첫 번째 원소를 14로), `linprog`가 반환하는 $$(v_1^*,v_2^*)$$와 쌍대값이 [3.6절](03.md)의 손 계산과 일치하는지 확인하십시오.
2. 단계 7의 코드를 응용해, 이번에는 산소는 고정하고(`EX_o2_e.lower_bound = -20`) 포도당 흡수 상한을 0~20까지 스캔하는 강건성 곡선을 그려 [5.4절](05.md) 그림 4.4와 비교하십시오.
3. 단계 3의 혐기 조건에서 `anaerobic.fluxes['EX_etoh_e']`(에탄올)와 `anaerobic.fluxes['EX_ac_e']`(아세테이트) 값을 출력해, 산소가 없을 때 어떤 발효 부산물이 나타나는지 확인하십시오([6.4절](06.md)과 비교).

다음 단계로는 이 장의 [8절(pFBA)](08.md)과 [9절(FVA)](09.md)에서 비유일성을 다루는 원리를 복습하고, 결손 분석과 균주 설계로 확장하는 [Chapter 8](../chapter-8/README.md)로 이어가면 좋습니다.

---
