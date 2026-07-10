# 마무리: 요약 · 스스로 점검 · 용어

## 한 장 요약

- Generic GEM은 게놈이 암호화하는 모든 이론적 반응을 담은 “요리책”과 같지만, 실제 조직·세포는 이 중 일부만을 “오늘의 식탁”에 올립니다. **맥락 특이적 모델**은 오믹스 증거를 이용해 이 실제 사용 네트워크를 추출합니다. 요리사가 “냉장고 재고”(오믹스 데이터)를 보고 오늘의 메뉴를 정하듯, 전사체·단백체·대사체는 각각 “재료 주문서 발주”, “재료 도착”, “요리 완성”이라는 서로 다른 단계의 증거를 제공합니다.
- 발현 데이터는 **GPR 규칙(AND=min, 이어달리기의 가장 느린 주자 / OR=max, 대타 선수)**을 통해 반응 활성 점수(RAS)로 변환됩니다. 작은 손 계산 예제(2.2절, 2.2.1절)에서 확인했듯, 이 원리는 137개 유전자짜리 `e_coli_core`에서도 13,070개 반응짜리 Human1에서도 완전히 동일하게 적용되며, 중첩된 GPR은 항상 가장 안쪽 괄호부터 계산합니다.
- RAS를 이산화하는 **임계값 설정 방법**(고정값, 백분위수, z-score/통계적 혼합모델)의 선택이 결과 모델 품질에 가장 큰 영향을 미치며, 이산화를 유전자 단계에서 하느냐 반응 단계에서 하느냐도 방법에 따라 결과가 달라질 수 있습니다. 실습(2단계)에서 확인했듯, 같은 데이터에 세 방법을 적용하면 “활성” 유전자 수가 극단적으로 달라질 수 있습니다.
- **GIMME**(요구 기능 유지), **iMAT**(발현-활성 일치), **E-Flux**(발현으로 용량 스케일링), **INIT/tINIT**(증거 가중치와 작업 보호)은 서로 다른 질문에 답합니다. 3.2.1절의 손 계산에서 GIMME가 성장률의 10%를 희생하는 대신 저발현 경로를 완전히 차단하는 과정을, 3.3.1절에서 big-M 상수를 잘못 설정하면 물리적으로 정당한 flux 값이 잘못 차단될 수 있음을 숫자로 확인했습니다. LAD·E-Flux2·SPOT은 추출된 해 공간에서 점 플럭스를 고르는 시뮬레이션 규칙이며, 모델 추출법과 구분해야 합니다.
- RNA-seq의 **raw counts**는 count 기반 차등발현 검정에, **TPM**은 한 샘플 안의 상대 조성과 GEM 가중치 후보에 주로 사용합니다. TPM은 합이 고정된 조성 자료이므로 “샘플 간 절대 발현을 가장 잘 비교한다”는 뜻이 아닙니다(4.1.1절의 FPKM·TPM 손 계산 참고). 또한 벌크 RNA-seq 외에도 단일세포·단일핵·공간 전사체 등 다양한 유형이 있으며, 단일세포 데이터를 통합할 때는 흔히 pseudobulk 집계가 필요합니다.
- 단백질체는 **GECKO 효소 제약**(정해진 “장보기 예산” 비유, 5.1.1절의 kcat별 효소 소비량 손 계산)으로, 대사체는 **열역학적 제약**(5.2.1절의 Gibbs 자유에너지 손 계산) 또는 tINIT의 **정성적 순생산 제약**으로 GEM에 통합됩니다.
- 다중 오믹스 통합은 시너지가 크지만, 전사체-단백체 불일치(발현-활성 역설), 시간 규모 차이, 정량성 비대칭, 데이터 희소성 등 근본적 한계가 있어 항상 독립적 지표(대사 작업 통과율, gene essentiality)로 검증해야 합니다. 실습 7단계에서 확인했듯, 맥락 특이적 제약이 완전히 억제한 반응의 관련 유전자를 generic 모델의 필수성 예측과 비교하는 것이 이 검증의 가장 단순한 형태입니다.
- 맥락 특이적 모델의 **재구축 알고리즘 상세**(tINIT의 6단계, MILP 유도, gap-filling)는 [Chapter 5](../chapter-5/README.md)에서, 추출된 모델의 FBA/FVA 실행은 [Chapter 4](../chapter-4/README.md)에서 이미 다뤘습니다. 이제 이렇게 준비된 맥락 특이적 모델을 **질병 이해와 약물 표적 발굴**에 쓸 차례입니다 — [Chapter 7](../chapter-7/README.md)에서 이어집니다.

