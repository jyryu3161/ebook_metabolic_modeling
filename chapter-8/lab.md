# 💡 실습: `e_coli_core`로 결손·MOMA/ROOM·production envelope 한 번에

이 장의 개별 스니펫을 하나의 흐름으로 묶으면 다음과 같습니다. 전체 실행 가능한 예제와 시각화는 실습 노트북 `gem9_w04_lab.ipynb`에 있습니다.

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

# 2) tpiA 결손에 대해 FBA/linear MOMA/ROOM 비교
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

# 3) 아세테이트 생산 포락선으로 growth-coupled 여부 판정
env = production_envelope(
    model,
    reactions=[model.reactions.Biomass_Ecoli_core],
    objective="EX_ac_e",
)
max_growth_row = env.loc[env[biomass_id].idxmax()]
print(max_growth_row[[biomass_id, "flux_minimum", "flux_maximum"]])
# flux_minimum > 0일 때만 최대 생장 지점에서 생산이 강제된다.
```

FBA는 같은 mutant feasible space에서 성장을 직접 최대화하므로 MOMA·ROOM 성장률보다 작을 수는 없지만, **MOMA와 ROOM 사이의 성장률 순서는 보장되지 않습니다.** 위 코드는 실행 시간을 위해 COBRApy의 zero-tolerance linear ROOM 변형을 사용했습니다. 정확한 ROOM MILP는 `linear=False`와 tolerance를 명시하며 GLPK에서 오래 걸릴 수 있습니다. 게놈 규모로 확장할 때는 후보 유전자를 좁히고 MILP solver·시간 제한·optimality gap을 명시하십시오.

---
