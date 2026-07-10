# 마무리: 요약 · 스스로 점검 · 용어

## 한 장 요약

이 장은 하나의 큰 질문에서 출발했습니다 — "질병에 걸린 세포는 정상 세포와 대사적으로 무엇이 다른가, 그리고 그 차이를 어떻게 치료에 이용할 수 있는가?" 이 질문에 답하기 위해 우리는 GEM을 활용해 질병의 대사적 취약성을 찾고 약물 표적을 발굴하는 두 개의 상호보완적 패러다임을 다뤘습니다.

- **질병 = 대사 재프로그래밍**: 암의 Warburg 효과·6대 대사 특성·온코대사물(2-HG, succinate, fumarate)뿐 아니라, 당뇨병(인슐린 저항성)·NAFLD(세린 결핍)·노화(미토콘드리아 기능 저하)도 모두 "정상 대사 항상성의 붕괴"라는 공통 패턴을 공유합니다.
- **성장 억제 패러다임(§3~§5)**: Ch6에서 구축한 암/정상 모델에 단일·이중 유전자 KO를 적용하고, 상대 성장률과 전구체별 대사 작업, 암-정상 효과 차이, DepMap 데이터를 서로 분리해 검증합니다. 근거 없는 복합 점수나 선택성 등급은 피합니다.
- **합성 치사(SL)**: PARP-BRCA 사례처럼 정상 세포를 보호하면서 암세포만 선택적으로 공격하는 조합 표적을 Bliss 독립성 모델과 gMCS로 찾을 수 있습니다.
- **상태 변환 가설(§6~§7)**: MTA는 source 기준 flux와 source-target 발현 비교를 입력으로 반응 분류($$R_S/R_F/R_B$$) → 후보 교란 MIQP → 원 TS 랭킹을 수행합니다. 결과는 target 방향으로의 flux 이동 가능성을 뜻하며, 건강 회복을 보장하지 않습니다.
- 암(MLYCD), 당뇨병, NAFLD(세린), 노화(GRE3/ADH2), COVID-19까지 폭넓게 적용되었으며, 낮은 선택압·광범위한 적용성·가역성이라는 이점 덕분에 정밀의학과 약물 재배치의 유망한 도구로 주목받고 있습니다.
- 두 패러다임 모두 계산적 예측일 뿐이므로, siRNA/CRISPR 시험관 내 검증과 동물 모델 검증을 거쳐야 임상 전환이 가능하다는 점을 항상 유의해야 합니다.

두 패러다임(§3~§5의 "죽이기"와 §6~§7의 "고치기")은 겉보기에는 반대 방향을 향하지만, 계산적 기반은 완전히 동일합니다 — 둘 다 [Chapter 6](../chapter-6/README.md)에서 만든 맥락 특이적 모델을 입력으로 받고, 둘 다 화학량론적 정상상태 제약 $$\mathbf{S}\mathbf{v}=\mathbf{0}$$ 위에서 최적화를 풉니다. 차이는 오직 "무엇을 목표로 삼는가"뿐입니다 — 하나는 생물량 반응을 최소화하는 개입을 찾고, 다른 하나는 target 방향으로의 flux 이동을 극대화하는 개입을 찾습니다. 이 공통 기반을 이해하면, 이 장에서 배운 도구들이 앞으로 [Chapter 8](../chapter-8/README.md)에서 완전히 다른 목적(생산 증대)으로 재사용되는 것도 자연스럽게 받아들일 수 있습니다.

---

## 스스로 점검

1. **개념 확인**: AFR(ATP Flux Ratio)이 무엇을 측정하는 지표인지 설명하고, 어떤 세포주의 글리콜라이시스 관련 ATP 유속(PGK+PYK)이 18, 산화적 인산화 유속(ATPS4m)이 6이라면 AFR은 얼마인지 계산해 보세요.
   > *힌트*: §1.2의 공식 $$AFR = Glycolytic\ ATP\ flux / Oxidative\ ATP\ flux$$을 그대로 대입하면 됩니다. 답: $$18/6=3.0$$. AFR이 1보다 훨씬 크므로 강한 Warburg 표현형을 시사합니다.