## 스스로 점검

1. 간세포와 근육세포는 동일한 유전체를 갖지만 서로 다른 맥락 특이적 모델을 필요로 합니다. 그 이유를 "요리책과 오늘의 식탁" 비유를 써서 두세 문장으로 설명해 보세요.
2. GPR 규칙 `(GeneA and GeneB) or GeneC`에서 발현값이 각각 $$w_A=6,\ w_B=2,\ w_C=4$$일 때 RAS를 손으로 계산해 보세요. (힌트: 안쪽 괄호부터 계산합니다.) 정답: $$\max(\min(6,2), 4) = \max(2,4) = 4$$
3. iMAT은 별도의 biomass 같은 생물학적 flux 목적이 필요 없지만 발현–활성 일치 목적은 가집니다. high/moderate/low 분류 경계가 바뀔 때 MILP의 보상 구조가 어떻게 달라지는지 설명해 보세요.
4. TPM의 합이 항상 $$10^6$$이 되는 이유를 설명하고, 이 고정합 특성이 샘플 비교에 편리한 점과 동시에 조성 편향을 만드는 이유를 논하세요. 차등발현 검정에 raw counts가 필요한 이유도 함께 쓰세요.
5. GECKO의 효소 용량 제약이 추가되면, 포도당이 매우 풍부한 조건에서 세포가 TCA 회로를 통한 완전 산화 대신 발효(과잉 배출, overflow metabolism)를 선택하는 이유를 한 문장으로 설명해 보세요.
6. 5.1.1절의 손 계산에서 반응 C($$k_{cat}=5$$)는 반응 A($$k_{cat}=100$$)와 같은 flux 10을 내는 데 20배 많은 효소가 필요했습니다. 만약 세포의 총 효소 예산이 딱 반응 C 하나가 flux 10을 내는 데 필요한 양(100)뿐이라면, 그 세포는 반응 A·B·C를 동시에 그 수준으로 가동할 수 있을까요? 이유를 설명하세요.
7. iMAT의 big-M 제약에서 $$M$$을 반응의 실제 flux 범위보다 작게 설정하면 어떤 문제가 생기나요? 3.3.1절의 숫자 예제($$M=5$$, 실제 하한 $$-10$$)를 참고해 설명해 보세요.
8. scRNA-seq(단일세포 RNA-seq) 데이터로 특정 세포 유형의 맥락 특이적 모델을 만들고 싶습니다. 개별 세포 하나하나의 발현값을 그대로 GPR에 대입하지 않고 pseudobulk로 먼저 묶는 이유는 무엇인가요?

## 다음 장 예고

이 장에서 우리는 범용 GEM을 특정 조직·세포의 "오늘의 식탁"으로 좁히는 방법을 배웠습니다. 발현 데이터를 GPR 규칙으로 반응 활성 점수(RAS)로 바꾸고, 임계값으로 이진화하고, GIMME·iMAT·E-Flux·tINIT 같은 알고리즘으로 맥락 특이적 서브네트워크를 추출했습니다. 손 계산 예제를 통해 GIMME의 2단계 LP가 실제로 무엇을 최소화하는지, big-M 설정이 왜 까다로운지, GECKO의 효소 예산이 왜 발효 경로를 유리하게 만드는지, 그리고 대사체 농도가 어떻게 반응 방향을 열역학적으로 좁히는지 직접 손으로 확인했습니다. 요약하면 이 장의 질문은 "이 세포는 지금 **무엇을 켜고 있는가**, 그리고 그 증거를 어떻게 모델에 새겨 넣는가"였습니다.

다음 [Chapter 7. 질병 모델링과 약물 표적 발굴](../chapter-7/README.md)에서는 **암 모델**과 **대응 정상 모델**을 나란히 놓고 KO 효과가 다른 대사 취약성을 선별합니다. 계산상 선택성은 정상 세포 안전성의 증명이 아니며, MTA의 target 방향 이동도 건강 회복의 보장이 아닙니다. 이 한계를 명시한 채 Warburg 효과·온코대사물·필수성·합성 치사와 source-target 상태 변환 가설을 연결합니다. 이 장에서 배운 맥락 특이적 모델 추출 기법(특히 tINIT/rank-based tINIT, GIMME)은 Chapter 7의 암-정상 세포주 쌍 모델 구축에 그대로 재사용됩니다.

