# 실습: 배지·유전자 결손·FBA·MOMA·ROOM 비교

> 이 실습은 COBRApy 0.30.0의 `textbook` 모델을 사용합니다. 같은 모델에서 기준 배지, 산소 차단, 유전자 결손을 순서대로 적용하고 FBA·pFBA·FVA·linear MOMA·linear ROOM의 출력을 구분합니다.

## 이 실습에서 하는 일

하나의 계산 파이프라인으로 다음 질문을 확인합니다.

1. 기준 배지에서 모델이 성장합니까?
2. 산소를 차단하면 성장률과 분비 플럭스가 어떻게 달라집니까?
3. `tpiA` 결손은 어떤 반응 경계를 바꾸고 성장률을 얼마나 낮춥니까?
4. pFBA 대표 해와 FVA 허용 범위는 어떤 정보를 추가합니까?
5. 같은 결손에 대한 FBA·linear MOMA·linear ROOM의 성장률은 어떻게 다릅니까?

## 학습 목표

이 실습을 마치면 다음을 할 수 있습니다.

1. 모델·배지·목적함수와 솔버를 기록한 기준 FBA를 실행합니다.
2. 교환 반응 경계를 바꾸어 호기와 혐기 조건을 비교합니다.
3. GPR을 확인하고 유전자 결손을 안전하게 적용합니다.
4. pFBA 대표값과 FVA 범위를 구분하여 해석합니다.
5. MOMA와 ROOM의 목적값이 성장률과 다름을 코드로 확인합니다.
6. 같은 교란에 대한 FBA·MOMA·ROOM 결과를 비교표로 정리합니다.

## 준비

- Python 3.10 이상
- COBRApy 0.30.0
- GLPK
- `pandas`

설치가 필요하면 [설치 가이드](../installation.md)를 먼저 확인합니다. 원래의 quadratic MOMA에는 이차계획 지원 솔버가, 원 ROOM에는 혼합정수선형계획 솔버가 필요합니다. 이 실습은 기본 GLPK 환경에서 실행하기 위해 linear 변형을 사용합니다.

{% hint style="warning" %}
아래 결과는 교육용 `textbook` 모델의 조건부 예측입니다. 실제 균주의 성장률이나 결손 표현형으로 직접 인용하지 않습니다.
{% endhint %}

## 단계 1. 기준 모델과 계산 계약 확인

```python
# 기준 모델과 솔버 설정
import cobra
import pandas as pd
from cobra.io import load_model

model = load_model("textbook")
model.solver = "glpk"
biomass_id = "Biomass_Ecoli_core"

print("COBRApy:", cobra.__version__)
print("solver:", model.solver.interface.__name__)
print("model size:", len(model.reactions), len(model.metabolites), len(model.genes))
print("objective:", model.objective.expression)
print("medium:", model.medium)
```

반응·대사물·유전자 수, 목적함수와 열린 배지를 기록합니다. 모델 파일이나 릴리스가 다르면 이후 결과도 달라질 수 있습니다.

## 단계 2. 기준 FBA와 산소 차단 비교

```python
# 기준 FBA 계산
wt_fba = model.optimize()
assert wt_fba.status == "optimal"

exchange_ids = [
    "EX_glc__D_e", "EX_o2_e", "EX_co2_e",
    "EX_ac_e", "EX_etoh_e", "EX_for_e",
]

print("WT growth:", wt_fba.fluxes[biomass_id])
print(wt_fba.fluxes[exchange_ids])

# 산소 경계만 변경
with model:
    model.reactions.EX_o2_e.lower_bound = 0
    anaerobic = model.optimize()
    print("anaerobic status:", anaerobic.status)
    print("anaerobic growth:", anaerobic.fluxes[biomass_id])
    print(anaerobic.fluxes[exchange_ids])
```

호기와 혐기 계산은 산소 섭취 경계 하나만 다릅니다. 성장률과 발효 부산물 플럭스를 함께 비교합니다. 값이 예상과 다르면 `model.medium`과 산소 반응식을 다시 확인합니다.

## 단계 3. GPR 확인과 `tpiA` 결손

```python
# 결손 전 GPR과 관련 반응 확인
gene = model.genes.get_by_id("b3919")
print(gene.id, gene.name)
print([reaction.id for reaction in gene.reactions])

with model as mutant:
    mutant.genes.get_by_id("b3919").knock_out()
    for reaction in gene.reactions:
        mutant_reaction = mutant.reactions.get_by_id(reaction.id)
        print(mutant_reaction.id, mutant_reaction.gene_reaction_rule, mutant_reaction.bounds)

    mutant_fba = mutant.optimize()
    print("mutant status:", mutant_fba.status)
    print("mutant FBA growth:", mutant_fba.fluxes[biomass_id])
```

`knock_out()`은 GPR 전체를 평가해 기능을 잃은 반응의 경계를 조정합니다. `with model:` 블록을 벗어나면 결손이 복원됩니다.

`b3919`가 등장하는 반응 목록만으로 비활성화 여부를 판단하지 않습니다. `or` 분기에 다른 유전자가 남으면 반응이 유지될 수 있습니다.

## 단계 4. pFBA 대표 해와 FVA 범위

