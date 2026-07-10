# 보충 학습. SBML로 GEM 저장·교환·검증하기

> GEM의 반응·대사물·구획·GPR·목적함수·flux bound를 소프트웨어 사이에서 잃지 않고 교환하는 표준인 SBML을 파일 수준에서 읽고 점검합니다. 원 강의의 **SBML format** 19개 슬라이드 내용을 실무 절차로 재구성했습니다.

## 1. SBML은 무엇이며 왜 필요한가

**SBML(Systems Biology Markup Language)**은 생화학 반응 네트워크와 동적 모델을 표현하는 XML 기반 공개 표준입니다. 특정 프로그램의 저장 형식이 아니라 여러 도구가 공유하는 언어입니다.

- **상호운용성**: COBRApy, COBRA Toolbox, RAVEN, COPASI, CellDesigner 등이 같은 모델을 읽을 수 있습니다.
- **재현성**: 반응식·구획·목적함수·bound를 파일에 명시해 분석 조건을 보존합니다.
- **투명성**: 텍스트 기반 XML이므로 버전 비교와 검토가 가능합니다.
- **저장소 연계**: BiGG Models와 BioModels 같은 공개 저장소가 SBML 모델을 배포합니다.

HTML이 문서의 구조를 태그로 표현하듯 SBML도 모델의 구조를 태그로 표현합니다. 그러나 SBML은 화면 모양이 아니라 생물학적 의미와 수학적 관계를 저장합니다.

## 2. GEM의 정보가 XML에 들어가는 방식

SBML Level 3 Core는 모델·구획·화학종·반응 같은 기본 구조를 제공합니다. constraint-based model에 필요한 목적함수, flux bounds, 유전자 산물과 GPR은 **FBC(Flux Balance Constraints) version 2** 패키지가 추가합니다. 경로·subsystem 묶음은 **Groups** 패키지로 표현할 수 있습니다.

아래를 포함한 이 장의 XML 블록은 요소 사이의 관계만 보여 주는 **개념적 조각**입니다. 읽기 편하게 `xmlns` namespace 선언, 일부 `required` 속성과 기타 필수 요소를 생략했으므로 그대로 저장한 독립 SBML 문서로는 유효하지 않습니다.

```xml
<sbml level="3" version="1" fbc:required="false">
  <model id="toy_model" fbc:strict="true">
    <listOfCompartments>...</listOfCompartments>
    <listOfSpecies>...</listOfSpecies>
    <listOfReactions>...</listOfReactions>
    <fbc:listOfObjectives>...</fbc:listOfObjectives>
    <fbc:listOfGeneProducts>...</fbc:listOfGeneProducts>
  </model>
</sbml>
```

| GEM 개념 | 대표 SBML 요소 |
|:---|:---|
| 구획 | `compartment` |
| 대사물 | `species` |
| 반응 | `reaction`, `speciesReference` |
| 반응 방향성 | `reversible`와 FBC bounds |
| flux 하한·상한 | `fbc:lowerFluxBound`, `fbc:upperFluxBound` |
| 목적함수 | `fbc:listOfObjectives`, `fbc:fluxObjective` |
| 유전자 | `fbc:geneProduct` |
| GPR | `fbc:geneProductAssociation`의 `and`/`or` |
| subsystem | Groups package 또는 주석 |
| 외부 DB ID | `annotation`의 MIRIAM URI |

{% hint style="warning" %}
SBML Core만 읽고 FBC를 무시하면 반응식은 남아도 목적함수·bound·GPR이 사라질 수 있습니다. “파일이 열렸다”와 “동일한 GEM이 재현됐다”는 같은 말이 아닙니다.
{% endhint %}

## 3. 대사물과 반응을 읽는 법

아래는 세포질 포도당의 단순화된 예입니다.

```xml
<species id="M_glc__D_c"
         name="D-Glucose"
         compartment="c"
         boundaryCondition="false"
         fbc:chemicalFormula="C6H12O6"
         fbc:charge="0"/>
```

반응은 반응물과 생성물의 목록으로 저장합니다.

```xml
<reaction id="R_PGI" name="phosphoglucose isomerase" reversible="true">
  <listOfReactants>
    <speciesReference species="M_g6p_c" stoichiometry="1"/>
  </listOfReactants>
  <listOfProducts>
    <speciesReference species="M_f6p_c" stoichiometry="1"/>
  </listOfProducts>
</reaction>
```

