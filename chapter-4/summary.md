# 마무리: 요약 · 스스로 점검 · 용어

## 한 장 요약

- Chapter 2~3에서 만든 모델($$\mathbf{S}$$, bounds, 바이오매스)은 일반적으로 여러 플럭스 해를 허용한다. FBA는 목적함수를 추가해 지정한 모델·환경·목적 가설 아래의 최적해 또는 최적해 집합을 구하는 [선형 계획법](../glossary.md)(LP)이다. 계산 최적해를 곧바로 생물학적으로 유일한 상태라고 해석할 수는 없다.
- FBA는 **[의사정상상태](../glossary.md)**($$\mathbf{S}\mathbf{v}=\mathbf{0}$$), **플럭스 제약**($$\mathbf{v}^{lb}\le\mathbf{v}\le\mathbf{v}^{ub}$$), **최적화 원리**($$\max\mathbf{c}^\mathsf{T}\mathbf{v}$$)라는 세 가정을 결합한다. **슬랙 변수**와 $$v=v^+-v^-$$ 분해로 이 문제를 등식·비음수 표준형으로 바꿀 수 있다.
- 3개 반응짜리 장난감 네트워크를 손으로 풀어보면, 가능 영역은 볼록 다각형(폴리토프)이고 적어도 하나의 최적 꼭짓점이 존재한다. 목적함수 계수나 제약의 상한을 바꾸면 최적 꼭짓점의 위치·개수 자체가 바뀔 수 있고, 한 면 전체가 최적이 되는 **[대안 최적해](../glossary.md)**도 직접 관찰할 수 있다. 이는 엄밀한 LP 용어의 퇴화와 구분된다.
- 비가역 반응만 남기거나 가역 반응을 순·역방향 비음수 변수로 분할하면 가능한 정상상태 플럭스가 **[플럭스 원추](../glossary.md)**를 이룬다. 충분한 유한 상하한이 더해져 집합이 유계이면 **플럭스 폴리토프**가 된다. LP는 **심플렉스법** 또는 **내점법**으로 풀 수 있으며, [COBRApy](https://opencobra.github.io/cobrapy/)는 여러 솔버를 공통 인터페이스로 연결한다.
- **쌍대 문제**의 **[그림자 가격](../glossary.md)**은 물질수지 등식 또는 bound의 국소 민감도를 제공한다. exchange bound의 민감도와 대사물 물질수지 등식의 그림자 가격은 다른 대상이다. 양의 자원 제약 한계가치와 그 제약에 추가한 슬랙 변수의 reduced cost는 좌표 방향이 반대이므로 부호도 반대다. 목적 방향, 제약 작성법, 솔버 convention과 쌍대 비유일성을 확인하고 유한차분으로 해석을 검증해야 한다.
- 표준 FBA의 해는 유일하지 않을 수 있다(**대안 최적해**). **[pFBA](../glossary.md)**는 주 목적값을 유지하며 총 절대 플럭스(**[L1 노름](../glossary.md)**)가 작은 대표 해를 구해 불필요한 순환을 줄일 수 있지만, 해의 유일성이나 열역학적 loop 제거를 보장하지 않으며 $$\sum|v|$$도 효소 질량이 아니다. **[FVA](../glossary.md)**는 각 반응을 따로 투영한 허용 범위를 주지만 반응 간 공동분포, 통계적 신뢰구간 또는 필수성 판정 자체는 아니다.
- COBRApy 0.30.0 `textbook` 모델의 기본 배지·bounds와 바이오매스 목적함수를 GLPK로 풀면 호기 조건에서 $$\mu\approx0.874$$ h$$^{-1}$$이고, 산소 섭취를 차단하면 더 낮은 성장률과 발효 부산물 분비가 계산된다. 이 값은 모델·배지·유지에너지·solver 허용오차에 의존한다.
- FBA는 의사정상상태, 목적함수, 조절·동역학·단백질체 정보의 생략이라는 구조적 한계를 가진다. 특히 화학량론과 바이오매스 최대화만으로는 overflow 대사의 단백질 비용 기전을 표현하지 못할 수 있다. 방향별 절대 flux와 단위가 일관된 효소·단백질체 제약은 이 기전을 모델에 추가하는 한 방법이다. 유전자 결손·균주 설계·오믹스 통합·질병 응용은 각각 [Chapter 8](../chapter-8/README.md), [Chapter 6](../chapter-6/README.md), [Chapter 7](../chapter-7/README.md)에서 이어진다.

---

## 스스로 점검

1. **손 계산:** 3.1절의 장난감 네트워크에서 경로 1과 경로 2의 효율이 각각 0.9와 0.4로 바뀌었다고 하자($$\max Z=0.9v_1+0.4v_2$$, 나머지 제약은 동일). 다섯 꼭짓점에서 $$Z$$를 계산하여 새로운 최적해를 구하라.
   > **힌트:** 두 목적계수의 대소 관계가 3.3절과 반대로 뒤집혔다. 어느 경로를 먼저 상한까지 채우게 되는지 다시 판단한 뒤, 다섯 꼭짓점 $$(0,0),(6,0),(6,4),(2,8),(0,8)$$에서 $$Z$$를 모두 계산해 비교한다.

2. **개념 확인:** "정상상태(steady state)"와 "평형(equilibrium)"의 차이를 물탱크 비유를 이용해 한 문장으로 설명하라.
   > **힌트:** 두 개념이 각각 무엇을 0으로 두는지 구분한다. 1.2절의 경고 상자에서 순 구동력과 순축적률 중 어느 쪽이 어느 개념에 대응하는지 확인한다.

3. **계산:** `e_coli_core`에서 $$Z^*\approx0.874$$ h$$^{-1}$$을 얻었다고 하자. 포도당 exchange의 lower bound를 -10에서 -10.01로 바꾸었더니 성장률이 0.0005 증가했다. 이 bound에 대한 국소 민감도를 유한차분으로 계산하라. 이것이 `solution.shadow_prices['glc__D_e']`와 반드시 같은가?
   > **힌트:** 유한차분은 (목적값 변화)/(bound 변화)이며 부호는 bound 좌표 방향을 따른다. 두 값이 같은 대상인지는 5.2절이 구분한 "exchange bound의 민감도"와 "물질수지 등식의 쌍대값"의 정의를 대조해 판단한다.

4. **분류:** FVA를 `fraction_of_optimum=1.0`으로 실행했더니 어떤 반응의 최소·최대 플럭스가 각각 $$-5$$와 $$-5$$로 나왔다. 무엇을 말할 수 있고, 무엇은 말할 수 없는가? 결과가 $$0$$과 $$0$$이라면?
   > **힌트:** 9.2절의 분류 기준(고정 활성 / 목표 유지에 필요 / 차단됨)과 같은 절이 정의한 **반응 필수성**의 판정 절차가 어떻게 다른지 대조한다. 차단의 경우 조건부 비활성과 전역 차단을 구분해야 한다.

5. **한계 인지:** 산소가 충분한데도 세포가 아세테이트를 분비하는 overflow 대사 현상을 표준 FBA가 잘 예측하지 못하는 이유를 한 문장으로 설명하고, 이를 보완하는 방법 하나를 제시하라.
   > **힌트:** 10.2절 표의 "목적·자원 제약의 편향" 행에서 표준 FBA가 무엇을 모델에 담고 있지 않은지 먼저 특정한 뒤, 10.4절의 효소 비용 제약이 그 빈자리를 어떻게 채우는지 연결한다.

6. **pFBA의 동작 원리:** 8.4절의 무익한 순환 반응 $$v_4,v_5$$(목적계수 0, $$v_4=v_5$$) 예제에서, 만약 두 반응에 아주 작더라도 0이 아닌 목적계수(예: $$c_4=c_5=0.001$$)가 붙는다면 pFBA의 2단계 목적식 $$\min(v_1+v_2+v_4+v_5)$$가 여전히 $$v_4=v_5=0$$을 최적으로 고를까?
   > **힌트:** 8.4절에서 "2단계 목적식이 $$k$$에 대해 단조 증가"라는 결론을 얻으려면 1단계 최적값 $$Z^*$$가 $$k$$와 무관해야 했다. 목적계수가 0이 아니게 될 때 그 전제가 유지되는지 확인한다.

<details>

<summary>정답 핵심</summary>

1. $$(v_1,v_2)=(6,4)$$, $$Z^*=0.9(6)+0.4(4)=5.4+1.6=7.0$$이다. $$(2,8)$$의 $$Z=0.9(2)+0.4(8)=5.0$$보다 크다.
2. 열역학적 평형에서는 순 구동력과 순 반응 플럭스가 0이지만, 정상상태는 대사물의 순축적률만 0이므로 비영 플럭스가 네트워크를 통과할 수 있다.
3. 민감도는 $$0.0005/(-0.01)=-0.05$$이며 부호는 bound 좌표 방향을 따른다. 이는 exchange bound의 민감도이고, `shadow_prices`는 물질수지 등식의 쌍대값이므로 일반적으로 동일한 대상이 아니다.
4. 최소·최대가 모두 $$-5$$이면 최적 목적을 유지하는 모든 허용 해에서 고정 활성이라는 뜻이지만, 무성장까지 포함한 "필수 반응"임을 곧바로 증명하지는 않는다. 모두 $$0$$이면 현재 조건·목표 아래 차단되었다는 뜻이며, 전역 차단 여부는 모든 교환 조건을 고려해 별도로 검사한다.
5. 기질 섭취량을 고정한 바이오매스 최대화는 높은 성장수율의 호흡 해를 선호할 수 있지만, 표준 FBA에는 유한한 단백질체 배분이 없다. 방향별 효소량과 $$k_{cat}$$을 연결한 GECKO류 효소-제약 모델이 한 대응책이며, 단순 pFBA의 총 절대 플럭스는 효소 질량을 대신하지 않는다.
6. 고르지 않을 수 있다. 1단계에서 $$Z^*$$ 자체가 바뀌므로 문제가 달라진다. 목적계수가 정확히 0일 때만 8.4절의 논리가 그대로 성립하며, 조금이라도 양의 계수가 붙으면 1단계 최적화가 오히려 그 반응의 플럭스를 늘리려 할 수 있다.

</details>

---

## 다음 장 예고

이 장은 이미 구성된 모델($$\mathbf{S}$$, bounds, 목적함수)을 이용해 FBA, FVA와 pFBA를 수행하는 방법을 다뤘다. 다음 [Chapter 5. 모델 구축과 품질 관리](../chapter-5/README.md)에서는 게놈 서열과 생화학 근거로 반응 목록을 조립하고, gap-filling과 품질 검증을 거쳐 계산 모델을 구축하는 과정을 다룬다.

---

## 핵심 용어 정리

| 용어(한글) | English | 정의 |
|:---|:---|:---|
| 과소결정계 | Underdetermined System | 미지수가 방정식보다 많아 해가 유일하지 않은 연립방정식 |
| [의사정상상태 가정](../glossary.md) | Pseudo-Steady-State Assumption | 관심 시간 척도에서 대사물 농도가 일정하다는 가정, $$d\mathbf{x}/dt=\mathbf{0}$$ |
| [선형 계획법](../glossary.md) | Linear Programming (LP) | 선형 목적함수를 선형 제약 하에서 최적화하는 수학적 기법 |
| [플럭스 원추](../glossary.md) | Flux Cone | 가역 반응을 방향별 비음수 변수로 표현하고 정상상태·방향성만 부과했을 때 가능한 플럭스가 이루는 볼록 다면체 원추 |
| 플럭스 폴리토프 | Flux Polytope | 충분한 유한 상하한으로 플럭스 원추를 잘라 얻은 유계 다면체; FBA 실행가능 영역이 항상 유계인 것은 아님 |
| 심플렉스법 | Simplex Method | 폴리토프의 꼭짓점을 순회하며 목적함수를 개선하는 LP 알고리즘 |
| 내점법 | Interior-Point Method | 가능 영역 내부의 중앙 경로를 따라 최적해에 수렴하는 LP 알고리즘 |
| 쌍대 문제 | Dual Problem | 원 LP 문제의 제약에 대한 민감도 정보를 제공하는 짝 문제 |
| [그림자 가격](../glossary.md) | Shadow Price | 물질수지 제약이 완화될 때 목적함수값이 변하는 정도, $$\partial Z^*/\partial b_i$$ |
| 환원비용 | Reduced Cost | 현재 쌍대 가격으로 변수 열의 기회비용을 보정한 목적계수 잔차; bound 민감도와의 부호 관계는 정식화에 의존 |
| 강건성 분석 | Robustness Analysis | 특정 반응의 플럭스를 고정해가며 목적함수값의 변화를 관찰하는 방법 |
| [대안 최적해](../glossary.md) | Alternate Optima | 동일한 최적 목적함수값을 갖는 서로 다른 플럭스 분포 |
| LP 퇴화 | LP Degeneracy | 한 기본 실행가능해에서 필요한 수보다 많은 제약이 동시에 활성인 성질 |
| Parsimonious FBA | [pFBA](../glossary.md) | 주 목적값을 유지하며 총 절대 플럭스 $$\sum_j|v_j|$$를 최소화하는 순차 LP |
| 플럭스 가변성 분석 | [Flux Variability Analysis (FVA)](../glossary.md) | 준최적 조건 하 각 반응의 플럭스 최소·최대 범위를 계산하는 방법 |
| [표현형 상 평면](../glossary.md) | Phenotypic Phase Plane (PhPP) | 두 환경 변수에 대한 최적 성장률 표면과 대사 전환 영역을 나타낸 도표 |
| 제3형 경로 | Type-III Pathway | 환경과 물질 교환 없이 내부 순환만으로 에너지를 생성하는 열역학적으로 불가능한 경로 |
| 슬랙 변수 | Slack Variable | 부등식 제약을 등식으로 바꾸기 위해 도입하는 여분(0 이상)을 나타내는 변수 |
| KKT 조건 | Karush–Kuhn–Tucker Conditions | 부등식 제약이 있는 최적화 문제의 최적해가 만족해야 하는 원 실행가능성·쌍대 실행가능성·정상성·상보 여유성 조건 |
| 상보 여유성 | Complementary Slackness | 빠듯하지 않은 제약의 쌍대 변수는 0이고, 0이 아닌 원 변수에 대응하는 쌍대 제약은 등식으로 빠듯하다는 LP 쌍대 정리의 핵심 규칙 |
| [L1 노름](../glossary.md) | L1-norm | 벡터 성분의 절댓값을 모두 더한 값 $$\sum_j\lvert v_j\rvert$$; pFBA가 최소화하는 대상 |
| 단백질체 예산 | Proteome Budget | 세포가 효소 합성에 배정할 수 있는 총 단백질 질량이 유한하다는 제약; 효소-제약 모델(GECKO 등)의 핵심 가정 |

---

## 참고문헌 / 더 읽을거리

> 각 논문이 어떤 질문·근거·한계를 가졌는지 다섯 질문으로 정리한 서술은 [필독 논문 가이드](../landmark-papers.md)에 있다.

1. Savinell, J. M., & Palsson, B. O. (1992). Network analysis of intermediary metabolism using linear optimization. I. Development of mathematical formalism. *Journal of Theoretical Biology*, 154(4), 421–454. [doi:10.1016/S0022-5193(05)80161-4](https://doi.org/10.1016/S0022-5193(05)80161-4).
2. Varma, A., & Palsson, B. O. (1994). Stoichiometric flux balance models quantitatively predict growth and metabolic by-product secretion in wild-type *Escherichia coli* W3110. *Applied and Environmental Microbiology*, 60(10), 3724–3731. [doi:10.1128/AEM.60.10.3724-3731.1994](https://doi.org/10.1128/AEM.60.10.3724-3731.1994).
3. Edwards, J. S., Ibarra, R. U., & Palsson, B. O. (2001). In silico predictions of *Escherichia coli* metabolic capabilities are consistent with experimental data. *Nature Biotechnology*, 19(2), 125–130. [doi:10.1038/84379](https://doi.org/10.1038/84379).
4. Ibarra, R. U., Edwards, J. S., & Palsson, B. O. (2002). *Escherichia coli* K-12 undergoes adaptive evolution to achieve in silico predicted optimal growth. *Nature*, 420, 186–189. [doi:10.1038/nature01149](https://doi.org/10.1038/nature01149).
5. Mahadevan, R., & Schilling, C. H. (2003). The effects of alternate optimal solutions in constraint-based genome-scale metabolic models. *Metabolic Engineering*, 5(4), 264–276. [doi:10.1016/j.ymben.2003.09.002](https://doi.org/10.1016/j.ymben.2003.09.002).
6. Lewis, N. E., Hixson, K. K., Conrad, T. M., et al. (2010). Omic data from evolved *E. coli* are consistent with computed optimal growth from genome-scale models. *Molecular Systems Biology*, 6, 390. [doi:10.1038/msb.2010.47](https://doi.org/10.1038/msb.2010.47).
7. Schuetz, R., Kuepfer, L., & Sauer, U. (2007). Systematic evaluation of objective functions for predicting intracellular fluxes in *Escherichia coli*. *Molecular Systems Biology*, 3, 119.
8. Orth, J. D., Thiele, I., & Palsson, B. O. (2010). What is flux balance analysis? *Nature Biotechnology*, 28(3), 245–248. [doi:10.1038/nbt.1614](https://doi.org/10.1038/nbt.1614).
9. Feist, A. M., & Palsson, B. O. (2010). The biomass objective function. *Current Opinion in Microbiology*, 13(3), 344–349. [doi:10.1016/j.mib.2010.03.003](https://doi.org/10.1016/j.mib.2010.03.003).
10. Monk, J. M., Lloyd, C. J., Brunk, E., et al. (2017). iML1515, a knowledgebase that computes *Escherichia coli* traits. *Nature Biotechnology*, 35(10), 904–908. [doi:10.1038/nbt.3956](https://doi.org/10.1038/nbt.3956).
11. Ebrahim, A., Lerman, J. A., Palsson, B. O., & Hyduke, D. R. (2013). COBRApy: COnstraints-Based Reconstruction and Analysis for Python. *BMC Systems Biology*, 7, 74. [doi:10.1186/1752-0509-7-74](https://doi.org/10.1186/1752-0509-7-74).
12. Gudmundsson, S., & Thiele, I. (2010). Computationally efficient flux variability analysis. *BMC Bioinformatics*, 11, 489.
13. Palsson, B. O. (2015). *Systems Biology: Constraint-based Reconstruction and Analysis* (2nd ed.). Cambridge University Press.
14. [COBRApy Documentation](https://cobrapy.readthedocs.io/)
15. [BiGG Models Database](http://bigg.ucsd.edu/)
16. Schilling, C. H., Letscher, D., & Palsson, B. O. (2000). Theory for the systemic definition of metabolic pathways and their use in interpreting metabolic function from a pathway-oriented perspective. *Journal of Theoretical Biology*, 203(3), 229–248. [doi:10.1006/jtbi.2000.1073](https://doi.org/10.1006/jtbi.2000.1073).
17. Edwards, J. S., & Palsson, B. O. (2000). Robustness analysis of the *Escherichia coli* metabolic network. *Biotechnology Progress*, 16(6), 927–939. [doi:10.1021/bp0000712](https://doi.org/10.1021/bp0000712).
18. Edwards, J. S., Ramakrishna, R., & Palsson, B. O. (2002). Characterizing the metabolic phenotype: A phenotype phase plane analysis. *Biotechnology and Bioengineering*, 77(1), 27–36. [doi:10.1002/bit.10047](https://doi.org/10.1002/bit.10047).
19. Basan, M., Hui, S., Okano, H., et al. (2015). Overflow metabolism in *Escherichia coli* results from efficient proteome allocation. *Nature*, 528, 99–104. [doi:10.1038/nature15765](https://doi.org/10.1038/nature15765).
20. Wiechert, W., Möllney, M., Petersen, S., & de Graaf, A. A. (2001). A universal framework for $$^{13}$$C metabolic flux analysis. *Metabolic Engineering*, 3(3), 265–283. [doi:10.1006/mben.2001.0188](https://doi.org/10.1006/mben.2001.0188).
21. Sánchez, B. J., Zhang, C., Nilsson, A., et al. (2017). Improving the phenotype predictions of a yeast genome-scale metabolic model by incorporating enzymatic constraints. *Molecular Systems Biology*, 13(8), 935. [doi:10.15252/msb.20167411](https://doi.org/10.15252/msb.20167411).