2. **계산/판단**: 어떤 유전자를 암 모델에서 KO했더니 생물량이 88% 감소했고, 동일 KO를 정상 모델에 적용했더니 22% 감소했습니다. 선택성 차이와 탐색적 비율을 계산하고, 왜 이것만으로 high/medium/low 등급을 붙이면 안 되는지 설명해 보세요.
   > *힌트*: 차이는 $$88-22=66$$%p, 비율은 $$88/22=4$$입니다. 그러나 보편적으로 검증된 등급 경계가 없고 정상 조직 범위·모델 불확실성·비대사 독성을 반영하지 않으므로 두 원자료를 그대로 보고해야 합니다.

3. **개념 확인**: DepMap CRISPR 데이터처럼 필수 유전자가 전체의 10%에 불과한 불균형 데이터셋에서, ROC-AUC보다 PR-AUC가 더 신뢰할 수 있는 이유를 설명해 보세요.
   > *힌트*: §3.6의 정보 hint 박스를 참고하세요. ROC의 FPR은 분모(FP+TN)에 압도적으로 많은 비필수 유전자가 있어 잘 변하지 않으므로 낙관적으로 보일 수 있지만, PR의 Precision은 "필수로 예측한 것 중 실제 필수 비율"을 직접 측정해 소수 클래스에 대한 성능을 더 정직하게 드러냅니다.

4. **계산**: 유전자 A 단독 KO 후 상대 생존율이 0.9, 유전자 B 단독 KO 후 0.6이라 합시다. 두 유전자가 서로 독립적이라면 이중 KO의 기대 생존율은 얼마이며, 만약 실제 이중 KO 생존율이 0.15로 측정되었다면 Bliss Score는 얼마이고 어떻게 해석해야 할까요?
   > *힌트*: §4.3을 참고하세요. 기대 생존율 $$E_A \times E_B = 0.9\times 0.6=0.54$$. Bliss Score $$=0.15-0.54=-0.39$$. -0.1보다 훨씬 작으므로(더 음수) 강한 시너지, 즉 합성 치사 관계로 해석합니다.

5. **개념 비교**: MOMA/ROOM과 MTA는 둘 다 유전자 결손 후의 대사 상태를 다루지만, 근본적으로 다른 질문에 답합니다. 두 질문이 각각 무엇인지, 그리고 왜 MTA에는 "발현 데이터(source+target)"가 반드시 필요한 반면 MOMA/ROOM에는 필요하지 않은지 설명해 보세요.
   > *힌트*: MOMA/ROOM은 주어진 기준 flux에 대한 최소 조정을 찾지만 target 변화 방향은 입력받지 않습니다. MTA는 source 기준 flux와 source-target 차등발현에서 유도한 방향을 함께 사용해 후보를 순위화합니다.

6. **계산/해석**: 유전자 W를 KO한 뒤 WT와 KO에서 각각 지질 전구체 생산 작업의 최대값을 다시 최적화했더니 $$v^{WT,*}_{task,lipid}=5.0$$, $$v^{KO,*}_{task,lipid}=0.5$$였습니다. 전구체 생산 비율 $$r_{W,lipid}$$를 계산하고, 이 값이 전체 생물량 감소율과 별도로 어떤 정보를 추가로 알려주는지 설명해 보세요.
   > *힌트*: §3.3을 참고하세요. $$r_{W,lipid}=0.5/5.0=0.10$$. 전체 생물량 감소율이 대단치 않더라도, 이 비율이 낮다면 유전자 W가 지질 합성 경로에 특이적으로 중요하다는 것을 알려줍니다 — 총괄 지표 하나로는 보이지 않는 "어떤 기능이 병목인가"라는 정보입니다.

