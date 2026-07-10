# 마무리: 요약 · 스스로 점검 · 용어

## 한 장 요약

- Chapter 2~3에서 만든 모델($$\mathbf{S}$$, bounds, 바이오매스)에는 무한히 많은 플럭스 해가 있다. FBA는 여기에 **최적화 원리** 하나를 추가해 그중 "생물학적으로 최적"인 하나를 골라내는 선형 계획법(LP) 문제다.
- FBA는 **의사정상상태**($$\mathbf{S}\mathbf{v}=\mathbf{0}$$), **플럭스 제약**($$\mathbf{v}^{lb}\le\mathbf{v}\le\mathbf{v}^{ub}$$), **최적화 원리**($$\max\mathbf{c}^\mathsf{T}\mathbf{v}$$)라는 세 가정을 결합한다.
- 3개 반응짜리 장난감 네트워크를 손으로 풀어보면, 가능 영역은 볼록 다각형(폴리토프)이고 적어도 하나의 최적 꼭짓점이 존재한다. 목적함수 계수를 바꾸면 한 면 전체가 최적이 되는 **대안 최적해**도 직접 관찰할 수 있다. 이는 엄밀한 LP 용어의 퇴화와 구분된다.
- 가능한 플럭스 벡터의 집합은 **플럭스 원추**를 이루며, 상하한이 더해지면 **플럭스 폴리토프**로 잘린다. LP는 **심플렉스법**(꼭짓점 순회) 또는 **내점법**(중앙 경로 추적)으로 풀리며, COBRApy는 GLPK/Gurobi/CPLEX 등 다양한 솔버를 동일한 인터페이스로 지원한다.
- **쌍대 문제**의 **그림자 가격**은 물질수지 등식의 국소 민감도이고, exchange bound의 민감도와 구분해야 한다. 부호 규약과 쌍대 비유일성을 확인하며 해석하고, 영양 제한은 bound 스캔으로 검증한다.
- 표준 FBA의 해는 유일하지 않을 수 있다(**대안 최적해**). **pFBA**는 최적 성장률을 유지하며 총 절대 플럭스를 최소화하지만 항상 유일하지 않고, $$\sum|v|$$도 효소 질량 자체는 아니다. **FVA**는 각 반응의 허용 범위를 주지만 통계적 신뢰구간이나 필수성 판정 그 자체는 아니다.
- `e_coli_core`에서 FBA를 실행하면 호기 조건에서 μ ≈ 0.874 h⁻¹, 산소를 차단하면(혐기) 훨씬 낮은 성장률과 발효 부산물 분비가 나타난다.
- FBA는 강력하지만 의사정상상태·동역학 정보 부재·최적성 가정·조절 제약 부재 등의 구조적 한계를 가지며, overflow 대사와 같은 실패 모드를 보인다. 유전자 결손·균주 설계·오믹스 통합·질병 응용은 각각 [Chapter 8](../chapter-8/README.md), [Chapter 6](../chapter-6/README.md), [Chapter 7](../chapter-7/README.md)에서 이어진다.

---

## 스스로 점검

1. **손 계산:** 3.1절의 장난감 네트워크에서 경로 1과 경로 2의 효율이 각각 0.9와 0.4로 바뀌었다고 하자($$\max Z=0.9v_1+0.4v_2$$, 나머지 제약은 동일). 다섯 꼭짓점에서 $$Z$$를 계산하여 새로운 최적해를 구하라.
   > **힌트:** 이번에는 경로 1(계수 0.9)이 더 효율적이므로, 먼저 $$v_1$$을 최대한 채우는 전략을 시도해 보라. 정답은 $$(v_1,v_2)=(6,4)$$, $$Z^*=0.9(6)+0.4(4)=5.4+1.6=7.0$$이다 — $$(2,8)$$의 $$Z=0.9(2)+0.4(8)=5.0$$보다 크다.

2. **개념 확인:** "정상상태(steady state)"와 "평형(equilibrium)"의 차이를 물탱크 비유를 이용해 한 문장으로 설명하라.
   > **힌트:** 1.2절의 흔한 오해 콜아웃을 참고하라. 평형은 흐름이 0인 상태, 정상상태는 흐름은 있지만 농도(수위)가 변하지 않는 상태다.

