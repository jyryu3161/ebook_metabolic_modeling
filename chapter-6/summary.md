# 마무리: 요약 · 스스로 점검 · 용어

## 한 장 요약

- 범용 인체 재구축은 여러 세포 유형에서 지지된 반응을 모은 지식 기반이다. 조직의 평균 활성 상태나 한 세포의 실제 flux를 나타내지 않는다.
- Recon·HMR·Human-GEM은 병렬 계승과 통합을 거쳤다. 반응·대사물·유전자 수는 릴리스와 집계 정의의 속성이므로 tag·파일·checksum과 함께 인용한다.
- Human1은 HMR2·iHsa·Recon3D의 식별자·반응식·구획·GPR을 조정했다. Human2의 LLM은 불일치 후보를 선별했고 최종 판정은 전문가 검토와 공개 시험이 담당했다.
- 맥락 특이화는 범용 모델에서 반응을 제거하거나 bounds·벌점을 조정한다. 높은 발현은 포함의 절대 명령이 아니고 낮은 발현은 제거의 직접 증거가 아니다.
- INIT은 반응 증거를 선택 기준으로 사용하고, tINIT은 대사 과제 보존을 결합한다. ftINIT mode의 속도·크기·성능은 기저 모델과 설정에 의존한다.
- GPR의 AND·OR를 연속 RAS로 옮길 때 흔히 min·max를 쓰지만 이는 휴리스틱이다. 결측 유전자, GPR이 없는 반응과 임계값 정책을 별도로 기록한다.
- GIMME는 기능 하한과 저발현 벌점, iMAT은 발현–활성 일치, E-Flux는 발현 비례 용량, tINIT은 증거 기반 선택과 대사 과제를 사용한다.
- raw counts, FPKM과 TPM은 의미와 용도가 다르다. TPM은 고정합 조성 자료이고, 단일세포 자료는 희소성과 donor 복제를 고려한 pseudobulk가 흔한 입력 단위이다.
- 다중 오믹스는 서로 다른 증거 층의 일치·충돌·결측을 드러낸다. 자료 수가 많다는 사실은 정확도를 보장하지 않으며 표본·시점·세포 유형 정합과 독립 검증이 필요하다.

## 스스로 점검

1. **정의 확인:** 범용 인체 재구축과 간세포 맥락 특이 모델이 서로 다른 객체인 이유를 반응 근거·배지·기능 요구로 설명하라.
   > **힌트:** 지식 기반의 포함 범위와 조건별 반응 선택을 분리한다.
2. **수치 해석:** Human2의 LLM 선별에서 2,195개 불일치 후보 가운데 1,985개가 전문가 검토에서 부정 근거로 확인되었다. 이 비율을 계산하고 전체 GPR 정확도로 부를 수 없는 이유를 쓰라.
   > **힌트:** 분모가 전체 26,246개 pair가 아니라 선별된 부분집합이다.
3. **손 계산:** GPR `(GeneA and GeneB) or GeneC`와 발현값 $$w_A=6,\ w_B=2,\ w_C=4$$에 AND=min, OR=max를 적용해 RAS를 계산하라.
   > **힌트:** 가장 안쪽 AND 가지를 먼저 계산한다.
4. **방법 비교:** 저발현 반응이 조직 기능에 반드시 필요할 때 GIMME와 tINIT이 그 반응을 다루는 방식을 비교하라.
   > **힌트:** 벌점과 대사 과제 보호의 차이를 본다.
5. **활성 기준 검토:** iMAT의 최소 활성 flux 기준을 너무 작게 또는 너무 크게 정했을 때 생길 수 있는 해석 오류를 각각 설명하라.
   > **힌트:** 수치 잡음의 활성 판정과 약하지만 필요한 경로의 누락을 구분한다.
6. **자료 해석:** TPM 합이 항상 $$10^6$$인 이유와, 이 성질이 샘플 간 절대 발현 비교를 보장하지 않는 이유를 설명하라.
   > **힌트:** 길이 보정 뒤 모든 유전자의 비율 합으로 다시 나눈다.
7. **가정 비판:** 전사체는 반응을 지지하지만 단백질체는 결측인 경우, 결측을 0으로 치환하는 정책이 만들 수 있는 오류를 설명하라.
   > **힌트:** 측정 실패와 생물학적 부재를 구분한다.
8. **검증 설계:** 암 세포주 맥락 모델의 유전자 취약성을 평가할 때 내부 검사와 외부 검증을 각각 두 가지 제시하라.
   > **힌트:** 대사 과제·일관성과 독립 CRISPR·교환 자료를 분리한다.

