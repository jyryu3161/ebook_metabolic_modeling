# 실습: COBRApy로 GPR·구획·바이오매스·경계 반응 탐색하기

> 💡 **실습:** 아래 코드는 핵심 개념만 담은 발췌본입니다. 전체 실습(GPR 파싱 클래스, 구획별 반응 카운트 시각화, 자동 재구축 모델 비교 등)은 `raw_data/GEM_lecture_notes/gem9_w02_lab.ipynb`에서 확인할 수 있습니다. 아래 예시는 [Chapter 1](../chapter-1/README.md)에서 처음 불러온 COBRApy 내장 예제 모델 `e_coli_core`(95개 반응·72개 대사물·137개 유전자·2개 구획)를 그대로 다시 사용합니다.

**1) GPR 문자열 조회와 간단한 파싱**

```python
from cobra.io import load_model
import re

model = load_model("textbook")

print(f"Model: {model.id}")
print(f"Reactions: {len(model.reactions)}, Genes: {len(model.genes)}")

# 2.1~2.2절의 네 가지 GPR 유형을 대표하는 반응을 골라서 조회
# (gene_reaction_rule은 b-번호 locus tag를, gene_name_reaction_rule은 읽기 쉬운 유전자명을 돌려줍니다)
for rid in ["PGK", "PGL", "PFK", "PDH", "SUCDi"]:
    rxn = model.reactions.get_by_id(rid)
    print(f"  {rxn.id}: {rxn.gene_name_reaction_rule}")

# 기대 출력:
# Model: e_coli_core
# Reactions: 95, Genes: 137
#   PGK: pgk
#   PGL: pgl
#   PFK: pfkA or pfkB
#   PDH: aceF and aceE and lpd
#   SUCDi: sdhA and sdhC and sdhD and sdhB
```

`PGK`·`PGL`은 단일 유전자, `PFK`의 `pfkA or pfkB`는 2.1절의 OR(동위 효소) 관계, `PDH`의 `aceF and aceE and lpd`와 `SUCDi`의 4-소단위 규칙은 AND(복합체) 관계입니다 — `SUCDi`는 사실 Table 2.1의 $$R_2$$(석신산 탈수소효소, sdhA/B/C/D)와 정확히 같은 반응입니다. 전체 모델에 대해 이 관계들을 분류하면 다음과 같은 통계를 얻습니다.

```python
def classify_gpr(gpr_string):
    """GPR 문자열의 AND/OR 유형을 분류 (단순화된 파서)"""
    has_and = " and " in gpr_string.lower()
    has_or = " or " in gpr_string.lower()
    return has_and, has_or

stats = {"single": 0, "isozyme": 0, "complex": 0, "no_gpr": 0}
for rxn in model.reactions:
    rule = rxn.gene_name_reaction_rule
    if not rule:
        stats["no_gpr"] += 1
        continue
    has_and, has_or = classify_gpr(rule)
    if has_or:
        stats["isozyme"] += 1
    elif has_and:
        stats["complex"] += 1
    else:
        stats["single"] += 1

print(stats)
# 기대 출력 (e_coli_core 기준):
# {'single': 27, 'isozyme': 32, 'complex': 10, 'no_gpr': 26}
```

{% hint style="info" %}
💡 **팁:** `load_model("textbook")`은 캐시에 모델이 없으면 원격 모델 저장소에서 내려받습니다. 원격 자산은 갱신될 수 있으므로, 위 통계 `{'single': 27, 'isozyme': 32, 'complex': 10, 'no_gpr': 26}`은 이 책을 검산한 COBRApy 0.30.0·`e_coli_core` 스냅숏의 기준값으로 읽으십시오. 엄밀한 재현에는 환경 구축 안내처럼 실제 SBML과 SHA256을 보존해야 합니다. 반면 2.5절 Table 2.3의 iML1515 GPR 분포(대략값, %)는 원 논문(Monk et al., 2017)에 보고된 스냅숏입니다.
{% endhint %}

**2) 손 계산을 코드로 재현하기: 유전자 결손 시뮬레이션**

2.3절에서 손으로 계산했던 GPR 판정을, 이번에는 코드로 재현해 봅니다. 실제 결과가 손 계산과 일치하는지 직접 확인해 보세요.

```python
def simulate_knockout(gpr_rule, knocked_out_genes):
    """GPR 문자열과 결손 유전자 집합을 받아 반응의 ON/OFF를 판정 (단순 OR-only / AND-only 케이스)"""
    if not gpr_rule:
        return True, "GPR 없음 (자발 반응)"
    if " or " in gpr_rule.lower() and " and " not in gpr_rule.lower():
        genes = {g.strip() for g in re.split(r"\s+or\s+", gpr_rule, flags=re.I)}
        remaining = genes - set(knocked_out_genes)
        return (True, f"동위 효소 {remaining} 생존") if remaining else (False, "모든 동위 효소 결손")
    if " and " in gpr_rule.lower() and " or " not in gpr_rule.lower():
        genes = {g.strip() for g in re.split(r"\s+and\s+", gpr_rule, flags=re.I)}
        missing = genes & set(knocked_out_genes)
        return (False, f"필수 소단위 {missing} 결손") if missing else (True, "복합체 완전")
    return None, "중첩 AND/OR — 2.3절처럼 손으로 괄호 단위로 계산 필요"

pfk_rule = model.reactions.get_by_id("PFK").gene_name_reaction_rule
pdh_rule = model.reactions.get_by_id("PDH").gene_name_reaction_rule

print(simulate_knockout(pfk_rule, ["pfkA"]))
print(simulate_knockout(pfk_rule, ["pfkA", "pfkB"]))
print(simulate_knockout(pdh_rule, ["aceE"]))

# 기대 출력:
# (True, "동위 효소 {'pfkB'} 생존")
# (False, '모든 동위 효소 결손')
# (False, "필수 소단위 {'aceE'} 결손")
```

