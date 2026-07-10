# 실습: COBRApy 모델의 구성요소 조사

이론적 개념을 확인하는 가장 좋은 방법은 실제로 모델을 열어 보는 것입니다. 여기서는 Python 라이브러리 **COBRApy**(Constraints-Based Reconstruction and Analysis in Python)를 이용해, 교육용으로 널리 쓰이는 *E. coli* core 모델을 불러오고 앞서 정의한 구성 요소(반응·대사물·유전자)의 개수를 확인해 보겠습니다.

이 모델은 **이 책 전체에서 반복적으로 등장할 "동반 모델(companion model)"**입니다. 앞으로 Chapter 2에서는 이 모델의 화학량론 행렬을, Chapter 3에서는 이 모델의 GPR과 구획 구조를, Chapter 4에서는 이 모델로 실제 FBA를 실행하는 법을 배우게 됩니다. 지금은 첫 만남으로서, 이 모델이 "무엇으로 이루어져 있는지" 개수만 세어 봅니다.

{% hint style="info" %}
✅ **독립 실행:** 먼저 재현 가능한 실습 환경의 core 패키지와 Jupyter kernel을 준비하십시오. `load_model("textbook")`은 캐시에 모델이 없으면 원격 저장소에서 내려받으므로 첫 실행에는 네트워크가 필요할 수 있습니다. 장기 분석에서는 이름과 캐시만 믿지 말고 Chapter 10처럼 SBML과 checksum을 보존합니다.
{% endhint %}

{% hint style="warning" %}
❓ **흔한 오해(문제 해결 팁):** `cobra.io.load_model("textbook")` 실행 시 `ModuleNotFoundError: No module named 'cobra'` 오류가 뜬다면 COBRApy가 설치되지 않은 것입니다(`pip install cobra`로 해결). 네트워크 연결 문제로 다운로드가 실패한다면, COBRApy 저장소에서 `e_coli_core` 모델의 SBML 파일을 직접 내려받아 `cobra.io.read_sbml_model("경로/e_coli_core.xml")`로 불러올 수도 있습니다. 두 방법 모두 결과는 동일한 `e_coli_core` 모델을 만듭니다.
{% endhint %}

**1단계 — 모델 불러오기**

```python
import cobra

# COBRApy 모델 저장소의 교육용 E. coli core 모델을 내려받거나 캐시에서 불러오기
model = cobra.io.load_model("textbook")

print(f"모델 ID: {model.id}")
print(f"반응 수: {len(model.reactions)}")
print(f"대사물 수: {len(model.metabolites)}")
print(f"유전자 수: {len(model.genes)}")

# 기대 출력:
# 모델 ID: e_coli_core
# 반응 수: 95
# 대사물 수: 72
# 유전자 수: 137
```

**2단계 — 반응·대사물을 몇 개만 들여다보기**

숫자만 세는 것보다, 실제로 반응과 대사물이 어떻게 이름 붙여져 있는지 눈으로 보는 것이 감을 잡는 데 도움이 됩니다.

```python
# 처음 5개 반응의 ID와 반응식을 출력
for rxn in model.reactions[:5]:
    print(f"{rxn.id:10s} : {rxn.reaction}")

# 기대 출력(예시, 순서는 버전에 따라 다를 수 있음):
# ACALD      : acald_c + coa_c + nad_c <=> accoa_c + h_c + nadh_c
# ACALDt     : acald_e <=> acald_c
# ACKr       : ac_c + atp_c <=> actp_c + adp_c
# ACONTa     : cit_c <=> acon_C_c + h2o_c
# ACONTb     : acon_C_c + h2o_c <=> icit_c
```

```python
# 처음 5개 대사물의 ID와 이름을 출력
for met in model.metabolites[:5]:
    print(f"{met.id:10s} : {met.name}")

# 기대 출력(예시):
# 13dpg_c    : 3-Phospho-D-glyceroyl phosphate
# 2pg_c      : D-Glycerate 2-phosphate
# 3pg_c      : 3-Phospho-D-glycerate
# 6pgc_c     : 6-Phospho-D-gluconate
# 6pgl_c     : 6-phospho-D-glucono-1,5-lactone
```

대사물 ID 끝에 붙은 `_c`, `_e`는 각각 세포질(cytoplasm)과 세포외(extracellular) 구획을 나타냅니다. 이 모델은 구획 2개(c, e)만을 가진 비교적 단순한 모델이며, 구획이 무엇이고 왜 중요한지는 [Chapter 3](../chapter-3/README.md)에서 자세히 다룹니다.