```python
# 대표 해와 허용 범위 계산
from cobra.flux_analysis import pfba, flux_variability_analysis

wt_pfba = pfba(model)
fva = flux_variability_analysis(
    model,
    reaction_list=["PGI", "TPI", "EX_glc__D_e", biomass_id],
    fraction_of_optimum=0.9,
    processes=1,
)

comparison = fva.rename(columns={"minimum": "fva_min", "maximum": "fva_max"})
comparison["pfba_flux"] = wt_pfba.fluxes[comparison.index]
comparison["fva_width"] = comparison["fva_max"] - comparison["fva_min"]
print(comparison)
```

`pfba_flux`는 한 대표 해의 값이고, `fva_min`과 `fva_max`는 반응마다 별도 최적화로 얻은 허용 경계입니다. 모든 `fva_max`가 동시에 나타나는 하나의 플럭스 상태를 뜻하지 않습니다.

## 단계 5. 같은 결손을 FBA·linear MOMA·linear ROOM으로 비교

```python
# 같은 결손과 같은 WT 기준을 사용한 방법 비교
from cobra.flux_analysis import moma, room

with model as mutant:
    mutant.genes.get_by_id("b3919").knock_out()

    fba_solution = mutant.optimize()
    lmoma_solution = moma(
        mutant,
        solution=wt_pfba,
        linear=True,
    )
    lroom_solution = room(
        mutant,
        solution=wt_pfba,
        linear=True,
    )

    results = pd.DataFrame(
        {
            "biomass_flux": {
                "FBA": fba_solution.fluxes[biomass_id],
                "linear_MOMA": lmoma_solution.fluxes[biomass_id],
                "linear_ROOM": lroom_solution.fluxes[biomass_id],
            },
            "method_objective": {
                "FBA": fba_solution.objective_value,
                "linear_MOMA": lmoma_solution.objective_value,
                "linear_ROOM": lroom_solution.objective_value,
            },
        }
    )
    print(results)
```

`biomass_flux` 열만 세 방법의 성장률을 비교할 수 있습니다. `method_objective`는 FBA에서는 성장 목적값, linear MOMA에서는 절대거리 합, linear ROOM에서는 연속 변형의 비용입니다. 서로 단위와 의미가 다르므로 한 수치축에서 크기를 비교하지 않습니다.

{% hint style="warning" %}
COBRApy 0.30.0의 `room(..., linear=True)`는 zero-tolerance 연속 변형입니다. 목적값을 원 ROOM에서 유의하게 변한 반응 수라고 부르지 않습니다.
{% endhint %}

## 단계 6. 단일 유전자 결손 스크리닝

```python
# 조건부 필수성 스크리닝
from cobra.flux_analysis import single_gene_deletion

wt_growth = model.slim_optimize()
screen = single_gene_deletion(model, processes=1)
screen["growth_ratio"] = screen["growth"].fillna(0) / wt_growth

screen["class"] = "nonessential_at_threshold"
screen.loc[screen["growth_ratio"] < 0.9, "class"] = "growth_reduced"
screen.loc[screen["growth_ratio"] < 0.01, "class"] = "essential_at_threshold"

print(screen["class"].value_counts())
print(screen.sort_values("growth_ratio").head(10))
```

임계값 `0.01`과 `0.9`는 이 실습의 분류 설정입니다. 배지와 임계값을 바꾸면 분류가 달라질 수 있습니다.

## 단계 7. 재현 기록 정리

```python
# 재현 가능한 조건 기록
record = {
    "model": "COBRApy textbook / e_coli_core",
    "cobrapy_version": cobra.__version__,
    "solver_interface": model.solver.interface.__name__,
    "medium": dict(model.medium),
    "objective": str(model.objective.expression),
    "knockout": "b3919",
    "wt_reference": "COBRApy pfba(model)",
    "moma_variant": "linear=True",
    "room_variant": "linear=True, zero-tolerance continuous variant",
    "essential_threshold": 0.01,
}
print(record)
```

계산값만 저장하지 않고 조건과 구현 변형을 함께 저장합니다. 원 MOMA 또는 원 ROOM을 추가로 실행할 때에는 솔버, 시간 제한, 허용오차와 ROOM 임계값도 기록합니다.

## 정리

- 배지는 교환 반응 경계로 표현하며 산소 한 조건만 바꾸어 대조했습니다.
- 유전자 결손은 GPR을 평가한 뒤 반응 경계 변화로 적용했습니다.
- pFBA 대표 해와 FVA 반응별 범위를 구분했습니다.
- FBA·linear MOMA·linear ROOM의 성장률은 바이오매스 플럭스에서 비교했습니다.
- 방법별 목적값은 서로 다른 질문과 단위를 가지므로 성장률로 혼용하지 않았습니다.

## 스스로 해보기

1. `b1676` 단일 결손에서 `PYK`의 경계와 성장률이 유지되는지 확인합니다.
2. 산소 차단 조건에서 단일 유전자 결손 스크리닝을 다시 실행하고 기준 배지의 분류와 비교합니다.
3. `fraction_of_optimum`을 `1.0`, `0.95`, `0.9`로 바꾸어 `PGI`의 FVA 폭을 비교합니다.
4. 다른 WT 기준 해를 사용해 linear MOMA와 linear ROOM의 바이오매스 플럭스가 유지되는지 확인합니다.

---
