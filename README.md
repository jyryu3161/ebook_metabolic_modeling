# 게놈 규모 대사 모델링 (Genome-scale Metabolic Modeling)

> 미생물부터 인체 세포까지, 대사 네트워크를 수학으로 읽고 예측하는 법

이 책은 **게놈 규모 대사 모델(Genome-scale Metabolic Model, GEM)** 을 처음 접하는 대학원생·연구자·엔지니어를 위한 한국어 교재입니다. 미생물 생장·대사와 선형대수 기초에서 출발하여, 대사 네트워크를 행렬로 표현하고, 제약 기반 최적화([FBA](chapter-4.-flux-balance-analysis-fba.md))로 세포의 대사 흐름을 예측하며, 모델을 구축·검증하고, 오믹스 데이터를 통합해 질병·세포공장·인공지능 응용으로 확장하는 전 과정을 다룹니다.

## 이 책의 특징

* **개념 + 수식 + 코드의 3중 서술** — 각 개념을 직관적 비유와 수학적 정형화로 설명한 뒤, 검산한 [COBRApy](https://opencobra.github.io/cobrapy/) 실행 예제 또는 구현 원리를 보여 주는 명시적 의사코드로 확인합니다.
* **실습 중심** — 주요 개념마다 `💡 실습` 블록으로 재현 가능한 예제와 해석 기준을 제공합니다.
* **최적화를 눈으로 확인** — LP 가능 영역, QP MOMA 투영, ROOM의 MILP 허용구간, FVA와 production envelope를 재현 가능한 그림으로 연결하고, Jupyter에서 Plotly·widget 예제를 직접 조작합니다.
* **상호 연결된 개념** — 핵심 용어는 처음 정의된 챕터로 링크되어 있으며, 권말 [핵심 용어집](glossary.md)에서 한눈에 찾아볼 수 있습니다.
* **원 강의 전체 범위** — 18개 PPT의 미생물 생장, 합성생물학, 선형대수, SBML, 기초 통계와 Human GEM 강의를 준비 학습·보충 페이지까지 포함해 연결했습니다. 자료별 위치는 [PPT–전자책 대응표](lecture-coverage-map.md)에서 확인할 수 있습니다.
* **원 논문의 결론과 한계를 함께 읽기** — FBA, FVA, pFBA, MOMA, ROOM, OptKnock, tINIT 등은 [대표 논문 가이드](landmark-papers.md)에서 “질문–방법–검증–결론–한계” 형식으로 비교합니다.

## 대상 독자와 선수 지식

* 시스템생물학·대사공학·생물정보학에 관심 있는 학부 고학년/대학원생
* 파이썬 기초에 대한 친숙함이 있으면 좋습니다. 필요한 미생물 생리·생화학·선형대수·통계 배경은 [준비 학습](supplements/microbial-growth-metabolism.md)과 보충 페이지에서 함께 설명합니다.

## 책의 구성

| 부 | 챕터 | 내용 |
|----|------|------|
| **준비 학습** | [미생물 생장·대사·효소](supplements/microbial-growth-metabolism.md) | 배지, 성장률, Monod, flux 단위, 중심대사, EC·효소 예측 |
| | [선형대수](supplements/linear-algebra.md) | 벡터·행렬, 내적·투영, 연립방정식, rank·null space |
| | [합성생물학](supplements/synthetic-biology.md) | 회로·합성 게놈, DBTL, biofoundry, 세포공장 |
| | [재현 가능한 실습 환경](supplements/reproducible-environment.md) | 가상환경, Jupyter kernel, solver 능력, 설치 회귀 테스트 |
| **I. 기초** | [1. 대사모델링의 개요](chapter-1..md) | 동기, 역사, 모델의 종류 |
| | [2. 생화학 반응과 대사 네트워크 표현](chapter-2..md) | 반응·대사물, 화학량론 행렬, 질량보존 |
| | [3. GEM의 구조](chapter-3.-genome-scale-metabolic-model-gem.md) | GPR, 구획, 바이오매스 목적함수 |
| | [4. Flux Balance Analysis (FBA)](chapter-4.-flux-balance-analysis-fba.md) | 제약 기반 최적화, FVA, pFBA |
| **핵심 방법** | [유전자 교란, MOMA와 ROOM](supplements/perturbation-analysis.md) | 결손 예측, reference flux, QP·MILP 결과 해석 |
| **II. 구축·통합** | [5. 모델 구축과 품질 관리](chapter-5..md) | 재구축, gap-filling, Recon1–Human2 |
| | [6. Omics 데이터 통합](chapter-6.-omics.md) | 맥락 특이 모델, RNA-seq 통합 |
| **III. 응용** | [7. 질병 모델링과 약물 표적 발굴](chapter-7..md) | 암 대사, 필수성, MTA |
| | [8. 미생물·세포공장·합성생물학 응용](chapter-8..md) | 균주 설계, MOMA/ROOM, 커뮤니티 |
| **IV. 최신 동향** | [9. AI와 대사모델링](chapter-9.-ai.md) | 머신러닝, 딥러닝, foundation model |
| **V. 통합 실습** | [10. COBRApy 완전 실행형 튜토리얼](chapter-10.-cobrapy-tutorial.md) | 환경 검증부터 FBA·pFBA·FVA·결손·MOMA·ROOM·MILP·SBML까지 |

## 실습 환경

본문의 기준 수치는 Python 3.10+와 [COBRApy](https://opencobra.github.io/cobrapy/) 0.30.0에서 검산했습니다. 최소 설치:

```bash
python -m pip install "cobra==0.30.0"
python -m pip check
```

Jupyter·시각화·머신러닝 패키지를 포함한 전체 core 환경, 커널 등록, 모델 checksum, LP/QP/MILP solver 선택은 [준비 학습 D](supplements/reproducible-environment.md)에서 다룹니다. 설치를 마친 뒤에는 [Chapter 10](chapter-10.-cobrapy-tutorial.md)을 순서대로 실행해 환경과 개념을 함께 검증하십시오. SBML 파일의 구조와 round-trip 검증은 [SBML 보충](supplements/sbml-practical.md), RNA-seq 정규화와 다중검정은 [통계 보충](supplements/omics-statistics.md)을 참고하십시오.

---

*이 교재는 `raw_data/GEM_ppt`의 18개 강의 PPT(총 488슬라이드)와 9주 과정의 GEM 강의 노트·실습 노트북을 바탕으로 재구성되었습니다.*
