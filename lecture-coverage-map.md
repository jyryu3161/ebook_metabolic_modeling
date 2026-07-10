# 강의 PPT–전자책 대응표

> `raw_data/GEM_ppt`의 PPTX 18개, 총 488장을 슬라이드 텍스트·도형·표·그림 기준으로 대조한 결과입니다. 이 표는 강의의 학습 내용이 전자책 어디에 반영됐는지 추적하기 위한 색인입니다.

## 포함 원칙

1. 제목·강의실·평가 비율·연락처 같은 **학기 행정 정보**는 전자책 본문에 반복하지 않았습니다.
2. 뉴스 화면이나 장식용 이미지는 핵심 개념과 출처가 있는 설명으로 바꿨습니다.
3. 설치 명령·웹 주소·소프트웨어 출력은 슬라이드 제작 시점의 화면을 그대로 옮기지 않고, 현재 실행 가능한 workflow와 버전 주의사항으로 교정했습니다.
4. 논문 수치와 방법 결론은 원 논문으로 다시 확인했습니다. 특히 pFBA의 “98%”, MOMA/ROOM 비교, MEMOTE 점수, Human2 수치는 적용 범위를 함께 적었습니다.
5. 같은 개념이 여러 PPT에서 반복되면 가장 자연스러운 장에서 한 번 충분히 설명하고, 다른 장에서는 링크로 연결했습니다.

## 18개 자료의 대응 위치

