# Chapter 1 Nano Banana Pro QA Report

- 검수일: 2026-07-27
- 검수 방식: 각 최종 JPEG를 `view_image`의 원본 해상도 모드로 개별 확인
- 공통 출력 해상도: 2752×1536 (16:9, 2K)
- 공통 판정 기준: 과학적 방향·부호·관계, 지정 문구와 철자, 명세 외 텍스트·수치·기호, 잘림·겹침·과도한 장식·gradient·shadow, 핵심 패널 누락

## 최종 판정

| 그림 | 최종 모델 | 시도 / 재시도 | 판정 |
|---|---|---:|---|
| `ch1_fig06_reconstruction_to_models.jpg` | `nano-banana-pro-preview` | 12 / 11 | PASS |
| `ch1_fig08_constraints_vs_dynamics.jpg` | `nano-banana-pro-preview` | 8 / 7 | PASS |
| `ch1_fig10_model_card_four_axes.jpg` | `nano-banana-pro-preview` | 4 / 3 | PASS |
| `ch1_fig11_history_claim_contract.jpg` | `nano-banana-pro-preview` | 4 / 3 | PASS |
| `ch1_fig12_history_added_layers.jpg` | `gemini-3-pro-image` | 3 / 2 | PASS |
| `ch1_fig14_community_exchange_contract.jpg` | `nano-banana-pro-preview` | 4 / 3 | PASS |
| `ch1_fig16_mismatch_diagnosis.jpg` | `gemini-3-pro-image` | 3 / 2 | PASS |

## 개별 PASS 근거

### fig06 — Reconstruction to Conditional Models

- 과학 관계: 하나의 `공유 재구축`에서 검은 Y자 분기가 A와 B 조건으로 각각 직접 연결되고, A와 B 사이에는 연결이 없어 병렬 조건화를 정확히 표현한다.
- 텍스트: 공유 요소와 A/B 조건·출력 라벨이 명세와 일치하며 임의 수치, 보조 문구, 아이콘이 없다.
- 시각 품질: 텍스트와 선만으로 된 평면 도식으로 잘림·겹침, gradient, shadow, 질감, 과도한 장식이 없다.
- 핵심 요소: 공유 재구축, 두 조건 묶음, 두 조건부 예측과 서로 다른 플럭스 화살표 묶음이 모두 있다.

### fig08 — Constraint-Based vs Kinetic Modeling

- 과학 관계: 제약 기반 패널은 시간축 없이 복수의 가능한 경로와 강조 경로를, 동역학 패널은 시간에 따른 녹색 감소·적색 증가의 두 곡선을 표현한다.
- 텍스트: `화학량론`, `반응 경계`, `배지`, `목적`, `초기 농도`, `속도식`, `매개변수`, `농도`, `시간`, 비교 라벨이 정확하며 임의 눈금·수치가 없다.
- 시각 품질: 그래프 곡선 아래나 사이에 면 채움이 없고, 모든 패널이 평면 선화이며 잘림·겹침, gradient, shadow가 없다.
- 핵심 요소: A/B 패널, 각 입력 묶음, 상태 범위, 시간 궤적, 정확히 두 개의 동역학 곡선이 모두 있다.

### fig10 — Four-Axis Model Card

- 과학 관계: 중앙 모델에서 생화학적 범위, 시스템 경계, 수학적 형식, 맥락화의 네 독립 축이 동시에 연결되고 기록 띠가 별도로 연결된다.
- 텍스트: 네 축의 제목·하위 문자열과 `릴리스 · 배지 · 목적 · solver · 검증`이 중복이나 분할 없이 정확하다.
- 시각 품질: 모든 카드가 균일한 무채색 내부와 평면 윤곽선으로 구성되어 잘림·겹침, gradient, shadow, 장식성 아이콘이 없다.
- 핵심 요소: 중앙 모델 카드, 네 축 카드, 하단 기록 띠가 모두 있다.

### fig11 — Evidence Contract for Historical Claims

- 과학 관계: 원 출처, 모델 파일, 검증 계약의 세 기록이 하나의 `비교 가능한 주장`으로 모이며, `모델 이름의 숫자만` 카드는 연결되지 않은 채 X로 배제된다.
- 텍스트: A/B/C의 모든 필드와 결과·배제 라벨이 정확하며 버전 문자열, 샘플 ID, 임의 숫자·문자가 없다.
- 시각 품질: 아이콘·작은 그림 없이 평면 카드와 선만 사용했고 잘림·겹침, gradient, shadow가 없다.
- 핵심 요소: 세 기록 카드, 수렴 연결선, 결과 카드, 배제 카드가 모두 있다.

### fig12 — Historical Layers Added Over Time

- 과학 관계: 1990, 1999, 2008, 2018의 네 시점이 왼쪽에서 오른쪽으로 이어지고, 기본 제약에서 세포 규모, 조직·다세포, 군집·통합으로 층이 누적된다.
- 텍스트: 네 연도와 각 단계 라벨이 정확하며 반복 라벨, 임의 수치, 보조 설명이 없다.
- 시각 품질: 누적 층을 채움 없는 윤곽 스택으로 표현하여 잘림·겹침, gradient, shadow, 과도한 장식이 없다.
- 핵심 요소: 네 시점, 방향 화살표, 기본 층과 누적 층이 모두 있다.

### fig14 — Two-Member Community Exchange

- 과학 관계: 배지 유입은 공유 세포외 풀로 들어가고, 구성원 A의 `대사물 M 분비`는 풀로, 풀의 `대사물 M 흡수`는 구성원 B로 향하며 배출은 바깥으로 나간다.
- 텍스트: 공유 풀의 불필요한 영문 번역 없이 지정 한글·영문과 균형식, `상대 풍부도 ≠ 교환 플럭스`가 정확하며 임의 수치가 없다.
- 시각 품질: 모든 구획과 화살표가 평면 윤곽선으로 구성되어 잘림·겹침, gradient, shadow가 없다.
- 핵심 요소: 두 구성원, 공유 풀, 배지, 유입·분비·흡수·배출, 종별 생물량, 단일 군집 목적, 균형 띠가 모두 있다.

### fig16 — Diagnosing Model–Experiment Mismatch

- 과학 관계: 불일치에서 실험 조건, 교환 경계, 반응식·구획, GPR, 바이오매스·목적을 점검한 뒤 판별 근거에 따라 보류·추가 측정 또는 근거 기반 갱신으로 나뉜다. 근거 없는 반응 추가 분기는 X에서 종료되고 갱신 루프에 연결되지 않는다.
- 텍스트: 모든 진단 항목과 분기 라벨이 명세와 일치하며 `Check`, `Decision` 같은 보조 영문이나 임의 수치가 없다.
- 시각 품질: 평면 윤곽선 흐름도로 잘림·겹침, gradient, shadow, 불필요한 장식이 없다.
- 핵심 요소: 불일치 입력, 다섯 점검 항목, 판별 근거, 보류, 갱신 루프, 금지 분기가 모두 있다.