## 후속 응용

[Chapter 9 §3](../chapter-9/03.md)은 맥락 모델의 계산 유전자 필수성과 DepMap 같은 실험 레이블을 분리해 평가한다. [Chapter 4 §13](../chapter-4/13.md)은 FBA·MOMA·ROOM의 교란 가정을 비교하고, [Chapter 10 §11](../chapter-10/11.md)은 생산–성장 포락선을 재현한다. 이들 유지 절에서도 이 장의 기저 모델 버전, 배지, 반응 선택과 독립 검증 원칙을 적용한다.

---

## 핵심 용어 정리

| 용어 | English | 정의 |
|:---|:---|:---|
| 범용 인체 재구축 | Generic Human Reconstruction | 여러 인간 세포 유형에서 지지된 대사 반응과 근거의 통합 지식 기반 |
| 맥락 특이 모델 | Context-Specific Model | 조직·세포·조건 자료와 기능 요구를 반응 집합 또는 bounds에 반영한 모델 |
| 릴리스 | Release | 특정 시점에 고정해 배포한 모델 파일·주석·시험의 버전 |
| 반응 활성 점수 | Reaction Activity Score (RAS) | GPR 집계 규칙으로 유전자 발현을 반응 수준에 옮긴 휴리스틱 점수 |
| 대사 과제 | Metabolic Task | 명시한 입력·출력·경계에서 특정 기능의 실행 가능성을 시험하는 정의 |
| INIT | Integrative Network Inference for Tissues | 반응 증거를 사용해 기능 가능한 부분 네트워크를 선택하는 방법 |
| tINIT | task-driven INIT | 반응 증거 선택에 대사 과제 보존을 결합한 방법 |
| ftINIT | fast task-driven INIT | 사전 계산과 단계별 mode로 반복 추출의 계산 부담을 줄인 방법 |
| GIMME | Gene Inactivity Moderated by Metabolism and Expression | 기능 하한을 지키며 저발현 반응 사용 벌점을 줄이는 방법 |
| iMAT | integrative Metabolic Analysis Tool | high·moderate·low 발현과 반응 활성 상태의 일치를 최대화하는 방법 |
| E-Flux | Expression-based Flux Constraints | 발현값에 비례해 반응의 허용 용량을 축소하는 방법 |
| zFPKM | z-transformed FPKM | 발현 주봉의 half-Gaussian 적합값으로 표준화한 표본별 점수 |
| TPM | Transcripts Per Million | 길이와 라이브러리 규모를 보정해 합을 $$10^6$$으로 만든 상대 발현값 |
| Pseudobulk | Pseudobulk Aggregation | 단일세포 count를 donor·세포 유형 등 생물학적 단위로 합산한 자료 |
| 다중 오믹스 통합 | Multi-Omics Integration | 자료별 증거와 불확실성을 구분해 모델 선택·제약·검증에 결합하는 전략 |

## 답안

1. 범용 재구축은 여러 세포 유형의 반응 근거를 합친 지식 기반이고, 간세포 모델은 간세포 자료·배지·기능 요구를 적용한 조건별 계산 모델이다. 포함 반응이 범용 모델에 있다는 사실은 간세포에서 활성이라는 뜻이 아니다.
2. 확인 비율은 $$1{,}985/2{,}195\approx0.904$$, 즉 약 90.4%이다. 이 분모는 LLM이 불일치 후보로 선별한 부분집합이므로 전체 pair의 정확도나 표현형 예측 성능을 나타내지 않는다.
3. AND 가지는 $$\min(6,2)=2$$이고 바깥 OR는 $$\max(2,4)=4$$이므로 RAS는 4이다. 이 값은 발현 증거의 휴리스틱 집계이며 효소 용량이나 flux의 측정값이 아니다.
4. GIMME에서는 저발현 반응 사용이 벌점을 받지만 기능 하한에 필요하면 사용될 수 있다. tINIT에서는 음의 포함 증거가 있어도 보호 대사 과제를 수행하는 데 필요하면 반응 부분집합에 남는다.
5. 최소 활성 기준이 너무 작으면 solver 허용오차 안의 작은 수치 잡음도 활성 반응으로 셀 수 있다. 너무 크면 실제로는 약하게 사용되지만 기능에 필요한 반응을 비활성으로 판정할 수 있다. 여러 기준에서 결과가 유지되는지 확인하고 사용한 값을 보고해야 한다.
6. TPM은 길이 보정 rate를 모든 유전자의 rate 합으로 나누고 $$10^6$$을 곱하므로 합이 고정된다. 한 유전자의 상대값은 다른 유전자 조성에도 의존하므로 서로 다른 샘플의 절대 RNA 양 차이는 보존되지 않는다.
7. 단백질체 결측은 낮은 abundance·펩타이드 검출 특성·플랫폼 범위 때문에 생길 수 있다. 0 치환은 측정되지 않은 반응을 생물학적으로 부재한다고 오판해 필요한 경로를 제거할 수 있다.
8. 내부 검사는 보호 대사 과제 통과와 flux consistency·에너지 생성 순환 검사를 포함한다. 외부 검증은 구축에 쓰지 않은 동일 조건 CRISPR 의존성과 교환 flux 또는 분비 자료의 비교를 포함한다.

