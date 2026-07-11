# 제5장 요약과 연습문제

## 핵심 개념

1. **[재구축과 모델](../glossary.md)은 구분된다.** 재구축은 반응·대사산물·GPR·구획·근거의 지식 표현이고, 모델은 여기에 조건별 bounds와 objective 또는 task를 부여한 계산 객체이다.
2. **서열 유사성은 기능 증거의 한 종류이다.** BLASTP의 E-value는 현재 검색공간에서 해당 점수 이상의 우연 정렬이 기대되는 수이다. Identity, 양쪽 coverage, domain, catalytic residue, phylogeny 및 genomic context를 함께 평가한다.
3. **BBH는 orthology의 휴리스틱이다.** 유전자 중복·소실, many-to-many orthology 및 domain fusion이 있으면 reciprocal best hit와 실제 계통관계가 다를 수 있다.
4. **수동 큐레이션의 핵심은 provenance이다.** 반응의 존재, 방향성, 화학량론, 구획 및 GPR에 대해 증거 유형과 변경 이력을 기록한다.
5. **자동 재구축 도구는 서로 다른 prior를 사용한다.** CarveMe는 범용 모델을 축소하는 top-down 전략, ModelSEED는 주석과 template로 반응을 구성하는 bottom-up 전략, gapseq는 경로 문맥과 반응 증거를 활용한다.
6. **[Gap-filling](../glossary.md)은 누락 반응의 가설을 제안한다.** 최소 반응 수 또는 증거 비용을 최적화해 지정 task를 만족시키지만, 추가 반응의 생물학적 존재를 증명하지 않는다.
7. **모델 품질은 다차원적이다.** [Mass balance](../glossary.md), [stoichiometric consistency](../glossary.md), flux consistency, energy cycle, annotation 및 외부 phenotype accuracy는 서로 다른 속성을 측정한다.
8. **[MEMOTE](../glossary.md) 총점은 설정에 의존한다.** 모델 release, MEMOTE version, solver, test selection 및 weight가 같을 때 회귀를 비교하고, 독립 표현형 검증을 별도로 수행한다.
9. **SBML package의 역할을 구분한다.** [FBC](../glossary.md)는 bounds·objective·[GPR](../chapter-3/README.md) 등을, Groups는 pathway·subsystem grouping을 표현한다.
10. **[범용 인체 재구축](../glossary.md)은 평균 세포가 아니다.** 여러 인간 세포 유형에서 지지된 대사 지식의 통합 집합이며, 조직·세포 모델은 omics와 task를 이용해 별도로 추출한다.
11. **Human1과 Human2는 버전이 명시된 release로 인용한다.** Human2의 LLM은 GPR 후보를 선별했고, 전문가 검토·공개 provenance·자동 시험이 최종 큐레이션을 담당했다.
12. **[tINIT](../glossary.md)은 evidence selection과 task preservation을 결합한다.** Task는 반응 하나의 포함 여부가 아니라 지정 입력·출력·bounds 아래 feasible flux state의 존재이다.

## 주요 식

### 서열 정렬의 E-value

$$
E=Kmn e^{-\lambda S}
$$

$$E$$는 데이터베이스 크기와 scoring system에 의존한다.

### 유전자 필수성 판정

$$
r_i=\frac{\mu_{\Delta i}}{\mu_{WT}},\qquad
\widehat y_i=\mathbb 1(r_i<\theta)
$$

$$\theta$$, 배지, 균주 및 solver tolerance를 함께 보고한다.

### 증거 가중 gap-filling

$$
\min_{\mathbf v,\mathbf y}\sum_{r\in\mathcal U}w_ry_r
$$

$$
\mathbf S\mathbf v=0,\qquad
\ell_ry_r\le v_r\le u_ry_r,\qquad
\mathbf A_{task}\mathbf v\ge\mathbf b_{task}
$$

### 화학량론적 일관성

$$
\exists\ \mathbf m>0\quad\text{such that}\quad
\mathbf S_I^T\mathbf m=0
$$

### 반응 집합 유사도

$$
J(A,B)=\frac{|A\cap B|}{|A\cup B|}
$$

Jaccard similarity는 정규화된 반응 집합의 중복 정도를 나타낼 뿐 정확도를 판정하지 않는다.

## 용어

| 용어 | 정의 |
|:---|:---|
| Reconstruction | 생화학 지식과 근거를 구조화한 반응 네트워크 |
| Homology search | 공통 조상 후보를 지지하는 서열 유사성 검색 |
| E-value | 현재 검색공간에서 해당 점수 이상의 우연 정렬 기대 개수 |
| BBH | 두 proteome에서 상호 최고 hit인 ortholog 후보 pair |
| Reaction confidence | 반응을 지지하는 증거의 종류와 수준을 기록한 범주 |
| Gap-filling | 지정 기능을 회복하는 후보 반응 조합을 찾는 최적화 |
| Orphan reaction | 생화학 반응은 지지되지만 촉매 유전자가 알려지지 않은 반응 |
| Stoichiometric consistency | 내부 반응이 양의 질량 벡터와 양립하는 성질 |
| Flux consistency | 각 반응이 어떤 feasible state에서 비영 flux를 가질 수 있는 성질 |
| MIRIAM | 정량 모델의 최소 보고·주석 원칙 |
| FBC | 제약 기반 모델을 표현하는 SBML Level 3 package |
| Generic human reconstruction | 여러 인간 세포 유형의 대사 지식을 통합한 범용 네트워크 |
| [Metabolic task](../glossary.md) | 지정 경계와 출력 조건을 만족하는 flux state의 존재로 정의한 기능 |
| tINIT / ftINIT | Task 보존형 INIT과 그 계산 효율 개선 구현 |