7. **개념 확인**: gMCS(gene Minimal Cut Sets)의 "크기(size)"라는 개념을 이용하면 §3의 필수성 분석과 §4의 합성 치사 분석을 하나의 통합된 틀로 볼 수 있습니다. 크기 1과 크기 2의 gMCS는 각각 이 장의 어떤 분석에 대응하는지 설명해 보세요.
   > *힌트*: §4.4를 참고하세요. 크기 1의 gMCS(단일 유전자 하나만으로 생물량 생산이 완전히 차단됨)는 §3의 단일 유전자 필수성 분석과, 크기 2의 gMCS(두 유전자를 함께 제거해야 차단됨)는 §4의 이중 유전자 합성 치사 분석과 대응됩니다.

---

## 다음 장 예고

이 장에서 우리는 맥락 특이적 모델을 무기로 삼아 질병(특히 암)의 대사적 취약성을 찾고, 필수성·합성 치사·MTA라는 세 갈래의 표적 발굴 전략을 배웠습니다. 요약하면 이 장의 질문은 "무엇을 **끄면**(또는 어떻게 되돌리면) 질병을 이길 수 있는가"였습니다.

산업 현장에서는 정반대의 질문이 던져집니다: "무엇을 **더 만들게** 하면 이윤을 낼 수 있는가?" 다음 [Chapter 8. 미생물·세포공장·합성생물학 응용](../chapter-8/README.md)에서는 이 장에서 다룬 유전자 결손 개념을 확장하여, 유전자 KO의 메커니즘(GPR 불리언 평가, MOMA/ROOM의 수학적 정형화)을 상세히 배우고, 이를 발판으로 미생물을 산업용 화합물 생산 공장으로 재설계하는 **균주 설계(strain design)** 알고리즘(OptKnock, OptForce, OptGene, FSEOF)과 **production envelope**를 통한 생장-생산 트레이드오프 시각화, 그리고 여러 미생물이 대사를 나누는 **커뮤니티 모델링**까지 살펴봅니다. "죽이거나 고치는" 관점에서 "만들어내는" 관점으로, 같은 도구가 얼마나 다른 목적에 쓰일 수 있는지 확인하게 될 것입니다.

이 전환이 낯설게 느껴진다면, §3.1에서 이미 그 씨앗을 심어두었다는 점을 떠올려 보십시오 — "유전자 KO 시 대사 흐름이 어떻게 재배치되는가"라는 예측 문제 자체는 목적이 "생장 억제"든 "생산 증대"든 동일한 화학량론적 제약 $$\mathbf{S}\mathbf{v}=\mathbf{0}$$ 위에서 풀립니다. Chapter 8을 읽을 때는 "이 장(Ch7)에서 배운 KO 시뮬레이션과 무엇이 같고 무엇이 다른가"를 계속 자문하면서 읽으면, 두 장이 하나의 큰 도구상자를 공유하는 자매 장이라는 사실이 더 선명하게 드러날 것입니다.

---

## 핵심 용어 정리

