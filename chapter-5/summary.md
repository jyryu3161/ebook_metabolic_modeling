# 마무리: 요약 · 스스로 점검 · 용어

## 핵심 용어 정리

| 용어(English) | 정의 |
|:---|:---|
| 재구축(Reconstruction) | 게놈 주석·문헌·데이터베이스를 통합한 정성적 반응 네트워크. Flux bounds와 biomass가 부여되면 시뮬레이션 가능한 모델이 된다. |
| 동원성 검색(Homology search) | BLASTP 등으로 서열 유사성을 찾아 기능(EC 번호·반응)을 추론하는 절차. |
| E-value | 우연히 관측될 것으로 기대되는 alignment 수. 작을수록 신뢰도 높음. |
| BBH(Bidirectional Best Hit) | 두 게놈 간 상호 최우수 hit로 ortholog를 판별하는 방법. |
| Confidence Score(0-4점) | Thiele & Palsson(2010)의 반응별 증거 등급(0=미평가, 1=모델링 가설, 2=생리/서열, 3=유전, 4=생화학적 증거). BLASTP Tier(§2.4)와는 별개의 축. |
| Gap-filling | 모델이 biomass 등 목표를 생산하도록 보편 DB에서 최소 반응을 추가하는 MILP 최적화. |
| Gene-less reaction / Orphan reaction | 유전자가 연결되지 않은 반응. Gap-filling의 대표적 부작용이자 세균 GEM의 30-40%를 차지. |
| MEMOTE | GEM의 구조·biomass·일관성·주석을 자동 검사하고 회귀를 추적하는 오픈소스 도구. 총점의 실제 가중치는 리포트/설정에서 확인한다. |
| 화학량론적 일관성(Stoichiometric consistency) | 내부 반응에 대해 양의 질량 벡터 $$\mathbf{m}>0$$가 존재하여 $$S_I^T\mathbf{m}=0$$을 만족하는 성질. 연결성·flux consistency와 다르다. |
| MIRIAM / SBML L3 FBC2 | 모델 요소를 외부 DB에 연결하는 주석 표준 / GEM의 표준 파일 인코딩. |
| 합의적 모델링(Consensus modeling) | 여러 재구축 도구의 결과를 교집합·합집합으로 결합해 신뢰도를 높이는 절차. |
| Top-down / Bottom-up / Hybrid | 게놈 주석에서 출발 / 대사물질 관측에서 출발 / 둘을 결합한 인체 GEM 구축 철학. |
| Human1 / Human2 | HMR2·iHsa·Recon3D를 통합한 2020년 인체 GEM / LLM 보조 선별·전문가 검토·자동 테스트로 갱신한 2026년 Human-GEM v2. |
| Metabolic Task Enforcement | 추출 모델이 지정한 대사 기능의 전체 입력-출력 flux 경로를 수행하도록 task-essential 반응 보호와 작업별 gap-filling을 적용하는 것. |
| tINIT / ftINIT | task enforcement를 결합한 INIT 계열 조직 특이 모델 추출법 / 2단계 최적화와 모드 선택으로 10배 넘게 고속화한 버전. |

---

## 한 장 요약

- 미생물 GEM의 품질은 **분비 생성물 프로파일·유전자 필수성·탄소원 이용**이라는 세 가지 독립적 표현형 벤치마크로 평가되며, 이는 수동 재구축 Stage 4와 MEMOTE 이후의 생물학적 검증에서 반복적으로 등장하는 공통 잣대입니다.
- 반응 할당의 출발점은 **BLASTP 기반 동원성 검색**입니다 — E-value·identity·coverage와 BBH로 신뢰도를 계층화하고, KEGG/MetaCyc/UniProt/BiGG/SEED 등 데이터베이스의 선택이 최종 모델을 크게 좌우합니다.
- **Thiele & Palsson 96단계 프로토콜**은 Stage 1(Steps 1-5) 초안 → Stage 2(6-37) 수동 정제와 0-4점 confidence → Stage 3(38-42) 계산 모델 변환 → Stage 4(43-96) 평가·디버깅의 표준 워크플로우입니다.
- **CarveMe(top-down)·ModelSEED(bottom-up)·gapseq(경로 기반)·AuReMe/RAVEN/Merlin**은 서로 다른 철학과 트레이드오프(속도 vs. 정확도 vs. 진핵생물 지원)를 가지며, 하나의 "완벽한" 도구는 없습니다.
- **Gap-filling**은 MILP로 정식화되는 조합 최적화 문제로, 전통적 방법(SMILEY, GapFind/GapFill, growMatch, FastGapFill)과 딥러닝 기반 후보 순위화(CHESHIRE, CLOSEgaps, DNNGIOR, GHCN-SE)가 공존합니다. 이 가운데 DNNGIOR는 초그래프가 아니라 반응 공존·계통 정보를 사용하며, 이들 방법 모두 추가한 반응에 GPR 근거가 없을 수 있다는 한계가 있습니다.
- **MEMOTE**는 구조·biomass·일관성·주석을 반복 검사하지만, 고정된 4개 가중치나 보편적 합격선은 없습니다. 같은 버전·설정의 회귀 검사와 목적별 표현형 검증을 함께 써야 합니다.
- 인체 GEM은 **Recon과 HMR의 분기·상호 흡수·병합**으로 발전했습니다. Recon2M은 transcript/protein isoform을 연결한 응용 가지이고, HMR2·iHsa·Recon3D가 Human1에 통합된 뒤 Human-GEM v1.x가 Human2로 갱신되었습니다.
- **tINIT**은 task-essential 반응을 보호하고 추출 후 실패한 작업을 순차적으로 보정합니다. task는 반응 하나가 아니라 전체 실행 가능 경로이며, ftINIT은 2단계 최적화로 10배 넘게 빨라졌습니다. GIMME/iMAT과의 비교는 [Omics 통합](../chapter-6/README.md)에서 이어집니다.
- 결국 이 장 전체를 관통하는 하나의 메시지는 "**재구축은 반복이다**" — 레시피를 맛보고 고치듯, 지도를 답사하며 고치듯, 모든 좋은 GEM은 초안→검증→수정의 순환을 여러 번 거쳐 탄생합니다.

