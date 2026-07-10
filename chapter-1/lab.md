# 💡 실습: COBRApy로 첫 GEM 만나기

이론적 개념을 확인하는 가장 좋은 방법은 실제로 모델을 열어 보는 것입니다. 여기서는 Python 라이브러리 **COBRApy**(Constraints-Based Reconstruction and Analysis in Python)를 이용해, 교육용으로 널리 쓰이는 *E. coli* core 모델을 불러오고 앞서 정의한 구성 요소(반응·대사물·유전자)의 개수를 확인해 보겠습니다.

이 모델은 **이 책 전체에서 반복적으로 등장할 "동반 모델(companion model)"**입니다. 앞으로 Chapter 2에서는 이 모델의 화학량론 행렬을, Chapter 3에서는 이 모델의 GPR과 구획 구조를, Chapter 4에서는 이 모델로 실제 FBA를 실행하는 법을 배우게 됩니다. 지금은 첫 만남으로서, 이 모델이 "무엇으로 이루어져 있는지" 개수만 세어 봅니다.

{% hint style="info" %}
✅ **독립 실행:** 먼저 재현 가능한 실습 환경의 core 패키지와 Jupyter kernel을 준비하십시오. `load_model("textbook")`은 캐시에 모델이 없으면 원격 저장소에서 내려받으므로 첫 실행에는 네트워크가 필요할 수 있습니다. 장기 분석에서는 이름과 캐시만 믿지 말고 Chapter 10처럼 SBML과 checksum을 보존합니다.
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
💡 **팁:** 위 코드에서 `PGI`(포스포글루코스 이성질화효소, phosphoglucose isomerase)라는 반응 ID를 기억해 두세요. 이 반응은 해당과정의 두 번째 단계를 촉매하며, [Chapter 2](../chapter-2/README.md)에서 화학량론 행렬 $$\mathbf{S}$$의 한 열(column)이 실제로 어떻게 구성되는지 보여주는 대표 예시로 다시 등장합니다.
{% endhint %}

**3단계 — 이 모델이 "코어(core)"라는 의미 되새기기**

이 72개 대사물, 95개 반응, 137개 유전자로 구성된 "코어 모델"은 해당과정, TCA 회로, 산화적 인산화 등 중심 탄소 대사만을 포함한 축소판으로, iML1515(반응 2,712개) 같은 완전한 게놈 규모 모델과 대비됩니다. 왜 이 책은 완전한 게놈 규모 모델이 아니라 이 작은 코어 모델로 시작할까요? 이유는 간단합니다 — 95개 반응은 사람이 한눈에 훑어볼 수 있는 규모이면서도, 게놈 규모 모델이 가진 핵심 구조(화학량론, GPR, 구획, 목적함수)를 모두 갖추고 있기 때문입니다. 작은 지도로 지도 읽는 법을 먼저 익힌 뒤, 큰 지도로 넘어가는 것입니다.

{% hint style="info" %}
💡 **팁:** 이 장에서 실행한 코드는 COBRApy 설치와 모델 불러오기의 "맛보기"입니다. 설치 과정(Gurobi 등 solver 설정 포함)과 iML1515·Recon3D 같은 대형 모델을 불러와 원핵생물·진핵생물 모델을 비교하는 전체 실습은 이번 주차 실습 노트북 `gem9_w01_lab.ipynb`에 있습니다. COBRApy로 실제 FBA를 실행하여 성장률을 계산하는 법은 [Chapter 4](../chapter-4/README.md)에서 이어집니다.
{% endhint %}

---