`id`는 기계가 참조하는 안정적 식별자이고 `name`은 사람이 읽는 이름입니다. 모델 병합에서는 이름보다 식별자와 외부 DB 매핑을 우선해야 합니다.

## 4. 세 가지 경계 반응

| 유형 | 전형적 반응식 | 방향 | 목적 |
|:---|:---|:---|:---|
| Exchange | `glc__D_e ↔ ∅` | uptake·secretion 설정에 따라 양방향 | 외부 환경과 교환 |
| Demand | `atp_c → ∅` | 보통 단방향 | 특정 대사물의 생산 능력 측정·소비 허용 |
| Sink | `met_c ↔ ∅` | 양방향 | 미확인 생산·소비 경로를 임시 허용 |

Demand와 sink는 편리하지만 모델의 결함을 숨길 수 있습니다. 특히 sink를 열어 둔 채 성장이나 표적 생산을 분석하면 존재하지 않는 경로가 물질을 공급할 수 있습니다. [Chapter 5의 gap-filling과 QC](../chapter-5/README.md)에서 이를 다시 점검합니다.

## 5. 바이오매스와 ATP maintenance

**바이오매스 반응**도 SBML에서는 다른 반응과 같은 형식으로 저장됩니다. 차이는 단백질·RNA·DNA·지질·세포벽 전구체와 에너지 비용이 매우 긴 화학량론 계수로 들어가고 FBC 목적함수의 계수가 보통 1로 설정된다는 점입니다.

**ATPM**은 다음과 같은 비성장 유지 에너지 소비를 나타냅니다.

$$
ATP+H_2O\rightarrow ADP+P_i+H^+
$$

ATPM의 하한이 NGAM이며, 바이오매스 반응에 포함된 ATP 가수분해 계수가 GAM입니다. 기질 흡수율과 성장률 관계를 현실적으로 재현하려면 둘을 구분해야 합니다. 자세한 생물학적 해석은 [Chapter 3 §6](../chapter-3/README.md)을 참고하십시오.

## 6. COBRApy로 읽기, 검사, 다시 저장하기

```python
import cobra

# COBRApy가 공개 model repository에서 모델을 불러와 캐시에 저장합니다.
# 따라서 작업 폴더에 iML1515.xml이 미리 있을 필요가 없습니다.
model = cobra.io.load_model("iML1515")

print(model.id)
print(len(model.metabolites), len(model.reactions), len(model.genes))
print(model.objective.expression)
print(model.solver)

# 경계 반응과 ATP maintenance 확인
print(len(model.exchanges), len(model.demands), len(model.sinks))
print(model.reactions.get_by_id("ATPM").bounds)

# SBML로 내보낸 뒤 그 파일을 다시 읽어 round-trip 검증
roundtrip_path = "iML1515.roundtrip.xml"
cobra.io.write_sbml_model(model, roundtrip_path)
reloaded = cobra.io.read_sbml_model(roundtrip_path)

assert len(reloaded.reactions) == len(model.reactions)
assert len(reloaded.metabolites) == len(model.metabolites)
assert len(reloaded.genes) == len(model.genes)
```

텍스트 편집기에서 XML을 열어보는 것은 구조를 이해하는 데 유용하지만, 대형 GEM을 손으로 직접 고치는 주 작업 방식으로는 권장하지 않습니다. COBRApy/RAVEN 같은 라이브러리로 수정하고 검증한 뒤, Git diff로 변경을 검토하십시오.

## 7. round-trip 검증 체크리스트

다른 도구로 저장한 뒤 다시 읽을 때 단순한 개수만 비교하면 충분하지 않습니다.

1. 모델·반응·대사물·유전자 ID가 보존됐는가?
2. 모든 반응의 화학량론과 방향성이 같은가?
3. lower/upper bound와 활성 목적함수가 같은가?
4. GPR의 불리언 의미(AND·OR 우선순위)가 보존됐는가? 단, 결합법칙상 같은 괄호를 펼치는 문자열 정규화는 허용한다.
5. 구획, 화학식, 전하, SBO term과 외부 DB 주석이 남았는가?
6. exchange/demand/sink 분류가 같은가?
7. 동일 배지에서 최적 목적함수값과 FVA 범위가 같은가?
8. MEMOTE 결과가 동일하거나 차이의 이유가 설명되는가?