{% hint style="info" %}
`PGI`(phosphoglucose isomerase)는 [Chapter 2](../chapter-2/README.md)에서 화학량론 행렬 $$\mathbf{S}$$의 한 열을 구성하는 예로 다시 사용한다. 여기서는 반응식, bounds와 GPR을 함께 기록해 두면 후속 계산을 동일한 객체에서 추적할 수 있다.
{% endhint %}

**3단계 — 반응 하나를 골라 그 안에 담긴 정보를 모두 열어보기**

숫자 세기(1단계)와 목록 훑어보기(2단계)를 넘어, 반응 객체 하나를 골라 그 안에 어떤 정보가 들어 있는지 좀 더 자세히 살펴봅시다. `PGI` 반응을 예로 들겠습니다.

```python
pgi = model.reactions.get_by_id("PGI")

print(f"반응 이름: {pgi.name}")
print(f"반응식: {pgi.reaction}")
print(f"하한/상한: {pgi.lower_bound} / {pgi.upper_bound}")
print(f"연관 유전자(GPR): {pgi.gene_reaction_rule}")

# 기대 출력(예시):
# 반응 이름: glucose-6-phosphate isomerase
# 반응식: g6p_c <=> f6p_c
# 하한/상한: -1000.0 / 1000.0
# 연관 유전자(GPR): b4025
```

여기서 하한이 음수(-1000.0)이고 상한이 양수(1000.0)라는 것은, 이 반응이 §3.1에서 언급한 **가역(reversible)** 반응이라는 뜻입니다(음의 통량은 역반응 방향을 의미합니다). 그리고 `gene_reaction_rule`에 `b4025`라는 유전자 하나가 표시된 것은, 이 반응이 그 유전자 하나에 의해서만 촉매됨을 뜻합니다. 반응에 따라서는 여러 유전자가 `and`/`or`로 묶여 나타나기도 하는데, 이 논리 구조는 [Chapter 3](../chapter-3/README.md)에서 자세히 다룹니다. 지금은 "반응 객체 하나에 이름·반응식·bounds·GPR이라는 네 가지 핵심 정보가 함께 들어 있다"는 것만 확인하고 넘어갑니다.

**해석 확인.** `pgi.lower_bound = 0`, `pgi.upper_bound = 1000`이면 모델에 기록된 정방향 플럭스만 허용되므로 비가역 반응으로 취급된다. 화학량론 열은 그대로이며 방향성 정보는 bounds에 저장된다.

비가역입니다. 하한이 0이라는 것은 "역방향으로는 흐를 수 없다"(음의 통량 불가)는 뜻이므로, §4.1에서 배운 열역학적 제약 $$v_j \geq 0$$에 해당합니다. 이렇게 `lower_bound`와 `upper_bound`라는 두 숫자만으로 반응의 방향성 정보 전체를 표현할 수 있다는 점이 COBRApy(와 GEM 전반)의 실용적인 설계입니다.

**4단계 — 이 모델이 "코어(core)"라는 의미 되새기기**

이 72개 대사물, 95개 반응, 137개 유전자로 구성된 "코어 모델"은 해당과정, TCA 회로, 산화적 인산화 등 중심 탄소 대사만을 포함한 축소판으로, iML1515(반응 2,712개) 같은 완전한 게놈 규모 모델과 대비됩니다. 왜 이 책은 완전한 게놈 규모 모델이 아니라 이 작은 코어 모델로 시작할까요? 이유는 간단합니다 — 95개 반응은 사람이 한눈에 훑어볼 수 있는 규모이면서도, 게놈 규모 모델이 가진 핵심 구조(화학량론, GPR, 구획, 목적함수)를 모두 갖추고 있기 때문입니다. 작은 지도로 지도 읽는 법을 먼저 익힌 뒤, 큰 지도로 넘어가는 것입니다.

{% hint style="info" %}
이 실습은 객체 구조와 경계조건을 읽는 단계까지 다룬다. 성장률 최적화와 해 상태·잔차 검산은 [Chapter 4](../chapter-4/README.md), 환경·solver·파일 hash를 포함한 완전한 실행 기록은 [Chapter 10](../chapter-10/README.md)에서 이어진다.
{% endhint %}

---