## 연습문제

1. 같은 protein pair를 작은 reference DB와 큰 metagenomic DB에서 BLASTP로 검색했다. Raw score가 같아도 E-value가 달라지는 이유를 식으로 설명하라.
2. 90% identity이지만 query coverage가 18%인 hit와 38% identity이지만 양쪽 coverage가 95%이고 catalytic domain이 보존된 hit가 있다. 전체 효소 기능 전이를 위해 추가로 확인할 증거를 설계하라.
3. `geneA AND geneB` 복합체에서 A만 강하게 검출되었다. 빈 GPR, `geneA`, 불완전 후보 표시 가운데 각 처리의 gene-deletion 예측 영향을 비교하라.
4. Gap-filling 후보 $$U_1,U_2,U_3$$의 비용이 각각 1, 1, 5이고 가능한 경로가 $$\{U_1,U_2\}$$와 $$\{U_3\}$$라고 하자. Cardinality objective와 evidence-weighted objective의 해를 각각 계산하고, 어느 해도 생물학적 사실을 보장하지 않는 이유를 쓰라.
5. Mass-balanced하지만 blocked reactions가 있는 네트워크와, flux-consistent하지만 stoichiometrically inconsistent한 네트워크가 가능한지 논증하라.
6. 두 자동 재구축 모델의 Jaccard similarity를 계산하기 전에 필요한 metabolite·reaction normalization 절차를 제시하라.
7. Human1의 평균 annotation score 66%와 Human2의 MEMOTE total score 81%를 직접 비교할 수 없는 이유를 설명하라.
8. LLM이 `inconsistent`로 flag한 2,195 gene–reaction pairs 중 1,985가 전문가에 의해 confirmed negative였다. 이 비율이 전체 GPR accuracy가 아닌 이유와 필요한 추가 분모를 설명하라.
9. 조직 특이 모델이 모든 필수 task를 통과했지만 독립 CRISPR dependency 자료와 일치하지 않았다. 가능한 원인을 reference network, GPR, expression mapping, media 및 task design으로 나누어 진단하라.
10. 모델 release를 재현 가능하게 인용하기 위한 metadata schema를 작성하라. 최소한 파일 checksum, DB release, solver, bounds, objective, task file 및 phenotype test split을 포함하라.

## 주요 문헌

1. Thiele I, Palsson BØ. [A protocol for generating a high-quality genome-scale metabolic reconstruction](https://doi.org/10.1038/nprot.2009.203). *Nature Protocols* (2010).
2. Altschul SF et al. [Basic local alignment search tool](https://doi.org/10.1016/S0022-2836(05)80360-2). *Journal of Molecular Biology* (1990).
3. Machado D et al. [Fast automated reconstruction of genome-scale metabolic models for microbial species and communities](https://doi.org/10.1093/nar/gky537). *Nucleic Acids Research* (2018).
4. Henry CS et al. [High-throughput generation, optimization and analysis of genome-scale metabolic models](https://doi.org/10.1038/nbt.1672). *Nature Biotechnology* (2010).
5. Zimmermann J et al. [gapseq](https://doi.org/10.1186/s13059-021-02295-1). *Genome Biology* (2021).
6. Thiele I et al. [fastGapFill](https://doi.org/10.1093/bioinformatics/btu321). *Bioinformatics* (2014).
7. Lieven C et al. [MEMOTE](https://doi.org/10.1038/s41587-020-0446-y). *Nature Biotechnology* (2020).
8. Brunk E et al. [Recon3D](https://doi.org/10.1038/nbt.4072). *Nature Biotechnology* (2018).
9. Robinson JL et al. [An atlas of human metabolism](https://doi.org/10.1126/scisignal.aaz1482). *Science Signaling* (2020).
10. Luo J et al. [Reconstruction of human metabolic models with large language models](https://doi.org/10.1073/pnas.2516511123). *PNAS* (2026).
11. Agren R et al. [Reconstruction of genome-scale active metabolic networks](https://doi.org/10.1371/journal.pcbi.1002518). *PLoS Computational Biology* (2012).
12. Agren R et al. [Personalized genome-scale metabolic modeling with tINIT](https://doi.org/10.1002/msb.145122). *Molecular Systems Biology* (2014).
13. Gustafsson J et al. [Context-specific models and ftINIT](https://doi.org/10.1073/pnas.2217868120). *PNAS* (2023).

## 다음 장

[Chapter 6](../chapter-6/README.md)은 transcriptomics·proteomics·metabolomics 자료를 flux constraint와 reaction evidence로 변환하는 방법을 다룬다. 특히 normalization, threshold, GPR aggregation 및 context-specific extraction의 선택이 예측에 미치는 영향을 비교한다.

---
