# 실습: RNA-seq 발현 데이터를 GEM에 통합하기

> **실습 범위:** 아래 코드는 [COBRApy](https://opencobra.github.io/cobrapy/) 0.30.0의 `textbook` 모델([`e_coli_core`](http://bigg.ucsd.edu/models/e_coli_core): 반응 95개, 대사물 72개, 유전자 137개)에 합성 발현값을 통합합니다. 결과는 알고리즘 검산용이며 실제 조직의 생물학적 결론으로 해석하지 않습니다.
>
> **재현 조건:** 이 문서의 모든 수치는 COBRApy 0.30.0, 기본 솔버 GLPK 5.0(`optlang.glpk_interface`), 모델 허용오차 `model.tolerance = 1e-07`, 모델의 기본 배지와 `Biomass_Ecoli_core` 목적함수, `processes=1`, 그리고 본문에 표시한 난수 시드(`np.random.seed(0)`, `np.random.seed(42)`)에서 얻은 값입니다. 솔버·허용오차·시드 가운데 하나라도 다르면 마지막 자리 수치나 대체 최적해의 선택이 달라질 수 있습니다.

## 이 실습에서 하는 일

가상의 RNA-seq 발현값을 실제 대사 모델 `e_coli_core`에 단계별로 통합해 봅니다. 구체적으로 raw counts를 [TPM](../glossary.md)으로 정규화하고([4.1절](04.md)), 여러 임계값 방법을 비교하고([2.3절](02.md)), 실제 [GPR](../chapter-3/README.md)로 [반응 활성 점수](../glossary.md)(RAS)를 계산한 뒤([2.1~2.2절](02.md)), 그 RAS를 [GIMME](../landmark-papers.md)([3.2절](03.md))와 E-Flux([3.4절](03.md)) 제약으로 번역해 모델에 직접 실행합니다. 마지막에는 맥락 특이적 제약이 유전자 필수성 예측을 바꾸는지 계산으로 확인합니다. 이 실습은 [1절](01.md)의 7단계 통합 파이프라인 중 3~7단계를 손으로 따라가 보는 것입니다.

## 학습 목표

이 실습을 마치면 다음을 할 수 있습니다.

1. `counts_to_tpm` 함수로 raw counts를 TPM으로 **정규화하고** 합이 항상 100만이 되는지 **확인합니다**.
2. 고정·백분위수·z-score 세 가지 임계값 방법이 활성 유전자 수를 어떻게 다르게 만드는지 **비교합니다**.
3. COBRApy의 GPR 파서를 이용해 AND=min, OR=max 휴리스틱으로 RAS를 **계산합니다**.
4. GIMME 2단계 LP와 E-Flux 경계 스케일링을 `e_coli_core`에 **실행하고** 성장률 변화를 **해석합니다**.
5. generic 모델과 context 모델의 단일 유전자 결손 결과를 같은 기준으로 **비교합니다**.

## 준비물

- **실행 환경**: [Chapter 11 §1](../chapter-11/01.md)의 격리된 가상환경 또는 [설치 가이드](../installation.md)를 따라 Python 3.10 이상과 COBRApy 0.30.0을 준비하십시오. Jupyter Notebook 또는 IPython에서 셀을 순서대로 실행하는 방식을 권장합니다.
- **필요한 패키지**: `numpy`, `pandas`, `scipy`, `sympy`, `cobra`. 대부분 설치 가이드의 core 패키지에 포함됩니다.
- **모델**: `e_coli_core`(COBRApy에서는 `load_model("textbook")`으로 불러오는 교육용 *E. coli* 모델). 첫 실행에는 원격 저장소에서 내려받으므로 네트워크가 필요할 수 있습니다.
- **선행 셀 주의**: 이 실습은 앞 단계에서 만든 변수를 뒤 단계가 그대로 이어받습니다. 예를 들어 단계 4·5·7은 단계 3에서 만든 `reaction_weights`와 `model`을 사용하고, 단계 7은 단계 4에서 만든 `context_model`을 사용합니다. **반드시 단계 1부터 순서대로, 같은 세션(같은 노트북 커널) 안에서 실행하십시오.** 커널을 새로 시작했다면 앞 단계를 다시 실행해야 합니다.

flux는 `mmol gDW⁻¹ h⁻¹` 단위의 반응 진행률(속도)이고, 성장률은 biomass 반응의 flux로 단위가 `h⁻¹`입니다. 이 점을 기억하면 뒤에 나오는 성장률 숫자를 읽기 쉽습니다.

---

### 단계 1. Raw counts를 TPM으로 정규화하기

**무엇을·왜.** RNA-seq의 원시 계수(raw counts)는 라이브러리 크기와 유전자 길이에 의존하므로 그대로 반응 점수로 쓸 수 없습니다. [4.1절](04.md)에서 손으로 계산해 본 TPM 공식을 코드로 옮겨 정규화합니다. 핵심은 "길이로 나눈 비율(rate)을 구한 뒤, 그 비율의 합으로 다시 정규화해 항상 100만이 되도록 만든다"는 두 단계입니다.

**코드.** 아래 코드는 다섯 유전자의 counts와 길이로부터 TPM을 계산하고, 검증용으로 TPM의 합을 함께 출력합니다.

```python
import numpy as np

def counts_to_tpm(counts, gene_lengths):
    """raw counts를 TPM으로 변환: TPM_i = (counts_i/length_i) / sum_j(counts_j/length_j) * 1e6"""
    rate = counts / gene_lengths
    return rate / rate.sum() * 1e6

genes = ['HK2', 'PKM', 'LDHA', 'SDHA', 'FH']
raw_counts = np.array([850, 1200, 2400, 300, 210])
gene_lengths = np.array([2200, 1650, 1000, 1750, 1500])   # bp

tpm = counts_to_tpm(raw_counts, gene_lengths)
for g, v in zip(genes, tpm):
    print(f"{g:6s}: TPM = {v:8.2f}")
print(f"TPM 합계 (검증용, 항상 1e6): {tpm.sum():.1f}")

# 기대 출력:
# HK2   : TPM = 101008.39
# PKM   : TPM = 190133.43
# LDHA  : TPM = 627440.33  (길이가 짧고 counts가 높아 TPM이 가장 큼)
# SDHA  : TPM =  44817.17
# FH    : TPM =  36600.69
# TPM 합계 (검증용, 항상 1e6): 1000000.0
```

**예상 출력.** 콘솔에 다음이 그대로 나오면 성공입니다.

```
HK2   : TPM = 101008.39
PKM   : TPM = 190133.43
LDHA  : TPM = 627440.33
SDHA  : TPM =  44817.17
FH    : TPM =  36600.69
TPM 합계 (검증용, 항상 1e6): 1000000.0
```

**확인 포인트.** 마지막 줄의 TPM 합계가 `1000000.0`이면 정규화가 정확히 된 것입니다. 이 합이 100만이 아니면 계산 어딘가에서 길이나 counts가 잘못 들어간 것입니다.

**자주 나는 오류와 해결.**

- `ModuleNotFoundError: No module named 'numpy'` — numpy가 설치되지 않았습니다. 가상환경을 활성화한 뒤 `pip install numpy`로 설치하십시오.
- 숫자가 다르게 나온다 — `raw_counts`나 `gene_lengths` 배열의 값을 바꾸지 않았는지 확인하십시오. 위 숫자는 주어진 입력에서만 재현됩니다.

표준적인 full-length short-read RNA-seq에서는 같은 transcript molecule abundance라면 **긴 transcript가 더 많은 fragment를 생성**하므로 raw count의 기댓값이 길이에 비례합니다. TPM은 count를 유효 길이로 나누어 이 기회를 보정합니다. 이 합성 예제에서 LDHA는 count가 가장 높고 길이가 가장 짧아 $$2400/1000$$이 가장 크므로 TPM도 가장 큽니다.

{% hint style="warning" %}
**해석상의 주의:** LDHA의 TPM이 가장 크다는 것이 "짧은 유전자가 같은 발현에서 더 많은 count를 만든다"는 뜻은 아닙니다. 실제 정량에서는 gene length 대신 isoform abundance와 fragment length를 반영한 effective length를 사용해야 합니다([Oshlack & Wakefield, 2009](https://doi.org/10.1186/gb-2009-10-2-r14)).
{% endhint %}

### 단계 2. 발현 임계값 이산화 방법 비교하기

**무엇을·왜.** RAS 같은 연속 발현값을 "활성/비활성"으로 나눌 때 어떤 임계값 규칙을 쓰느냐에 따라 활성으로 분류되는 유전자 수가 크게 달라집니다. [2.3절](02.md)의 세 전략(고정값, 백분위수, 일반 z-score)을 같은 합성 데이터에 적용해 그 차이를 눈으로 확인합니다. 아래 `standard_zscore`는 전체 값의 평균·표준편차를 쓰는 탐색적 규칙이며 rFASTCORMICS의 zFPKM이 아닙니다.

**코드.** 이 코드는 세 방법으로 각각 활성 유전자 수를 세어 출력합니다. 결과를 재현하려면 `np.random.seed(42)`를 반드시 함께 실행해야 합니다.

```python
import pandas as pd
from scipy import stats

def discretize_expression(log2_expr, method='percentile', threshold=None):
    """연속 log2(TPM+1) 발현값을 이산 활성/비활성 라벨로 변환 (2.3절의 세 전략)"""
    if method == 'fixed':
        thr = threshold if threshold is not None else 1.0
        return (log2_expr > thr).astype(int)
    elif method == 'percentile':
        p75 = np.percentile(log2_expr, 75)          # 상위 25%를 활성으로 간주
        return (log2_expr > p75).astype(int)
    elif method == 'standard_zscore':
        z = stats.zscore(log2_expr)
        thr = threshold if threshold is not None else 0.0
        return (z > thr).astype(int)
    raise ValueError(f"알 수 없는 method: {method}")

np.random.seed(42)
sample_expr = pd.Series(np.random.lognormal(mean=2, sigma=1.5, size=200))
log2_expr = np.log2(sample_expr + 1)

for method in ['fixed', 'percentile', 'standard_zscore']:
    labels = discretize_expression(log2_expr, method=method)
    print(f"{method:12s}: 활성 유전자 {labels.sum()} / {len(labels)}개")

# 기대 출력 (난수 시드 고정, 방법마다 활성 유전자 수가 크게 달라짐에 유의):
# fixed       : 활성 유전자 184 / 200개
# percentile  : 활성 유전자  50 / 200개   (정의상 상위 25%)
# standard_zscore: 활성 유전자 98 / 200개   (표본평균보다 큰 값)
```

**예상 출력.** 콘솔에 다음이 나오면 성공입니다.

```
fixed       : 활성 유전자 184 / 200개
percentile  : 활성 유전자  50 / 200개
standard_zscore: 활성 유전자 98 / 200개
```

**확인 포인트.** 세 방법의 활성 유전자 수가 각각 184, 50, 98이면 성공입니다. 같은 데이터인데도 방법에 따라 활성 유전자 수가 이렇게 달라진다는 점이 이 단계의 핵심입니다. `percentile`이 정확히 50개(=200의 상위 25%)인 것도 확인해 보십시오.

**자주 나는 오류와 해결.**

- 숫자가 다르게 나온다 — 가장 흔한 원인은 `np.random.seed(42)`를 건너뛰었거나 다른 셀에서 난수를 먼저 소비한 경우입니다. 이 셀을 처음부터 다시 실행하십시오.
- `ModuleNotFoundError: No module named 'scipy'`(또는 `pandas`) — `pip install scipy pandas`로 설치하십시오.

{% hint style="warning" %}
**해석상의 주의:** `fixed`는 절대 cutoff에, `percentile`은 선택 비율에, `standard_zscore`는 전체 분포의 평균과 표준편차에 의존합니다. rFASTCORMICS는 이 셋째 코드를 사용하지 않습니다. 표본별 $$\log_2(\mathrm{FPKM})$$ 주봉의 오른쪽에 half-Gaussian을 적합해 얻은 $$\mu_E,\sigma_E$$로 zFPKM을 계산하고 발현·불확실·비발현 영역을 나눕니다. full workflow를 재현하려면 density fitting과 적합 진단이 추가로 필요합니다([2.3.1절](02.md)).
{% endhint %}

### 단계 3. `e_coli_core`의 실제 GPR로 RAS 계산하기

**무엇을·왜.** 이제 장난감 예제가 아니라 실제 모델의 [유전자-단백질-반응 연관](../chapter-3/README.md)(Gene-Protein-Reaction, GPR)에 min/max 휴리스틱을 적용해 RAS를 계산합니다([2.1~2.2절](02.md)). COBRApy는 GPR을 자체 파서로 읽어 논리식 객체로 보관합니다. 따라서 문자열을 `eval()`하거나 파이썬 식별자 규칙에 맞게 임의로 바꾸지 않고, `Reaction.gpr.as_symbolic()`이 반환하는 SymPy 논리식을 재귀적으로 평가합니다. 이 방식은 하이픈이나 마침표가 포함된 유전자 ID도 모델의 GPR 파서가 처리한 결과를 그대로 사용합니다.

**코드.** 이 코드는 모델을 불러오고(`load_model`), 데모용 임의 발현값을 만든 뒤, 대표 반응 다섯 개의 RAS를 출력합니다. 마지막으로 GPR을 가진 모든 반응의 RAS를 `reaction_weights` 딕셔너리에 저장합니다. **이 `reaction_weights`는 단계 4·5에서 그대로 재사용되므로 반드시 이 셀을 먼저 실행해야 합니다.**

```python
from sympy import Symbol
from sympy.logic.boolalg import And, Or
from cobra.io import load_model

def ras_from_gpr(gpr, expr, default=np.nan):
    """COBRApy GPR을 재귀 평가: AND->min, OR->max 휴리스틱."""
    symbolic = gpr.as_symbolic()
    if symbolic is None:
        return default

    def _walk(node):
        if isinstance(node, Symbol):
            return expr.get(str(node), default)
        values = [_walk(child) for child in node.args]
        if any(np.isnan(value) for value in values):
            return default
        if isinstance(node, And):
            return min(values)
        if isinstance(node, Or):
            return max(values)
        raise TypeError(f"지원하지 않는 GPR 노드: {type(node).__name__}")

    return _walk(symbolic)

model = load_model("textbook")                  # e_coli_core, Chapter 1과 동일 모델
np.random.seed(0)
gene_expr = {g.id: round(np.random.uniform(0, 10), 2) for g in model.genes}  # 데모용 임의 발현값

for rid in ["PGI", "PFK", "PFL", "CYTBD", "GLCpts"]:
    rxn = model.reactions.get_by_id(rid)
    print(f"{rid:8s} GPR={rxn.gene_reaction_rule:55s} RAS={ras_from_gpr(rxn.gpr, gene_expr):.2f}")

reaction_weights = {r.id: ras_from_gpr(r.gpr, gene_expr)
                     for r in model.reactions if r.gene_reaction_rule}
print(f"GPR 보유 반응 (RAS 계산 대상): {len(reaction_weights)} / {len(model.reactions)}")

# 기대 출력 (난수 시드 고정):
# PGI      GPR=b4025                                                  RAS=5.72
# PFK      GPR=b3916 or b1723                                         RAS=6.78
# PFL      GPR=(b0902 and b3114) or (b0903 and b0902 and b2579) or... RAS=5.76
# CYTBD    GPR=(b0978 and b0979) or (b0733 and b0734)                 RAS=5.22
# GLCpts   GPR=(b2415 and b1818 and b1817 and b1819 and b2416) or ... RAS=1.29
# GPR 보유 반응 (RAS 계산 대상): 69 / 95   (나머지 26개에는 GPR 문자열이 없음)
```

**예상 출력.** 다음과 같이 다섯 반응의 RAS와, GPR을 가진 반응이 69/95개라는 요약이 나오면 성공입니다.

```
PGI      GPR=b4025                                                  RAS=5.72
PFK      GPR=b3916 or b1723                                         RAS=6.78
PFL      GPR=(b0902 and b3114) or (b0903 and b0902 and b2579) or... RAS=5.76
CYTBD    GPR=(b0978 and b0979) or (b0733 and b0734)                 RAS=5.22
GLCpts   GPR=(b2415 and b1818 and b1817 and b1819 and b2416) or ... RAS=1.29
GPR 보유 반응 (RAS 계산 대상): 69 / 95
```

**확인 포인트.** 마지막 줄이 `69 / 95`이고 GLCpts의 RAS가 `1.29`이면 성공입니다. `reaction_weights`가 만들어졌는지 확인하려면 `len(reaction_weights)`가 69인지 보십시오.

**자주 나는 오류와 해결.**

- `ModuleNotFoundError: No module named 'cobra'`(또는 `sympy`) — `pip install cobra sympy`로 설치하십시오.
- 다운로드 관련 오류로 `load_model("textbook")`이 실패한다 — 네트워크 연결을 확인하십시오. 오프라인이라면 COBRApy 저장소에서 `e_coli_core.xml`을 내려받아 `cobra.io.read_sbml_model("경로/e_coli_core.xml")`로 대체할 수 있습니다.
- RAS 값이 다르게 나온다 — `np.random.seed(0)`을 함께 실행했는지, 그리고 이 셀 이전에 다른 난수를 소비하지 않았는지 확인하십시오.

{% hint style="warning" %}
**해석상의 주의:** GLCpts(포도당 PTS 수송 시스템)의 RAS가 1.29인 것은 이 합성 데이터에서 AND로 연결된 소단위 가운데 최솟값이 작기 때문입니다. 독립적으로 같은 분포에서 값을 뽑는 이 예제에서는 AND 항이 많을수록 최솟값이 작아지는 경향도 생깁니다. 실제 데이터에서는 유전자 간 공발현과 복합체 조절이 있으므로 이를 일반 법칙으로 해석해서는 안 됩니다. 또한 AND=min, OR=max는 Boolean GPR을 연속 점수로 옮기는 휴리스틱이지 효소량의 물리식은 아닙니다.
{% endhint %}

### 단계 4. GIMME 2단계 LP를 `e_coli_core`에 실행하기

**무엇을·왜.** 단계 3에서 얻은 `reaction_weights`를 그대로 이어받아, [3.2절](03.md)의 GIMME 2단계 LP(선형계획, Linear Programming)를 실제로 풀어봅니다. [3.2.1절](03.md)에서 손으로 풀어본 장난감 3-반응 네트워크와 원리는 완전히 같습니다 — 다만 이번에는 반응 95개짜리 실제 대사 네트워크 전체에서 solver가 그 계산을 대신 수행합니다. GIMME는 (1) 원래 FBA로 최적 성장률 $$Z^*$$를 구하고, (2) 성장률을 $$0.9Z^*$$ 이상으로 유지한다는 하한을 둔 채 저발현 반응의 flux를 최소화합니다.

**코드.** 이 코드는 네 부분으로 이루어집니다: 원래 FBA 성장률 계산, 저발현 반응 선정(하위 25%), 최소 패널티 해 계산, 그리고 최적면 전체에서 항상 0인 반응만 찾아 차단한 교육용 `context_model` 구성입니다. **여기서 만든 `context_model`은 단계 7에서 다시 사용됩니다.**

```python
model.objective = "Biomass_Ecoli_core"
# 재현 조건을 결과와 함께 기록: 솔버와 허용오차가 다르면 마지막 자리가 달라질 수 있음
print(f"solver: {model.solver.interface.__name__.split('.')[-1]}, tolerance: {model.tolerance}")
Z_star = model.slim_optimize()
print(f"1단계(원래 FBA) 최적 성장률 Z* = {Z_star:.4f} h^-1")

threshold_low = np.percentile(list(reaction_weights.values()), 25)
low_rxns = [rid for rid, w in reaction_weights.items() if w <= threshold_low]
print(f"저발현 반응(하위 25%, GPR 보유 반응 중): {len(low_rxns)}개")

f = 0.9
stage2 = model.copy()
biomass = stage2.reactions.get_by_id("Biomass_Ecoli_core")
stage2.add_cons_vars(stage2.problem.Constraint(
    biomass.flux_expression, lb=f * Z_star, name="growth_floor"))

# |v|의 선형 표현: COBRApy의 정·역방향 비음수 변수의 합
low_flux_terms = []
for rid in low_rxns:
    rxn = stage2.reactions.get_by_id(rid)
    low_flux_terms += [rxn.forward_variable, rxn.reverse_variable]
penalty_expr = sum(low_flux_terms)
stage2.objective = stage2.problem.Objective(penalty_expr, direction="min")

gimme_sol = stage2.optimize()
penalty_star = gimme_sol.objective_value
active_in_one_solution = [
    rid for rid in low_rxns if abs(gimme_sol.fluxes[rid]) > 1e-6
]

# 최소 패널티 값을 고정한 뒤 각 저발현 반응의 가능한 flux 범위를 조사
stage2.add_cons_vars(stage2.problem.Constraint(
    penalty_expr, ub=penalty_star + 1e-9, name="minimum_penalty_face"))
guaranteed_off = []
for rid in low_rxns:
    rxn = stage2.reactions.get_by_id(rid)
    stage2.objective = stage2.problem.Objective(rxn.flux_expression, direction="min")
    flux_min = stage2.slim_optimize()
    stage2.objective = stage2.problem.Objective(rxn.flux_expression, direction="max")
    flux_max = stage2.slim_optimize()
    if max(abs(flux_min), abs(flux_max)) < 1e-7:
        guaranteed_off.append(rid)

# 교육용 hard-pruned 모델: 최소 패널티 최적면 전체에서 항상 0인 반응만 차단
context_model = model.copy()
for rid in guaranteed_off:
    context_model.reactions.get_by_id(rid).bounds = (0.0, 0.0)
context_model.objective = "Biomass_Ecoli_core"
context_baseline = context_model.slim_optimize()

print(f"2단계 상태: {gimme_sol.status}")
print(f"한 최소 패널티 해의 성장률: {gimme_sol.fluxes['Biomass_Ecoli_core']:.4f}")
print(f"그 해에서 활성인 저발현 반응: {len(active_in_one_solution)} / {len(low_rxns)}")
print(f"모든 최소 패널티 해에서 0인 반응: {len(guaranteed_off)}개")
print(f"hard-pruned 모델의 최대 성장률: {context_baseline:.4f} h^-1")

# 기대 출력:
# solver: glpk_interface, tolerance: 1e-07
# 1단계(원래 FBA) 최적 성장률 Z* = 0.8739 h^-1
# 저발현 반응(하위 25%, GPR 보유 반응 중): 18개
# 2단계 상태: optimal
# 한 최소 패널티 해의 성장률: 0.7865
# 그 해에서 활성인 저발현 반응: 10 / 18
# 모든 최소 패널티 해에서 0인 반응: 8개
# hard-pruned 모델의 최대 성장률: 0.7967 h^-1
```

**예상 출력.** 콘솔에 다음이 나오면 성공입니다.

```
solver: glpk_interface, tolerance: 1e-07
1단계(원래 FBA) 최적 성장률 Z* = 0.8739 h^-1
저발현 반응(하위 25%, GPR 보유 반응 중): 18개
2단계 상태: optimal
한 최소 패널티 해의 성장률: 0.7865
그 해에서 활성인 저발현 반응: 10 / 18
모든 최소 패널티 해에서 0인 반응: 8개
hard-pruned 모델의 최대 성장률: 0.7967 h^-1
```

**확인 포인트.** `2단계 상태`가 `optimal`이고 $$Z^*$$가 `0.8739`, hard-pruned 모델의 최대 성장률이 `0.7967`이면 성공입니다. `2단계 상태`가 `infeasible`로 나오면 성장 하한이 잘못 설정된 것이므로 앞 셀들을 다시 실행하십시오.

**자주 나는 오류와 해결.**

- `NameError: name 'reaction_weights' is not defined` — 단계 3을 실행하지 않았습니다. 단계 3을 먼저 실행하십시오.
- `NameError: name 'model' is not defined` — 마찬가지로 단계 3에서 `model`을 만들었으니 단계 3을 먼저 실행하십시오.
- 실행이 느리다 — 기본 솔버(GLPK)로도 이 크기의 LP는 빠르게 풀립니다. 아주 느리다면 커널을 재시작하고 단계 1부터 다시 실행하십시오.

성장률 제약은 $$v_{biomass}\ge0.9Z^*$$라는 **하한**입니다. 이 데이터에서는 최소 패널티 해가 하한에서 얻어졌지만, GIMME가 성장률을 일반적으로 정확히 90%로 고정하는 것은 아닙니다.

{% hint style="warning" %}
**해석상의 주의:** LP 해 하나에서 flux가 0이라는 사실만으로 반응을 제거할 수 없습니다. 대체 최적해에서는 그 반응이 사용될 수 있기 때문입니다. 위 코드는 최소 패널티 값을 고정하고 각 저발현 반응을 최소화·최대화하여, 최적면 전체에서 flux가 0인 8개만 차단합니다. `context_model`에는 GIMME의 성장 하한과 penalty 목적을 옮기지 않았으므로 최대 성장률이 2단계 반환 해와 같을 필요는 없습니다. 이 모델은 비교를 위한 교육용 hard-pruned 모델이며, 정식 GIMME 구현의 모든 후처리를 재현한 것은 아닙니다.
{% endhint %}

### 단계 5. E-Flux 경계 스케일링을 `e_coli_core`에 실행하기

**무엇을·왜.** [3.4.1절](03.md)에서 손으로 계산한 경계 스케일링(원래 상한에 정규화된 발현값을 곱하는 것)을 그대로 코드로 적용합니다. E-Flux는 별도의 성장 하한 없이, 발현이 낮은 반응일수록 그 반응이 흐를 수 있는 최대 용량 자체를 줄입니다. 단계 3에서 만든 `reaction_weights`와 `model`을 다시 사용합니다.

**코드.** 이 코드는 각 반응의 RAS를 0~1로 정규화한 뒤(`E`), `with model:` 블록 안에서 상·하한을 스케일링하고 FBA를 다시 풉니다. `with model:` 블록은 안에서 바꾼 경계를 블록이 끝나면 자동으로 원래대로 되돌리므로, 원본 `model`은 손상되지 않습니다.

```python
w_max = max(reaction_weights.values())
E = {rid: w / w_max for rid, w in reaction_weights.items()}   # 0~1로 정규화 (GPR 없는 반응은 원래 경계 유지)

model.objective = "Biomass_Ecoli_core"
baseline = model.optimize().objective_value

with model:
    for rid, e in E.items():
        rxn = model.reactions.get_by_id(rid)
        if rxn.upper_bound > 0:
            rxn.upper_bound = e * rxn.upper_bound
        if rxn.lower_bound < 0:
            rxn.lower_bound = e * rxn.lower_bound
    eflux_sol = model.optimize()
    print(f"원래 성장률:            {baseline:.4f} h^-1")
    print(f"E-Flux 스케일링 후 성장률: {eflux_sol.objective_value:.4f} h^-1")

# 기대 출력:
# 원래 성장률:            0.8739 h^-1
# E-Flux 스케일링 후 성장률: 0.6139 h^-1   (발현 낮은 반응의 용량이 줄어 성장률이 함께 낮아짐)
```

**예상 출력.** 콘솔에 다음이 나오면 성공입니다.

```
원래 성장률:            0.8739 h^-1
E-Flux 스케일링 후 성장률: 0.6139 h^-1
```

**확인 포인트.** 원래 성장률이 `0.8739`, E-Flux 스케일링 후가 `0.6139`이면 성공입니다. 스케일링 후 값이 원래보다 낮아진 것은 저발현 반응의 용량이 줄어 성장 여지가 좁아졌기 때문입니다.

**자주 나는 오류와 해결.**

- `NameError: name 'reaction_weights' is not defined` 또는 `model` 미정의 — 단계 3을 먼저 실행하십시오.
- 스케일링 후 성장률이 원래와 같다 — `with model:` 블록 안쪽 들여쓰기가 어긋나 경계 변경이 실제로 적용되지 않은 경우입니다. 블록 전체를 다시 실행하십시오.

{% hint style="warning" %}
**해석상의 주의:** GIMME는 원래 최적 성장률의 90% 이상을 허용 가능한 영역으로 두고 그 안에서 저발현 flux penalty를 최소화합니다. 이 예제의 반환 해는 우연이 아니라 목적함수 구조 때문에 하한에 놓였지만, 제약 자체는 등식이 아닙니다. E-Flux는 별도의 성장 하한 없이 발현으로 경계를 스케일링하여 최대 성장률이 0.6139 h$$^{-1}$$가 되었습니다. 따라서 두 숫자는 각각 "기능 하한을 둔 뒤 발현 불일치를 줄이는 방법"과 "발현을 용량의 대리값으로 쓰는 방법"의 차이를 보여 줍니다.
{% endhint %}

### 단계 6. iMAT을 개념 코드로 이해하기

**무엇을·왜.** iMAT은 GIMME·E-Flux와 달리 [MILP](../glossary.md)(혼합정수선형계획)로 정형화되며, $$y_j$$–$$v_j$$ big-M 연결 제약을 반응마다 정확한 하한·상한으로 조정해야 합니다([3.3절](03.md)의 구현상의 주의, [3.3.1절](03.md)의 숫자 예제 참고). 이 상수를 잘못 설정하면 손쉽게 infeasible에 빠지므로, 이 단계는 실행이 아니라 **구조 이해**가 목적입니다. 아래 개념 코드는 고발현·저발현 반응 집합을 나누는 뼈대만 보여 줍니다. 실제 연구에서는 이를 직접 처음부터 구현하기보다 **[Troppo](https://github.com/BioSystemsUM/troppo)**(`troppo.methods.reconstruction`) 프레임워크의 검증된 GIMME/iMAT/FastCORE/tINIT 구현체나 [COBRA Toolbox](https://opencobra.github.io/cobratoolbox/)/[RAVEN](https://github.com/SysBioChalmers/RAVEN)(MATLAB)의 대응 함수를 사용하는 것이 권장됩니다.

**코드.** 이 코드는 함수 정의만 하며, 실행해도 화면에 출력되는 내용은 없습니다. 주석은 실제 iMAT MILP에서 이 두 집합을 어떻게 제약으로 옮기는지 설명합니다.

```python
# 개념 코드 (실행 목적이 아닌 구조 설명용) — 실제로는 Troppo 등의 패키지 사용을 권장
def imat_style_reconstruction(model, reaction_weights, high_q=75, low_q=25, eps=1.0):
    vals = list(reaction_weights.values())
    hi, lo = np.percentile(vals, high_q), np.percentile(vals, low_q)
    R_high = [rid for rid, w in reaction_weights.items() if w >= hi]
    R_low  = [rid for rid, w in reaction_weights.items() if w <= lo]
    # 이후 R_high는 "y=1이면 |v|>=eps", R_low는 "y=1이면 v=0"이 되도록
    # 반응별 lower_bound/upper_bound를 반영한 big-M 제약을 세우고
    # y_low를 "저발현 반응이 비활성"인 지시자로 정의했다면
    # sum(y_high_active) + sum(y_low_inactive)를 최대화한다 (3.3절 참고).
    return R_high, R_low
```

**예상 출력.** 이 셀은 함수를 정의만 하므로 출력이 없습니다. 오류 없이 실행이 끝나면(다음 프롬프트로 넘어가면) 성공입니다. 직접 호출해 보려면 `R_high, R_low = imat_style_reconstruction(model, reaction_weights)`처럼 실행할 수 있습니다.

**확인 포인트.** 오류 메시지 없이 셀이 완료되면 함수가 정상적으로 정의된 것입니다. 이 단계에서 성장률 같은 숫자를 기대하지 마십시오.

암 맥락에서의 완전한 Troppo 파이프라인 예시는 [Chapter 7](../chapter-7/README.md)에서 이어집니다.

### 단계 7. 맥락 특이적 제약이 유전자 필수성에 미치는 영향 검증하기

**무엇을·왜.** 단계 4에서 만든 `context_model`과 원래 `model`에 동일한 단일 유전자 결손(single gene deletion) 분석을 적용해, 맥락 제약이 유전자 필수성 예측을 바꾸는지 확인합니다. 유전자 결손은 그 유전자가 담당하는 반응을 껐을 때 성장이 얼마나 유지되는지를 봅니다. 각 모델의 무결손 최대 성장률이 다르므로, 필수성은 절대값이 아니라 **해당 모델 baseline에 대한 상대 성장률 1% 미만**으로 정의합니다.

**코드.** 이 코드는 두 모델 각각에 `single_gene_deletion`을 실행해 유전자별 성장률을 구하고, 두 모델의 상대 성장률을 하나의 표로 모아 필수 유전자를 비교합니다. 마지막에는 context 모델에서 새로 필수가 된 유전자를 출력합니다.

```python
from cobra.flux_analysis import single_gene_deletion

model.objective = "Biomass_Ecoli_core"
generic_baseline = model.slim_optimize()
context_model.objective = "Biomass_Ecoli_core"
context_baseline = context_model.slim_optimize()

def deletion_growth_by_gene(cobra_model):
    result = single_gene_deletion(cobra_model, processes=1).copy()
    # COBRApy의 ids 열은 한 원소짜리 set이므로 유전자 ID를 명시적으로 꺼낸다.
    result["gene"] = result["ids"].map(lambda ids: next(iter(ids)))
    return result.set_index("gene")["growth"]

generic_growth = deletion_growth_by_gene(model)
context_growth = deletion_growth_by_gene(context_model)
comparison = pd.DataFrame({
    "generic": generic_growth / generic_baseline,
    "context": context_growth / context_baseline,
})

essential_cutoff = 0.01
generic_essential = comparison.index[comparison["generic"] < essential_cutoff]
context_essential = comparison.index[comparison["context"] < essential_cutoff]
new_context_essential = comparison.index[
    (comparison["generic"] >= essential_cutoff)
    & (comparison["context"] < essential_cutoff)
]

print(f"generic/context baseline: {generic_baseline:.4f} / {context_baseline:.4f}")
print(f"generic 필수 유전자: {len(generic_essential)}개")
print(f"context 필수 유전자: {len(context_essential)}개")
print(f"context에서 새로 필수가 된 유전자: {sorted(new_context_essential)}")

# 기대 출력 (위 난수 시드와 COBRApy 0.30.0):
# generic/context baseline: 0.8739 / 0.7967
# generic 필수 유전자: 5개
# context 필수 유전자: 7개
# context에서 새로 필수가 된 유전자: ['b1761', 'b3956']
```

**예상 출력.** 콘솔에 다음이 나오면 성공입니다.

```
generic/context baseline: 0.8739 / 0.7967
generic 필수 유전자: 5개
context 필수 유전자: 7개
context에서 새로 필수가 된 유전자: ['b1761', 'b3956']
```

**확인 포인트.** generic 필수 유전자 5개, context 필수 유전자 7개, 새로 필수가 된 유전자가 `['b1761', 'b3956']`이면 성공입니다. 두 baseline이 `0.8739 / 0.7967`로 나오는지도 확인하십시오(context 쪽이 단계 4의 hard-pruned 성장률과 같아야 합니다).

**자주 나는 오류와 해결.**

- `NameError: name 'context_model' is not defined` — 단계 4를 실행하지 않았습니다. 단계 4를 먼저 실행하십시오.
- 실행 중 병렬 처리 관련 오류가 난다 — 코드에 이미 `processes=1`을 지정해 단일 프로세스로 돌립니다. 이 인자를 지우지 마십시오. 일부 환경에서는 다중 프로세스가 오류를 일으킵니다.
- context baseline이 단계 4와 다르다 — 단계 4를 다시 실행하지 않고 `context_model`을 수정한 경우입니다. 단계 4부터 순서대로 재실행하십시오.

동일한 유전자 결손을 두 모델에 적용하면 맥락 제약이 대체 경로를 제거해 새 취약성을 만들 수 있음을 계산적으로 확인할 수 있습니다. 여기서는 `b1761`과 `b3956`이 그 예입니다.

{% hint style="warning" %}
**해석상의 주의:** 입력 발현값이 난수이고 실험 관측과 비교하지 않았으므로, 이는 **외부 검증이 아니라 모델 간 민감도 비교**입니다. 예측 정확도를 주장하려면 배지와 세포 상태를 맞춘 실험적 유전자 필수성 자료를 독립적으로 대조해야 합니다. 암-정상 모델과 DepMap CRISPR 자료를 이용한 비교는 [Chapter 7](../chapter-7/README.md)에서 다룹니다.
{% endhint %}

---

## 정리

- 단계 1에서 raw counts를 TPM으로 정규화하고 합이 항상 100만이 되는 것을 확인했습니다.
- 단계 2에서 고정·백분위수·z-score 세 임계값 방법이 같은 데이터에서도 활성 유전자 수를 크게 다르게 만든다는 것을 보았습니다.
- 단계 3에서 COBRApy의 실제 GPR 파서로 RAS를 계산해 반응 가중치 `reaction_weights`를 만들었습니다.
- 단계 4·5에서 그 가중치를 GIMME 2단계 LP와 E-Flux 경계 스케일링으로 번역해 `e_coli_core`에 직접 실행하고, 성장률이 각각 어떻게 달라지는지 해석했습니다.
- 단계 6에서 iMAT을 개념 코드로 이해하고, 실제로는 검증된 패키지를 쓰는 것이 권장된다는 점을 확인했습니다.
- 단계 7에서 맥락 특이적 제약이 유전자 필수성 예측을 바꿀 수 있음을 generic/context 모델 비교로 확인했습니다.

전체를 관통하는 결론은, 임계값·알고리즘·경계조건을 바꾸면 결과 숫자가 함께 달라지므로 이 값들을 항상 기록하고 민감도 분석과 독립 검증을 함께 수행해야 한다는 것입니다.

## 스스로 해보기

아래 과제는 위 코드를 조금씩 바꿔 결과가 어떻게 달라지는지 직접 확인하는 것입니다. 정답 숫자를 미리 계산해 두지 말고, 실행 결과를 관찰하며 이유를 설명해 보십시오.

1. **임계값 민감도 실험.** 단계 4의 `threshold_low`를 하위 25%(`np.percentile(..., 25)`) 대신 하위 10%나 40%로 바꾸면 저발현 반응 수와 hard-pruned 성장률이 어떻게 변하는지 관찰하고, 그 방향이 상식과 맞는지 설명해 보십시오.
2. **E-Flux 성장 하한 비교.** 단계 5의 E-Flux에는 성장 하한이 없습니다. GIMME(단계 4)의 성장 하한 비율 `f`를 0.9에서 0.5로 낮추면 hard-pruned 성장률이 어떻게 바뀌는지 확인하고, E-Flux 결과와 비교해 두 방법의 철학 차이를 정리해 보십시오.
3. **필수성 정의 바꾸기.** 단계 7의 `essential_cutoff`를 0.01에서 0.05로 올리면 generic·context 필수 유전자 수와 "새로 필수가 된 유전자" 목록이 어떻게 달라지는지 살펴보고, 필수성 기준을 명확히 기록하는 것이 왜 중요한지 설명해 보십시오.

## 다음 단계

- 임계값과 zFPKM 통계 배경을 더 보려면 [2.3절](02.md)과 [오믹스 데이터 분석과 기초 통계](../supplements/omics-statistics.md)를 참고하십시오.
- 여기서 다룬 GIMME·iMAT·E-Flux·tINIT의 정형화 비교는 [3절](03.md)에, RNA-seq 전처리 파이프라인 전체는 [4절](04.md)에 있습니다.
- 암 세포주 맥락 특이적 모델을 이용한 약물 표적 예측과 실험 필수성 자료 대조는 [Chapter 7](../chapter-7/README.md)에서 이어집니다.

---