3. **계산:** `e_coli_core`에서 $$Z^*\approx0.874$$ h$$^{-1}$$을 얻었다고 하자. 포도당 exchange의 lower bound를 -10에서 -10.01로 바꾸었더니 성장률이 0.0005 증가했다. 이 bound에 대한 국소 민감도를 유한차분으로 계산하라. 이것이 `solution.shadow_prices['glc__D_e']`와 반드시 같은가?
   > **힌트:** 민감도는 $$0.0005/(-0.01)=-0.05$$이며 부호는 bound 좌표 방향을 따른다. 이는 **exchange bound의 민감도**이고, `shadow_prices`는 물질수지 등식의 쌍대값이므로 일반적으로 동일한 대상이 아니다.

4. **분류:** FVA를 `fraction_of_optimum=1.0`으로 실행했더니 어떤 반응의 최소·최대 플럭스가 각각 $$-5$$와 $$-5$$로 나왔다. 무엇을 말할 수 있고, 무엇은 말할 수 없는가? 결과가 $$0$$과 $$0$$이라면?
   > **힌트:** 전자는 최적 목적을 유지하는 모든 허용 해에서 고정 활성이라는 뜻이지만, 무성장까지 포함한 "필수 반응"임을 곧바로 증명하지는 않는다. 후자는 현재 조건·목표 아래 차단되었다는 뜻이며, 전역 차단 여부는 모든 교환 조건을 고려해 별도로 검사한다.

5. **한계 인지:** 산소가 충분한데도 세포가 아세테이트를 분비하는 overflow 대사 현상을 표준 FBA가 잘 예측하지 못하는 이유를 한 문장으로 설명하고, 이를 보완하는 방법 하나를 제시하라.
   > **힌트:** 10.2절을 참고하라. FBA는 최대 수율 해를 찾지만 전체 단백질체 예산 제약을 고려하지 않는다. GECKO(효소-제약 모델)나 pFBA가 부분적 대응책이다.

---

## 다음 장 예고

이 장에서 우리는 이미 완성된 모델($$\mathbf{S}$$, bounds, 목적함수)을 "풀어서" 세포의 대사 흐름과 성장률을 예측하는 방법 — FBA, FVA, pFBA — 을 익혔습니다. 그런데 지금까지 우리는 한 가지를 당연하게 가정해 왔습니다: **모델이 이미 있다**는 것입니다. 그렇다면 애초에 이 모델은 어떻게 만들어질까요? 게놈 서열에서 시작해 반응 목록을 조립하고, 빠진 반응을 채워 넣고(gap-filling), 품질을 검증하는 과정은 어떻게 이루어질까요? 다음 [Chapter 5. 모델 구축과 품질 관리](../chapter-5/README.md)에서는 바로 이 질문에 답합니다 — 미생물 모델의 재구축(reconstruction) 파이프라인부터, 훨씬 복잡한 인체 모델(Recon, Human1)의 구축 방법론까지 살펴봅니다.

---

## 핵심 용어 정리

| 용어(한글) | English | 정의 |
|:---|:---|:---|
| 과소결정계 | Underdetermined System | 미지수가 방정식보다 많아 해가 유일하지 않은 연립방정식 |
| 의사정상상태 가정 | Pseudo-Steady-State Assumption | 관심 시간 척도에서 대사물 농도가 일정하다는 가정, $$d\mathbf{x}/dt=\mathbf{0}$$ |
| 선형 계획법 | Linear Programming (LP) | 선형 목적 함수를 선형 제약 하에서 최적화하는 수학적 기법 |
| 플럭스 원추 | Flux Cone | 부호 제약만 부과했을 때 가능한 플럭스 벡터들이 이루는 볼록 다면체 원추 |
| 플럭스 폴리토프 | Flux Polytope | 상하한으로 잘린, 경계가 있는 플럭스 원추 (FBA의 가능 영역) |
| 심플렉스법 | Simplex Method | 폴리토프의 꼭짓점을 순회하며 목적 함수를 개선하는 LP 알고리즘 |
| 내점법 | Interior-Point Method | 가능 영역 내부의 중앙 경로를 따라 최적해에 수렴하는 LP 알고리즘 |
| 쌍대 문제 | Dual Problem | 원 LP 문제의 제약에 대한 민감도 정보를 제공하는 짝 문제 |
| 그림자 가격 | Shadow Price | 물질수지 제약이 완화될 때 목적 함수값이 변하는 정도, $$\partial Z^*/\partial b_i$$ |
| 환원비용 | Reduced Cost | 경계에 붙은 반응이 그 경계를 완화할 때 목적 함수값이 변하는 정도 |
| 강건성 분석 | Robustness Analysis | 특정 반응의 플럭스를 고정해가며 목적 함수값의 변화를 관찰하는 방법 |
| 대안 최적해 | Alternate Optima | 동일한 최적 목적 함수값을 갖는 서로 다른 플럭스 분포 |
| LP 퇴화 | LP Degeneracy | 한 기본 실행가능해에서 필요한 수보다 많은 제약이 동시에 활성인 성질 |
| Parsimonious FBA | pFBA | 최적 성장률을 유지하며 총 플럭스 합을 최소화하는 2단계 LP |
| 플럭스 가변성 분석 | Flux Variability Analysis (FVA) | 준최적 조건 하 각 반응의 플럭스 최소·최대 범위를 계산하는 방법 |
| 표현형 상 평면 | Phenotypic Phase Plane (PhPP) | 두 환경 변수에 대한 최적 성장률 표면과 대사 전환 영역을 나타낸 도표 |
| 제3형 경로 | Type-III Pathway | 환경과 물질 교환 없이 내부 순환만으로 에너지를 생성하는 열역학적으로 불가능한 경로 |