| 용어(한글) | English | 정의 | 관련 챕터 |
|---|---|---|---|
| 대사 재프로그래밍 | Metabolic Reprogramming | 질병 상태에서 대사 네트워크의 토폴로지·플럭스 분포가 질적으로 변화하는 현상 | Ch7 |
| Warburg 효과 | Warburg Effect | 암 세포가 산소가 충분해도 글리콜라이시스를 선호하는 호기성 글리콜라이시스 현상 | Ch7 |
| ATP Flux Ratio | AFR | 글리콜라이시스 대 산화적 인산화의 ATP 생산 비율로 Warburg 효과를 정량화한 지표 | Ch7 |
| 온코대사물 | Oncometabolite | 비정상 축적되어 암을 촉진하는 대사산물 (2-HG, succinate, fumarate 등) | Ch7 |
| 대사 이질성 | Metabolic Heterogeneity | 같은 종양 내에서도 위치·세포 상태에 따라 대사 특성이 다르게 나타나는 현상 | Ch7 |
| 전구체 생산 비율 | Precursor task ratio | 특정 전구체 대사 작업의 KO 최대값을 WT 최대값으로 나눈 값 | Ch7 |
| 선택성 차이 | Selectivity difference | 암 모델 성장 감소율에서 정상 모델 성장 감소율을 뺀 탐색 지표 | Ch7 |
| 합성 치사 | Synthetic Lethality (SL) | 두 유전자의 동시 교란만 치명적인 유전적 상호작용 | Ch7, Ch8 |
| gMCS | gene Minimal Cut Set | 생물량 생산을 차단하는 최소 유전자 집합, 구조적 취약점 식별에 사용 | Ch7 |
| DepMap | Cancer Dependency Map | CRISPR-Cas9 기반 대규모 암 유전자 필수성 데이터베이스 | Ch7 |
| CERES | Computational Correction of Copy-number Effect | CRISPR 스크린의 카피수변이 가성 신호를 보정하는 알고리즘 | Ch7 |
| 대사 상태 변환 | Metabolic state transformation | source의 flux를 target 전사체가 시사하는 방향으로 이동시키는 계산적 목표 | Ch7 |
| MTA | Metabolic Transformation Algorithm | source 기준 flux·source-target 발현 차이로 후보 교란을 MIQP/TS로 순위화 | Ch7 |
| rMTA | robust MTA | best-case TS, 반대 방향 worst-case TS, MOMA TS의 방향 일관성을 결합한 확장 | Ch7 |
| Transformation Score | TS | 목표 방향 변화와 비목표/unchanged 반응 변화를 비교하는 MTA의 사후 순위 점수 | Ch7 |
| iMAT | integrative Metabolic Analysis Tool | 발현 데이터를 목적함수 없이 반응 활성 상태로 통합하는 MILP 기반 알고리즘 | Ch6, Ch7 |
| 약물 재배치 | Drug Repositioning/Repurposing | 기존 승인 약물을 새로운 적응증에 적용하는 전략 | Ch7 |
| Bliss 독립성 모델 | Bliss Independence Model | 두 단독 결손 생존율의 곱을 독립 기대치로 삼아 이중 결손의 시너지·길항을 판정하는 모델 | Ch7 |
| 네오몰픽 반응 | Neomorphic reaction | 돌연변이가 원래 없던 새로운 촉매 활성을 획득해 생기는 반응(예: IDH1 R132H의 α-KG→2-HG) | Ch7 |
| 약물화 가능성 | Druggability | 표적 단백질에 소분자가 결합할 수 있는 구조적·화학적 가능성. 필수성·선택성과는 독립적으로 평가되어야 함 | Ch7 |

---

## 참고문헌

