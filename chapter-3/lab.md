# 실습: COBRApy로 모델 구조 검증하기

## 재현 환경

이 실습의 기대 출력은 다음 환경에서 확인하였다.

- Python 3.10
- COBRApy 0.30.0
- `cobra.io.load_model("textbook")`로 불러온 `e_coli_core`
- optlang GLPK 인터페이스

원격 예제 모델은 갱신될 수 있다. 장기 재현이 필요하면 사용한 SBML 파일, 패키지 잠금 파일과 파일 해시를 함께 보존한다.

```python
import ast
from collections import Counter

import cobra
from cobra.io import load_model
from cobra.manipulation.delete import knock_out_model_genes

model = load_model("textbook")

print(cobra.__version__)
print(model.id)
print(len(model.reactions), len(model.metabolites), len(model.genes))
print(model.solver.interface.__name__)
```

기준 출력은 COBRApy 0.30.0, 모델 ID `e_coli_core`, 반응 95개, 대사물 72개, 유전자 137개이다.

## 1. GPR을 구문 트리로 분류하기

GPR 문자열에 단순히 `" and "` 또는 `" or "`가 포함되어 있는지 찾으면 중첩식, 공백, 유전자 ID 표현에 취약하다. COBRApy가 이미 만든 GPR 구문 트리를 순회하면 AND와 OR 연산자를 안전하게 분류할 수 있다.

```python
def classify_gpr(reaction):
    rule = reaction.gene_reaction_rule.strip()
    if not rule:
        return "no_gpr"

    nodes = list(ast.walk(reaction.gpr))
    has_and = any(isinstance(node, ast.And) for node in nodes)
    has_or = any(isinstance(node, ast.Or) for node in nodes)

    if has_and and has_or:
        return "mixed"
    if has_and:
        return "and_only"
    if has_or:
        return "or_only"
    return "single"


counts = Counter(classify_gpr(reaction) for reaction in model.reactions)
for category in ["no_gpr", "single", "or_only", "and_only", "mixed"]:
    print(f"{category:>8}: {counts[category]}")
```

기대 결과는 다음과 같다.

```text
  no_gpr: 26
   single: 27
  or_only: 27
 and_only: 10
    mixed: 5
```

따라서 GPR이 있는 반응은 69개이다. OR을 포함한 반응을 모두 “OR-only”로 세면 mixed 5개가 중복되므로, 범주를 상호 배타적으로 정의해야 한다. 비율의 분모도 명시한다. 예를 들어 OR-only는 전체 반응 기준 $$27/95$$이고, GPR 연관 반응 기준 $$27/69$$이다.

빈 GPR은 “유전자 연관 규칙이 기록되어 있지 않다”는 뜻이다. Exchange와 바이오매스 같은 비효소 반응, 알려지지 않은 효소, 자발 반응, 주석 누락이 모두 이 범주에 들어갈 수 있다. 따라서 빈 GPR을 곧바로 자발 반응으로 해석하지 않는다.

대표 반응의 규칙도 확인한다.

```python
for reaction_id in ["PGK", "PFK", "PDH", "SUCDi"]:
    reaction = model.reactions.get_by_id(reaction_id)
    print(reaction.id, reaction.gene_reaction_rule,
          reaction.gene_name_reaction_rule, classify_gpr(reaction))
```

`PFK`는 `pfkA or pfkB`, `PDH`와 `SUCDi`는 효소 소단위 사이의 AND 관계를 보여준다.

## 2. GPR을 안전하게 평가하기

`reaction.gpr.eval()`은 결손 유전자 **ID 집합**을 받아 규칙의 참·거짓을 계산한다. 여기서 참은 유전자 기능 가용성에 따른 구조적 판정이며, 발현량이나 효소 활성의 크기를 뜻하지 않는다.

```python
gene_id_by_name = {gene.name: gene.id for gene in model.genes}
pfk = model.reactions.get_by_id("PFK")

pfk_a = gene_id_by_name["pfkA"]
pfk_b = gene_id_by_name["pfkB"]

print(pfk.gpr.eval({pfk_a}))
print(pfk.gpr.eval({pfk_a, pfk_b}))
```