---

## 핵심 용어 정리

| 용어(한글) | English | 정의 |
|---|---|---|
| 맥락 특이적 모델 | Context-Specific Model | Generic GEM에서 오믹스 증거로 추출한 조직·세포·질병 특이적 서브네트워크 |
| 반응 활성 점수 | Reaction Activity Score (RAS) | GPR 규칙으로 유전자 발현을 반응 수준으로 변환한 값 |
| 유전자-단백질-반응 연관 | Gene-Protein-Reaction (GPR) | 유전자가 단백질을 거쳐 반응을 촉매하는 관계를 나타내는 부울 논리 |
| 발현 임계값 | Expression Threshold | 연속 발현값을 활성/비활성으로 이산화하는 절단 기준 |
| GIMME | Gene Inactivity Moderated by Metabolism and Expression | 목적함수 달성 + 저발현 반응 사용 최소화(LP, 2단계) |
| iMAT | integrative Metabolic Analysis Tool | 발현-flux 상태 일치를 최대화(MILP, 3-level) |
| big-M 기법 | Big-M Constraint | 이진 변수의 on/off를 연속 변수 제약에 연결할 때 큰 상수로 조건을 느슨하게 만드는 MILP 기법 |
| E-Flux | Expression-based Flux constraints | 발현값을 반응 상한(bound)에 직접 비례 스케일링(LP) |
| E-Flux2 / SPOT | Flux inference methods | 각각 목적값 고정 후 L2 최소화 / 발현-절대 flux 비중심 상관 최대화 |
| LAD / FALCON | Least Absolute Deviation flux assignment | 반응 flux와 효소복합체 발현의 정규화 절대편차를 최소화 |
| PRECISE-1K | Precision RNA-seq Expression Compendium | 표준화 프로토콜로 생성한 *E. coli* RNA-seq 1,035개 샘플 자원 |
| tINIT | task-driven Integrative Network Inference for Tissues | 가중치 최대화 + 대사 작업 충족을 강제(MILP) |
| FASTCORE / rFASTCORMICS | Fast reCOnstruction / robust FASTCORMICS | Core 반응 집합 기반 최소 일관 네트워크 추출(LP), 통계적 이진화로 확장 |
| GECKO | Genome-scale model with Enzymatic Constraints using Kinetic and Omics data | 단백질체 기반 효소 용량 제약을 GEM에 추가 |
| TPM | Transcripts Per Million | 길이와 라이브러리 규모를 보정해 합을 $$10^6$$으로 만든 상대 발현값; 조성 효과에 주의 |
| FPKM | Fragments Per Kilobase of transcript per Million mapped reads | 길이·라이브러리 크기를 보정하나 샘플 간 비교에는 부적절한 정규화 값 |
| 조성 자료 | Compositional Data | 전체 합이 고정된 값(예: TPM의 100만)으로 정규화되어, 한 성분의 변화가 다른 성분의 상대값에 영향을 주는 자료 |
| Pseudobulk | Pseudobulk Aggregation | 단일세포 RNA-seq에서 비슷한 세포를 묶어 발현을 합산함으로써 개별 세포의 희소성(drop-out) 문제를 완화하는 전처리 |
| 열역학적 제약 | Thermodynamic Constraints | Gibbs 자유에너지 기반으로 반응 방향성을 데이터로 제약하는 방식 |
| 발현-활성 역설 | Transcriptomics Paradox | mRNA 발현량과 실제 단백질·효소 활성이 항상 일치하지는 않는 현상 |
| 다중 오믹스 통합 | Multi-Omics Integration | 전사체·단백체·대사체 데이터를 동시에 GEM에 반영하는 전략 |

## 참고문헌