```python
from cobra.util.solver import linear_reaction_coefficients

def reaction_signature(model):
    return {
        r.id: (
            tuple(sorted((m.id, float(c)) for m, c in r.metabolites.items())),
            float(r.lower_bound),
            float(r.upper_bound),
        )
        for r in model.reactions
    }

assert reaction_signature(model) == reaction_signature(reloaded)
assert {m.id for m in model.metabolites} == {m.id for m in reloaded.metabolites}
assert {g.id for g in model.genes} == {g.id for g in reloaded.genes}

# 목적함수 계수도 반응별로 비교한다.
def objective_signature(model):
    return {
        reaction.id: float(coefficient)
        for reaction, coefficient in linear_reaction_coefficients(model).items()
    }

assert objective_signature(model) == objective_signature(reloaded)

# SBML 왕복 과정에서 `a and (b and c)`가 `a and b and c`로 정규화될 수 있다.
# 문자열 대신 COBRApy GPR 객체의 symbolic equality로 불리언 의미를 비교한다.
for reaction in model.reactions:
    other = reloaded.reactions.get_by_id(reaction.id)
    assert reaction.gpr == other.gpr
```

GPR은 문자열 완전일치로 검사하지 마십시오. 결합법칙상 동치인 괄호가 저장 과정에서 펼쳐질 수 있기 때문입니다. 반대로 `and`가 `or`로 바뀌거나 우선순위가 달라지는 변화는 위의 symbolic equality에서 실패합니다.

## 8. 주석과 표준 식별자

재사용 가능한 SBML은 반응식만 맞는 파일이 아닙니다. 각 요소가 ChEBI, Rhea, KEGG, MetaNetX, UniProt, HGNC 등 외부 자원에 연결되어야 합니다.

- **MIRIAM** 원칙은 모델 구성 요소를 영구적이고 해석 가능한 URI로 주석하는 관행을 제공합니다.
- **SBO(Systems Biology Ontology)** term은 exchange reaction, biomass reaction, flux bound 같은 역할을 기계가 해석하도록 돕습니다.
- 동일 화합물이 protonation state·구획·식별자 체계 때문에 중복되는지 확인해야 합니다.

이 주석 품질은 [MEMOTE](../chapter-5/README.md)의 annotation 점수와 모델 병합 성공률에 직접 영향을 줍니다.

## 9. 흔한 실패와 진단 순서

| 증상 | 가능한 원인 | 먼저 확인할 것 |
|:---|:---|:---|
| 모델은 열리지만 성장하지 않음 | 목적함수·배지 bound 소실 | `model.objective`, `model.medium` |
| 유전자 결실이 아무 효과 없음 | GPR/FBC 미지원 또는 파싱 손실 | `reaction.gene_reaction_rule` |
| 무한 ATP 생성 | 잘못된 가역성·sink·질량 불균형 | ATP yield test, loopless FVA |
| 대사물 중복 | ID·구획·protonation 불일치 | formula, charge, annotation |
| 도구마다 결과가 다름 | solver tolerance 또는 SBML package 지원 차이 | 버전·solver·FBC 지원 |

## 10. 다음 읽기

- SBML 안에 들어가는 GPR·구획·경계·바이오매스: [Chapter 3](../chapter-3/README.md)
- SBML을 만들고 MEMOTE로 검증하는 재구축 과정: [Chapter 5](../chapter-5/README.md)
- 목적함수·bound가 실제 계산에 미치는 영향: [Chapter 4](../chapter-4/README.md)

## 참고 자료

1. Hucka, M. et al. (2019). [The Systems Biology Markup Language (SBML): Language Specification for Level 3 Version 2 Core Release 2](https://doi.org/10.1515/jib-2019-0021). *Journal of Integrative Bioinformatics*.
2. Olivier, B. G., & Bergmann, F. T. (2018). [SBML Level 3 Package: Flux Balance Constraints version 2](https://doi.org/10.1515/jib-2017-0082). *Journal of Integrative Bioinformatics*.
3. [SBML Level 3 FBC 공식 명세](https://sbml.org/documents/specifications/level-3/version-1/fbc)
4. [COBRApy 공식 문서](https://opencobra.github.io/cobrapy/)
5. [BioModels](https://www.ebi.ac.uk/biomodels/) · [BiGG Models](http://bigg.ucsd.edu/)