기대 결과는 각각 `True`와 `False`이다. `pfkA`만 결손되면 `pfkB`가 규칙을 만족하지만 두 유전자가 모두 결손되면 PFK가 비활성화된다.

실제 모델의 반응 bounds까지 바꾸려면 COBRApy의 유전자 결손 함수를 사용한다. 변경은 컨텍스트 안에서 수행하여 원본 모델을 복원한다.

```python
original_bounds = pfk.bounds

with model:
    disabled = knock_out_model_genes(model, [pfk_a, pfk_b])
    print("PFK" in {reaction.id for reaction in disabled})
    print(model.reactions.get_by_id("PFK").bounds)

assert model.reactions.get_by_id("PFK").bounds == original_bounds
```

두 유전자 결손 조건에서는 `PFK`가 비활성 반응 목록에 포함되고 bounds가 $$(0,0)$$이 된다. 문자열을 직접 분할해 만든 파서는 연산자 우선순위, 괄호, 유전자 ID를 잘못 처리할 수 있으므로 사용하지 않는다.

## 3. 구획과 반응 범주 확인하기

대사물은 하나의 구획 라벨을 갖지만, 운송 반응은 여러 구획의 대사물을 포함한다. 따라서 구획별 반응 수의 합은 전체 반응 수보다 클 수 있다.

```python
for compartment_id, compartment_name in model.compartments.items():
    metabolite_count = sum(
        metabolite.compartment == compartment_id
        for metabolite in model.metabolites
    )
    reaction_count = sum(
        compartment_id in reaction.compartments
        for reaction in model.reactions
    )
    print(compartment_id, compartment_name,
          metabolite_count, reaction_count)
```

`e_coli_core`에는 `c`와 `e` 두 라벨이 있으며, 대사물 수는 각각 52와 20이다. 각 구획에 걸친 반응은 각각 75와 45개로 세어지며 운송 반응이 양쪽에 중복 집계된다.

경계 반응, 다중 구획 반응, 그 밖의 반응을 서로 겹치지 않게 분류할 수 있다.

```python
boundary_ids = {reaction.id for reaction in model.boundary}
transport_ids = {
    reaction.id
    for reaction in model.reactions
    if reaction.id not in boundary_ids
    and len(reaction.compartments) > 1
}
other_ids = {
    reaction.id for reaction in model.reactions
    if reaction.id not in boundary_ids | transport_ids
}

print(len(boundary_ids), len(transport_ids), len(other_ids))
print(len(model.exchanges), len(model.demands), len(model.sinks))
```

기대 결과는 `20 25 50`과 `20 0 0`이다. 마지막 50개는 경계도 다중 구획 운송도 아닌 반응이다. 이 집합에는 일반적인 세포질 대사 반응뿐 아니라 바이오매스와 ATP 유지처럼 단일 구획에 놓인 의사 반응도 포함되므로 모두를 “대사 반응”이라고 부르지 않는다.

이 분류는 서로 다른 구획의 대사물을 포함하는 반응을 운송 반응으로 보는 구조적 기준이다. 모델의 방향성 또는 운송 기작을 판정하려면 반응식과 주석을 추가로 확인한다.

## 4. 바이오매스 반응과 유지 에너지 확인하기

```python
biomass = model.reactions.get_by_id("Biomass_Ecoli_core")
atpm = model.reactions.get_by_id("ATPM")

print(biomass.id)
print(len(biomass.metabolites))
print(sorted({met.compartment for met in biomass.metabolites}))
print(biomass.objective_coefficient)

for metabolite_id in ["atp_c", "h2o_c", "adp_c", "pi_c", "h_c"]:
    metabolite = model.metabolites.get_by_id(metabolite_id)
    print(metabolite_id, biomass.metabolites.get(metabolite, 0.0))

print("ATPM bounds:", atpm.bounds)
solution = model.optimize()
print(solution.status, round(solution.objective_value, 4))
```

