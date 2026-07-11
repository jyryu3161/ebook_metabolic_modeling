# 마무리: 요약 · 스스로 점검 · 용어

## 한 장 요약

- **Perturbation 분석은 feasible space의 축소로 시작한다.** 유전자 결손·약물·환경 변화는 세 가지 제약(화학량론적·열역학적·perturbation-specific)에 반응 비활성화 제약 $$v_j=0$$을 더해 $$\mathcal{P}_{MUT}\subseteq\mathcal{P}_{WT}$$로 feasible space를 줄이며, 세포가 이 축소된 공간에서 어떤 flux를 택하는지가 핵심 질문이다.
- **GPR 규칙의 Boolean 평가가 유전자 결손을 반응 비활성화로 번역한다.** `or`(isozyme)는 둘 다 결손되어야, `and`(복합체)는 하나만 결손되어도 반응이 꺼지며(§1.3에서 손으로 확인), 이 논리가 대사 네트워크 강건성/취약성의 유전적 근거다.
- **FBA·MOMA·ROOM은 서로 다른 검증 가능한 가설이다.** FBA는 mutant 공간에서 주 목적을 재최적화하고 WT reference를 쓰지 않는다. quadratic MOMA는 WT와의 $$L_2$$ 거리를, linear MOMA는 $$L_1$$ 거리를, ROOM은 허용 범위를 벗어난 반응 수를 최소화한다. `objective_value`의 의미도 서로 다르므로 성장률은 바이오매스 flux에서 비교한다.
- **합성 치사는 이중 결손 분석의 자연스러운 산물이다.** epistasis score $$\varepsilon_{ij}=W_{ij}-W_i W_j$$가 강한 음수인 유전자 쌍은 항생제·항암 표적으로 유망하며(§2.4에서 손 계산), PARP-BRCA가 대표적 임상 사례다.
- **균주 설계 알고리듬은 perturbation을 예측 대상에서 최적화 변수로 바꾼다.** OptKnock(결손, 이중 레벨 MILP), OptForce(강제 flux 변화, FVA 기반), OptGene(유전 알고리듬, MOMA/ROOM 결합), FSEOF(증폭 표적)는 각기 다른 개입 유형과 정형화를 대표하며, growth-coupled 설계가 적응 진화에도 생산성을 유지시킨다.
- **Production envelope와 PhPP는 생산-생장 트레이드오프를 시각화한다.** 포락선의 하한이 최대 생장율에서 0보다 크면 growth-coupled 설계이며(§7.1에서 꼭짓점 읽기), PhPP는 두 환경 변수에 따른 최적 전략 전환(Line of Optimality)을 지도화한다.
- **계산 모델은 DBTL 주기의 한 구성요소다.** FSEOF–actinorhodin처럼 직접 검증된 예측도 있지만, succinate와 아르테미신산 사례의 성과를 특정 GEM 알고리듬 하나의 효과로 돌리면 안 된다. 후보 설계, 편집, 적응·배양, 분석과 공정 최적화의 기여를 원 논문에서 분리해 읽는다.
- **커뮤니티 모델링은 단일 종 방법을 다종 시스템으로 확장한다.** cross-feeding·competition·mutualism을 화학량론적 제약 안에 표현하며, MICOM·SteadyCom·OptCom·COMETS 등이 규모·해상도의 트레이드오프에 따라 선택되고, AGORA2(7,302 균주)와 결합해 장내 미생물·환경·합성 군집 응용을 가능하게 한다.

---

## 스스로 점검

1. **(GPR 손 계산)** 반응 R1의 GPR 규칙이 `(geneA and geneB) or geneC`이다. `geneA`만 결손시키고 `geneB`, `geneC`는 그대로 두었을 때 R1은 활성 상태로 남는가? §1.3의 절차대로 판정하라. *(정답: `geneA=False, geneB=True, geneC=True` → `(False and True) or True = True`. `and` 분기가 끊겨도 `or`로 연결된 `geneC` 경로가 살아있어 R1은 **활성** — isozyme·대체 경로가 있는 반응이 강건한 이유다.)*