---

## 스스로 점검

1. **E-value vs. Confidence score.** 어떤 두 단백질의 BLASTP 결과가 $$E=10^{-40}$$, identity 65%로 나왔습니다. §2.4의 Tier 체계로는 몇 등급입니까? 그런데 이 반응을 §3.2의 0-4점 confidence score로 매긴다면 반드시 4점을 줘야 할까요? 이유를 설명하십시오.
   > *힌트: 설명용 Tier 1에 해당합니다. 그러나 confidence score는 증거의 종류를 기록하므로 서열 증거만 있다면 2 범주이며, 대상 생물체의 직접 생화학 실험이 있어야 4입니다.*

2. **Gap-filling과 생물학적 진실.** §5.1의 장난감 예제에서 MILP는 $$\{U_3\}$$(반응 1개)를 $$\{U_1, U_2\}$$(반응 2개)보다 선호했습니다. 만약 실제 생물체에는 $$U_3$$ 같은 직접 반응이 존재하지 않고 $$U_1 \to U_2$$의 2단계 경로만 존재한다면 어떤 문제가 생깁니까? 이런 위험을 줄이는 실무적 방법 두 가지를 §5.2와 §5.4에서 찾아 설명하십시오.
   > *힌트: MILP의 "최소"는 수학적 최소일 뿐 생물학적 사실이 아닙니다. (1) 여러 대안 해(`iterations`를 늘려 alternative optima 확인)를 함께 검토하고, (2) 추가된 반응에 유전자 후보를 재검색해 gene-less로 남기지 않는 것이 완화책입니다.*

3. **MEMOTE 결과 비교.** 같은 모델이 서로 다른 MEMOTE 버전 또는 custom config에서 74%와 81%를 받았습니다. 어느 모델이 개선되었다고 결론 내릴 수 있을까요? 공정한 비교를 위해 무엇을 기록해야 합니까?
   > *힌트: 점수만으로 결론 내릴 수 없습니다. 모델 파일의 hash/release, MEMOTE 버전, solver, scored test 목록, section/test weight, skipped/error 항목과 설정 파일을 고정해야 합니다.*

4. **화학량론적 일관성과 dead-end.** $$\mathbf{m}>0$$이고 $$S_I^T\mathbf{m}=0$$인 질량 벡터가 존재하는 모델에도 dead-end metabolite가 있을 수 있을까요? 반대로 그래프가 잘 연결되어도 화학량론적으로 불일관할 수 있을까요?
   > *힌트: 둘 다 가능합니다. Stoichiometric consistency는 내부 반응의 질량 보존 가능성을, dead-end/flux consistency는 생산·소비 가능성과 bounds를 묻기 때문에 별도의 검사입니다.*

5. **tINIT task enforcement.** "아미노산 X를 합성한다"는 task에 관련 반응 중 하나만 포함하면 충분하지 않은 이유를 설명하고, tINIT이 추출 전후에 기능을 어떻게 보존하는지 서술하십시오.
   > *힌트: task는 기질 공급부터 산물 배출까지 이어지는 전체 flux 경로입니다. 범용 모델에서 task 가능성과 essential 반응을 확인해 보호하고, 추출 후 task를 다시 실행하여 실패한 기능을 증거 가중 gap-filling으로 보정합니다.*

---

## 다음 장 예고