## 참고문헌

1. Duarte NC, Becker SA, Jamshidi N, et al. “Global reconstruction of the human metabolic network based on genomic and bibliomic data.” *PNAS* 104:1777–1782, 2007. [DOI](https://doi.org/10.1073/pnas.0610772104).
2. Thiele I, Swainston N, Fleming RMT, et al. “A community-driven global reconstruction of human metabolism.” *Nature Biotechnology* 31:419–425, 2013. [DOI](https://doi.org/10.1038/nbt.2488).
3. Mardinoglu A, Agren R, Kampf C, et al. “Genome-scale metabolic modelling of hepatocytes reveals serine deficiency in patients with non-alcoholic fatty liver disease.” *Nature Communications* 5:3083, 2014. [DOI](https://doi.org/10.1038/ncomms4083).
4. Brunk E, Sahoo S, Zielinski DC, et al. “Recon3D enables a three-dimensional view of gene variation in human metabolism.” *Nature Biotechnology* 36:272–281, 2018. [DOI](https://doi.org/10.1038/nbt.4072).
5. Robinson JL, Kocabaş P, Wang H, et al. “An atlas of human metabolism.” *Science Signaling* 13:eaaz1482, 2020. [DOI](https://doi.org/10.1126/scisignal.aaz1482).
6. Luo P, et al. “Human2.” *PNAS*, 2026. [DOI](https://doi.org/10.1073/pnas.2516511123).
7. Agren R, Bordel S, Mardinoglu A, et al. “Reconstruction of genome-scale active metabolic networks for 69 human cell types and 16 cancer types using INIT.” *PLoS Computational Biology* 8:e1002518, 2012. [DOI](https://doi.org/10.1371/journal.pcbi.1002518).
8. Agren R, Mardinoglu A, Asplund A, et al. “Identification of anticancer drugs for hepatocellular carcinoma through personalized genome-scale metabolic modeling.” *Molecular Systems Biology* 10:721, 2014. [DOI](https://doi.org/10.1002/msb.145122).
9. Gustafsson J, et al. “Generation and analysis of context-specific genome-scale metabolic models derived from single-cell RNA-seq data.” *PNAS* 120:e2217868120, 2023. [DOI](https://doi.org/10.1073/pnas.2217868120).
10. Becker SA, Palsson BO. “Context-specific metabolic networks are consistent with experiments.” *PLoS Computational Biology* 4:e1000082, 2008. [DOI](https://doi.org/10.1371/journal.pcbi.1000082).
11. Zur H, Ruppin E, Shlomi T. “iMAT: an integrative metabolic analysis tool.” *Bioinformatics* 26:3140–3142, 2010. [DOI](https://doi.org/10.1093/bioinformatics/btq602).
12. Colijn C, Brandes A, Zucker J, et al. “Interpreting expression data with metabolic flux models.” *PLoS Computational Biology* 5:e1000489, 2009. [DOI](https://doi.org/10.1371/journal.pcbi.1000489).
13. Opdam S, Richelle A, Kellman B, et al. “A systematic evaluation of methods for tailoring genome-scale metabolic models.” *Cell Systems* 4:318–329.e6, 2017. [DOI](https://doi.org/10.1016/j.cels.2017.01.010).
14. Richelle A, Chiang AWT, Kuo CC, Lewis NE. “Increasing consensus of context-specific metabolic models by integrating data-inferred cell functions.” *PLoS Computational Biology* 15:e1006867, 2019. [DOI](https://doi.org/10.1371/journal.pcbi.1006867).

---
