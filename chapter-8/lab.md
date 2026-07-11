# 실습: `e_coli_core`로 결손·MOMA/ROOM·production envelope 한 번에

## 이 실습에서 하는 일

이 장에서 절마다 따로 배운 도구들 — 단일 결손 스크리닝([§2](02.md)), FBA·MOMA·ROOM 비교([§3~5](05.md)), production envelope([§7](07.md)) — 을 **하나의 파이프라인**으로 이어서 직접 실행해 봅니다. `e_coli_core` 모델 하나로 "필수 유전자 찾기 → 한 결손을 세 방법으로 비교하기 → 생산 포락선으로 성장 결합 여부 판정하기"를 처음부터 끝까지 따라 하는 것이 목표입니다. 큰 그림은 세 단계입니다.

```mermaid
flowchart LR
    A["1) 단일 결손 스크리닝<br/>필수 유전자 찾기 (§2)"] --> B["2) 한 결손을 골라<br/>FBA·MOMA·ROOM 비교 (§3~5)"]
    B --> C["3) production envelope로<br/>growth-coupled 판정 (§7)"]
```

*그림 8.8. 제8장 실습 파이프라인. `e_coli_core` 단일 유전자 결손 스크리닝으로 후보를 고른 뒤 같은 결손을 FBA·MOMA·ROOM의 서로 다른 상태 가정으로 비교하고, 마지막으로 production-envelope 하한에서 성장 결합 여부를 판정합니다. 출처: 저자 자체 제작; 계산 구현은 아래 COBRApy 0.30.0 실습 코드이며 외부 그림을 재사용하지 않았습니다.*

