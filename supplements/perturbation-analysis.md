# 핵심 방법. 유전자 교란, MOMA와 ROOM

> [Chapter 7의 질병 표적 탐색](../chapter-7/README.md)에 들어가기 전에 읽는 선행 페이지입니다. 유전자 결손을 반응 제약으로 바꾸는 법, FBA·MOMA·ROOM이 서로 다른 질문에 답한다는 점, COBRApy 결과를 올바르게 읽는 법을 정리합니다.

## 1. 유전자 결손은 GPR을 통해 반응 결손이 된다

유전자 하나를 제거했다고 그 유전자가 연결된 모든 반응이 자동으로 꺼지는 것은 아닙니다.

- `geneA AND geneB`: 둘 중 하나만 없어도 효소 복합체가 깨져 반응이 꺼집니다.
- `geneA OR geneB`: 둘 중 하나가 남아 있으면 isozyme이 반응을 유지합니다.

예를 들어 `e_coli_core`의 pyruvate kinase 반응 `PYK`는 `pykA OR pykF`이므로 `pykF(b1676)`만 제거해도 `pykA(b1854)`가 남습니다. COBRApy 0.30.0 `textbook` 모델에서 `pykF` 단독 결손의 FBA 성장률은 야생형과 사실상 같습니다. 이를 성장 결함 예제로 사용하면 안 됩니다.

## 2. FBA 결손 예측

FBA는 결손으로 바뀐 feasible space 안에서 목적함수를 다시 최대화합니다.

$$
\max_{\mathbf v}\;\mathbf c^\mathsf T\mathbf v
\quad\text{s.t.}\quad
\mathbf S\mathbf v=0,\quad
\mathbf l'\le\mathbf v\le\mathbf u'
$$

결손 반응의 bound는 0으로 바뀝니다. FBA가 답하는 질문은 “이 결손 세포가 주어진 제약 아래 **최적으로 적응했다면** 달성할 수 있는 최대 성장률은 얼마인가?”입니다. 교란 직후 실제 flux 분포나 적응 속도를 직접 예측하지는 않습니다.

## 3. MOMA: 야생형과의 거리를 최소화한다

Segrè, Vitkup, Church(2002)는 교란된 세포가 즉시 새 성장 최적점으로 이동하기보다 기존 flux 상태에서 가능한 한 적게 변한다는 가설을 제안했습니다.

$$
\min_{\mathbf v\in\mathcal P_{mut}}
\lVert\mathbf v-\mathbf w\rVert_2^2
$$

- $$\mathbf w$$: 야생형 reference flux
- $$\mathcal P_{mut}$$: 결손 제약을 적용한 feasible space
- 원래 MOMA는 convex QP입니다.

$$L_1$$ 거리를 최소화하는 **linear MOMA**도 널리 사용됩니다.

$$
\min_{\mathbf v\in\mathcal P_{mut}}
\sum_j|v_j-w_j|
$$

둘은 같은 방법이 아닙니다. COBRApy의 `moma(..., linear=True)`가 기본이므로 원 논문의 QP를 실행하려면 `linear=False`와 QP 지원 solver가 필요합니다.

## 4. ROOM: 크게 바뀌는 반응 수를 최소화한다

Shlomi, Berkman, Ruppin(2005)의 ROOM은 변화량의 제곱합이 아니라 야생형 허용 구간을 **유의하게 벗어난 반응의 개수**를 최소화합니다.

$$
\min_{\mathbf v,\mathbf y}\sum_j y_j,
\qquad y_j\in\{0,1\}
$$

$$y_j=0$$이면 $$v_j$$는 reference $$w_j$$ 주변의 허용 구간에 묶이고, $$y_j=1$$이면 그 구간을 벗어날 수 있습니다. 이 논리를 Big-M 제약으로 표현하므로 MILP가 됩니다.

