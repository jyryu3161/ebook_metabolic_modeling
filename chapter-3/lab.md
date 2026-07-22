# 실습: COBRApy로 모델 구조 검증하기

## 이 실습에서 하는 일

[COBRApy](https://opencobra.github.io/cobrapy/)로 대장균 교육용 모델 `e_coli_core`를 불러온 뒤, 이 장에서 배운 구조 요소인 [GPR](02.md), [구획(compartment)](03.md), 경계·운송 반응, [바이오매스 반응과 유지 에너지](06.md)를 코드로 하나씩 조회하고 검증합니다. 모델을 바꾸지 않고 안전하게 시험하는 방법(컨텍스트 매니저)과, 계산 결과를 과잉 해석하지 않는 방법도 함께 익힙니다.

## 학습 목표

이 실습을 마치면 다음을 수행할 수 있습니다.

1. 실행 환경을 확인하고 예제 모델 `e_coli_core`를 불러와 버전과 규모(반응·대사물·유전자 수)를 **확인한다**.
2. GPR을 구문 트리로 **분류**하고 단일·OR-only·AND-only·mixed·빈 GPR을 상호 배타적으로 **집계한다**.
3. 유전자 결손을 안전하게 **평가**하고, 컨텍스트 매니저로 원본 모델을 **복원한다**.
4. 구획·경계·운송 반응을 겹치지 않게 **분류**하고, 바이오매스 반응과 ATP 유지 반응을 **조회한다**.
5. 같은 모델에서 배지 조건만 바꿔 성장률을 **비교**하고, `infeasible`(실행 불가능)과 성장률 0을 **구분한다**.

## 준비물

- **실행 환경**: [Chapter 11 §1 (환경·솔버·Gurobi 라이선스)](../chapter-11/01.md) 또는 [설치 가이드](../installation.md)를 따라 가상환경을 만들고 패키지를 설치합니다. 기준 환경은 다음과 같습니다.
  - Python 3.10
  - [COBRApy](https://opencobra.github.io/cobrapy/) 0.30.0
  - optlang [GLPK](https://www.gnu.org/software/glpk/) 인터페이스(COBRApy에 기본 포함되는 오픈소스 솔버)
- **모델**: `cobra.io.load_model("textbook")`로 내려받는 `e_coli_core`. 처음 실행할 때 인터넷 연결이 필요합니다.
- **선행 셀**: 이 실습은 Chapter 3의 첫 실습이므로 다른 실습의 결과에 의존하지 않습니다. 다만 아래 **단계 1**의 import·모델 로드 셀을 먼저 실행해야, 이후 단계에서 쓰는 `model`, `classify_gpr`, `counts` 같은 변수가 정의됩니다. 각 단계의 코드는 위에서부터 순서대로 실행합니다.
- **용어 미리 보기**: **플럭스**(flux; 대사 통량)는 단위 시간당 반응 진행률로, 일반 대사 반응에서는 `mmol gDW⁻¹ h⁻¹` 단위로 봅니다. **성장률**은 바이오매스 반응의 플럭스이며 이 실습에서는 `h⁻¹` 단위로 해석합니다.

{% hint style="info" %}
원격 예제 모델은 갱신될 수 있습니다. 장기 재현이 필요하면 사용한 SBML 파일, 패키지 잠금 파일과 파일 해시를 함께 보존합니다. 이 실습의 기대 출력은 위 기준 환경에서 확인한 값입니다.
{% endhint %}

---

## 단계 1. 실행 환경을 확인하고 모델 불러오기

**무엇을·왜**: 먼저 필요한 라이브러리를 불러오고, 예제 모델을 메모리에 올립니다. 본격적인 분석에 앞서 패키지 버전과 모델 규모를 출력해, 뒤의 기대 출력과 같은 조건에서 시작하는지 확인하기 위한 단계입니다.

**코드**

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

**예상 출력**

```text
0.30.0
e_coli_core
95 72 137
optlang.glpk_interface
```

마지막 줄은 현재 사용 중인 솔버 인터페이스 이름입니다. 기본 GLPK 솔버를 쓰면 `optlang.glpk_interface`처럼 표시됩니다.

**확인 포인트**: 기준 출력은 COBRApy 0.30.0, 모델 ID `e_coli_core`, 반응 95개, 대사물 72개, 유전자 137개입니다. 이 네 줄이 일치하면 이 실습의 고정 환경과 같은 회귀 기준을 재현한 것입니다. 모델 artifact·solver build가 다르면 값의 차이를 먼저 기록하고 원인을 확인합니다.

**자주 나는 오류와 해결**

- `ModuleNotFoundError: No module named 'cobra'`: 가상환경이 활성화되지 않았거나 COBRApy가 설치되지 않은 경우입니다. [Chapter 11 §1](../chapter-11/01.md)의 순서대로 가상환경을 활성화한 뒤 `pip install "cobra==0.30.0"`을 실행합니다.
- `load_model("textbook")`에서 다운로드 오류가 나면 인터넷 연결을 확인합니다. 사내망·방화벽 환경에서는 미리 받아 둔 SBML 파일을 `cobra.io.read_sbml_model(경로)`로 불러올 수 있습니다.
- 버전이 0.30.0과 다르면 이후 단계의 숫자가 달라질 수 있습니다. 우선 버전을 맞춘 뒤 진행합니다.

---

## 단계 2. GPR을 구문 트리로 분류하기

**무엇을·왜**: [GPR(gene-protein-reaction association)](02.md)은 어떤 유전자 산물의 조합이 반응을 촉매할 수 있는지 Boolean 식으로 기록한 주석입니다. 그런데 GPR 문자열에 `" and "`나 `" or "`가 들어 있는지를 단순히 문자열로 찾으면 중첩식·괄호·유전자 ID 표기에 쉽게 속습니다. COBRApy가 이미 만들어 둔 GPR **구문 트리(syntax tree)**를 순회하면 AND와 OR 연산자를 안전하게 분류할 수 있습니다.

**코드**

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

이 코드는 각 반응의 GPR 트리에 AND/OR 노드가 있는지 확인해 다섯 범주 중 하나로 분류한 뒤, 범주별 개수를 셉니다.

**예상 출력**

```text
  no_gpr: 26
   single: 27
  or_only: 27
 and_only: 10
    mixed: 5
```

**확인 포인트**: 다섯 범주의 합이 현재 불러온 모델의 전체 반응 수와 같고, GPR이 있는 반응 수가 `no_gpr`를 뺀 값과 일치하는지 확인합니다. 95·26·69는 고정 tutorial 환경의 회귀값입니다. OR을 포함한 반응을 모두 “OR-only”로 세면 mixed 5개가 중복되므로, 범주는 상호 배타적으로 정의합니다. 비율을 보고할 때는 분모도 명시합니다. 예를 들어 OR-only는 전체 반응 기준 $$27/95$$이고, GPR 연관 반응 기준 $$27/69$$입니다.

> **해석상의 주의**
> - 빈 GPR은 “유전자 연관 규칙이 기록되어 있지 않다”는 뜻입니다. Exchange와 바이오매스 같은 비효소 반응, 알려지지 않은 효소, 자발 반응, 주석 누락이 모두 이 범주에 들어갈 수 있습니다. 따라서 빈 GPR을 곧바로 자발 반응으로 해석하지 않습니다.

대표 반응의 규칙도 직접 확인합니다.

**코드**

```python
for reaction_id in ["PGK", "PFK", "PDH", "SUCDi"]:
    reaction = model.reactions.get_by_id(reaction_id)
    print(reaction.id, reaction.gene_reaction_rule,
          reaction.gene_name_reaction_rule, classify_gpr(reaction))
```

**예상 출력**: 각 줄에 반응 ID, 유전자 ID 규칙, 유전자 이름 규칙, `classify_gpr`의 범주가 차례로 출력됩니다. `PFK`는 `pfkA or pfkB`(OR-only), `PDH`와 `SUCDi`는 효소 소단위 사이의 AND 관계를 보여줍니다.

**확인 포인트**: `PFK`가 `or_only`, `PDH`·`SUCDi`가 `and_only`로 분류되면 트리 순회가 올바르게 동작한 것입니다.

**자주 나는 오류와 해결**

- `NameError: name 'ast' is not defined` 또는 `Counter is not defined`: 단계 1의 import 셀을 먼저 실행하지 않은 경우입니다. 위에서부터 순서대로 실행합니다.
- `AttributeError: 'Reaction' object has no attribute 'gpr'`: 이 실습은 COBRApy 0.30.0의 `reaction.gpr` API를 씁니다. 버전이 낮으면 단계 1에서 버전을 맞춥니다.

---

## 단계 3. GPR을 안전하게 평가하기

**무엇을·왜**: `reaction.gpr.eval()`은 결손 유전자 **ID 집합**을 받아 규칙의 참·거짓을 계산합니다. 여기서 참은 유전자 기능 가용성에 따른 구조적 판정이며, 발현량이나 효소 활성의 크기를 뜻하지 않습니다. 먼저 유전자 이름을 모델 내부의 유전자 ID로 바꾼 뒤 평가합니다.

**코드**

```python
gene_id_by_name = {gene.name: gene.id for gene in model.genes}
pfk = model.reactions.get_by_id("PFK")

pfk_a = gene_id_by_name["pfkA"]
pfk_b = gene_id_by_name["pfkB"]

print(pfk.gpr.eval({pfk_a}))
print(pfk.gpr.eval({pfk_a, pfk_b}))
```

**예상 출력**

```text
True
False
```

**확인 포인트**: 첫 줄이 `True`, 둘째 줄이 `False`이면 성공입니다. `pfkA`만 결손되면 `pfkB`가 규칙을 만족하지만, 두 유전자가 모두 결손되면 PFK가 비활성화됩니다.

실제 모델의 반응 bounds(경계조건)까지 바꾸려면 COBRApy의 유전자 결손 함수를 사용합니다. 변경은 **컨텍스트 매니저**(`with model:`) 안에서 수행하여, 블록을 벗어나면 원본 모델이 자동 복원되도록 합니다.

**코드**

```python
original_bounds = pfk.bounds

with model:
    disabled = knock_out_model_genes(model, [pfk_a, pfk_b])
    print("PFK" in {reaction.id for reaction in disabled})
    print(model.reactions.get_by_id("PFK").bounds)

assert model.reactions.get_by_id("PFK").bounds == original_bounds
```

**예상 출력**: 두 유전자 결손 조건에서는 `PFK`가 비활성 반응 목록에 포함되어 첫 줄이 `True`, 둘째 줄의 bounds가 $$(0,0)$$으로 출력됩니다. 마지막 `assert`는 오류 없이 통과합니다(컨텍스트를 벗어나 bounds가 원래대로 복원되었기 때문입니다).

**확인 포인트**: 블록 안에서는 PFK가 `(0, 0)`으로 닫히고, 블록을 벗어난 뒤 `assert`가 `AssertionError` 없이 지나가면 성공입니다.

> **해석상의 주의**
> - 여기서의 참·거짓은 유전자 기능 가용성에 대한 **구조적 판정**이지, 발현량이나 효소 활성의 크기가 아닙니다.
> - 문자열을 직접 분할해 만든 파서는 연산자 우선순위, 괄호, 유전자 ID를 잘못 처리할 수 있으므로 사용하지 않습니다.

**자주 나는 오류와 해결**

- `KeyError: 'pfkA'`: `gene_id_by_name`은 유전자 **이름**을 키로 씁니다. 모델에 따라 이름과 ID 표기가 다르므로, `[g.name for g in model.genes]`로 실제 이름을 확인합니다.
- `with model:` 없이 `knock_out_model_genes`를 실행하면 결손이 모델에 그대로 남아 이후 단계의 결과가 달라집니다. 반드시 컨텍스트 안에서 수행합니다.

---

## 단계 4. 구획과 반응 범주 확인하기

**무엇을·왜**: 대사물은 하나의 [구획(compartment)](03.md) 라벨을 갖지만, 운송 반응은 여러 구획의 대사물을 포함합니다. 따라서 구획별 반응 수의 합은 전체 반응 수보다 클 수 있습니다. 먼저 구획별로 대사물 수와 반응 수를 세어 봅니다.

**코드**

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

**예상 출력**: 각 줄에 구획 ID, 구획 이름, 대사물 수, 그 구획에 걸친 반응 수가 출력됩니다. `e_coli_core`에는 `c`와 `e` 두 라벨이 있으며, 대사물 수는 각각 52와 20입니다. 각 구획에 걸친 반응은 각각 75와 45개로 세어지며, 운송 반응이 양쪽에 중복 집계됩니다.

**확인 포인트**: 대사물 수 52 + 20 = 72(전체 대사물 수)가 되고, 반응 수의 합(75 + 45)이 전체 반응 수 95보다 크면(운송 반응 중복 때문에) 정상입니다.

이제 경계 반응, 다중 구획 반응, 그 밖의 반응을 서로 겹치지 않게 분류합니다.

**코드**

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

**예상 출력**

```text
20 25 50
20 0 0
```

**확인 포인트**: 세 범주의 합 20 + 25 + 50 = 95(전체 반응 수)이면 분류가 겹치지 않은 것입니다. 둘째 줄은 경계 반응 20개가 모두 [exchange 반응](05.md)이고 demand·sink는 0개임을 보여 줍니다.

> **해석상의 주의**
> - 마지막 50개는 경계도 다중 구획 운송도 아닌 반응입니다. 이 집합에는 일반적인 세포질 대사 반응뿐 아니라 바이오매스와 ATP 유지처럼 단일 구획에 놓인 의사 반응도 포함되므로, 모두를 “대사 반응”이라고 부르지 않습니다.
> - 이 분류는 서로 다른 구획의 대사물을 포함하는 반응을 운송 반응으로 보는 **구조적 기준**입니다. 모델의 방향성 또는 운송 기작을 판정하려면 반응식과 주석을 추가로 확인합니다.

**자주 나는 오류와 해결**

- `NameError: name 'model' is not defined`: 커널을 새로 시작했다면 단계 1을 다시 실행합니다.
- 숫자가 위와 다르면, 단계 1에서 확인한 모델 규모(95·72·137)가 맞는지 먼저 점검합니다.

---

## 단계 5. 바이오매스 반응과 유지 에너지 확인하기

**무엇을·왜**: 성장 분석에 쓰는 [바이오매스 반응(BOF)](06.md)이 어떤 구획의 대사물을 소비하는지, 목적계수가 얼마인지, ATP 유지 반응(`ATPM`)의 하한이 얼마인지 파일에서 직접 확인합니다. 마지막에는 기본 배지에서 모델을 최적화해 최대 성장률을 구합니다.

**코드**

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

**예상 출력**

```text
Biomass_Ecoli_core
23
['c']
1.0
atp_c -59.81
h2o_c -59.81
adp_c 59.81
pi_c 59.81
h_c 59.81
ATPM bounds: (8.39, 1000.0)
optimal 0.8739
```

**확인 포인트**: 이 스냅샷에서 BOF는 23개 대사물을 포함하고 세포질(`c`) 대사물만 사용하며 목적계수는 1입니다. ATP와 물의 계수는 각각 $$-59.81$$이고 ADP, 인산, 양성자의 계수는 각각 $$+59.81$$입니다. `ATPM` 하한은 8.39이며, 기본 배지에서 최적 목적값(성장률)은 약 $$0.8739\ \mathrm{h^{-1}}$$입니다. 마지막 줄이 `optimal 0.8739`이면 성공입니다.

> **해석상의 주의**
> - ATP·물·ADP·인산·양성자의 이 묶음은 BOF에 포함된 **ATP 가수분해 항(GAM 관례)**으로 읽을 수 있습니다. 다만 일반 모델에서는 ATP가 조성 전구체로도 쓰일 수 있으므로, ATP 계수 하나만으로 GAM을 판정하지 않습니다.

**자주 나는 오류와 해결**

- `KeyError: 'Biomass_Ecoli_core'`: 다른 모델에서는 바이오매스 반응 이름이 다릅니다. `[r.id for r in model.reactions if "iomass" in r.id]`로 실제 ID를 찾습니다.
- `solution.objective_value`가 `None`이면 최적화가 `optimal`이 아닙니다. 앞 단계에서 컨텍스트를 벗어나지 못한 변경이 남아 있는지 확인합니다.

---

## 단계 6. 배지 전환을 동일 모델에서 비교하기

**무엇을·왜**: 같은 모델에서 배지 조건만 바꿔 성장률이 어떻게 달라지는지 비교합니다. 각 조건은 컨텍스트 매니저 안에서 bounds만 바꾸므로 원본 모델은 유지됩니다. 아래의 탄소원 결핍 조건은 탄소 원자를 포함하는 모든 exchange 대사물의 흡수를 보수적으로 닫습니다. 성장·최적화의 이론적 배경은 [Chapter 4](../chapter-4/README.md)에서 다룹니다.

**코드**

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

이 코드는 `growth_rate` 함수로 최적화 상태와 성장률을 함께 돌려받아, 호기·무산소·탄소원 결핍 네 조건을 차례로 비교합니다.

**예상 출력**

```text
aerobic ('optimal', 0.8739...)
anaerobic ('optimal', 0.2117...)
no carbon uptake, NGAM on ('infeasible', None)
no carbon uptake, NGAM off ('optimal', 0.0)
```

각 줄은 `(상태, 성장률)` 형태이며, 소수점 이하 자릿수는 환경에 따라 조금 달라질 수 있습니다. 기준 모델의 호기·무산소 목적값은 각각 약 0.8739와 0.2117입니다.

**확인 포인트**: 무산소 성장률이 호기보다 크게 낮고, “no carbon uptake, NGAM on”이 `infeasible`, 같은 조건에서 `ATPM` 하한을 0으로 완화한 “NGAM off”가 성장률 0이면 성공입니다.

> **해석상의 주의**
> - 모든 탄소 함유 exchange의 흡수를 닫고 NGAM 하한 8.39를 유지하면 모델은 `infeasible`입니다. 탄소 공급 없이 기저 ATP 소비까지 만족할 수 없기 때문입니다. 같은 조건에서 `ATPM` 하한을 0으로 완화하면 최적해가 존재하고 성장률은 0입니다. 이 대조는 “성장하지 않는다”와 “모든 제약을 만족하는 정상상태 자체가 없다”를 구분합니다.
> - 다른 모델에서는 CO$$_2$$ 고정 경로, 열려 있는 sink 또는 다른 탄소원 때문에 결과가 달라질 수 있습니다.

**자주 나는 오류와 해결**

- `KeyError: 'EX_o2_e'`: 산소 exchange 반응 ID가 모델마다 다를 수 있습니다. `[r.id for r in model.exchanges]`로 확인합니다.
- `infeasible`은 오류가 아니라 정상적인 결과입니다. `growth_rate` 함수가 이 경우 값을 `None`으로 돌려주도록 설계되어 있으니, `objective_value`를 곧바로 반올림하지 않도록 주의합니다.

---

## 단계 7. Demand 반응을 누출 없이 시험하기

**무엇을·왜**: 새 반응을 컨텍스트 밖에서 추가하면 목적함수만 복원되고 반응은 모델에 남습니다. 반응 생성부터 목적함수 변경까지 모두 컨텍스트 안에서 수행해, 시험이 끝난 뒤 모델이 원래대로 돌아오는지 확인합니다. 여기서는 세포질 ATP(`atp_c`)에 대한 demand 반응을 추가해 최대 제거 속도를 구합니다.

**코드**

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

**예상 출력**: 첫 줄에는 추가된 demand 반응의 ID `DM_atp_c`와 그 bounds가 출력되고, 둘째 줄에는 `optimal`과 양수의 최대 ATP demand 속도가 출력됩니다. 두 `assert`는 오류 없이 통과합니다.

**확인 포인트**: 컨텍스트를 벗어난 뒤 반응 ID 집합이 원래와 같고(`DM_atp_c`가 남아 있지 않고), 두 `assert`가 `AssertionError` 없이 지나가면 모델 변경이 누출되지 않은 것입니다.

> **해석상의 주의**
> - 이 계산은 ATP 농도나 축적량이 아니라, 주어진 정상상태 제약에서 ATP를 demand로 제거할 수 있는 **최대 속도**를 구합니다.

**자주 나는 오류와 해결**

- 셀을 두 번 실행하면(특히 컨텍스트 밖에서 추가한 경우) `DM_atp_c`가 이미 존재한다는 오류가 날 수 있습니다. 커널을 재시작하거나 단계 1부터 다시 실행합니다. 이 단계는 반드시 `with model:` 안에서 반응을 추가하는 것이 핵심입니다.
- 마지막 `assert`가 실패하면 반응 추가가 컨텍스트 밖으로 새어 나간 것입니다. 코드 들여쓰기를 확인합니다.

---

## 단계 8. 전체 검산으로 재현성 확인하기

**무엇을·왜**: 지금까지 얻은 핵심 수치를 한 번에 다시 검산해, 실습 전체가 기준 환경과 일치하는지 확인합니다. 모든 조건이 맞으면 `assert`는 아무것도 출력하지 않고 조용히 통과합니다.

**코드**

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

**예상 출력**: 아무 출력이 없습니다. 모든 `assert`가 통과하면 성공입니다.

**확인 포인트**: 셀이 오류 없이 끝나면(빨간 `AssertionError`가 없으면) 실습 결과가 기준값과 일치합니다.

**자주 나는 오류와 해결**

- `NameError: name 'counts' is not defined`: 단계 2를 실행하지 않은 경우입니다. 위에서부터 순서대로 다시 실행합니다.
- `AssertionError`가 나면, 패키지 또는 예제 모델 버전이 달라졌을 수 있습니다. 기대값을 즉시 덮어쓰지 말고, 모델 파일과 solver, 기본 배지, 목적함수 및 bounds의 차이를 먼저 기록합니다.

---

## 정리

- 예제 모델 `e_coli_core`를 불러오고, 반응 95개·대사물 72개·유전자 137개라는 규모를 확인했습니다.
- GPR을 구문 트리로 안전하게 분류(no_gpr 26, single 27, or_only 27, and_only 10, mixed 5)하고, 상호 배타적 범주와 분모 표기의 중요성을 익혔습니다.
- `gpr.eval`과 `knock_out_model_genes`로 유전자 결손을 평가하되, 컨텍스트 매니저로 원본 모델을 복원하는 습관을 들였습니다.
- 구획·경계·운송 반응을 겹치지 않게 분류하고, 바이오매스 반응과 ATP 유지 반응(하한 8.39)을 조회했습니다.
- 배지 조건만 바꿔 호기(약 0.8739)·무산소(약 0.2117)·탄소원 결핍(`infeasible` vs 성장률 0)을 비교하며, “성장하지 않음”과 “정상상태 자체가 없음”을 구분했습니다.

## 스스로 해보기

1. 단계 2의 `classify_gpr`를 이용해, GPR 유형별로 반응 ID 목록을 실제로 출력해 봅니다(예: `and_only`에 속하는 반응들). 각 유형의 대표 반응이 무엇인지 눈으로 확인해 봅니다.
2. 단계 3에서 `pfkA`, `pfkB` 대신 다른 반응(예: AND-only인 `PDH`)의 소단위 유전자 하나만 결손시켜 보고, `gpr.eval` 결과가 어떻게 달라지는지 예측한 뒤 확인합니다.
3. 단계 6의 배지 전환에서 산소 대신 포도당 흡수(`EX_glc__D_e`)의 하한을 바꿔 가며 성장률이 어떻게 변하는지 관찰합니다. 흡수를 완전히 닫으면 어떤 상태가 되는지도 확인합니다.

이 실습에서 조회한 구조 요소의 이론적 배경은 [2절 GPR](02.md), [3절 구획](03.md), [5절 경계 반응](05.md), [6절 바이오매스와 유지 에너지](06.md)에서, 성장·최적화의 원리는 [Chapter 4](../chapter-4/README.md)에서 이어서 다룹니다.