전체 실행 가능한 예제와 시각화는 실습 노트북 `gem9_w04_lab.ipynb`에 있습니다. 아래 단계들은 그 핵심 흐름을 네 개의 셀로 나눈 것으로, [COBRApy](https://opencobra.github.io/cobrapy/) 환경에 순서대로 복사해 실행하면 그대로 재현됩니다.

## 학습 목표

이 실습을 마치면 다음을 할 수 있습니다.

1. COBRApy로 `e_coli_core` 모델을 불러오고 야생형(wild-type, WT) 성장률과 [pFBA](../glossary.md) 기준 flux를 **계산한다**.
2. `single_gene_deletion()`으로 단일 결손 스크리닝을 **실행하고** 필수 유전자 수를 확인한다.
3. 같은 결손(tpiA)에 대해 FBA·MOMA·ROOM을 **실행하고** 세 방법이 내놓는 성장률과 목적값을 구분해 **해석한다**.
4. `production_envelope()`로 생산 포락선을 **계산하고** 최대 생장점의 하한으로 growth-coupled 여부를 **판정한다**.

## 준비물

시작하기 전에 아래를 갖추어 주십시오.

- **실행 환경**: [Chapter 11의 §1 환경·솔버 설정](../chapter-11/01.md)에서 만든 가상환경, 또는 [설치 가이드](../installation.md)의 core 패키지와 Jupyter kernel. 기준 환경은 Python 3.10 이상과 COBRApy 0.30.0입니다.
- **필요한 패키지**: `cobra`(COBRApy) 한 가지면 이 실습은 실행됩니다. 별도로 상용 솔버를 설치하지 않았다면 기본 LP 솔버인 [GLPK](https://www.gnu.org/software/glpk/)가 자동으로 사용됩니다.
- **모델**: `e_coli_core`(반응 95, 대사물 72, 유전자 137). 아래 코드의 `load_model("textbook")`이 자동으로 내려받거나 캐시에서 불러오므로, 첫 실행에는 네트워크 연결이 필요할 수 있습니다.
- **선행 지식(선택)**: 이 실습은 [§2](02.md)·[§3~5](05.md)·[§7](07.md)에서 다룬 개념을 압축한 것입니다. 각 절을 먼저 읽으면 결과 해석이 훨씬 수월하지만, 실습 자체는 아래 네 단계만으로 독립 실행됩니다.

아래 네 단계의 코드 셀은 **순서대로** 실행해야 합니다. 앞 단계에서 만든 변수(`model`, `wt_growth`, `wt_reference`, `biomass_id`)를 뒤 단계가 그대로 사용하기 때문입니다.

---

### 단계 1. 실습 환경을 준비하고 야생형 기준값 계산하기

**무엇을·왜.** 먼저 필요한 함수를 불러오고, 모델을 연 뒤, 뒤 단계에서 계속 쓸 두 가지 기준값을 미리 계산합니다. 하나는 야생형 성장률 `wt_growth`(아무 유전자도 끄지 않은 정상 모델의 최대 생장률)이고, 다른 하나는 `wt_reference`입니다. `wt_reference`는 [pFBA (parsimonious FBA)](../glossary.md)로 구한 **야생형 대표 flux 벡터**로, MOMA와 ROOM이 "결손 세포가 이 야생형 상태에서 얼마나 벗어났는가"를 재는 기준선 역할을 합니다. 여기서 flux란 단위 시간·단위 생물량당 반응 진행률(`mmol gDW⁻¹ h⁻¹`)을 뜻합니다.

```python
# 목적: 단일 결손 스크리닝 -> 세 방법 비교 -> production envelope까지 한 파이프라인으로
from cobra.io import load_model
from cobra.flux_analysis import (single_gene_deletion, moma, pfba,
                                 production_envelope, room)

model = load_model("textbook")               # 반응 95 / 대사물 72 / 유전자 137
biomass_id = "Biomass_Ecoli_core"
wt_growth = model.slim_optimize()              # μ ≈ 0.874 h⁻¹
wt_reference = pfba(model)                     # MOMA/ROOM용 WT 대표 flux
```

**예상 출력.** 이 셀은 화면에 아무것도 출력하지 않습니다. 계산 결과가 변수에 저장될 뿐이며, 오류 없이 다음 셀로 넘어가면 정상입니다.

**확인 포인트.** 오류 메시지 없이 셀이 끝나면 성공입니다. 값을 직접 눈으로 확인하고 싶다면 새 셀에서 `wt_growth`를 입력해 실행해 보십시오. `0.8739...`(≈ 0.874 h⁻¹)에 가까운 값이 나오면 모델과 솔버가 제대로 동작하는 것입니다.

**자주 나는 오류와 해결.**
- `ModuleNotFoundError: No module named 'cobra'` → COBRApy가 설치되지 않았습니다. `pip install cobra`로 설치하거나 준비물의 가상환경을 활성화하십시오.
- 다운로드가 멈추거나 실패한다 → `load_model("textbook")`은 첫 실행 시 원격에서 모델을 내려받습니다. 네트워크를 확인하거나, COBRApy에 포함된 SBML 파일을 `cobra.io.read_sbml_model("경로/e_coli_core.xml")`로 직접 불러와도 동일한 모델을 얻습니다.

### 단계 2. 단일 유전자 결손 스크리닝으로 필수 유전자 찾기

**무엇을·왜.** 모델의 유전자를 하나씩 껐다가 켜 보며 성장률이 얼마나 떨어지는지 전수 조사합니다. `single_gene_deletion()`이 137개 유전자 각각에 대해 FBA를 다시 풀어 결손 성장률을 계산합니다. 야생형 대비 성장률 비율(`ratio`)이 거의 0으로 떨어지는 유전자가 **필수 유전자(essential gene)**입니다 — 대체 경로가 없어 결손하면 세포가 자라지 못하는 유전자입니다. 여기서는 비율이 0.01 미만인 유전자를 필수로 셉니다. 필수성 분류의 배경은 [§2.1](02.md)을 참고하십시오.

```python
# 1) 단일 결손 스크리닝으로 필수 유전자 찾기
res = single_gene_deletion(model, processes=1)
res["ratio"] = res["growth"].fillna(0) / wt_growth
print("필수 유전자 수:", (res["ratio"] < 0.01).sum())
# 기대 출력: 필수 유전자 수: 7
```

**예상 출력.**

```
필수 유전자 수: 7
```

**확인 포인트.** `필수 유전자 수: 7`이 출력되면 성공입니다. `res["growth"]`에는 결손이 불가능(infeasible)한 경우 결측값(NaN)이 들어가는데, `fillna(0)`으로 그것을 성장률 0으로 처리했기 때문에 필수 유전자로 정확히 집계됩니다.

**자주 나는 오류와 해결.**
- `NameError: name 'wt_growth' is not defined` → 단계 1 셀을 먼저 실행하지 않았습니다. 이 실습의 셀들은 위에서부터 순서대로 실행해야 합니다.
- 실행이 오래 걸린다 → `processes=1`은 재현성을 위해 단일 코어로 계산합니다. `e_coli_core`는 작아서 보통 몇 초면 끝나지만, 노트북 환경에 따라 십수 초가 걸릴 수 있습니다.

### 단계 3. tpiA 결손을 FBA·MOMA·ROOM으로 비교하기

**무엇을·왜.** 이제 유전자 하나(`b3919`, tpiA)를 골라 **같은 결손**을 세 가지 방법으로 예측해 비교합니다. 세 방법은 "결손된 세포가 어디로 가는가"에 대해 서로 다른 가정을 둡니다 — FBA는 새 목적을 즉시 재최적화한다고 보고, MOMA는 야생형 flux에 최대한 가깝게 머문다고 보며, ROOM은 바뀌는 반응 수를 최소로 한다고 봅니다(비교표는 [§5.1](05.md)). `with model as m:` 블록은 그 안에서 가한 변경(여기서는 결손)을 블록을 빠져나갈 때 자동으로 되돌리므로, 모델을 훼손하지 않고 안전하게 실험할 수 있습니다. `knock_out()`은 해당 유전자가 담당하는 반응을 GPR 규칙에 따라 비활성화합니다.

```python
# 2) tpiA(b3919) 결손에 대해 FBA/linear MOMA/ROOM 비교
with model as m:
    m.genes.get_by_id("b3919").knock_out()
    fba_sol = m.optimize()
    lmoma_sol = moma(m, wt_reference, linear=True)
    room_sol = room(m, wt_reference, linear=True)

    print("FBA growth:", fba_sol.fluxes[biomass_id])
    print("linear MOMA: distance=", lmoma_sol.objective_value,
          "growth=", lmoma_sol.fluxes[biomass_id])
    print("zero-tolerance linear ROOM objective=", room_sol.objective_value,
          "growth=", room_sol.fluxes[biomass_id])
    # 기대 출력(솔버·버전에 따라 소수점은 달라질 수 있음):
    #   FBA growth: ~0.704
    #   linear MOMA: distance= ~280.6  growth= ~0.0
    #   zero-tolerance linear ROOM objective= ~2.46  growth= ~0.240
```

**예상 출력.** 소수점 자리는 솔버·버전에 따라 달라질 수 있지만, 대략 다음과 같은 값이 나옵니다.

```
FBA growth: ~0.704
linear MOMA: distance= ~280.6  growth= ~0.0
zero-tolerance linear ROOM objective= ~2.46  growth= ~0.240
```

**확인 포인트.** 세 줄이 모두 출력되고, 성장률이 **FBA(약 0.704) > ROOM(약 0.240) > MOMA(약 0.0)** 순서로 서로 다르게 나오면 성공입니다. 같은 결손인데도 값이 갈리는 것은 오류가 아니라, 세 방법이 애초에 서로 다른 질문(재최적화 vs. 거리 최소화 vs. 변화 수 최소화)에 답하기 때문입니다([§5.1](05.md)). FBA는 결손 후 feasible space에서 성장을 직접 최대화하므로 MOMA·ROOM의 성장률보다 작아질 수 없습니다. 다만 **MOMA와 ROOM 사이의 성장률 순서는 일반적으로 보장되지 않습니다** — 이 결손에서 우연히 ROOM이 더 높게 나온 것입니다.

{% hint style="warning" %}
**해석상의 주의:** `moma()`와 `room()`이 돌려주는 `objective_value`는 **성장률이 아닙니다.** MOMA의 목적값은 야생형과의 "거리"(약 280.6)이고, ROOM의 목적값은 "유의하게 바뀐 반응의 수"(약 2.46)입니다. 세 방법의 성장률을 비교하려면 반드시 바이오매스 flux, 즉 `sol.fluxes[biomass_id]`에서 값을 읽어야 합니다. 목적값과 성장률을 혼동하면 "MOMA 성장률이 280이다" 같은 잘못된 결론에 이르게 됩니다.
{% endhint %}

**자주 나는 오류와 해결.**
- `KeyError: 'b3919'` → 유전자 ID 표기를 확인하십시오. `e_coli_core`에서 tpiA의 ID는 `b3919`입니다.
- ROOM 계산이 지나치게 오래 걸린다 → 위 코드는 실행 시간을 줄이기 위해 COBRApy의 zero-tolerance **linear ROOM 변형**(`linear=True`)을 사용합니다. 원래의 정확한 ROOM은 MILP(혼합정수선형계획법)로, `linear=False`와 tolerance를 명시하며 GLPK에서는 오래 걸릴 수 있습니다.

### 단계 4. 아세테이트 production envelope로 growth-coupled 판정하기

**무엇을·왜.** 마지막으로, 이 야생형 모델이 아세테이트 생산에 **growth-coupled**(자라려면 반드시 산물을 만드는 상태)인지 확인합니다. `production_envelope()`는 각 생장률 값에서 목표 산물(`EX_ac_e`, 아세테이트 분비)의 flux 최솟값·최댓값을 계산해 [생산 포락선](../glossary.md)을 만듭니다. 판정의 핵심은 **최대 생장점에서 산물 flux의 하한(`flux_minimum`)**을 읽는 것입니다 — 하한이 0보다 커야 growth-coupled입니다([§7.1](07.md)).

```python
# 3) 아세테이트 생산 포락선으로 growth-coupled 여부 판정
env = production_envelope(
    model,
    reactions=[model.reactions.Biomass_Ecoli_core],
    objective="EX_ac_e",
)
max_growth_row = env.loc[env[biomass_id].idxmax()]
print(max_growth_row[[biomass_id, "flux_minimum", "flux_maximum"]])
# 기대 출력: 최대 생장률(~0.874)에서 flux_minimum=0, flux_maximum=0
# flux_minimum > 0일 때만 최대 생장 지점에서 생산이 강제된다.
```

**예상 출력.** 최대 생장률(약 0.874) 행에서 아세테이트 flux의 최솟값·최댓값이 모두 0으로 나옵니다(정확한 소수점은 솔버·버전에 따라 달라질 수 있습니다).

```
Biomass_Ecoli_core    ~0.874
flux_minimum             0.0
flux_maximum             0.0
```

**확인 포인트.** 최대 생장점에서 `flux_minimum`이 0이면, 이 야생형 모델은 아세테이트 생산에 **growth-coupled되어 있지 않습니다**([§7.1](07.md) 그림 8.7과 일치). 즉 세포는 아세테이트를 전혀 만들지 않고도 최고 속도로 자랄 수 있습니다. `flux_minimum > 0`일 때에만 "최대로 자라려면 반드시 산물을 만들어야 한다"는 성장 결합이 성립합니다. 이 하한을 0에서 양수로 밀어 올리는 것이 바로 [§6](06.md)의 균주 설계 알고리듬(OptKnock 등)이 하는 일입니다.

**자주 나는 오류와 해결.**
- `worker` 관련 오류나 프로세스 관련 경고가 뜬다(주로 Windows/macOS 노트북) → `production_envelope`는 내부적으로 여러 LP를 병렬로 풉니다. 워커 생성 문제를 피하려면 셀 맨 앞에 `from cobra import Configuration; Configuration().processes = 1`을 추가해 전역 워커 수를 1로 두십시오([§7.1](07.md)의 실습 참고).
- 출력 열 이름이 다르다 → COBRApy 버전에 따라 열 이름이 다를 수 있습니다. `env.columns`를 출력해 실제 열 이름을 확인한 뒤 `flux_minimum`/`flux_maximum`에 대응시키십시오.

{% hint style="info" %}
**팁:** genome-scale 모델(예: iML1515)로 확장할 때는 후보 유전자를 먼저 좁히고([§2.4](02.md)의 조합 폭발 문제 참고), MILP solver·시간 제한·optimality gap을 명시하십시오. [Gurobi](https://www.gurobi.com/)/[CPLEX](https://www.ibm.com/products/ilog-cplex-optimization-studio) 같은 상용 솔버는 [GLPK](https://www.gnu.org/software/glpk/)보다 MILP를 훨씬 빠르게 풉니다.
{% endhint %}

---

## 정리

이 실습에서는 `e_coli_core` 모델 하나로 다음을 순서대로 수행했습니다.

- **단계 1**에서 모델을 불러오고 야생형 성장률(`wt_growth` ≈ 0.874)과 pFBA 기준 flux(`wt_reference`)를 계산해 뒤 단계의 기준선을 마련했습니다.
- **단계 2**에서 단일 결손 스크리닝으로 137개 유전자 중 **필수 유전자 7개**를 찾았습니다.
- **단계 3**에서 tpiA(b3919) 결손 하나를 FBA(≈0.704)·MOMA(≈0.0)·ROOM(≈0.240)으로 비교해, 세 방법이 서로 다른 가정 때문에 다른 성장률을 내놓는다는 것을 확인했습니다. 또한 `objective_value`가 성장률이 아니라는 점을 익혔습니다.
- **단계 4**에서 아세테이트 생산 포락선을 계산해, 최대 생장점의 하한이 0이므로 이 야생형 조건이 **growth-coupled가 아님**을 판정했습니다.

핵심 메시지는, 같은 결손·같은 모델이라도 **어떤 질문을 던지느냐(재최적화 vs. 거리 최소 vs. 변화 수 최소)**에 따라 예측이 달라진다는 점, 그리고 growth-coupling은 야생형에서 저절로 생기는 것이 아니라 [§6](06.md)의 균주 설계를 거쳐야 만들어진다는 점입니다.

## 스스로 해보기

아래 과제는 위 네 단계의 코드를 조금씩 바꿔 보는 연습입니다. 정답 코드를 바로 보지 말고 먼저 직접 실행해 보십시오.

1. **다른 결손으로 바꿔 보기.** 단계 3의 `b3919`(tpiA)를 [§1.3](01.md)에서 본 `b1676`(pykF, isozyme 백업 있음)으로 바꿔 실행하면 세 방법의 성장률이 어떻게 달라질까요? *(예상: pykF는 pykA가 백업하므로 세 방법 모두 WT에 가까운 성장률을 유지 — 결손이 사실상 무해하기 때문입니다.)*
2. **다른 산물로 envelope 그리기.** 단계 4의 `objective="EX_ac_e"`를 `"EX_etoh_e"`(에탄올)나 `"EX_succ_e"`(succinate)로 바꿔 최대 생장점의 하한을 확인하십시오. 어떤 산물도 야생형에서는 growth-coupled가 아님을 관찰하게 됩니다 — growth-coupling은 [§6](06.md)의 균주 설계(결손)를 거쳐야 비로소 만들어집니다.
3. **필수 유전자 목록 출력.** 단계 2의 결과에서 `res[res["ratio"] < 0.01]`을 출력해 7개 필수 유전자가 무엇인지 확인하고, [§2.1](02.md)의 icd·eno·gltA가 그 안에 있는지 대조해 보십시오.

다음으로 넘어갈 준비가 되었다면, 이 예측 도구들을 공학적 설계로 확장하는 [§6 균주 설계](06.md)와, 커뮤니티 수준으로 넓히는 [§9](09.md)로 이어 읽는 것을 권합니다.

---