이 장에서 우리는 게놈 서열에서 출발해 재구축·gap-filling·품질 관리를 거쳐 iML1515나 Human1 같은 "범용(generic)" 고품질 GEM에 도달하는 전체 파이프라인을 익혔습니다. 그런데 범용 모델은 어디까지나 "**평균적 세포**"를 나타냅니다 — 간세포도, 근육세포도, 종양세포도 모두 같은 유전자 목록(Human1)을 공유하지만 실제로 사용하는 반응은 서로 다릅니다. §10에서 살짝 맛본 tINIT의 "조직 특이적 모델 추출"이 바로 이 간극을 메우는 방법이며, 그 핵심 재료는 **오믹스 데이터**(전사체·단백질체·대사체)입니다. 다음 [Chapter 6. Omics 데이터 통합](../chapter-6/README.md)에서는 발현 데이터를 GEM의 제약으로 바꾸는 GIMME·iMAT·tINIT·FASTCORE 등의 알고리즘을 철학적으로 비교하고, RNA-seq 전처리부터 맥락 특이적 모델 추출까지 직접 실습합니다.

---

## 참고문헌

1. Thiele, I. & Palsson, B.O. (2010). A protocol for generating a high-quality genome-scale metabolic reconstruction. *Nature Protocols*, 5(1), 93-121. DOI: [10.1038/nprot.2009.203](https://doi.org/10.1038/nprot.2009.203).
2. Lieven, C. et al. (2020). MEMOTE for standardized genome-scale metabolic model testing. *Nature Biotechnology*, 38(3), 272-276. DOI: [10.1038/s41587-020-0446-y](https://doi.org/10.1038/s41587-020-0446-y).
3. Mendoza, S.N. et al. (2019). A systematic evaluation of methods for genome-scale metabolic model reconstruction. *Genome Biology*, 20(1), 1-17.
4. Zimmermann, J. et al. (2021). gapseq: informed prediction of bacterial metabolic pathways and reconstruction of accurate metabolic models. *Genome Biology*, 22(1), 1-35.
5. Machado, D. et al. (2018). Fast automated reconstruction of genome-scale metabolic models for microbial species and communities (CarveMe). *Nucleic Acids Research*, 46(15), 7542-7553. DOI: [10.1093/nar/gky537](https://doi.org/10.1093/nar/gky537).
6. Orth, J.D. et al. (2011). A comprehensive genome-scale reconstruction of Escherichia coli metabolism. *Molecular Systems Biology*, 7(1), 535.
7. Monk, J.M. et al. (2017). iML1515, a knowledgebase that computes Escherichia coli traits. *Nature Biotechnology*, 35(10), 904-908.
8. Satish Kumar, V. et al. (2007). Optimization based automated curation of metabolic reconstructions. *BMC Bioinformatics*, 8(1), 1-15.
9. Kumar, A. & Maranas, C.D. (2009). GrowMatch: an automated method for reconciling in silico/in vivo growth predictions. *PLoS Computational Biology*, 5(3), e1000308.
10. Thiele, I. et al. (2014). FastGapFill: efficient gap filling in metabolic networks. *Bioinformatics*, 30(17), 2529-2531.
11. Chen C, Liao C, Liu Y-Y (2023). [Teasing out missing reactions in genome-scale metabolic networks through hypergraph learning](https://doi.org/10.1038/s41467-023-38110-7). *Nature Communications*, 14, 2375.
12. Liu X et al. (2024). [A generalizable framework for unlocking missing reactions in genome-scale metabolic networks using deep learning](https://arxiv.org/abs/2409.13259). arXiv:2409.13259 (CLOSEgaps preprint).
13. de Boer MD et al. (2024). [Improving genome-scale metabolic models of incomplete genomes with deep learning](https://doi.org/10.1016/j.isci.2024.111349). *iScience*, 27, 111349.
14. Qu J, Wang K (2026). [A Novel Topology-Based Candidate Reaction Prediction Approach for Gap-Fillings of Genome-Scale Metabolic Models](https://doi.org/10.3390/metabo16040258). *Metabolites*, 16, 258.
15. Henry, C.S. et al. (2010). High-throughput generation, optimization and analysis of genome-scale metabolic models (ModelSEED). *Nature Biotechnology*, 28(9), 977-982.
16. Altschul, S.F. et al. (1990). Basic local alignment search tool. *Journal of Molecular Biology*, 215(3), 403-410.
17. Buchfink, B. et al. (2015). Fast and sensitive protein alignment using DIAMOND. *Nature Methods*, 12(1), 59-60.
18. Kanehisa, M. & Goto, S. (2000). KEGG: kyoto encyclopedia of genes and genomes. *Nucleic Acids Research*, 28(1), 27-30.
19. Caspi, R. et al. (2020). The MetaCyc database of metabolic pathways and enzymes — a 2019 update. *Nucleic Acids Research*, 48(D1), D445-D453.
20. King, Z.A. et al. (2016). BiGG Models: A platform for integrating, standardizing and sharing genome-scale models. *Nucleic Acids Research*, 44(D1), D515-D522.
21. Moretti, S. et al. (2016). MetaNetX/MNXref: unified namespace for metabolites and biochemical reactions. *Nucleic Acids Research*, 44(D1), D246-D250.
22. Duarte, N.C. et al. (2007). Global reconstruction of the human metabolic network based on genomic and bibliomic data (Recon1). *PNAS*, 104(6), 1777-1782. DOI: [10.1073/pnas.0610772104](https://doi.org/10.1073/pnas.0610772104).
23. Thiele, I. et al. (2013). A community-driven global reconstruction of human metabolism (Recon2). *Nature Biotechnology*, 31(5), 419-425. DOI: [10.1038/nbt.2488](https://doi.org/10.1038/nbt.2488).
24. Mardinoglu, A. et al. (2014). Genome-scale metabolic modelling of hepatocytes reveals serine deficiency in patients with non-alcoholic fatty liver disease (HMR2). *Nature Communications*, 5, 3083. DOI: [10.1038/ncomms4083](https://doi.org/10.1038/ncomms4083).
25. Swainston, N. et al. (2016). Recon 2.2: from reconstruction to model of human metabolism. *Metabolomics*, 12(7), 109. DOI: [10.1007/s11306-016-1051-4](https://doi.org/10.1007/s11306-016-1051-4).
26. Blais, E.M. et al. (2017). Reconciled rat and human metabolic networks for comparative toxicogenomics and biomarker predictions (iHsa). *Nature Communications*, 8, 14250. DOI: [10.1038/ncomms14250](https://doi.org/10.1038/ncomms14250).
27. Ryu, J.Y., Kim, H.U. & Lee, S.Y. (2017). Framework and resource for more than 11,000 gene-transcript-protein-reaction associations in human metabolism (Recon2M). *PNAS*, 114(45), E9740-E9749. DOI: [10.1073/pnas.1713050114](https://doi.org/10.1073/pnas.1713050114).
28. Brunk, E. et al. (2018). Recon3D enables a three-dimensional view of gene variation in human metabolism. *Nature Biotechnology*, 36(3), 272-281. DOI: [10.1038/nbt.4072](https://doi.org/10.1038/nbt.4072).
29. Robinson, J.L. et al. (2020). An atlas of human metabolism (Human1). *Science Signaling*, 13(624), eaaz1482. DOI: [10.1126/scisignal.aaz1482](https://doi.org/10.1126/scisignal.aaz1482).
30. Luo, J. et al. (2026). Reconstruction of human metabolic models with large language models (Human2). *PNAS*, 123(15), e2516511123. DOI: [10.1073/pnas.2516511123](https://doi.org/10.1073/pnas.2516511123).
31. Agren, R. et al. (2012). Reconstruction of genome-scale active metabolic networks for 69 human cell types and 16 cancer types using INIT. *PLoS Computational Biology*, 8(5), e1002518. DOI: [10.1371/journal.pcbi.1002518](https://doi.org/10.1371/journal.pcbi.1002518).
32. Agren, R. et al. (2014). Identification of anticancer drugs for hepatocellular carcinoma through personalized genome-scale metabolic modeling (tINIT). *Molecular Systems Biology*, 10, 721. DOI: [10.1002/msb.145122](https://doi.org/10.1002/msb.145122).
33. Gustafsson, J. et al. (2023). Generation and analysis of context-specific genome-scale metabolic models derived from single-cell RNA-Seq data (ftINIT). *PNAS*, 120(6), e2217868120. DOI: [10.1073/pnas.2217868120](https://doi.org/10.1073/pnas.2217868120).
34. Xiao W, Zheng J, Li SZ (2026). [MetaGEM: Bottom-Up Reconstruction of Genome-Scale Metabolic Networks via Deep Enzyme-Metabolite Anchoring](https://arxiv.org/abs/2605.14812). arXiv:2605.14812 (preprint).
35. Palsson, B.O. (2015). *Systems Biology: Constraint-based Reconstruction and Analysis*. Cambridge University Press.

> 소프트웨어: COBRApy 0.29+ · MEMOTE 0.16+ · CarveMe 1.6+ · gapseq 1.2+ · ModelSEED/KBase v2 · RAVEN 2.8+ · Merlin 4.0+ · Diamond 2.1+ 데이터베이스: BiGG Models · KEGG · MetaCyc · UniProt · MetaNetX · Metabolic Atlas([metabolicatlas.org](https://metabolicatlas.org)) · Human-GEM GitHub([github.com/sysbiochalmers/Human-GEM](https://github.com/sysbiochalmers/Human-GEM))
