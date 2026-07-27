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
| `lec.선형대수학` | 37 | 벡터, 행렬, 연립방정식과 고급 선형대수 주제 | [Ch2](chapter-2/README.md), [Ch4](chapter-4/README.md) | 본문은 행렬을 반응 기록표로 읽고 생성·소비를 검산하는 데 필요한 내용만 남김 |
| `lec1-OT` | 22 | 과목 전체 지도, biotechnology, 합성생물학, bio-based chemical, DBTL, SDG, GEM의 역할 | [README](README.md), [Ch1](chapter-1/README.md) | 학기 행정 정보와 삭제된 응용 장의 상세 내용은 제외; `OT`는 orientation lecture |
| `lec2-introduction` | 43 | lac operon, toggle switch, repressilator, 합성 게놈·최소세포, BioBrick, biosensor, ALE와 biofoundry | [Ch1](chapter-1/README.md) | 대사 모델 입문에 필요한 역사·범위만 남기고 합성생물학 응용의 세부 전개는 제외 |
| `lec7-Microbial Growth and Specific Growth Rate` | 32 | OD/DCW, specific growth rate, doubling time, 성장곡선, Monod 식, batch/fed-batch/chemostat, 농도–flux 환산 | 준비 A, [Ch1](chapter-1/README.md), [Ch4](chapter-4/README.md) | 농도와 `mmol gDW⁻¹ h⁻¹` flux를 구분하고 손계산 예제 추가 |
| `lec8-Microbial Metabolism` | 29 | 영양 방식, 배지, 세포 조성, catabolism/anabolism, ATP·환원력, glycolysis/TCA/ETC, 발효 | 준비 A, [Ch2](chapter-2/README.md), [Ch3](chapter-3/README.md) | 중심대사 지식을 S matrix와 biomass로 연결 |
| `lec9-Enzyme Function` | 21 | 효소 촉매·저해·feedback, EC 번호, 서열/구조 기반 기능 예측, DeepEC, CLEAN | 준비 A, [Ch3](chapter-3/README.md), [Ch5](chapter-5/README.md), [Ch9](chapter-9/README.md) | EC 예측을 GPR 근거로 쓸 때의 confidence와 수동 검증 한계 추가 |
| `lec10-Metabolic Network Modeling` | 23 | 반응식, 방향성, stoichiometric matrix, 정상상태, GPR, 구획·수송, biomass·boundary reaction | [Ch2](chapter-2/README.md), [Ch3](chapter-3/README.md) | PTS 순반응, 실제 GPR 예시와 demand/sink 해석 교정 |
| `lec11-Constraint-based flux balance analysis` | 37 | 목적함수·반응 범위, FBA, pFBA, FVA와 knockout | [Ch4](chapter-4/README.md), [대표 논문 가이드](landmark-papers.md) | 솔버 내부 알고리즘 비교와 LP 표준형 유도는 제외하고 배지·목적함수·결과 검산에 집중 |
| `lec12-Simulation-genetic-perturbation` | 32 | GPR knockout, FBA·MOMA·ROOM, 유전자 필수성과 교란 해석 | [Ch4](chapter-4/README.md), [Ch10](chapter-10/README.md), [Ch11](chapter-11/README.md), [대표 논문 가이드](landmark-papers.md) | 결손에서 GPR·반응 경계·성장 표현형으로 이어지는 생물학적 흐름을 본문에 통합 |
| `lec13-SBML` | 19 | XML 계층, SBML 구성요소, FBC, exchange/demand/sink, biomass/ATPM, 모델 읽기·쓰기 | [SBML 실무 보충](supplements/sbml-practical.md), [Ch3](chapter-3/README.md), [Ch5](chapter-5/README.md) | SBML Level 3 FBC v2와 round-trip 검증 절차 추가 |
| `lec14-GEM reconstruction` | 30 | bottom-up/top-down, FASTA·EC, database, GPR, transport/spontaneous/boundary, biomass, gap-filling, CarveMe, essentiality, Recon2M | 준비 A, [Ch5](chapter-5/README.md), [SBML 보충](supplements/sbml-practical.md) | 96-step stage, confidence, Recon2M 계보와 수치 보강 |
| `lec15-GEM reconstruction practice` | 21 | CarveMe universal model/carving/gap-fill, reference sequence, media DB, biomass, FASTA 실행, MEMOTE | [Ch5](chapter-5/README.md), 준비 D, [SBML 보충](supplements/sbml-practical.md) | 버전별 CLI 차이를 경고하고 결과 모델을 MEMOTE·성장·음성 phenotype으로 검증 |
| `lec16-Metabolic simulation practice` | 4 | pixi/Python/COBRApy/Jupyter/solver 환경과 notebook 실행 | 준비 D, [Ch4](chapter-4/README.md) | PPT의 pixi 설정은 책에서 같은 목적의 표준 `venv` workflow로 대체했음을 명시; 무료 GLPK의 LP/MILP와 QP solver 요구를 분리하고 설치 검증용 assert 제공 |
| `lec16-Metabolic simulation practice-2` | 7 | 실습 환경, 생산 플럭스 스캔 | [Ch10](chapter-10/README.md), [Ch11](chapter-11/README.md), [대표 논문 가이드](landmark-papers.md) | 삭제된 균주 설계 장 대신 재현 가능한 실행과 범위 해석으로 연결 |
| `lec17-데이터분석 및 기초통계` | 57 | WGS와 RNA-seq의 구분, raw count, CPM/RPKM/TPM, negative binomial, edgeR/DESeq2, 기술·추론통계, 정규/t 분포, t-test, p-value, Type I/II error, Bonferroni/BH, 비모수 | [통계 보충](supplements/omics-statistics.md), [Ch6](chapter-6/README.md) | 통계 보충에서 WGS와 RNA-seq의 측정 대상·GEM 활용 차이를 구분해 보강; TPM을 sample 간 DEG 검정 입력으로 쓰지 않으며 p-value와 effect size를 구분 |
| `lec18-Transcriptome based flux prediction` | 11 | transcriptome–flux 문제, LAD, E-Flux, E-Flux2, SPOT, PRECISE1k | [Ch6](chapter-6/README.md), [통계 보충](supplements/omics-statistics.md) | expression이 flux를 직접 결정하지 않으며 E-Flux 뒤에도 downstream objective가 필요함을 명시 |
| `lec19-Human genome-scale metabolic models` | 47 | 인체 구획, Recon·HMR 계보, Human1·Human2, 데이터베이스와 ML 필수성 | [Ch6](chapter-6/README.md), [Ch9 §1–3](chapter-9/README.md), [대표 논문 가이드](landmark-papers.md) | Human2까지 갱신하고 질병·복합 표적 응용은 이번 본문 범위에서 제외 |
| `lec20-Omics integration` | 16 | 범용 모델에서 맥락 특이 모델로, INIT/tINIT, 대사 과제와 ftINIT | [Ch6](chapter-6/README.md) | 고급 수학 유도 대신 반응 선택 근거·기능 보존·독립 검증 절차를 설명 |

합계: **18개 파일, 488개 슬라이드**.

## 읽기 순서와 PPT 번호가 다른 이유

강의에서는 필요에 따라 개념을 먼저 보여준 뒤 수학을 되돌아가 설명할 수 있지만, 책은 독자가 혼자 순서대로 읽어도 의존성이 끊기지 않아야 합니다. 따라서 전자책은 다음 순서로 재배열했습니다.

```text
미생물 생리·반응 기록표·환경 설정
→ 네트워크 표현
→ GEM 구조와 SBML
→ FBA·대안해·유전자 교란
→ 재구축·품질관리
→ 인체 모델 계보와 오믹스 통합
→ AI·GEM 입문
→ 재현 가능한 통합 실습
```

이 순서에서는 Chapter 4에서 배지·유전자 결손·MOMA·ROOM을 한 흐름으로 익힌 뒤 재구축과 맥락화를 다룹니다. Chapter 6의 오믹스 임계값을 다루기 전에는 [통계 보충](supplements/omics-statistics.md)을 먼저 읽을 수 있습니다.
