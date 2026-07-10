# 실습: RNA-seq 발현 데이터를 GEM에 통합하기

> 💡 **실습:** 아래 코드는 핵심 흐름만 보여주는 발췌본입니다. [Chapter 1](../chapter-1/README.md)에서 불러온 것과 동일한 COBRApy 내장 모델 `e_coli_core`(95개 반응·72개 대사물·137개 유전자)를 다시 사용합니다. 대규모 TCGA 데이터와 실제 Human1/Recon3D, Troppo 프레임워크를 이용한 전체 파이프라인은 `gem9_w06_lab.ipynb`(간 특이적 tINIT 스타일 추출)와 `gem9_w07_lab.ipynb`(TCGA 스타일 RNA-seq 시뮬레이션과 맥락 특이적 암 모델 구축)를 참고하십시오.

이 실습은 1절의 7단계 통합 파이프라인 중 3~7단계를 손으로 따라가 봅니다 — raw counts를 TPM으로 정규화하고(4.1절), 여러 임계값 방법을 비교하고(2.3절), 실제 GPR로 RAS를 계산하고(2.1~2.2절), 그 RAS를 GIMME(3.2절)와 E-Flux(3.4절) 제약으로 번역해 `e_coli_core`에 직접 실행합니다. 마지막 7단계에서는 맥락 특이적 제약이 유전자 필수성 예측에 미치는 영향을 확인합니다.

## 1단계: raw counts → TPM 정규화

4.1절에서 손으로 계산해 본 TPM 공식을 그대로 코드로 옮깁니다. 핵심은 "길이로 나눈 비율(rate)을 구한 뒤, 그 비율의 합으로 다시 정규화해 항상 100만이 되도록 만든다"는 두 단계입니다.

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

이 결과에서 LDHA(젖산탈수소효소, 해당과정의 마지막 단계를 촉매)가 다른 유전자보다 훨씬 높은 TPM을 보입니다 — counts 자체도 가장 높고(2400) 유전자 길이도 가장 짧기(1000bp) 때문입니다. 만약 길이 보정을 하지 않고 raw counts만 비교했다면 PKM(1200)이 LDHA(2400)보다 절반 수준이라고 오해했겠지만, TPM으로 정규화하면 LDHA가 PKM보다 실제로는 훨씬 더 큰 차이로 우세하다는 것을 알 수 있습니다 — 짧은 유전자는 같은 발현 수준이라도 리드가 좁은 영역에 집중되어 counts가 더 크게 잡히기 때문에, 길이 보정 후 그 차이가 오히려 더 벌어지는 방향으로 나타날 수 있습니다.

## 2단계: 발현 임계값 이산화 방법 비교

2.3절에서 비교한 세 가지 임계값 전략(고정값, 백분위수, z-score)을 실제로 코드로 실행해, 같은 데이터에 적용해도 "활성"으로 분류되는 유전자 수가 방법마다 얼마나 크게 달라지는지 직접 확인합니다.

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
    elif method == 'zscore':
        z = stats.zscore(log2_expr)
        thr = threshold if threshold is not None else -3.0   # rFASTCORMICS 관례값
        return (z > thr).astype(int)
    raise ValueError(f"알 수 없는 method: {method}")

np.random.seed(42)
sample_expr = pd.Series(np.random.lognormal(mean=2, sigma=1.5, size=200))
log2_expr = np.log2(sample_expr + 1)

for method in ['fixed', 'percentile', 'zscore']:
    labels = discretize_expression(log2_expr, method=method)
    print(f"{method:12s}: 활성 유전자 {labels.sum()} / {len(labels)}개")

