# 마무리: 요약 · 스스로 점검 · 용어

## 한 장 요약

- Generic GEM은 유전체와 문헌이 지지하는 대사 능력의 범위를 나타냅니다. **맥락 특이적 모델**은 특정 조직·세포·조건의 오믹스 증거와 요구 기능을 반응 선택 또는 flux bounds에 반영한 계산 가설입니다. 발현된 네트워크를 직접 관측한 결과가 아니므로 독립 검증이 필요합니다.
- GPR의 AND와 OR는 각각 효소 복합체와 대체 아이소자임의 **Boolean 관계**입니다. 이를 연속 RAS로 옮길 때 흔히 AND=min, OR=max를 쓰지만 이는 휴리스틱입니다. 아이소자임 용량은 합산될 수 있고, 복합체 화학량론·단백질 조립·촉매율은 min/max만으로 표현되지 않습니다.
- 고정값, 백분위수와 일반 z-score는 서로 다른 활성 집합을 만들 수 있습니다. rFASTCORMICS의 zFPKM은 전체 값의 일반 z-score가 아니라 표본별 $$\log_2(\mathrm{FPKM})$$ 발현 주봉의 오른쪽 half-Gaussian에서 얻은 $$\mu_E,\sigma_E$$를 사용합니다. 임계값, 결측값 처리와 GPR 전후 이산화 순서를 민감도 분석에 포함해야 합니다.
- **GIMME**(기능 하한 아래에서 저발현 flux penalty 최소화), **iMAT**(발현-활성 상태 일치 최대화), **E-Flux**(발현으로 용량 경계 스케일링), **INIT/tINIT**(증거 가중치와 지정 작업 보호)은 목적함수와 결과물의 의미가 다릅니다. GIMME의 $$fZ^*$$는 등식이 아니라 하한이며, 한 최적해에서 flux가 0인 반응이 모든 대체 최적해에서도 0인 것은 아닙니다. iMAT의 big-M은 반응별 실제 bounds에서 유도해야 합니다.
- RNA-seq의 **raw counts**는 count 기반 차등발현 검정에, **TPM**은 한 샘플 안의 상대 조성과 GEM 가중치 후보에 주로 사용합니다. TPM은 합이 고정된 조성 자료이므로 “샘플 간 절대 발현을 가장 잘 비교한다”는 뜻이 아닙니다(4.1.1절의 FPKM·TPM 손 계산 참고). 또한 벌크 RNA-seq 외에도 단일세포·단일핵·공간 전사체 등 다양한 유형이 있으며, 단일세포 데이터를 통합할 때는 흔히 pseudobulk 집계가 필요합니다.
- 단백질체는 **GECKO 계열 효소 용량 제약**으로, 대사체는 농도 범위를 이용한 **열역학적 방향 제약** 또는 검출 대사물의 turnover·생산 가능성 요구로 통합할 수 있습니다. 가역 flux의 효소 비용은 정·역방향 비음수 변수를 사용해야 하며, flux·$$k_{cat}$$·분자량·효소 질량의 단위를 일치시켜야 합니다.
- 다중 오믹스는 서로 다른 층의 모순과 결측을 드러낼 수 있지만, 자료를 더 넣는다고 예측 정확도가 자동으로 높아지지는 않습니다. 실습에서는 합성 발현으로 만든 hard-pruned 모델과 generic 모델 전체에 같은 유전자 결손 분석을 적용해 필수 유전자 수가 5개에서 7개로 바뀌는 것을 확인했습니다. 이는 모델 간 민감도 비교이며, 실험적 필수성 자료를 사용한 외부 검증은 아닙니다.
- 맥락 특이적 모델의 **재구축 알고리즘 상세**(tINIT의 6단계, MILP 유도, gap-filling)는 [Chapter 5](../chapter-5/README.md)에서, 추출된 모델의 FBA/FVA 실행은 [Chapter 4](../chapter-4/README.md)에서 이미 다뤘습니다. 이제 이렇게 준비된 맥락 특이적 모델을 **질병 이해와 약물 표적 발굴**에 쓸 차례입니다 — [Chapter 7](../chapter-7/README.md)에서 이어집니다.

## 스스로 점검

