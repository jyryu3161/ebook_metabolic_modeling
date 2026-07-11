# 💡 실습: `e_coli_core`로 결손·MOMA/ROOM·production envelope 한 번에

## 이 실습에서 하는 일

이 장에서 절마다 따로 보았던 도구들 — 단일 결손 스크리닝(§2), FBA·MOMA·ROOM 비교(§3~5), production envelope(§7) — 을 **하나의 파이프라인**으로 이어 봅니다. 큰 그림은 세 단계입니다.

```mermaid
flowchart LR
    A["1) 단일 결손 스크리닝<br/>필수 유전자 찾기 (§2)"] --> B["2) 한 결손을 골라<br/>FBA·MOMA·ROOM 비교 (§3~5)"]
    B --> C["3) production envelope로<br/>growth-coupled 판정 (§7)"]
```

*그림 8.8. 제8장 실습 파이프라인. `e_coli_core` 단일 유전자 결손 스크리닝으로 후보를 고른 뒤 같은 결손을 FBA·MOMA·ROOM의 서로 다른 상태 가정으로 비교하고, 마지막으로 production-envelope 하한에서 성장 결합 여부를 판정합니다. 출처: 저자 자체 제작; 계산 구현은 아래 COBRApy 0.30.0 실습 코드이며 외부 그림을 재사용하지 않았습니다.*

전체 실행 가능한 예제와 시각화는 실습 노트북 `gem9_w04_lab.ipynb`에 있습니다. 아래 코드는 그 핵심 흐름을 압축한 것으로, [COBRApy](https://opencobra.github.io/cobrapy/) 환경에 그대로 복사해 실행할 수 있습니다.

## 파이프라인 코드

```python
# 목적: 단일 결손 스크리닝 -> 세 방법 비교 -> production envelope까지 한 파이프라인으로
from cobra.io import load_model
from cobra.flux_analysis import (single_gene_deletion, moma, pfba,
                                 production_envelope, room)

model = load_model("textbook")               # 반응 95 / 대사물 72 / 유전자 137
biomass_id = "Biomass_Ecoli_core"
wt_growth = model.slim_optimize()              # μ ≈ 0.874 h⁻¹
wt_reference = pfba(model)                     # MOMA/ROOM용 WT 대표 flux

# 1) 단일 결손 스크리닝으로 필수 유전자 찾기
res = single_gene_deletion(model, processes=1)
res["ratio"] = res["growth"].fillna(0) / wt_growth
print("필수 유전자 수:", (res["ratio"] < 0.01).sum())
# 기대 출력: 필수 유전자 수: 7

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

## 결과 해석

세 방법이 같은 tpiA 결손에 대해 서로 다른 성장률을 내놓는다는 점에 주목하십시오 — FBA는 약 0.704, linear MOMA는 0(거리 최소화가 우선이라 성장이 희생됨), zero-tolerance linear ROOM은 약 0.240입니다. 이는 §5.1에서 강조했듯 **세 방법이 애초에 다른 질문(재최적화 vs. 거리 최소 vs. 변화 수 최소)에 답하기 때문**입니다. 핵심 주의점을 정리하면 다음과 같습니다.

- FBA는 같은 mutant feasible space에서 성장을 직접 최대화하므로 MOMA·ROOM 성장률보다 작을 수는 없습니다. 그러나 **MOMA와 ROOM 사이의 성장률 순서는 보장되지 않습니다.**
- `moma()`·`room()`의 `objective_value`는 **성장률이 아니라** 각각 "거리"와 "바뀐 반응 수"입니다. 성장률은 반드시 바이오매스 flux(`sol.fluxes[biomass_id]`)에서 읽어야 합니다.
- 위 코드는 실행 시간을 위해 COBRApy의 zero-tolerance linear ROOM 변형을 사용했습니다. 정확한 ROOM MILP는 `linear=False`와 tolerance를 명시하며 GLPK에서 오래 걸릴 수 있습니다.
- 3단계에서 최대 생장점의 `flux_minimum`이 0이므로, 이 야생형 모델은 아세테이트 생산에 growth-coupled되어 있지 않습니다(§7.1 그림 8.7과 일치).

{% hint style="info" %}
💡 **팁:** genome-scale 모델(예: iML1515)로 확장할 때는 후보 유전자를 먼저 좁히고(§2.4의 조합 폭발 문제 참고), MILP solver·시간 제한·optimality gap을 명시하십시오. [Gurobi](https://www.gurobi.com/)/[CPLEX](https://www.ibm.com/products/ilog-cplex-optimization-studio) 같은 상용 솔버는 [GLPK](https://www.gnu.org/software/glpk/)보다 MILP를 훨씬 빠르게 풉니다.
{% endhint %}

## 스스로 해보기

1. **다른 결손으로 바꿔 보기.** `b3919`(tpiA)를 §1.3에서 본 `b1676`(pykF, isozyme 백업 있음)으로 바꿔 실행하면 세 방법의 성장률이 어떻게 달라질까요? *(예상: pykF는 pykA가 백업하므로 세 방법 모두 WT에 가까운 성장률을 유지 — 결손이 사실상 무해하기 때문입니다.)*
2. **다른 산물로 envelope 그리기.** 3단계의 `objective="EX_ac_e"`를 `"EX_etoh_e"`(에탄올)나 `"EX_succ_e"`(succinate)로 바꿔 최대 생장점의 하한을 확인하십시오. 어떤 산물도 야생형에서는 growth-coupled가 아님을 관찰하게 됩니다 — growth-coupling은 §6의 균주 설계(결손)를 거쳐야 비로소 만들어집니다.
3. **필수 유전자 목록 출력.** `res[res["ratio"] < 0.01]`을 출력해 7개 필수 유전자가 무엇인지 확인하고, §2.1의 icd·eno·gltA가 그 안에 있는지 대조해 보십시오.

---