원 논문의 핵심 결론은 “ROOM이 시간상 더 늦은 상태를 항상 나타낸다”가 아닙니다. 여러 반응을 조금씩 바꾸는 MOMA보다 **소수의 조절 스위치를 크게 바꾸는 해가 실제 결손 반응에 더 가까울 수 있다**는 조절 최소성 가설입니다. 5개 *E. coli* 결손 유전자를 여러 배지에서 측정한 9개 knockout–condition flux 실험의 평균 유의 변화 수는 ROOM 12, FBA 119, MOMA 317이었고, 최종 성장률 상대오차는 ROOM 14%, FBA 15%, MOMA 31%였습니다. 9개 중 8개에서 같거나 더 나았다는 비교는 **flux 예측**에 대한 결과입니다. 별도의 6개 결손 적응진화 성장 자료에서만 적응 전 MOMA, 적응 후 ROOM/FBA의 상관 경향을 비교했습니다. 이 결과는 해당 데이터·모델의 비교이며 모든 생물·조건의 보편적 순위를 뜻하지 않습니다.

## 5. 세 방법이 답하는 질문

| 방법 | 최적화 목표 | 필요한 reference | 출력 목적값의 의미 |
|:---|:---|:---|:---|
| FBA | 성장 등 생물학적 목적 최대화 | 불필요 | 최대 성장/산물 flux |
| QP MOMA | $$L_2$$ flux 거리 최소화 | 야생형 flux $$\mathbf w$$ | 제곱 거리 |
| linear MOMA | $$L_1$$ flux 거리 최소화 | 야생형 flux $$\mathbf w$$ | 절대거리 합 |
| ROOM | 허용범위 밖 반응 수 최소화 | 야생형 flux $$\mathbf w$$ | 변화 비용/반응 수 |

{% hint style="danger" %}
MOMA와 ROOM의 `solution.objective_value`는 성장률이 아닙니다. 성장률은 `solution.fluxes[biomass_reaction_id]`에서 읽어야 합니다.
{% endhint %}

## 6. COBRApy에서 올바르게 결과 읽기

```python
from cobra.io import load_model
from cobra.exceptions import SolverNotFound
from cobra.flux_analysis import moma, room, pfba

model = load_model("textbook")       # COBRApy 0.30 기준
biomass_id = "Biomass_Ecoli_core"

# 하나의 reference가 필요하므로 pFBA 해를 사용한다.
# pFBA도 이론적으로 항상 유일한 것은 아님에 유의한다.
wt = pfba(model)

with model as mutant:
    # tpiA는 이 교육용 조건에서 실제 성장 저하가 나타나는 예시
    mutant.genes.get_by_id("b3919").knock_out()

    fba_sol = mutant.optimize()
    print("FBA growth:", fba_sol.fluxes[biomass_id])

    # 무료 LP solver에서도 실행되는 L1 변형
    linear_moma_sol = moma(mutant, solution=wt, linear=True)
    print("linear MOMA L1 objective:", linear_moma_sol.objective_value)
    print("linear MOMA growth:", linear_moma_sol.fluxes[biomass_id])

    # 원 논문의 L2^2 QP MOMA는 QP-capable solver가 있을 때만 실행한다.
    try:
        qp_moma_sol = moma(mutant, solution=wt, linear=False)
        print("quadratic MOMA objective:", qp_moma_sol.objective_value)
        print("quadratic MOMA growth:", qp_moma_sol.fluxes[biomass_id])
    except SolverNotFound:
        print("quadratic MOMA skipped: QP-capable solver not found")

    # COBRApy 0.30의 zero-tolerance linear ROOM 변형
    linear_room_sol = room(mutant, solution=wt, linear=True)
    print("zero-tolerance linear ROOM objective:", linear_room_sol.objective_value)
    print("zero-tolerance linear ROOM growth:", linear_room_sol.fluxes[biomass_id])

    # 원 논문의 이진변수 MILP를 실행하려면 linear=False를 쓴다.
    # exact_room_sol = room(
    #     mutant, solution=wt, linear=False, delta=0.03, epsilon=0.001
    # )
```