**3) 구획별 반응·대사물 카운트**

```python
for comp_id, comp_name in model.compartments.items():
    rxn_count = sum(1 for r in model.reactions if comp_id in r.compartments)
    met_count = sum(1 for m in model.metabolites if m.compartment == comp_id)
    print(f"{comp_id} ({comp_name}): reactions={rxn_count}, metabolites={met_count}")

# 기대 출력:
# c (cytosol): reactions=75, metabolites=52
# e (extracellular): reactions=45, metabolites=20
```

대사물 수(52 + 20 = 72)는 정확히 전체 대사물 수와 일치합니다 — 대사물은 반드시 하나의 구획에만 속하기 때문입니다. 그러나 반응 수(75 + 45 = 120)는 전체 반응 수(95)보다 많습니다. 이는 이중 계산이 아니라 **4절에서 다룰 운송·경계 반응이 두 구획에 동시에 걸쳐 있어서** `c in r.compartments`와 `e in r.compartments`를 둘 다 만족하기 때문입니다 — 즉 이 코드 자체가 "구획 간 반응은 한 구획에만 속하지 않는다"는 3.4절의 블록-구조 논리를 그대로 보여주는 셈입니다. `e_coli_core`는 축소 모델이라 구획이 `c`(세포질)와 `e`(세포외) 둘뿐입니다. `p`(주변세포질)를 포함하는 전체 규모의 iML1515나 8개 이상 구획을 가진 Recon3D에서는 동일한 코드가 훨씬 더 많은 행을 출력합니다.

**4) 바이오매스 반응과 NGAM(ATPM) 조회**

```python
biomass_rxn = model.reactions.get_by_id("Biomass_Ecoli_core")
print(f"목적함수 반응: {biomass_rxn.id}")
print(f"전구체(반응물+생성물) 대사물 종류 수: {len(biomass_rxn.metabolites)}")
print(f"ATP 계수(GAM): {biomass_rxn.metabolites[model.metabolites.get_by_id('atp_c')]}")

atpm_rxn = model.reactions.get_by_id("ATPM")
print(f"ATPM 하한(NGAM, mmol/gDW/h): {atpm_rxn.lower_bound}")

solution = model.optimize()
print(f"최적 성장률 mu: {solution.objective_value:.4f} h-1")

# 기대 출력:
# 목적함수 반응: Biomass_Ecoli_core
# 전구체(반응물+생성물) 대사물 종류 수: 23
# ATP 계수(GAM): -59.81
# ATPM 하한(NGAM, mmol/gDW/h): 8.39
# 최적 성장률 mu: 0.8739 h-1
```

이 결과는 6.3절의 danger 콜아웃에서 설명한 대로, `e_coli_core`의 실제 NGAM(8.39)이 문헌에서 흔히 인용되는 3.15와 다르다는 것을 직접 보여줍니다. 이 성장률(μ ≈ 0.874 h⁻¹)을 어떻게 계산하는지는 [Chapter 4](../chapter-4/README.md)에서 본격적으로 다룹니다.

**5) 경계 반응(exchange/demand/sink) 조회와 운송 반응 식별**

```python
print(f"Exchange 반응 수: {len(model.exchanges)}")   # 20
print(f"Demand 반응 수:   {len(model.demands)}")      # 0 (e_coli_core에는 없음)
print(f"Sink 반응 수:     {len(model.sinks)}")        # 0

# 운송 반응: 서로 다른 두 구획에 걸친 대사물을 가진 반응
transport = [r for r in model.reactions
             if len({m.compartment for m in r.metabolites}) > 1
             and len(r.metabolites) > 1]
print(f"운송 반응 수: {len(transport)}")

# 기대 출력:
# Exchange 반응 수: 20
# Demand 반응 수:   0
# Sink 반응 수:     0
# 운송 반응 수: 25
```

95개 반응 중 20개가 exchange, 25개가 운송, 나머지 50개가 세포질 내부 반응으로 분류됩니다(20 + 25 + 50 = 95, 이번에는 겹침 없이 정확히 나뉩니다 — 앞의 3)번 코드와 달리 여기서는 각 반응을 "경계／운송／내부" 중 **하나의 범주로만** 배정했기 때문입니다). 이는 3~5절에서 다룬 "내부 반응 vs 운송 vs 경계 반응"이라는 삼분류가 실제 모델 파일에서 그대로 코드로 확인된다는 것을 보여줍니다.

---