2. **(Epistasis 계산)** 유전자 X 단일 결손 시 $$W_X=0.6$$, 유전자 Y 단일 결손 시 $$W_Y=0.9$$, 이중 결손 시 $$W_{XY}=0.1$$이다. $$\varepsilon_{XY}$$를 계산하고 §2.4의 어느 범주인지 판정하라. *(정답: $$\varepsilon_{XY}=0.1-(0.6\times0.9)=0.1-0.54=-0.44$$, 강한 음수 → **synergistic**이며 $$W_{XY}$$가 0에 가까워 합성 치사(엄밀히는 완전 치사에 못 미쳐 synthetic sick에 근접) 후보다.)*

3. **(방법 선택)** 항생제를 처리한 지 5분 된 세포의 flux 재분배를 예측하려 한다. 어떤 방법을 우선 가설로 시험하고, 어떤 검증이 필요한가? *(정답: 적응 전 WT 근접성 가설인 **MOMA**를 우선 비교할 수 있다. 그러나 시간만으로 정답이 정해지지 않으므로 같은 기준 flux로 FBA·ROOM과 비교하고, 시계열 flux 또는 성장 데이터로 검증해야 한다. 정상상태 가정 자체가 부적절한지도 확인한다.)*

4. **(Production envelope 해석)** 어떤 균주 설계의 production envelope에서 최대 생장율 지점의 산물 flux **하한이 0**으로 나타났다. 성공적인 growth-coupled 균주인가? 개선하려면 §6.6의 어떤 알고리듬을? *(정답: 하한이 0이면 산물 생산 없이도 최적 생장이 가능하므로 **growth-coupled로 보기 어렵다**. 대안 최적해 중 최악의 경우를 직접 최대화하는 **RobustKnock**(max-min)을 우선 고려할 수 있다. M-OptKnock도 사례에 따라 하한을 개선할 수 있지만 보편적 보장은 아니므로, 어느 설계든 production envelope로 재검증해야 한다.)*

5. **(커뮤니티 프레임워크 선택)** (a) 장내 미생물 200종의 메타지놈 상대 존재비 데이터가 있고 계산 자원은 제한적. (b) 토양 biofilm의 2차원 공간 구조를 재현하고 싶다. 각 상황에 §9.3의 어느 프레임워크가 적합한가? *(정답: (a) 종 수가 많고 공간 구조가 덜 중요 → **MICOM**(또는 SteadyCom) 같은 well-mixed·steady-state 프레임워크. (b) 공간적으로 이질적인 개체 단위 상호작용이 핵심 → **BacArena**(또는 COMETS) 같은 공간 explicit 프레임워크.)*