이 예제는 GLPK만 설치된 환경에서도 linear MOMA와 COBRApy의 **zero-tolerance linear ROOM 변형**까지 빠르게 실행됩니다. COBRApy 0.30.0은 `room(..., linear=True)`일 때 $$y_j$$를 연속구간으로 완화할 뿐 아니라 내부에서 $$\delta=\varepsilon=0$$으로 재설정하므로, 전달한 tolerance 값은 사용되지 않습니다. 따라서 이 해를 기본 tolerance $$(0.03, 0.001)$$를 둔 원 ROOM MILP의 단순 완화나 그 목적값의 하한이라고 부르면 안 됩니다. 같은 zero-tolerance 제약의 MILP와 비교할 때에만 연속 완화의 하한으로 해석할 수 있습니다. 원 논문의 정확한 ROOM은 `linear=False`와 명시한 tolerance로 실행하되 모델 규모와 solver에 따라 오래 걸릴 수 있습니다. 마찬가지로 `moma(..., linear=True)`를 “원래 MOMA QP”라고 부르지 말고 **linear MOMA**라고 명시하십시오.

## 7. reference flux의 불확실성

MOMA와 ROOM은 $$\mathbf w$$에 민감합니다. 표준 FBA는 대안 최적해 중 하나를 임의로 반환할 수 있으므로 solver가 바뀌면 reference가 달라질 수 있습니다.

권장 순서는 다음과 같습니다.

1. 가능하면 $$^{13}$$C-MFA 등 실측 flux를 reference로 사용합니다.
2. 그렇지 않다면 pFBA 또는 flux sampling으로 reference 선택 근거를 명시합니다.
3. 여러 가능한 reference에 대해 결론이 유지되는지 민감도 분석합니다.
4. 모델·배지·solver·tolerance·COBRApy 버전을 기록합니다.

MOMA와 ROOM은 정상상태 사이를 비교하는 최적화 방법이지, 초·분·시간에 따른 변화를 적분하는 kinetic time-course model이 아닙니다. 특정 시간척도를 기계적으로 배정하지 마십시오.

## 8. 필수성, 합성 치사와의 연결

유전자 필수성은 결손 후 성장 목적함수가 정한 임계값 아래로 떨어지는지를 deletion test로 판단합니다. FVA에서 어떤 반응 flux가 고정되어 있다는 사실과 동일하지 않습니다.

두 단일 결손은 생존하지만 이중 결손이 치명적이면 합성 치사입니다. 이는 [Chapter 7](../chapter-7/README.md)의 선택적 암 표적과 [Chapter 8](../chapter-8/README.md)의 균주 설계에서 모두 사용됩니다.

## 랜드마크 논문 읽기

### MOMA — Segrè et al. (2002)

- **연구 질문**: 진화적으로 최적화되지 않은 knockout의 flux를 성장 최대화보다 잘 예측할 수 있는가?
- **핵심 아이디어**: mutant feasible space에서 wild-type flux에 가장 가까운 점을 QP로 찾습니다.
- **주요 결론**: FBA의 즉시 재최적화 가정과 다른, 교란 상태의 suboptimal flux 가설을 계산 가능하게 만들었습니다.
- **한계**: reference flux와 거리 척도에 의존하며 time-resolved kinetics가 아닙니다.

### ROOM — Shlomi et al. (2005)

- **연구 질문**: 세포가 flux 전체를 조금씩 조절하기보다 소수 반응의 on/off 상태를 바꾼다고 보면 예측이 나아지는가?
- **핵심 아이디어**: 유의하게 변한 반응 수를 MILP로 최소화합니다.
- **주요 결론**: 조사한 *E. coli* knockout에서 MOMA보다 훨씬 희소한 변화와 더 낮은 성장률 오차를 보였습니다.
- **한계**: tolerance와 reference에 의존하고 MILP 대안해가 있을 수 있습니다.

## 참고문헌

1. Segrè, D., Vitkup, D., & Church, G. M. (2002). [Analysis of optimality in natural and perturbed metabolic networks](https://doi.org/10.1073/pnas.232349399). *PNAS*, 99, 15112–15117.
2. Shlomi, T., Berkman, O., & Ruppin, E. (2005). [Regulatory on/off minimization of metabolic flux changes after genetic perturbations](https://doi.org/10.1073/pnas.0406346102). *PNAS*, 102, 7695–7700.