1. 간세포와 근육세포는 동일한 유전체를 갖지만 서로 다른 맥락 특이적 모델이 필요합니다. generic GEM의 대사 능력과 조건별 발현·효소 용량·요구 기능을 구분하여 이유를 설명해 보세요.
2. AND=min, OR=max 휴리스틱을 적용할 때 GPR `(GeneA and GeneB) or GeneC`와 발현값 $$w_A=6,\ w_B=2,\ w_C=4$$의 RAS를 계산해 보세요. 정답: $$\max(\min(6,2),4)=4$$입니다. 이 값이 효소 용량의 물리적 측정값이 아닌 이유도 설명해 보세요.
3. iMAT은 별도의 biomass 같은 생물학적 flux 목적이 필요 없지만 발현–활성 일치 목적은 가집니다. high/moderate/low 분류 경계가 바뀔 때 MILP의 보상 구조가 어떻게 달라지는지 설명해 보세요.
4. TPM의 합이 항상 $$10^6$$이 되는 이유를 설명하고, 이 고정합 특성이 샘플 비교에 편리한 점과 동시에 조성 편향을 만드는 이유를 논하세요. 차등발현 검정에 raw counts가 필요한 이유도 함께 쓰세요.
5. GECKO의 효소 용량 제약이 추가되면, 포도당이 매우 풍부한 조건에서 세포가 TCA 회로를 통한 완전 산화 대신 발효(과잉 배출, overflow metabolism)를 선택하는 이유를 한 문장으로 설명해 보세요.
6. 5.1.1절에서 세 반응을 flux 10으로 유지하는 데 필요한 효소량은 각각 1.39, 6.94, 27.78 mg·gDW$$^{-1}$$입니다. 총 예산이 30 mg·gDW$$^{-1}$$일 때 세 반응을 동시에 유지할 수 있는지 단위와 합계를 써서 판단해 보세요.
7. iMAT 예제의 제약 $$v\ge1-M(1-y)$$에서 실제 하한이 $$-10$$일 때, $$y=0$$인 경우에도 하한 전체를 허용하려면 왜 $$M\ge11$$이어야 하나요? $$M=5$$가 만드는 잘못된 제한을 계산해 보세요.
8. scRNA-seq(단일세포 RNA-seq) 데이터로 특정 세포 유형의 맥락 특이적 모델을 만들고 싶습니다. 개별 세포 하나하나의 발현값을 그대로 GPR에 대입하지 않고 pseudobulk로 먼저 묶는 이유는 무엇인가요?

## 다음 장 예고

이 장에서는 전사체를 GPR과 RAS로 반응 수준에 매핑하고, GIMME·iMAT·E-Flux·tINIT·FASTCORE 계열이 그 증거를 서로 다른 목적과 제약으로 사용하는 방식을 비교했습니다. 또한 효소 질량과 대사물 농도가 각각 용량과 반응 방향에 주는 제약을 살펴보았습니다. 핵심은 맥락 모델이 관측된 활성 네트워크 자체가 아니라, 오믹스와 요구 기능에 조건화된 실행가능 공간이라는 점입니다.

다음 [Chapter 7. 질병 모델링과 약물 표적 발굴](../chapter-7/README.md)에서는 **암 모델**과 **대응 정상 모델**을 나란히 놓고 KO 효과가 다른 대사 취약성을 선별합니다. 계산상 선택성은 정상 세포 안전성의 증명이 아니며, MTA의 target 방향 이동도 건강 회복의 보장이 아닙니다. 이 한계를 명시한 채 Warburg 효과·온코대사물·필수성·합성 치사와 source-target 상태 변환 가설을 연결합니다. 이 장에서 배운 맥락 특이적 모델 추출 기법(특히 tINIT/rank-based tINIT, GIMME)은 Chapter 7의 암-정상 세포주 쌍 모델 구축에 그대로 재사용됩니다.

---

## 핵심 용어 정리