# 기대 출력 (난수 시드 고정, 방법마다 활성 유전자 수가 크게 달라짐에 유의):
# fixed       : 활성 유전자 184 / 200개
# percentile  : 활성 유전자  50 / 200개   (정의상 상위 25%)
# zscore      : 활성 유전자 200 / 200개   (z > -3은 거의 전부를 활성으로 분류)
```

세 방법의 결과가 이렇게 극단적으로 다른 이유를 짚어봅시다. `fixed` 방법은 로그값이 1.0보다 크면 무조건 활성으로 분류하는데, 이 장난감 데이터는 로그정규분포(lognormal)에서 뽑았기 때문에 대부분의 값이 1.0을 넘습니다. `percentile` 방법은 정의상 항상 정확히 상위 25%(200개 중 50개)만 활성으로 분류하므로, 데이터 분포와 무관하게 "비율"만은 고정됩니다. `zscore` 방법은 임계값을 $$-3$$으로 두었는데, 이 값은 rFASTCORMICS가 실제 대규모 RNA-seq 코호트(수천~수만 개 유전자)에서 검증한 값이라 이 작은 장난감 데이터(200개, 뚜렷한 이봉분포가 아님)에는 그대로 적용하기 부적절하다는 것을 보여줍니다 — **임계값 상수를 다른 맥락(데이터 규모·분포)에 그대로 가져다 쓰면 안 된다는 교훈**을 이 결과가 실증적으로 보여줍니다.

## 3단계: `e_coli_core`의 실제 GPR로 RAS 계산

파이썬에서 `and`/`or`는 예약어이므로, GPR 문자열(예: `"b3916 or b1723"`)은 그대로 하나의 불리언 표현식입니다. 이 성질을 이용해 `ast` 모듈로 파싱한 뒤 재귀적으로 평가하면, 2.2절에서 손으로 계산한 것과 똑같은 로직을 실제 137개 유전자·95개 반응 규모에 그대로 적용할 수 있습니다. `ast`를 쓰는 이유는 단순 문자열 `eval()`보다 안전하기 때문입니다 — GPR 문자열은 외부 데이터(모델 파일)에서 오므로, 임의 코드 실행 위험이 있는 `eval()` 대신 파싱된 구문 트리만 허용하는 `ast.parse(..., mode="eval")`를 사용하는 것이 안전한 관행입니다.

```python
import ast
from cobra.io import load_model

def ras_from_gpr(gpr_string, expr, default=0.0):
    """GPR 문자열을 AST로 파싱해 재귀 평가: and->min(복합체 병목), or->max(아이소자임)"""
    if not gpr_string:
        return default
    tree = ast.parse(gpr_string, mode="eval").body

    def _walk(node):
        if isinstance(node, ast.BoolOp):
            values = [_walk(v) for v in node.values]
            return min(values) if isinstance(node.op, ast.And) else max(values)
        if isinstance(node, ast.Name):          # leaf: 유전자 이름
            return expr.get(node.id, default)
        raise ValueError(f"지원하지 않는 GPR 구문: {ast.dump(node)}")
    return _walk(tree)

model = load_model("textbook")                  # e_coli_core, Chapter 1과 동일 모델
np.random.seed(0)
gene_expr = {g.id: round(np.random.uniform(0, 10), 2) for g in model.genes}  # 데모용 임의 발현값

for rid in ["PGI", "PFK", "PFL", "CYTBD", "GLCpts"]:
    rxn = model.reactions.get_by_id(rid)
    print(f"{rid:8s} GPR={rxn.gene_reaction_rule:55s} RAS={ras_from_gpr(rxn.gene_reaction_rule, gene_expr):.2f}")

reaction_weights = {r.id: ras_from_gpr(r.gene_reaction_rule, gene_expr)
                     for r in model.reactions if r.gene_reaction_rule}
print(f"GPR 보유 반응 (RAS 계산 대상): {len(reaction_weights)} / {len(model.reactions)}")