1. Yizhak K, Benyamini T, Liebermeister W, Ruppin E, Shlomi T (2014). "A computational study of the Warburg effect identifies metabolic targets inhibiting cancer migration." *Molecular Systems Biology* 10:744.
2. Yizhak K, Gaude E, Le Dévédec S, et al. (2014). "Phenotype-based cell-specific metabolic modeling reveals metabolic liabilities of cancer." *eLife* 3:e03641.
3. Yizhak K, Gabay O, Cohen H, Ruppin E (2013). "Model-based identification of drug targets that revert disrupted metabolism and its application to ageing." *Nature Communications* 4:2632.
4. Agren R, Mardinoglu A, Asplund A, Kampf C, Uhlen M, Nielsen J (2014). "Identification of anticancer drugs for hepatocellular carcinoma through personalized genome-scale metabolic modeling." *Molecular Systems Biology* 10:721.
5. Mardinoglu A, Agren R, Kampf C, et al. (2014). "Genome-scale metabolic modelling of hepatocytes reveals serine deficiency in patients with non-alcoholic fatty liver disease." *Nature Communications* 5:3083.
6. Mardinoglu A, et al. (2016). "Genome-scale study reveals reduced metabolic adaptability in patients with non-alcoholic fatty liver disease." *Nature Communications*.
7. Mardinoglu A, et al. (2020). "Genome-scale metabolic modeling of hepatocellular carcinoma reveals pan-cancer and cancer-type specific metabolic signatures." *Frontiers in Genetics* 11:576.
8. Pacheco MP, John E, Kaoma T, et al. (2019). "Identifying and targeting cancer-specific metabolism with rFASTCORMICS." *Cell Systems* 9(1):78-89.
9. Vieira V, Kaoma T, Klukas C, Sauter T (2022). "A pipeline for the reconstruction and evaluation of context-specific human metabolic models at a large-scale." *PLoS Computational Biology* 18(6):e1009294.
10. Folger O, Jerby L, Frezza C, Gottlieb E, Ruppin E, Shlomi T (2011). "Predicting selective drug targets in cancer through metabolic networks." *Molecular Systems Biology* 7:501.
11. Pey J, et al. (2024). "An automated network-based tool to search for metabolic vulnerabilities in cancer." *Nature Communications.*
12. Lee J, et al. (2023). "Genome-scale knockout simulation and clustering analysis of drug-resistant breast cancer cells reveal drug sensitization targets." *PNAS*.
13. Kim BK, Gu C, Farh MEA, Ryu JY (2026). "Integrating Genome-Scale Metabolic Modeling with Machine Learning Improves Gene Essentiality Prediction in Triple-Negative Breast Cancer." *International Journal of Molecular Sciences* 27(11):5059. DOI: 10.3390/ijms27115059.
14. Bordbar A, Feist AM, Usaite-Black R, et al. (2011). "A multi-tissue type genome-scale metabolic network for analysis of whole-body systems physiology." *BMC Systems Biology* 5:180.
15. Segre D, Vitkup D, Church GM (2002). "Analysis of optimality in natural and perturbed metabolic networks." *PNAS* 99(23):15112-15117. (MOMA 원 논문)
16. Shlomi T, Berkman O, Ruppin E (2005). "Regulatory on/off minimization of metabolic flux changes after genetic perturbations." *PNAS* 102(21):7695-7700. (ROOM 원 논문)
17. Zur H, Ruppin E, Shlomi T (2010). "iMAT: an integrative metabolic analysis tool." *Bioinformatics* 26(24):3140-3142.
18. Pavlova NN, Thompson CB (2016). "The Emerging Hallmarks of Cancer Metabolism." *Cell Metabolism* 23(1):27-47.
19. Lopez-Otin C, Blasco MA, Partridge L, et al. (2013). "The Hallmarks of Aging." *Cell* 153(6):1194-1217.
20. DepMap Portal: https://depmap.org/portal/ — 암 유전자 필수성 CRISPR 데이터
21. Human-GEM Guide: https://sysbiochalmers.github.io/Human-GEM-guide/
22. "Context-Specific Genome-Scale Metabolic Modelling and Its Application to COVID-19." (2023) *Metabolites* 13(1):126.
23. DiVito MR, et al. (2022). "Constraint-Based Reconstruction and Analyses of Metabolic Models: Open-Source Python Tools and Applications to Cancer." *Frontiers in Oncology* 12:930301.
24. Edwards JS, Palsson BO (2000). "Robustness analysis of the Escherichia coli metabolic network." *Biotechnology Progress* — gene essentiality/drug target 응용의 초기 사례.
25. Ryu JY, Kim HU, Lee SY (2017). "Framework and resource for more than 11,000 gene-transcript-protein-reaction associations in human metabolism." *PNAS* 114:E9740-E9749. DOI: 10.1073/pnas.1713050114. — Recon2M.
26. Valcárcel LV, Torrano V, Tobalina L, Carracedo A, Planes FJ (2019). "rMTA: robust metabolic transformation analysis." *Bioinformatics* 35:4350-4355. DOI: 10.1093/bioinformatics/btz231. — best/worst/MOMA TS를 결합한 rMTA.