| 강의 자료 | 슬라이드 | 핵심 학습 내용 | 전자책 반영 위치 | 검토·교정 메모 |
|:---|---:|:---|:---|:---|
| `lec.선형대수학` | 37 | 벡터, norm, 내적, 행렬, 전치, 연립방정식, span, rank, null space, 공분산, tensor | [준비 B](supplements/linear-algebra.md), [Ch2](chapter-2..md), [Ch4](chapter-4.-flux-balance-analysis-fba.md) | rank와 자유도를 실제 `textbook` 모델(rank 67, nullity 28)로 연결 |
| `lec1-OT` | 22 | 과목 전체 지도, biotechnology의 색, 합성생물학, bio-based chemical, DBTL, SDG, GEM의 역할 | [README](README.md), [준비 C](supplements/synthetic-biology.md), [Ch1](chapter-1..md), [Ch8](chapter-8..md) | 학기 일정·평가·개인 연락처는 제외; `OT`는 orientation lecture |
| `lec2-introduction` | 43 | lac operon, toggle switch, repressilator, 합성 게놈·최소세포, abstraction/standardization/modularity, BioBrick, Cello, biosensor, 치료 미생물, ALE, T7-ORACLE, biofoundry | [준비 C](supplements/synthetic-biology.md), [Ch8](chapter-8..md) | T7-ORACLE은 “10만 년”이 아니라 약 10만 배 빠른 mutation-rate engineering으로 교정 |
| `lec7-Microbial Growth and Specific Growth Rate` | 32 | OD/DCW, specific growth rate, doubling time, 성장곡선, Monod 식, batch/fed-batch/chemostat, 농도–flux 환산 | [준비 A](supplements/microbial-growth-metabolism.md), [Ch1](chapter-1..md), [Ch4](chapter-4.-flux-balance-analysis-fba.md) | 농도와 `mmol gDW⁻¹ h⁻¹` flux를 구분하고 손계산 예제 추가 |
| `lec8-Microbial Metabolism` | 29 | 영양 방식, 배지, 세포 조성, catabolism/anabolism, ATP·환원력, glycolysis/TCA/ETC, 발효 | [준비 A](supplements/microbial-growth-metabolism.md), [Ch2](chapter-2..md), [Ch3](chapter-3.-genome-scale-metabolic-model-gem.md) | 중심대사 지식을 S matrix와 biomass로 연결 |
| `lec9-Enzyme Function` | 21 | 효소 촉매·저해·feedback, EC 번호, 서열/구조 기반 기능 예측, DeepEC, CLEAN | [준비 A](supplements/microbial-growth-metabolism.md), [Ch3](chapter-3.-genome-scale-metabolic-model-gem.md), [Ch5](chapter-5..md), [Ch9](chapter-9.-ai.md) | EC 예측을 GPR 근거로 쓸 때의 confidence와 수동 검증 한계 추가 |
| `lec10-Metabolic Network Modeling` | 23 | 반응식, 방향성, stoichiometric matrix, 정상상태, GPR, 구획·수송, biomass·boundary reaction | [Ch2](chapter-2..md), [Ch3](chapter-3.-genome-scale-metabolic-model-gem.md) | PTS 순반응, 실제 GPR 예시와 demand/sink 해석 교정 |
| `lec11-Constraint-based flux balance analysis` | 37 | underdetermined system, feasible space, gradient descent와 LP 비교, objective/bounds, FBA, pFBA, FVA, knockout | [Ch4](chapter-4.-flux-balance-analysis-fba.md), [대표 논문 가이드](landmark-papers.md) | FBA는 학습률 없이 LP 솔버로 전역 최적값을 구함을 명시; 대안 최적해와 퇴화를 구분; FVA·pFBA 해석 범위 교정 |
| `lec12-Simulation-genetic-perturbation` | 32 | GPR knockout, feasible-space 변화, FBA·MOMA·ROOM, 유전자 필수성, perturbation 해석 | [유전자 교란 보충](supplements/perturbation-analysis.md), [Ch7](chapter-7..md), [Ch8](chapter-8..md), [대표 논문 가이드](landmark-papers.md) | 원 논문의 ROOM 수치와 COBRApy objective/growth 구분으로 교정 |
| `lec13-SBML` | 19 | XML 계층, SBML 구성요소, FBC, exchange/demand/sink, biomass/ATPM, 모델 읽기·쓰기 | [SBML 실무 보충](supplements/sbml-practical.md), [Ch3](chapter-3.-genome-scale-metabolic-model-gem.md), [Ch5](chapter-5..md) | SBML Level 3 FBC v2와 round-trip 검증 절차 추가 |
| `lec14-GEM reconstruction` | 30 | bottom-up/top-down, FASTA·EC, database, GPR, transport/spontaneous/boundary, biomass, gap-filling, CarveMe, essentiality, Recon2M | [준비 A](supplements/microbial-growth-metabolism.md), [Ch5](chapter-5..md), [SBML 보충](supplements/sbml-practical.md) | 96-step stage, confidence, Recon2M 계보와 수치 보강 |
| `lec15-GEM reconstruction practice` | 21 | CarveMe universal model/carving/gap-fill, reference sequence, media DB, biomass, FASTA 실행, MEMOTE | [Ch5](chapter-5..md), [준비 D](supplements/reproducible-environment.md), [SBML 보충](supplements/sbml-practical.md) | 버전별 CLI 차이를 경고하고 결과 모델을 MEMOTE·성장·음성 phenotype으로 검증 |
| `lec16-Metabolic simulation practice` | 4 | pixi/Python/COBRApy/Jupyter/solver 환경과 notebook 실행 | [준비 D](supplements/reproducible-environment.md), [Ch4](chapter-4.-flux-balance-analysis-fba.md) | PPT의 pixi 설정은 책에서 같은 목적의 표준 `venv` workflow로 대체했음을 명시; 무료 GLPK의 LP/MILP와 QP solver 요구를 분리하고 설치 검증용 assert 제공 |
| `lec16-Metabolic simulation practice-2` | 7 | 실습 환경, FSEOF, FVSEOF | [준비 D](supplements/reproducible-environment.md), [Ch8 §6.5](chapter-8..md), [대표 논문 가이드](landmark-papers.md) | 강제 product flux 스캔 코드와 pFBA/FVA 기반 재검증 주의 추가 |
| `lec17-데이터분석 및 기초통계` | 57 | WGS와 RNA-seq의 구분, raw count, CPM/RPKM/TPM, negative binomial, edgeR/DESeq2, 기술·추론통계, 정규/t 분포, t-test, p-value, Type I/II error, Bonferroni/BH, 비모수 | [통계 보충](supplements/omics-statistics.md), [Ch6](chapter-6.-omics.md) | 통계 보충에서 WGS와 RNA-seq의 측정 대상·GEM 활용 차이를 구분해 보강; TPM을 sample 간 DEG 검정 입력으로 쓰지 않으며 p-value와 effect size를 구분 |
| `lec18-Transcriptome based flux prediction` | 11 | transcriptome–flux 문제, LAD, E-Flux, E-Flux2, SPOT, PRECISE1k | [Ch6](chapter-6.-omics.md), [통계 보충](supplements/omics-statistics.md) | expression이 flux를 직접 결정하지 않으며 E-Flux 뒤에도 downstream objective가 필요함을 명시 |
| `lec19-Human genome-scale metabolic models` | 47 | 인체 구획, bottom-up/top-down, Recon1/2/2.2/2M/3D, Human1, database, 응용, DepMap, ML essentiality, synthetic lethality | [Ch5](chapter-5..md), [Ch7](chapter-7..md), [Ch9](chapter-9.-ai.md), [대표 논문 가이드](landmark-papers.md) | Recon2M 포함; Human2(2026)까지 갱신; MOMA-RF 논문 귀속·표본·성능 교정 |
| `lec20-Omics integration` | 16 | generic→context-specific, PCAWG/TCGA, INIT/tINIT, metabolic task, rank-tINIT, ftINIT | [Ch5](chapter-5..md), [Ch6](chapter-6.-omics.md) | tINIT task 보장을 단순 반응 활성식으로 축약하지 않고 실제 절차로 설명 |

합계: **18개 파일, 488개 슬라이드**.

## 읽기 순서와 PPT 번호가 다른 이유

강의에서는 필요에 따라 개념을 먼저 보여준 뒤 수학을 되돌아가 설명할 수 있지만, 책은 독자가 혼자 순서대로 읽어도 의존성이 끊기지 않아야 합니다. 따라서 전자책은 다음 순서로 재배열했습니다.

```text
미생물 생리·선형대수·합성생물학·환경 설정
→ 네트워크 표현
→ GEM 구조와 SBML
→ FBA와 대안해
→ 유전자 교란(MOMA/ROOM)
→ 재구축·품질관리·인체 모델 역사
→ 통계와 오믹스 통합
→ 질병·세포공장 응용
→ AI 보조 모델링
```

이 순서에서는 Chapter 7에서 knockout 결과를 해석하기 전에 [유전자 교란 보충](supplements/perturbation-analysis.md)을 먼저 읽고, Chapter 6의 omics threshold를 다루기 전에 [통계 보충](supplements/omics-statistics.md)을 먼저 읽습니다.
