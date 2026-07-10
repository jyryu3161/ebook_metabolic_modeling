# 실습: RNA-seq 발현 데이터를 GEM에 통합하기

> 💡 **실습:** 아래 코드는 핵심 흐름만 보여주는 발췌본입니다. [Chapter 1](../chapter-1/README.md)에서 불러온 것과 동일한 COBRApy 내장 모델 `e_coli_core`(95개 반응·72개 대사물·137개 유전자)를 다시 사용합니다. 대규모 TCGA 데이터와 실제 Human1/Recon3D, Troppo 프레임워크를 이용한 전체 파이프라인은 `gem9_w06_lab.ipynb`(간 특이적 tINIT 스타일 추출)와 `gem9_w07_lab.ipynb`(TCGA 스타일 RNA-seq 시뮬레이션과 맥락 특이적 암 모델 구축)를 참고하십시오.

## 1단계: raw counts → TPM 정규화

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

## 2단계: 발현 임계값 이산화 방법 비교

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

## 3단계: `e_coli_core`의 실제 GPR로 RAS 계산

파이썬에서 `and`/`or`는 예약어이므로, GPR 문자열(예: `"b3916 or b1723"`)은 그대로 하나의 불리언 표현식입니다. 이 성질을 이용해 `ast` 모듈로 파싱한 뒤 재귀적으로 평가하면, 2.2절에서 손으로 계산한 것과 똑같은 로직을 실제 137개 유전자·95개 반응 규모에 그대로 적용할 수 있습니다.

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

## 4단계: GIMME 2단계 LP를 `e_coli_core`에 직접 실행

3단계에서 얻은 `reaction_weights`를 그대로 이어받아, 3.2절의 GIMME 2단계 LP를 실제로 풀어봅니다.

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

`with model:` 블록을 벗어나면 원래 목적 함수와 경계가 자동으로 복원되어([Chapter 4](../chapter-4/README.md) 참고), 다음 실습에 영향을 주지 않습니다.

## 5단계: E-Flux 경계 스케일링을 `e_coli_core`에 직접 실행

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

## 6단계: iMAT은 왜 개념 코드로만 소개하는가

iMAT의 MILP는 $$y_j$$–$$v_j$$ big-M 연결 제약을 반응마다 정확한 하한·상한으로 조정해야 하며(3.3절의 흔한 함정 참고), 잘못 설정하면 손쉽게 infeasible에 빠집니다. 아래는 구조를 보여주는 개념 코드이며, 실제 연구에서는 이를 직접 처음부터 구현하기보다 **Troppo**(`troppo.methods.reconstruction`) 프레임워크의 검증된 GIMME/iMAT/FastCORE/tINIT 구현체나 COBRA Toolbox/RAVEN(MATLAB)의 대응 함수를 사용하는 것이 권장됩니다.

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

---