6. **(MOMA QP 손 계산)** §3.2의 장난감 네트워크($$v_1$$ 흡수, $$v_2$$ 주경로, $$v_3$$ 대체경로, 질량보존 $$v_1=v_2+v_3$$, WT flux $$\mathbf{w}=(10,10,0)$$)에서 $$v_2$$를 결손했다. $$v_1=v_3=t$$로 매개변수화한 MOMA 목적함수 $$f(t)=(t-10)^2+(0-10)^2+(t-0)^2$$을 최소화하는 $$t$$와 그때의 산출($$v_3$$)을 구하라. 같은 결손에서 FBA는 산출을 얼마로 예측하는가? *(정답: $$f(t)=2t^2-20t+200$$, $$f'(t)=4t-20=0$$에서 $$t=5$$. 따라서 MOMA 해는 $$(5,0,5)$$로 산출 5. 반면 FBA는 대체경로 용량을 끝까지 써서 $$v_1=v_3=10$$, 산출 10을 예측한다 — MOMA가 더 보수적이다.)*

7. **(OptKnock 이중 레벨 손 계산)** §6.2의 네트워크에서 세포(하위 문제)는 바이오매스 $$v_2+0.5v_3$$을 최대화하고, $$v_2$$($$A\to$$바이오매스, 계수 1)와 $$v_3$$($$A\to$$바이오매스 0.5 + 산물 0.5)가 흡수 $$v_1\le10$$을 나눠 쓴다. $$v_2$$를 결손했을 때 세포의 최대 생장점에서 산물 flux는 얼마이며 growth-coupled인가? *(정답: $$v_2=0$$이면 세포는 $$v_3=10$$만 쓸 수 있어 바이오매스 5, 산물 $$0.5\times10=5$$. 세포가 최적으로 자라는 바로 그 점에서 산물이 필연적으로 5가 나오므로 **growth-coupled**다 — 결손 전에는 세포가 $$v_2$$에 몰아 산물 0인 non-coupled였다.)*

---

## 다음 장 예고

이 장에서 우리는 유전자 결손의 메커니즘(GPR 불리언 평가, MOMA/ROOM의 정형화)부터, 세포를 유용 물질 공장으로 개조하는 균주 설계 알고리듬(OptKnock·OptForce·OptGene·FSEOF), production envelope를 통한 생장-생산 트레이드오프 시각화, 그리고 여러 미생물이 대사를 나누는 커뮤니티 모델링까지 살펴봤습니다.

그런데 여기서 다룬 모든 방법 — perturbation 예측(MOMA/ROOM)과 균주 설계(OptKnock 등) — 은 공통적으로 **화학량론·최적화에 기반한 기계론적(mechanistic) 방법**입니다. 결손 조합을 MILP·QP로 정확히 풀거나 유전 알고리듬으로 탐색하는 식이지요. 하지만 이런 정확해 탐색은 계산 비용이 크고, 유전자 서열·효소 동역학처럼 화학량론만으로는 담을 수 없는 정보를 활용하지 못합니다. 만약 실험 데이터에서 **패턴을 학습**해 "이 유전자를 끄면 어떻게 될지"를 빠르게 예측할 수 있다면 어떨까요? 다음 [Chapter 9. AI와 대사모델링](../chapter-9/README.md)에서는 AMN-Reservoir·FlowGAT·FluxGAT처럼 **머신러닝이 필수성 예측과 플럭스 추정을 가속·보완**하는 흐름을 다룹니다 — 기계론적 모델과 데이터 기반 모델이 어떻게 손잡는지 확인하게 될 것입니다.

---

## 핵심 용어 정리

아래 표는 이 장에서 새로 도입한 용어를 정리한다. 여러 챕터에 걸쳐 반복되는 핵심 용어(MOMA·ROOM·OptKnock·OptForce·FSEOF·production envelope·PhPP·null space·synthetic lethality 등)는 [핵심 용어집](../glossary.md)에도 통합되어 있으니, 다른 장을 읽다가 정의가 가물가물하면 그쪽을 먼저 확인해도 좋다.

| 용어 (한글 / English) | 정의 | 관련 챕터 |
|:---|:---|:---|
| 섭동 / Perturbation | 유전적·환경적·화학적 변화에 의해 feasible space와 flux distribution이 재배치되는 과정 | 본 장 §1 |
| 유전자 결손 / Gene knockout | GPR 규칙을 통해 특정 유전자 관련 반응을 $$v_j=0$$으로 비활성화하는 in silico 조작 | 본 장 §1–2 |
| GPR / Gene-Protein-Reaction | 유전자·단백질·반응의 관계를 Boolean logic으로 표현한 규칙 | [Ch3](../chapter-3/README.md) |
| Null space / 영공간 | $$\mathbf{Sv}=\mathbf{0}$$을 만족하는 모든 flux 벡터의 집합; 차원 = $$n-\text{rank}(\mathbf{S})$$ | 본 장 §1.2, [Ch2](../chapter-2/README.md) |
| 필수성 / Essentiality | 유전자 결손이 생장을 불가능하게 만드는 정도 (essential/growth-reduced/non-essential) | 본 장 §2 |
| 에피스태시 / Epistasis | $$\varepsilon_{ij}=W_{ij}-W_i W_j$$; 두 유전자 결합 효과의 비가산성 | 본 장 §2.4 |
| 합성 치사 / Synthetic lethality | 개별로는 비필수이나 동시 결손 시 치명적인 유전자 쌍 | 본 장 §2.4, [Ch7](../chapter-7/README.md) |
| MOMA | 원형은 QP로 $$L_2^2$$ 거리를 최소화하며, linear MOMA는 LP로 $$L_1$$ 거리를 최소화하는 perturbation 예측법 | 본 장 §3 |
| ROOM | MILP로 유의하게 변한 반응의 수 $$\sum_i y_i$$를 최소화하는 perturbation 예측법 | 본 장 §4 |
| Tolerance threshold ($$\delta$$) | ROOM에서 "유의한 변화"를 판정하는 허용 범위 | 본 장 §4.2–4.3 |
| 균주 설계 / Strain design | 목표 화합물 생산을 위한 유전적 개입을 계산적으로 탐색하는 과정 | 본 장 §6 |
| OptKnock | 이중 레벨 MILP로 growth-coupled 결손 전략을 찾는 알고리듬 | 본 장 §6.2 |
| OptForce | FVA 기반 MUST/FORCE set으로 강제 flux 변화 표적을 찾는 알고리듬 | 본 장 §6.3 |
| OptGene | 유전 알고리듬으로 비선형 목적함수(BPCY)를 최적화하는 균주 설계법 | 본 장 §6.4 |
| FSEOF | 강제 생산 flux 증가에 반응하는 증폭(과발현) 표적을 스캐닝하는 방법 | 본 장 §6.5 |
| Growth-coupled production | 생산이 최적 생장의 필연적 부산물이 되도록 설계된 대사 상태 | 본 장 §6.2, §7.1 |
| Production envelope | 생장율과 목표 산물 flux 사이의 실현 가능 영역(포락선) | 본 장 §7.1 |
| PhPP / Phenotype Phase Plane | 두 환경 변수 축 위에 최적 대사 전략을 지도화한 위상 평면 | 본 장 §7.2, [Ch4](../chapter-4/README.md) |
| Line of Optimality (LO) | PhPP에서 두 기질이 최적 비율로 소비되는 경계선 | 본 장 §7.2 |
| Cross-feeding / 교차 급식 | 한 종의 분비 대사물을 다른 종이 흡수·이용하는 상호작용 | 본 장 §9 |
| Community FBA | 여러 종의 GEM을 공통 환경 제약 아래 결합해 최적화하는 확장 FBA | 본 장 §9.3 |
| AGORA2 | 7,302개 균주 수준 장내 미생물 GEM 자원 | 본 장 §9.4, [Ch5](../chapter-5/README.md) |
| FBA / FVA / pFBA | 제약 기반 최적화의 기초 방법론 (본 장의 모든 예측이 이 위에 구축됨) | [Ch4](../chapter-4/README.md) |

---

## 참고문헌 / 더 읽을거리

**Perturbation 예측 방법론 (MOMA / ROOM / KO)**
1. Segrè D, Vitkup D, Church GM (2002). "Analysis of optimality in natural and perturbed metabolic networks." *PNAS* 99(23): 15112–15117. doi: `10.1073/pnas.232349399`. — MOMA 원 논문 (QP 정형화).
2. Shlomi T, Berkman O, Ruppin E (2005). "Regulatory on/off minimization of metabolic flux changes after genetic perturbations." *PNAS* 102(21): 7695–7700. doi: `10.1073/pnas.0406346102`. — ROOM 원 논문 (MILP 정형화), MOMA와의 비교 포함.
3. Edwards JS, Palsson BO (2000). "Robustness analysis of the Escherichia coli metabolic network." *Biotechnol. Prog.* 16(6): 927–939. — genome-scale 유전자 결손·강건성 분석의 선구적 연구.
4. Lewis NE, Nagarajan H, Palsson BO (2012). "Constraining the metabolic genotype–phenotype relationship using a phylogeny of in silico methods." *Nat. Rev. Microbiol.* 10(4): 291–305. — FBA·MOMA·ROOM 등 방법론 종합 리뷰.

**균주 설계 알고리듬**
5. Burgard AP, Pharkya P, Maranas CD (2003). "OptKnock: A bilevel programming framework for identifying gene knockout strategies for microbial strain optimization." *Biotechnol. Bioeng.* 84(6): 647–657. doi: `10.1002/bit.10803`.
6. Ranganathan S, Suthers PF, Maranas CD (2010). "OptForce: An optimization procedure for identifying all genetic manipulations leading to targeted overproductions." *PLoS Comput. Biol.* 6(4): e1000744. doi: `10.1371/journal.pcbi.1000744`.
7. Patil KR, Rocha I, Förster J, Nielsen J (2005). "Evolutionary programming as a platform for in silico metabolic engineering." *BMC Bioinformatics* 6: 308. doi: `10.1186/1471-2105-6-308`. — OptGene.
8. Choi HS, Lee SY, Kim TY, Woo HM (2010). "In silico identification of gene amplification targets for improvement of lycopene production." *Appl. Environ. Microbiol.* 76(10): 3097–3105. doi: `10.1128/AEM.00115-10`. — FSEOF.
9. Park JM, Park HM, Kim WJ, et al. (2012). "Flux variability scanning based on enforced objective flux for identifying gene amplification targets." *BMC Systems Biology* 6:106. doi: `10.1186/1752-0509-6-106`. — FVSEOF.
10. Kim M, Sang Yi J, Kim J, et al. (2014). "Reconstruction of a high-quality metabolic model enables the identification of gene overexpression targets for enhanced antibiotic production in Streptomyces coelicolor A3(2)." *Biotechnology Journal* 9(9):1185–1194. doi: `10.1002/biot.201300539`.
11. Wang B, Jiang S, Xu S, Li J (2025). "Bilevel modelling of metabolic networks for computational strain design." *Algorithms* 18(12):786. doi: `10.3390/a18120786`. — M-OptKnock/M-OptYield 비교.

**합성 치사 및 임상 응용**
12. Hartman JL, Garvik B, Hartwell L (2001). "Principles for the buffering of genetic variation." *Science* 291(5506): 1001–1004.
13. Lord CJ, Ashworth A (2017). "PARP inhibitors: Synthetic lethality in the clinic." *Science* 355(6330): 1152–1158.

**바이오 생산 사례 및 산업 응용** (강의 노트 1주차 §5.3 및 종합 자료 기반)
14. Jantama K, et al. (2008). "Combining metabolic engineering and metabolic evolution to develop nonrecombinant strains of E. coli C that produce succinate and malate." *Biotechnol. Bioeng.* 99(5): 1140–1153. doi: `10.1002/bit.21694`. — succinate KJ060/KJ134.
15. Paddon CJ, Keasling JD (2014). "Semi-synthetic artemisinin: a model for the use of synthetic biology in pharmaceutical development." *Nat. Rev. Microbiol.* 12(5): 355–367. — 아르테미신산 세포공장.
16. Paddon CJ, et al. (2013). "High-level semi-synthetic production of the potent antimalarial artemisinin." *Nature* 496:528–532. doi: `10.1038/nature12051`. — 아르테미신산 25 g/L의 1차 연구.

**커뮤니티 / 마이크로바이옴 모델링**
17. Diener C, Gibbons SM, Resendis-Antonio O (2020). "MICOM: Metagenome-scale modeling to infer metabolic interactions in the gut microbiota." *mSystems* 5(1): e00606-19.
18. Chan SHJ, Simons MN, Maranas CD (2017). "SteadyCom: Predicting microbial abundances while ensuring community stability." *PLoS Comput. Biol.* 13(5): e1005539.
19. Zomorrodi AR, Maranas CD (2012). "OptCom: A multi-level optimization framework for the metabolic modeling and analysis of microbial communities." *PLoS Comput. Biol.* 8(2): e1002363.
20. Heinken A, et al. (2023). "Genome-scale metabolic reconstruction of 7,302 human microorganisms for personalized medicine." *Nat. Biotechnol.* 41: 1320–1331. — AGORA2.

**소프트웨어**
- COBRApy — `single_gene_deletion`, `double_gene_deletion`, `moma`, `room`, `production_envelope` (https://opencobra.github.io/cobrapy/)
- StrainDesign — OptKnock·RobustKnock·MCS 통합 Python 패키지 (https://github.com/klamt-lab/straindesign)
- MICOM — 커뮤니티 대사 모델링 Python 패키지 (https://github.com/micom-dev/micom)
- 본 장의 실습 코드 전체: `raw_data/GEM_lecture_notes/gem9_w04_lab.ipynb`

> 본 장의 방법론 서술은 9주차 GEM 강의자료 4주차(Perturbation 분석·MOMA·ROOM)와 1주차(§5.3 산업적 응용, §6.3 AGORA2)를 바탕으로 재구성하였으며, 균주 설계 알고리듬·커뮤니티 프레임워크의 세부 사례는 강의 종합 자료를 참고하였습니다.
