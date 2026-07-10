# 게놈 규모 대사 모델링 (Genome-scale Metabolic Modeling)

> 화학량론적 재구축에서 제약 기반 분석과 실험 검증까지

이 책은 **게놈 규모 대사 모델(genome-scale metabolic model, GEM)**을 다루는 학부 고학년·대학원 입문 수준의 한국어 교재이다. 생화학 반응을 화학량론 행렬로 표현하고, 제약 기반 분석으로 가능한 플럭스 상태를 계산하며, 재구축과 품질관리, 오믹스 맥락화, 질병·세포공장·미생물군집·AI 응용으로 확장하는 과정을 다룬다. 모델의 출력은 명시된 배지·경계조건·목적함수에 따른 조건부 예측이며, 실험 관찰과 구분하여 해석한다.

## 이 책의 특징

* **정의–가정–수식–해석의 일관된 전개** — 대사물·반응·플럭스의 단위와 모델 경계를 먼저 정의하고, 각 방법의 가정과 적용 범위를 명시한다.
* **재현 가능한 계산** — [COBRApy](https://opencobra.github.io/cobrapy/) 예제에 모델·solver·배지·목적함수와 검산 기준을 기록하고, 모식도와 실제 계산 결과를 구분한다.
* **수학적 기하와 생물학적 해석의 연결** — LP 가능 영역, MOMA 투영, ROOM의 허용구간, FVA와 production envelope를 도식과 코드로 교차 검토한다.
* **불확실성과 대안해의 명시** — 하나의 최적 플럭스를 유일한 세포 상태로 해석하지 않고 FVA, sampling, 민감도 및 외부 검증을 함께 다룬다.
* **일차 문헌 중심의 근거** — FBA, pFBA, MOMA, ROOM, OptKnock, tINIT 등은 [대표 논문 가이드](landmark-papers.md)에서 질문·방법·검증·결론·한계로 비교하며, 주요 도식의 출처와 재사용 조건은 [그림 출처 대장](FIGURE_SOURCES.md)에 기록한다.
* **표준 형식과 품질관리** — SBML/FBC 저장·교환, MEMOTE, 오믹스 통계와 교란 분석을 보충 자료와 통합 실습에서 검증한다.

## 대상 독자와 선수 지식

* 시스템생물학·대사공학·생물정보학을 공부하는 학부 고학년과 대학원 입문 학습자
* 행렬·벡터, 몰과 화학량론, 함수·부등식 및 Python 기초를 선수 지식으로 권장한다. 선형계획법과 생화학의 세부 전제는 해당 장에서 정의한다.

## 책의 구성

| 부 | 챕터 | 내용 |
|----|------|------|
| **I. 기초** | [1. 대사모델링의 개요](chapter-1/README.md) | 동기, 역사, 모델의 종류 |
| | [2. 생화학 반응과 대사 네트워크 표현](chapter-2/README.md) | 반응·대사물, 화학량론 행렬, 질량보존 |
| | [3. GEM의 구조](chapter-3/README.md) | GPR, 구획, 바이오매스 목적함수 |
| | [4. Flux Balance Analysis (FBA)](chapter-4/README.md) | 제약 기반 최적화, FVA, pFBA |
| **핵심 방법** | [유전자 교란, MOMA와 ROOM](supplements/perturbation-analysis.md) | 결손 예측, reference flux, QP·MILP 결과 해석 |
| **II. 구축·통합** | [5. 모델 구축과 품질 관리](chapter-5/README.md) | 재구축, gap-filling, Recon1–Human2 |
| | [6. Omics 데이터 통합](chapter-6/README.md) | 맥락 특이 모델, RNA-seq 통합 |
| **III. 응용** | [7. 질병 모델링과 약물 표적 발굴](chapter-7/README.md) | 암 대사, 필수성, MTA |
| | [8. 미생물·세포공장·합성생물학 응용](chapter-8/README.md) | 균주 설계, MOMA/ROOM, 커뮤니티 |
| **IV. 최신 동향** | [9. AI와 대사모델링](chapter-9/README.md) | 머신러닝, 딥러닝, foundation model |
| **V. 통합 실습** | [10. COBRApy 완전 실행형 튜토리얼](chapter-10/README.md) | 환경 검증부터 FBA·pFBA·FVA·결손·MOMA·ROOM·MILP·SBML까지 |

## 실습 환경

실행 예제의 기준 환경은 Python 3.10+와 [COBRApy](https://opencobra.github.io/cobrapy/) 0.30.0이다. 최소 설치는 다음과 같다.

```bash
python -m pip install "cobra==0.30.0"
python -m pip check
```

설치 후 [Chapter 10](chapter-10/README.md)의 preflight에서 Python·COBRApy·solver·모델 checksum을 먼저 확인한다. Jupyter·시각화·머신러닝 패키지, LP/QP/MILP solver 선택과 결과 provenance도 같은 장에서 다룬다. SBML 구조와 round-trip 검증은 [SBML 보충](supplements/sbml-practical.md), RNA-seq 정규화와 다중검정은 [통계 보충](supplements/omics-statistics.md)을 참고한다.

---

*이 교재는 `raw_data/GEM_ppt`의 18개 강의 PPT(총 488슬라이드)와 9주 과정의 GEM 강의 노트·실습 노트북을 바탕으로 재구성되었습니다.*
