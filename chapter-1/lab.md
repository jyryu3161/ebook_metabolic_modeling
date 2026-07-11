# 실습: COBRApy 모델의 구성요소 조사

## 이 실습에서 하는 일

이 실습에서는 Python 라이브러리 **[COBRApy](https://opencobra.github.io/cobrapy/)**(Constraints-Based Reconstruction and Analysis in Python)로 교육용 *E. coli* core 모델을 불러와, 대사 네트워크가 어떤 구성요소로 이루어져 있는지 직접 열어 봅니다. 앞 절([1장 1절](01.md))에서 정의한 **대사물**(metabolite)·**반응**(reaction)·**[플럭스](../glossary.md)**(flux) 개념을 실제 모델 객체에서 눈으로 확인하는 것이 목표입니다.

이 모델은 이 책 전체에서 반복적으로 등장할 "동반 모델(companion model)"입니다. 앞으로 [Chapter 2](../chapter-2/README.md)에서는 이 모델의 화학량론 행렬을, [Chapter 3](../chapter-3/README.md)에서는 이 모델의 GPR과 구획 구조를, [Chapter 4](../chapter-4/README.md)에서는 이 모델로 실제 FBA를 실행하는 법을 배우게 됩니다. 지금은 첫 만남으로서, 이 모델이 "무엇으로 이루어져 있는지" 개수와 구조만 살펴봅니다.

## 학습 목표

이 실습을 마치면 다음을 수행할 수 있습니다.

1. COBRApy로 교육용 *E. coli* core 모델을 불러온다(load).
2. 모델의 반응·대사물·유전자 개수를 확인한다.
3. 반응과 대사물의 ID·이름과 구획 표기(`_c`, `_e`)를 읽어 해석한다.
4. 반응 객체 하나에서 이름·반응식·경계조건(bounds)·GPR을 조사한다.
5. 코어 모델과 완전한 게놈 규모 모델(iML1515)의 차이를 설명한다.

## 준비물

- **실행 환경**: [Chapter 11 §1](../chapter-11/01.md)(환경·솔버·Gurobi 라이선스) 또는 [설치 가이드](../installation.md)를 따라 Python 3.10 이상 가상환경과 Jupyter 커널을 준비합니다. 시스템 Python에 바로 설치하지 말고 프로젝트별 가상환경을 쓰면 버전 충돌을 피할 수 있습니다.
- **필요한 패키지**: COBRApy(권장 버전 0.30.0). 아직 설치하지 않았다면 가상환경을 활성화한 상태에서 `pip install "cobra==0.30.0"`로 설치합니다. 첫 실행에는 모델을 내려받기 위한 인터넷 연결이 필요할 수 있습니다.
- **선행 셀**: 별도의 선행 실습 없이 독립적으로 실행할 수 있습니다. 다만 아래 코드는 **위에서부터 순서대로** 실행해야 합니다. 단계 1에서 만든 `model` 변수를 이후 모든 단계에서 계속 사용하기 때문입니다.
- **사용하는 모델**: `e_coli_core`(별칭 `textbook`). 반응 95개, 대사물 72개, 유전자 137개로 이루어진 교육용 네트워크입니다.

{% hint style="info" %}
**독립 실행:** 먼저 [재현 가능한 실습 환경](../installation.md)의 core 패키지와 Jupyter kernel을 준비하십시오. `load_model("textbook")`은 캐시에 모델이 없으면 원격 저장소에서 내려받으므로 첫 실행에는 네트워크가 필요할 수 있습니다. 장기 분석에서는 이름과 캐시만 믿지 말고 Chapter 10처럼 [SBML](https://sbml.org/)과 checksum을 보존합니다.
{% endhint %}

## 실습 단계

### 단계 1. 모델 불러오고 구성요소 개수 세기

**무엇을·왜.** 가장 먼저 COBRApy로 모델을 메모리에 불러온 뒤, 이 모델이 반응·대사물·유전자를 각각 몇 개 담고 있는지 세어 봅니다. 개수를 세는 것은 모델의 규모를 가장 빠르게 파악하는 방법이며, 이후 단계에서 사용할 `model` 객체를 만드는 준비 과정이기도 합니다.

**코드.** 아래 코드는 모델을 불러오고, 모델 ID와 세 구성요소의 개수를 출력합니다. `len(...)`은 목록의 길이를 세는 Python 기본 함수입니다.

```python
import cobra

# COBRApy 모델 저장소의 교육용 E. coli core 모델을 내려받거나 캐시에서 불러오기
model = cobra.io.load_model("textbook")

print(f"모델 ID: {model.id}")
print(f"반응 수: {len(model.reactions)}")
print(f"대사물 수: {len(model.metabolites)}")
print(f"유전자 수: {len(model.genes)}")
```

**예상 출력.**

```
모델 ID: e_coli_core
반응 수: 95
대사물 수: 72
유전자 수: 137
```

**확인 포인트.** 모델 ID가 `e_coli_core`로 나오고 반응 95, 대사물 72, 유전자 137이 그대로 출력되면 성공입니다. 이 세 숫자는 이후 단계의 기준값이 됩니다.

**자주 나는 오류와 해결.**

{% hint style="warning" %}
**해석상의 주의(문제 해결 팁):** `cobra.io.load_model("textbook")` 실행 시 `ModuleNotFoundError: No module named 'cobra'` 오류가 뜬다면 COBRApy가 설치되지 않은 것입니다(`pip install cobra`로 해결). 네트워크 연결 문제로 다운로드가 실패한다면, COBRApy 저장소에서 `e_coli_core` 모델의 SBML 파일을 직접 내려받아 `cobra.io.read_sbml_model("경로/e_coli_core.xml")`로 불러올 수도 있습니다. 두 방법 모두 결과는 동일한 `e_coli_core` 모델을 만듭니다.
{% endhint %}

### 단계 2. 반응 목록 훑어보기

**무엇을·왜.** 숫자만 세는 것보다, 실제로 반응이 어떻게 이름 붙여져 있고 어떤 반응식을 가지는지 눈으로 보면 모델의 감을 잡는 데 도움이 됩니다. 여기서는 앞의 5개 반응만 뽑아 ID와 반응식을 나란히 출력합니다.

**코드.** `model.reactions[:5]`는 반응 목록의 처음 5개를 뜻합니다. `rxn.id`는 반응 ID, `rxn.reaction`은 사람이 읽을 수 있는 반응식 문자열입니다.

```python
# 처음 5개 반응의 ID와 반응식을 출력
for rxn in model.reactions[:5]:
    print(f"{rxn.id:10s} : {rxn.reaction}")
```

**예상 출력.** 반응의 순서는 모델 버전에 따라 달라질 수 있습니다.

```
ACALD      : acald_c + coa_c + nad_c <=> accoa_c + h_c + nadh_c
ACALDt     : acald_e <=> acald_c
ACKr       : ac_c + atp_c <=> actp_c + adp_c
ACONTa     : cit_c <=> acon_C_c + h2o_c
ACONTb     : acon_C_c + h2o_c <=> icit_c
```

**확인 포인트.** ID(예: `ACALD`)와 반응식(예: `acald_c + coa_c + nad_c <=> accoa_c + h_c + nadh_c`)이 짝지어 5줄이 출력되면 성공입니다. `<=>` 기호는 정·역 양방향이 허용된 가역 반응을 나타냅니다.

### 단계 3. 대사물 목록과 구획 표기 읽기

**무엇을·왜.** 이번에는 대사물 쪽을 살펴봅니다. 대사물 ID 끝에 붙은 접미사가 구획을 나타낸다는 점을 확인하는 것이 핵심입니다. **[구획](../glossary.md)**(compartment)은 세포질·세포외처럼 대사물이 존재하는 공간을 뜻합니다.

**코드.** `model.metabolites[:5]`는 대사물 목록의 처음 5개입니다. `met.id`는 대사물 ID, `met.name`은 사람이 읽는 이름입니다.

```python
# 처음 5개 대사물의 ID와 이름을 출력
for met in model.metabolites[:5]:
    print(f"{met.id:10s} : {met.name}")
```

**예상 출력.**

```
13dpg_c    : 3-Phospho-D-glyceroyl phosphate
2pg_c      : D-Glycerate 2-phosphate
3pg_c      : 3-Phospho-D-glycerate
6pgc_c     : 6-Phospho-D-gluconate
6pgl_c     : 6-phospho-D-glucono-1,5-lactone
```

**확인 포인트.** 대사물 ID(예: `13dpg_c`)와 이름(예: `3-Phospho-D-glyceroyl phosphate`)이 짝지어 5줄이 출력되면 성공입니다. 모든 ID가 `_c`로 끝난다는 점에 주목합니다.

대사물 ID 끝에 붙은 `_c`, `_e`는 각각 세포질(cytoplasm)과 세포외(extracellular) [구획](../glossary.md)을 나타냅니다. 이 모델은 구획 2개(c, e)만을 가진 비교적 단순한 모델이며, 구획이 무엇이고 왜 중요한지는 [Chapter 3](../chapter-3/README.md)에서 자세히 다룹니다.

### 단계 4. 반응 하나를 골라 그 안의 정보 열어보기

**무엇을·왜.** 숫자 세기(단계 1)와 목록 훑어보기(단계 2~3)를 넘어, 반응 객체 하나를 골라 그 안에 어떤 정보가 들어 있는지 자세히 살펴봅니다. `PGI` 반응을 예로 들어 이름·반응식·경계조건(bounds)·GPR이라는 네 가지 핵심 정보를 한꺼번에 꺼내 봅니다.

{% hint style="info" %}
`PGI`(phosphoglucose isomerase)는 [Chapter 2](../chapter-2/README.md)에서 [화학량론 행렬](../glossary.md) $$\mathbf{S}$$의 한 열을 구성하는 예로 다시 사용한다. 여기서는 반응식, bounds와 GPR을 함께 기록해 두면 후속 계산을 동일한 객체에서 추적할 수 있다.
{% endhint %}

**코드.** `get_by_id("PGI")`는 ID로 특정 반응 객체 하나를 찾아옵니다. `lower_bound`/`upper_bound`는 허용된 플럭스 경계, `gene_reaction_rule`은 이 반응과 연관된 유전자 규칙(GPR)입니다.

```python
pgi = model.reactions.get_by_id("PGI")

print(f"반응 이름: {pgi.name}")
print(f"반응식: {pgi.reaction}")
print(f"하한/상한: {pgi.lower_bound} / {pgi.upper_bound}")
print(f"연관 유전자(GPR): {pgi.gene_reaction_rule}")
```

**예상 출력.**

```
반응 이름: glucose-6-phosphate isomerase
반응식: g6p_c <=> f6p_c
하한/상한: -1000.0 / 1000.0
연관 유전자(GPR): b4025
```

**확인 포인트.** 반응 이름이 `glucose-6-phosphate isomerase`, 반응식이 `g6p_c <=> f6p_c`, 하한/상한이 `-1000.0 / 1000.0`, GPR이 `b4025`로 출력되면 성공입니다.

여기서 하한이 음수(-1000.0)이고 상한이 양수(1000.0)라는 것은, [1장 1절](01.md)에서 정의했듯이 저장된 반응식의 정·역방향 [플럭스](../glossary.md)를 모두 허용한다는 뜻입니다. 플럭스는 반응이 진행되는 속도로, 흔히 $$\mathrm{mmol\,gDW^{-1}\,h^{-1}}$$(단위 건조 세포 질량·단위 시간당 물질량) 단위로 나타냅니다. 음의 플럭스는 저장된 반응식의 역방향을 의미합니다. 그리고 `gene_reaction_rule`에 `b4025`라는 유전자 하나가 표시된 것은, 이 반응이 그 유전자 하나에 의해서만 촉매됨을 뜻합니다. 반응에 따라서는 여러 유전자가 `and`/`or`로 묶여 나타나기도 하는데, 이 논리 구조는 [Chapter 3](../chapter-3/README.md)에서 자세히 다룹니다. 지금은 "반응 객체 하나에 이름·반응식·플럭스 경계(bounds)·[GPR](../chapter-3/README.md)이라는 네 가지 핵심 정보가 함께 들어 있다"는 것만 확인하고 넘어갑니다.

**해석 확인.** `pgi.lower_bound = 0`, `pgi.upper_bound = 1000`이면 모델에 기록된 정방향 플럭스만 허용되므로 비가역 반응으로 취급된다. 화학량론 열은 그대로이며 방향성 정보는 bounds에 저장된다.

하한이 0이라는 것은 모델에서 역방향 플럭스를 허용하지 않도록 설정했다는 뜻입니다. 이는 제2장 §1.2에서 다룰 방향성 플럭스 경계이며, 이 설정만으로 해당 조건의 열역학적 가역성이 직접 증명되는 것은 아닙니다. 이렇게 `lower_bound`와 `upper_bound`라는 두 숫자로 반응의 방향성 제약을 표현할 수 있다는 점이 COBRApy와 GEM의 실용적인 설계입니다.

이제 기록한 PGI의 화학량론 계수는 Chapter 2 실습에서 $$\mathbf S$$의 한 열로 확인하고, GPR·구획·경계 반응의 구조적 의미는 Chapter 3에서 분리해 검토합니다.

### 단계 5. 이 모델이 "코어(core)"라는 의미 되새기기

**무엇을·왜.** 이 단계에는 실행할 코드가 없습니다. 지금까지 확인한 숫자와 구조가 무엇을 의미하는지, 왜 이렇게 작은 모델로 시작하는지를 정리하는 개념 단계입니다.

이 72개 대사물, 95개 반응, 137개 유전자로 구성된 "코어 모델"은 해당과정, TCA 회로, 산화적 인산화 등 중심 탄소 대사만을 포함한 축소판으로, [iML1515](https://bigg.ucsd.edu/models/iML1515)(반응 2,712개) 같은 완전한 게놈 규모 모델과 대비됩니다. 이 책이 완전한 게놈 규모 모델 대신 이 작은 코어 모델로 시작하는 이유는 분명합니다. 95개 반응은 사람이 한눈에 훑어볼 수 있는 규모이면서도, 게놈 규모 모델이 가진 핵심 구조(화학량론, GPR, 구획, [목적함수](../glossary.md))를 모두 갖추고 있기 때문입니다. 작은 지도로 지도 읽는 법을 먼저 익힌 뒤, 큰 지도로 넘어가는 것입니다.

**확인 포인트.** 코어 모델과 iML1515의 규모 차이를 설명할 수 있고, "네트워크 규모는 생물 종의 고정된 특성이 아니라 모델 버전·재구축 범위의 속성"이라는 점([1장 5절](01.md))을 말로 정리할 수 있으면 이 실습의 개념 목표에 도달한 것입니다.

{% hint style="info" %}
이 실습은 객체 구조와 경계조건을 읽는 단계까지 다룬다. 성장률 최적화와 해 상태·잔차 검산은 [Chapter 4](../chapter-4/README.md), 환경·solver·파일 hash를 포함한 완전한 실행 기록은 [Chapter 10](../chapter-10/README.md)에서 이어진다.
{% endhint %}

## 정리

- COBRApy로 교육용 *E. coli* core 모델(`e_coli_core`)을 불러오고, 반응 95·대사물 72·유전자 137이라는 규모를 확인했습니다.
- 반응과 대사물의 ID·이름을 훑어보고, 대사물 ID의 `_c`·`_e` 접미사가 세포질·세포외 구획을 뜻한다는 것을 읽었습니다.
- `PGI` 반응 하나를 열어 이름·반응식·경계조건(bounds)·GPR이 한 객체에 함께 담겨 있음을 확인했습니다.
- 경계조건의 부호가 반응의 방향성을 어떻게 표현하는지, 코어 모델과 게놈 규모 모델의 차이가 무엇인지 정리했습니다.

## 스스로 해보기

아래 과제는 지금까지 배운 코드를 조금씩 바꿔 보는 연습입니다. 정답 코드는 바로 제시하지 않으니, 단계 1~4의 코드를 참고해 직접 수정해 봅니다.

1. 단계 2와 단계 3에서 `[:5]`를 `[:10]`으로 바꾸면 몇 줄이 출력되는지 예상한 뒤 실행해 확인해 봅니다.
2. 단계 4의 `"PGI"` 자리에 다른 반응 ID(예: 단계 2에서 본 `ACKr`)를 넣어 그 반응의 하한·상한과 GPR을 조사해 봅니다. 하한이 음수인지 0인지에 따라 가역·비가역이 어떻게 달라지는지 살펴봅니다.
3. `model.compartments`를 출력해 이 모델이 가진 구획의 전체 목록을 확인하고, 단계 3에서 관찰한 `_c`·`_e`와 대응되는지 비교해 봅니다.

## 다음 단계

- 화학량론 행렬 $$\mathbf{S}$$의 구성은 [Chapter 2](../chapter-2/README.md)에서 이어집니다.
- GPR과 구획 구조의 자세한 의미는 [Chapter 3](../chapter-3/README.md)에서 다룹니다.
- 이 모델로 성장률을 최적화하는 FBA는 [Chapter 4](../chapter-4/README.md)에서, 환경·solver·파일 hash까지 포함한 완전한 실행 기록은 [Chapter 10](../chapter-10/README.md)에서 다룹니다.

---