---

## 참고문헌 / 더 읽을거리

1. Savinell, J. M., & Palsson, B. O. (1992). Network analysis of intermediary metabolism using linear optimization. I. Development of mathematical formalism. *Journal of Theoretical Biology*, 154(4), 421–454. doi: `10.1016/S0022-5193(05)80161-4`.
2. Varma, A., & Palsson, B. O. (1994). Stoichiometric flux balance models quantitatively predict growth and metabolic by-product secretion in wild-type *Escherichia coli* W3110. *Applied and Environmental Microbiology*, 60(10), 3724–3731. doi: `10.1128/AEM.60.10.3724-3731.1994`.
3. Edwards, J. S., Ibarra, R. U., & Palsson, B. O. (2001). In silico predictions of *Escherichia coli* metabolic capabilities are consistent with experimental data. *Nature Biotechnology*, 19(2), 125–130. doi: `10.1038/84379`.
4. Ibarra, R. U., Edwards, J. S., & Palsson, B. O. (2002). *Escherichia coli* K-12 undergoes adaptive evolution to achieve in silico predicted optimal growth. *Nature*, 420, 186–189. doi: `10.1038/nature01149`.
5. Mahadevan, R., & Schilling, C. H. (2003). The effects of alternate optimal solutions in constraint-based genome-scale metabolic models. *Metabolic Engineering*, 5(4), 264–276. doi: `10.1016/j.ymben.2003.09.002`.
6. Lewis, N. E., Hixson, K. K., Conrad, T. M., et al. (2010). Omic data from evolved *E. coli* are consistent with computed optimal growth from genome-scale models. *Molecular Systems Biology*, 6, 390. doi: `10.1038/msb.2010.47`.
7. Schuetz, R., Kuepfer, L., & Sauer, U. (2007). Systematic evaluation of objective functions for predicting intracellular fluxes in *Escherichia coli*. *Molecular Systems Biology*, 3, 119.
8. Orth, J. D., Thiele, I., & Palsson, B. O. (2010). What is flux balance analysis? *Nature Biotechnology*, 28(3), 245–248.
9. Feist, A. M., & Palsson, B. O. (2010). The biomass objective function. *Current Opinion in Microbiology*, 13(3), 344–349.
10. Monk, J. M., Lloyd, C. J., Brunk, E., et al. (2017). iML1515, a knowledgebase that computes *Escherichia coli* traits. *Nature Biotechnology*, 35(10), 904–908.
11. Ebrahim, A., Lerman, J. A., Palsson, B. O., & Hyduke, D. R. (2013). COBRApy: COnstraints-Based Reconstruction and Analysis for Python. *BMC Systems Biology*, 7, 74.
12. Gudmundsson, S., & Thiele, I. (2010). Computationally efficient flux variability analysis. *BMC Bioinformatics*, 11, 489.
13. Palsson, B. O. (2015). *Systems Biology: Constraint-based Reconstruction and Analysis* (2nd ed.). Cambridge University Press.
14. [COBRApy Documentation](https://cobrapy.readthedocs.io/)
15. [BiGG Models Database](http://bigg.ucsd.edu/)