# 기대 출력 (난수 시드 고정):
# PGI      GPR=b4025                                                  RAS=5.72
# PFK      GPR=b3916 or b1723                                         RAS=6.78
# PFL      GPR=(b0902 and b3114) or (b0903 and b0902 and b2579) or... RAS=5.76
# CYTBD    GPR=(b0978 and b0979) or (b0733 and b0734)                 RAS=5.22
# GLCpts   GPR=(b2415 and b1818 and b1817 and b1819 and b2416) or ... RAS=1.29
# GPR 보유 반응 (RAS 계산 대상): 69 / 95   (나머지 26개는 교환·경계 반응 등 GPR이 없는 반응)
```

GLCpts(포도당 PTS 수송 시스템)의 RAS가 유독 낮게(1.29) 나온 이유를 살펴봅시다 — 이 반응의 GPR은 5개 유전자가 모두 AND로 연결된 복합체이므로, 그중 가장 낮은 발현값 하나가 전체 RAS를 결정합니다(2.1절의 "이어달리기" 비유 그대로). 복합체를 이루는 유전자 수가 많을수록(GLCpts는 5개), 우연히 그중 하나라도 낮은 난수값을 뽑을 확률이 높아지므로, **AND로 연결된 유전자 수가 많은 반응일수록 RAS가 낮게 나올 통계적 경향**이 있다는 점도 함께 기억해 둘 만합니다.

## 4단계: GIMME 2단계 LP를 `e_coli_core`에 직접 실행

3단계에서 얻은 `reaction_weights`를 그대로 이어받아, 3.2절의 GIMME 2단계 LP를 실제로 풀어봅니다. 3.2.1절에서 손으로 풀어본 장난감 3-반응 네트워크와 원리는 완전히 같습니다 — 다만 이번에는 반응 95개짜리 실제 대사 네트워크 전체에서 solver가 그 계산을 대신 수행합니다.

```python
model.objective = "Biomass_Ecoli_core"
Z_star = model.optimize().objective_value
print(f"1단계(원래 FBA) 최적 성장률 Z* = {Z_star:.4f} h^-1")

threshold_low = np.percentile(list(reaction_weights.values()), 25)
low_rxns = [rid for rid, w in reaction_weights.items() if w <= threshold_low]
print(f"저발현 반응(하위 25%, GPR 보유 반응 중): {len(low_rxns)}개")

f = 0.9
with model:
    biomass = model.reactions.get_by_id("Biomass_Ecoli_core")
    model.add_cons_vars(model.problem.Constraint(
        biomass.flux_expression, lb=f * Z_star, ub=1000, name="growth_floor"))

    low_flux_terms = []
    for rid in low_rxns:
        rxn = model.reactions.get_by_id(rid)
        low_flux_terms += [rxn.forward_variable, rxn.reverse_variable]
    model.objective = model.problem.Objective(sum(low_flux_terms), direction="min")

    sol = model.optimize()
    active_low = [rid for rid in low_rxns if abs(sol.fluxes[rid]) > 1e-6]
    print(f"2단계 상태: {sol.status}")
    print(f"2단계 성장률: {sol.fluxes['Biomass_Ecoli_core']:.4f}  (>= {f*Z_star:.4f} 확인)")
    print(f"저발현 반응 중 실제로 켜진 반응: {len(active_low)} / {len(low_rxns)}")