이 스냅샷에서 BOF는 23개 대사물을 포함하고 세포질 대사물만 사용하며 목적계수는 1이다. ATP와 물의 계수는 각각 $$-59.81$$이고 ADP, 인산, 양성자의 계수는 각각 $$+59.81$$이다. 이 묶음은 BOF에 포함된 **ATP 가수분해 항(GAM 관례)**으로 읽을 수 있다. 일반 모델에서는 ATP가 조성 전구체로도 쓰일 수 있으므로 ATP 계수 하나만으로 GAM을 판정하지 않는다. `ATPM` 하한은 8.39이며, 기본 배지에서 최적 목적값은 약 $$0.8739\ \mathrm{h^{-1}}$$이다.

## 5. 배지 전환을 동일 모델에서 비교하기

각 조건은 컨텍스트 안에서 bounds만 바꾼다. 아래의 탄소원 결핍 조건은 탄소 원자를 포함하는 모든 exchange 대사물의 흡수를 보수적으로 닫는다.

```python
def growth_rate(current_model):
    solution = current_model.optimize()
    value = solution.objective_value if solution.status == "optimal" else None
    return solution.status, value


print("aerobic", growth_rate(model))

with model:
    model.reactions.get_by_id("EX_o2_e").lower_bound = 0.0
    print("anaerobic", growth_rate(model))

with model:
    for exchange in model.exchanges:
        boundary_metabolite = next(iter(exchange.metabolites))
        if boundary_metabolite.elements.get("C", 0) > 0:
            exchange.lower_bound = 0.0
    print("no carbon uptake, NGAM on", growth_rate(model))

    model.reactions.get_by_id("ATPM").lower_bound = 0.0
    print("no carbon uptake, NGAM off", growth_rate(model))
```

기준 모델의 호기·무산소 목적값은 각각 약 0.8739와 0.2117이다. 모든 탄소 함유 exchange의 흡수를 닫고 NGAM 하한 8.39를 유지하면 모델은 `infeasible`이다. 탄소 공급 없이 기저 ATP 소비까지 만족할 수 없기 때문이다. 같은 조건에서 `ATPM` 하한을 0으로 완화하면 최적해가 존재하고 성장률은 0이다. 이 대조는 “성장하지 않는다”와 “모든 제약을 만족하는 정상상태 자체가 없다”를 구분한다. 다른 모델에서는 CO$$_2$$ 고정 경로, 열려 있는 sink 또는 다른 탄소원 때문에 결과가 달라질 수 있다.

## 6. Demand 반응을 누출 없이 시험하기

새 반응을 컨텍스트 밖에서 추가하면 목적함수만 복원되고 반응은 모델에 남는다. 반응 생성부터 목적함수 변경까지 모두 컨텍스트 안에서 수행한다.

```python
reaction_ids_before = {reaction.id for reaction in model.reactions}

with model:
    atp_demand = model.add_boundary(
        model.metabolites.get_by_id("atp_c"),
        type="demand",
    )
    model.objective = atp_demand
    demand_solution = model.optimize()
    print(atp_demand.id, atp_demand.bounds)
    print(demand_solution.status, demand_solution.objective_value)

reaction_ids_after = {reaction.id for reaction in model.reactions}
assert reaction_ids_after == reaction_ids_before
assert "DM_atp_c" not in reaction_ids_after
```

이 계산은 ATP 농도나 축적량이 아니라, 주어진 정상상태 제약에서 ATP를 demand로 제거할 수 있는 최대 속도를 구한다. 컨텍스트를 벗어난 뒤 반응 ID 집합이 원래와 같다는 assertion이 모델 변경의 누출을 검사한다.

## 7. 전체 검산

```python
assert counts == Counter({
    "no_gpr": 26,
    "single": 27,
    "or_only": 27,
    "and_only": 10,
    "mixed": 5,
})
assert len(model.reactions) == 95
assert len(model.metabolites) == 72
assert len(model.genes) == 137
assert abs(model.reactions.get_by_id("ATPM").lower_bound - 8.39) < 1e-12
assert abs(model.optimize().objective_value - 0.8739) < 1e-4
```

패키지 또는 예제 모델 버전이 달라 assertion이 실패하면 기대값을 즉시 덮어쓰지 말고, 모델 파일과 solver, 기본 배지, 목적함수 및 bounds의 차이를 먼저 기록한다.