1. Becker SA, Palsson BO. "Context-specific metabolic networks are consistent with experiments." *PLoS Computational Biology* 4(5):e1000082, 2008. — GIMME 원논문.
2. Zur H, Ruppin E, Shlomi T. "iMAT: an integrative metabolic analysis tool." *Bioinformatics* 26(24):3140-3142, 2010. — iMAT 원논문.
3. Colijn C, Brandes A, Zucker J, et al. "Interpreting expression data with metabolic flux models: predicting *Mycobacterium tuberculosis* mycolic acid production." *PLoS Computational Biology* 5(8):e1000489, 2009. — E-Flux 원논문.
4. Agren R, Mardinoglu A, Asplund A, et al. "Identification of anticancer drugs for hepatocellular carcinoma through personalized genome-scale metabolic modeling." *Molecular Systems Biology* 10:721, 2014. — tINIT 원논문.
5. Vlassis N, Pacheco MP, Sauter T. "Fast reconstruction of compact context-specific metabolic network models." *PLoS Computational Biology* 10(1):e1003424, 2014. — FASTCORE 원논문.
6. Pacheco MP, Pfau T, Sauter T. "Benchmarking procedures for high-throughput context specific reconstruction algorithms." *Frontiers in Physiology* 6:410, 2015. — FASTCORMICS.
7. Pacheco MP, Bintener T, Ternes D, et al. "Identifying and targeting cancer-specific metabolism with network-based drug target prediction." *EBioMedicine* 43:98-106, 2019. DOI: 10.1016/j.ebiom.2019.04.046. — rFASTCORMICS로 TCGA 10,005개 모델 구축.
8. Tefagh M, Boyd SP. "SWIFTCORE: a tool for the context-specific reconstruction of genome-scale metabolic networks." *BMC Bioinformatics* 21:140, 2020.
9. Schultz A, Qutub AA. "Reconstruction of tissue-specific metabolic networks using CORDA." *PLoS Computational Biology* 12(3):e1004808, 2016.
10. Sanchez BJ, Zhang C, Nilsson A, et al. "Improving the phenotype predictions of a yeast genome-scale metabolic model by incorporating enzymatic constraints." *Molecular Systems Biology* 13(8):935, 2017. — GECKO 원논문.
11. Robaina Estevez S, Nikoloski Z. "Generalized framework for context-specific metabolic model extraction methods." *Frontiers in Plant Science* 5:491, 2014. — 임계값 민감도 비교.
12. Richelle A, Chiang AW, Kuo CC, Lewis NE. "Increasing consensus of context-specific metabolic models by integrating data-inferred cell functions." *PLoS Computational Biology* 15(4):e1006867, 2019.
13. "A systematic evaluation of methods for tailoring genome-scale metabolic models." *Cell Systems* 2(5):316-323, 2016. — 739개 세포주 MEM 비교.
14. The Cancer Genome Atlas Research Network. *Nature* 및 *Nature Genetics* 다수 논문 (TCGA 프로젝트 개요), 2006년 시작.
15. Wilks C, Zheng SC, Chen FY, et al. "recount3: summaries and queries for large-scale RNA-seq expression and splicing." *Genome Biology* 22:323, 2021. — recount3 포털.
16. Vieira V, et al. "Troppo: a Python framework for context-specific metabolic model reconstruction." (CCLE 739개 세포주, 25종 암, Achilles CRISPR 필수성 데이터와의 비교), 2022. — Troppo 프레임워크와 대규모 세포주 패널 적용.
17. Palsson BO. *Systems Biology: Constraint-based Reconstruction and Analysis*. 2nd Edition, Cambridge University Press, 2015. — FBA·COBRA 이론적 기초.
18. Barker BE, Sadagopan N, Wang Y, et al. "A robust and efficient method for estimating enzyme complex abundance and metabolic flux from expression data." *Computational Biology and Chemistry* 59:98-112, 2015. DOI: 10.1016/j.compbiolchem.2015.08.002. — FALCON/LAD.
19. Kim MK, Lane A, Kelley JJ, Lun DS. "E-Flux2 and SPOT: Validated methods for inferring intracellular metabolic flux distributions from transcriptomic data." *PLoS ONE* 11:e0157101, 2016. DOI: 10.1371/journal.pone.0157101.
20. Lamoureux CR, Decker KT, Sastry AV, et al. "A multi-scale expression and regulation knowledge base for *Escherichia coli*." *Nucleic Acids Research*, 2023. DOI: 10.1093/nar/gkad750. — PRECISE-1K(1,035 samples).
21. Agren R, Bordel S, Mardinoglu A, et al. "Reconstruction of genome-scale active metabolic networks for 69 human cell types and 16 cancer types using INIT." *PLoS Computational Biology* 8:e1002518, 2012. DOI: 10.1371/journal.pcbi.1002518.
22. Lee SM, Lee GR, Kim HU. "Machine learning-guided evaluation of extraction and simulation methods for cancer patient-specific metabolic models." *Computational and Structural Biotechnology Journal* 20:3041-3052, 2022. DOI: 10.1016/j.csbj.2022.06.027. — PCAWG·rank-based tINIT·LAD 비교.