# 기대 출력:
# 1단계(원래 FBA) 최적 성장률 Z* = 0.8739 h^-1
# 저발현 반응(하위 25%, GPR 보유 반응 중): 18개
# 2단계 상태: optimal
# 2단계 성장률: 0.7865  (>= 0.7865 확인)
# 저발현 반응 중 실제로 켜진 반응: 10 / 18   (18개 중 8개는 완전히 꺼짐)
```

`with model:` 블록을 벗어나면 원래 목적 함수와 경계가 자동으로 복원되어([Chapter 4](../chapter-4/README.md) 참고), 다음 실습에 영향을 주지 않습니다. 여기서 저발현 반응 18개 중 8개만 완전히 꺼지고 나머지 10개는 여전히 켜진 채로 남았다는 점에 주목하십시오 — 이는 3.2.1절 장난감 예제와 달리, 실제 `e_coli_core` 네트워크에서는 저발현 반응 중 일부가 성장에 필수적이라 완전히 배제할 수 없었다는 뜻입니다. GIMME는 "가능한 한" 저발현 반응을 피하지만, 네트워크 연결성상 불가피하다면 사용을 허용합니다.

## 5단계: E-Flux 경계 스케일링을 `e_coli_core`에 직접 실행

3.4.1절에서 손으로 계산한 경계 스케일링(원래 상한에 정규화된 발현값을 곱하는 것)을 그대로 코드로 적용합니다.

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

GIMME(4단계)와 E-Flux(5단계)의 결과를 나란히 비교해 보면 흥미로운 대조가 드러납니다 — GIMME는 성장률을 명시적으로 90%(0.7865)까지만 낮추도록 **강제**한 반면, E-Flux는 그런 하한을 두지 않고 경계를 스케일링한 결과 성장률이 원래의 약 70%(0.6139/0.8739)까지 자연스럽게 떨어졌습니다. 이는 두 방법론의 철학 차이(3.1절)가 실제 숫자로 드러나는 지점입니다 — GIMME는 "목적 달성을 우선하고 발현은 그 다음"이지만, E-Flux는 "발현이 곧 용량이므로 그 결과로 나오는 성장률은 부차적"입니다.

## 6단계: iMAT은 왜 개념 코드로만 소개하는가

iMAT의 MILP는 $$y_j$$–$$v_j$$ big-M 연결 제약을 반응마다 정확한 하한·상한으로 조정해야 하며(3.3절의 흔한 함정, 3.3.1절의 숫자 예제 참고), 잘못 설정하면 손쉽게 infeasible에 빠집니다. 아래는 구조를 보여주는 개념 코드이며, 실제 연구에서는 이를 직접 처음부터 구현하기보다 **Troppo**(`troppo.methods.reconstruction`) 프레임워크의 검증된 GIMME/iMAT/FastCORE/tINIT 구현체나 COBRA Toolbox/RAVEN(MATLAB)의 대응 함수를 사용하는 것이 권장됩니다.

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

암 맥락에서의 완전한 Troppo 파이프라인 예시는 [Chapter 7](../chapter-7/README.md)에서 이어집니다.

## 7단계: 검증 — 맥락 특이적 제약이 유전자 필수성 예측을 바꾸는가

1.1절에서 "generic 모델을 그대로 쓰면 유전자 필수성 예측이 부정확할 수 있다"고 이야기했습니다. 이제 4단계에서 얻은 GIMME 스타일 저발현 반응 억제가 실제로 유전자 필수성 예측에 영향을 주는지, `e_coli_core`로 간단히 확인해 봅니다. 여기서는 GIMME가 완전히 꺼버린 저발현 반응들과 관련된 유전자에 한해 원래 모델과 비교합니다.

```python
from cobra.flux_analysis import single_gene_deletion

model.objective = "Biomass_Ecoli_core"
baseline_growth = model.optimize().objective_value

# 4단계에서 완전히 꺼진(off) 저발현 반응들의 유전자를 모아 확인 대상으로 삼는다
off_rxns = [rid for rid in low_rxns if rid not in active_low]
genes_to_check = set()
for rid in off_rxns:
    genes_to_check.update(g.id for g in model.reactions.get_by_id(rid).genes)

print(f"GIMME가 완전히 억제한 반응 수: {len(off_rxns)}, 관련 유전자 수: {len(genes_to_check)}")

result = single_gene_deletion(model, gene_list=list(genes_to_check))
essential = result[result['growth'] < 1e-6]
print(f"원래(generic) 모델 기준 필수 유전자: {len(essential)} / {len(genes_to_check)}개")

# 기대 출력 형태 (실제 유전자 목록과 개수는 난수 시드·데이터에 따라 달라짐):
# GIMME가 완전히 억제한 반응 수: 8, 관련 유전자 수: N개
# 원래(generic) 모델 기준 필수 유전자: M / N개
```

이 검증의 논리는 다음과 같습니다 — 만약 어떤 유전자가 generic 모델에서는 "필수가 아님"으로 나오는데, 그 유전자와 관련된 반응이 이 조직의 맥락 특이적 모델(GIMME 결과)에서는 아예 억제되어 있다면, 그 유전자를 실제로 결손시켰을 때 이 조직에서는 대체 경로가 없어 훨씬 더 치명적인 영향을 줄 수 있습니다. 반대로 generic 모델과 맥락 특이적 모델의 필수성 예측이 일치한다면, 그 유전자는 조직과 무관하게 핵심적인 "하우스키핑" 기능을 담당할 가능성이 높습니다. 이처럼 **generic 모델과 맥락 특이적 모델의 예측을 나란히 비교하는 것**이 1.1절에서 예고한 "표현형 예측 정확도" 검증의 가장 단순한 형태이며, 더 정교한 버전(암-정상 쌍 비교, DepMap CRISPR 데이터 검증)은 [Chapter 7](../chapter-7/README.md)에서 다룹니다.

---
