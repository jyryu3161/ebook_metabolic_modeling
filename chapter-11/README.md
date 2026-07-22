# Chapter 11. 실습 워크벤치: 설치부터 맥락 특이적 재구축까지

이 장은 앞선 장에서 정의한 개념을 하나의 연속된 실습으로 재현합니다. 각 장에 이미 있는 `실습` 절은 그대로 두고, 이 장은 **환경 설치 → 범용 모델 분석 → 초안 재구축 → 맥락 특이적 재구축**으로 이어지는 도구 사용의 전체 흐름을 한곳에 모읍니다. 목표는 코드를 읽는 것이 아니라, 같은 명령을 직접 실행해 동일한 숫자와 그림을 얻는 것입니다.

## 이 장의 실행 환경

이 장의 모든 터미널 출력과 그림은 아래 환경에서 **실제로 실행한 결과**입니다. 모식도가 아니라 계산 결과이므로, 같은 버전을 맞추면 숫자가 재현됩니다.

| 항목 | 값 |
|:---|:---|
| OS | macOS (darwin) |
| Python | 3.10 |
| COBRApy | 0.30.0 |
| LP·MILP solver | GLPK(기본), Gurobi(선택, QP·대형 MILP) |
| 예제 모델 | BiGG `e_coli_core`(COBRApy `textbook`), Human-GEM |
| 그림 | matplotlib로 계산 결과를 직접 렌더한 PNG |

솔버·모델 릴리스가 바뀌면 숫자가 달라질 수 있으므로, 각 절은 모델 ID·버전, solver, 배지, 목적함수, 허용오차를 함께 기록합니다. flux는 항상 `mmol gDW⁻¹ h⁻¹` 단위의 반응 진행률로 해석합니다([Chapter 1](../chapter-1/README.md)).

## 장의 구성과 의존 흐름

```mermaid
flowchart TD
    A["1. 환경·솔버·Gurobi 라이선스"] --> B["2. COBRApy 기초와 FBA"]
    B --> C["3. pFBA와 FVA"]
    B --> D["4. 유전자·반응 결손과 MOMA"]
    A --> E["5. CarveMe: 게놈에서 초안 GEM"]
    E --> F["6. mmplatform: tINIT 맥락 특이적 재구축"]
    E --> G["7. TRACE-GEM: 근거기반 gap-filling"]
    C --> H["8. CMM: LAD·E-Flux2 발현 통합"]
    D --> H
    F --> I["9. CMIG: 커뮤니티 모델링"]
```

*그림 11.1. 제11장 실습의 의존 흐름. 환경 준비(1)를 마친 뒤 범용 모델 분석(2–4)과 초안 재구축(5)이 갈라지고, 맥락 특이적 재구축(6)이 이들을 합류시킨다. 저자 작성.*

- **1. 환경·솔버·Gurobi 라이선스** — 격리된 가상환경, COBRApy 설치, GLPK 확인, Gurobi 학술 라이선스 발급·활성화.
- **2. COBRApy 기초와 FBA** — 모델 적재, 정상상태 최적화, 교환 flux 해석([Chapter 4](../chapter-4/README.md)).
- **3. pFBA와 FVA** — 대안 최적해와 flux 범위, blocked 반응([Chapter 4](../chapter-4/README.md)).
- **4. 유전자·반응 결손과 MOMA** — 결손 예측과 MOMA의 조정 최소화 가정, production envelope([Chapter 8](../chapter-8/README.md)).
- **5. CarveMe** — 게놈 주석에서 top-down으로 초안 GEM을 만드는 자동 재구축([Chapter 5](../chapter-5/README.md)).
- **6. mmplatform** — 수정 TROPPO 기반 tINIT으로 발현에서 시료 특이적(인체) 모델을 재구축하고 LAD·선형 MOMA로 교란을 평가합니다([Chapter 5](../chapter-5/README.md), [Chapter 6](../chapter-6/README.md)).
- **7. TRACE-GEM** — 단백질 FASTA에서 CarveMe 초안을 만든 뒤, 대사 task 통과를 기준으로 KEGG 근거 가중 gap-filling으로 수리합니다([Chapter 5](../chapter-5/README.md)).
- **8. CMM** — 발현-제약 통합(LAD·E-Flux2)과 교란·생산·정상화 분석을 제공합니다([Chapter 6](../chapter-6/README.md), [Chapter 8](../chapter-8/README.md)).
- **9. CMIG** — MICOM 기반 미생물 군집·숙주-미생물 상호작용 모델링을 다룹니다([Chapter 8](../chapter-8/README.md) 9절).

이 장의 6–9절은 저자가 개발·공개한 도구([mmplatform](https://github.com/jyryu3161/mmplatform), [TRACE-GEM](https://github.com/jyryu3161/TRACE-GEM), [CMM](https://github.com/jyryu3161/CMM), [CMIG](https://github.com/jyryu3161/CMIG))를 실제로 실행한 결과입니다.

## 이 장을 읽는 법

각 절은 `실행 → 출력 → 해석`의 순서를 따릅니다. 코드 블록은 실제로 입력한 명령이고, 그 아래 회색 출력 블록은 그 명령이 실제로 낸 출력입니다. 숫자가 다르게 나오면 먼저 모델 버전과 solver, 배지 설정을 점검합니다. 개념의 근거가 필요할 때는 각 절이 가리키는 본문 장을 참조합니다.