| 용어(한글) | English | 정의 |
|---|---|---|
| 맥락 특이적 모델 | Context-Specific Model | 오믹스 증거와 요구 기능을 반응 집합 또는 bounds에 반영한 조건별 GEM |
| 반응 활성 점수 | Reaction Activity Score (RAS) | GPR을 정한 집계 규칙으로 평가해 유전자 발현을 반응 수준으로 변환한 휴리스틱 점수 |
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
| FASTCORE / rFASTCORMICS | Fast reCOnstruction / robust FASTCORMICS | Core 반응을 포함하는 compact flux-consistent 네트워크 추출과 표본별 통계적 이산화의 결합 |
| GECKO | Genome-scale model with Enzymatic Constraints using Kinetic and Omics data | 단백질체 기반 효소 용량 제약을 GEM에 추가 |
| zFPKM | z-transformed FPKM | $$\log_2(\mathrm{FPKM})$$ 발현 주봉의 half-Gaussian 적합값으로 표준화한 표본별 점수 |
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
13. Opdam S, Richelle A, Kellman B, et al. "A systematic evaluation of methods for tailoring genome-scale metabolic models." *Cell Systems* 4(3):318-329.e6, 2017. DOI: 10.1016/j.cels.2017.01.010. — 4개 암 세포주에서 6개 추출법과 여러 임계값·대사 제약을 비교.
14. Weinstein JN, Collisson EA, Mills GB, et al. "The Cancer Genome Atlas Pan-Cancer analysis project." *Nature Genetics* 45:1113-1120, 2013. DOI: 10.1038/ng.2764.
15. Wilks C, Zheng SC, Chen FY, et al. "recount3: summaries and queries for large-scale RNA-seq expression and splicing." *Genome Biology* 22:323, 2021. — recount3 포털.
16. Vieira V, Ferreira J, Rocha M. "A pipeline for the reconstruction and evaluation of context-specific human metabolic models at a large-scale." *PLoS Computational Biology* 18(6):e1009294, 2022. DOI: 10.1371/journal.pcbi.1009294. — Troppo 기반으로 CCLE 733개 세포주의 6,000개 이상 모델을 구축·평가.
17. Palsson BO. *Systems Biology: Constraint-based Reconstruction and Analysis*. 2nd Edition, Cambridge University Press, 2015. — FBA·COBRA 이론적 기초.
18. Barker BE, Sadagopan N, Wang Y, et al. "A robust and efficient method for estimating enzyme complex abundance and metabolic flux from expression data." *Computational Biology and Chemistry* 59:98-112, 2015. DOI: 10.1016/j.compbiolchem.2015.08.002. — FALCON/LAD.
19. Kim MK, Lane A, Kelley JJ, Lun DS. "E-Flux2 and SPOT: Validated methods for inferring intracellular metabolic flux distributions from transcriptomic data." *PLoS ONE* 11:e0157101, 2016. DOI: 10.1371/journal.pone.0157101.
20. Lamoureux CR, Decker KT, Sastry AV, et al. "A multi-scale expression and regulation knowledge base for *Escherichia coli*." *Nucleic Acids Research*, 2023. DOI: 10.1093/nar/gkad750. — PRECISE-1K(1,035 samples).
21. Agren R, Bordel S, Mardinoglu A, et al. "Reconstruction of genome-scale active metabolic networks for 69 human cell types and 16 cancer types using INIT." *PLoS Computational Biology* 8:e1002518, 2012. DOI: 10.1371/journal.pcbi.1002518.
22. Lee SM, Lee GR, Kim HU. "Machine learning-guided evaluation of extraction and simulation methods for cancer patient-specific metabolic models." *Computational and Structural Biotechnology Journal* 20:3041-3052, 2022. DOI: 10.1016/j.csbj.2022.06.027. — PCAWG·rank-based tINIT·LAD 비교.
23. Hart T, Komori HK, LaMere S, Podshivalova K, Salomon DR. "Finding the active genes in deep RNA-seq gene expression studies." *BMC Genomics* 14:778, 2013. DOI: 10.1186/1471-2164-14-778. — zFPKM 원논문.
24. Schmidt BJ, Ebrahim A, Metz TO, et al. "GIM3E: condition-specific models of cellular metabolism developed from metabolomics and expression data." *Bioinformatics* 29(22):2900-2908, 2013. DOI: 10.1093/bioinformatics/btt493.
25. Lloyd CJ, Ebrahim A, Yang L, et al. "COBRAme: A computational framework for genome-scale models of metabolism and gene expression." *PLoS Computational Biology* 14(7):e1006302, 2018. DOI: 10.1371/journal.pcbi.1006302.
26. Oshlack A, Wakefield MJ. "Transcript length bias in RNA-seq data confounds systems biology." *Genome Biology* 10:R14, 2009. DOI: 10.1186/gb-2009-10-2-r14.
