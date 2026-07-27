# Chapter 2 Nano Banana Pro 생성·검수 보고서

## 검수 범위와 판정 기준

- 대상: `specs/ch2/fig03.json`, `fig04.json`, `fig05.json`, `fig06.json`, `fig08.json`, `fig09.json`, `fig10.json`, `fig11.json`
- 생성 크기: 모든 spec에서 `2K`
- 검수 방법: 각 최종 JPEG를 `view_image`의 원본 해상도로 한 장씩 직접 확인
- PASS 기준: 과학적 화살표·부호·계수·bounds·물질수지 관계가 맞고, 지정 문구의 철자와 수식이 정확하며, 명세 밖 텍스트·숫자·기호가 없고, 잘림·겹침·gradient·shadow·과도한 장식·핵심 패널 누락이 없음
- 재시도 수: 최초 생성 이후 `--force`로 다시 생성한 횟수이다. 탈락 출력은 최종 JPEG에 남기지 않았고 게시하지 않았다.

## 최종 결과

| 그림 | 최종 모델 | 원본 해상도 | 재시도 | 판정 |
|---|---|---:|---:|---|
| `ch2_fig03_reaction_record.jpg` | `nano-banana-pro-preview` | 2752×1536 | 3 | PASS |
| `ch2_fig04_flux_bounds.jpg` | `gemini-3-pro-image` | 2752×1536 | 5 | PASS |
| `ch2_fig05_reaction_to_column.jpg` | `nano-banana-pro-preview` | 2752×1536 | 3 | PASS |
| `ch2_fig06_matrix_balance_ledger.jpg` | `nano-banana-pro-preview` | 2400×1792 | 3 | PASS |
| `ch2_fig08_bipartite_projection.jpg` | `nano-banana-pro-preview` | 2752×1536 | 3 | PASS |
| `ch2_fig09_path_vs_balance.jpg` | `gemini-3-pro-image` | 2752×1536 | 2 | PASS |
| `ch2_fig10_metabolite_balance.jpg` | `nano-banana-pro-preview` | 2752×1536 | 3 | PASS |
| `ch2_fig11_pssa_scope.jpg` | `gemini-3-pro-image` | 2752×1536 | 2 | PASS |

## 그림별 PASS 근거

### 그림 2.3 — reaction record

- 중앙 반응식 `A + 2B → 3C`의 화살표와 계수가 정확하다.
- 반응 ID, 화학량론, 플럭스 범위, 유전자 규칙, 구획, 주석의 여섯 필드와 bounds 게이지가 모두 있다.
- 지정 한글·영문·수식 외 환각 텍스트가 없고, 모든 연결과 라벨이 잘림 없이 보인다.
- 평면 outline 표현이며 gradient, shadow, glow와 불필요한 장식이 없다.

### 그림 2.4 — stored direction and flux bounds

- 세 열 모두 저장 반응은 동일한 `A → B`이고, 양방향성은 반응 화살표가 아니라 `−10 ≤ v ≤ 10` 구간으로만 표현했다.
- 정방향 `0 ≤ v ≤ 10`, 양방향 `−10 ≤ v ≤ 10`, 정지 `v = 0`의 부호와 범위가 정확하다.
- 정지 열의 `v = 0`은 한 번만 나오고 중심 눈금 `0`과 중복되지 않으며, 저장 반응 화살표 위의 빨간 X가 있다.
- 독립 글자와 단선 화살표를 사용한 평면 구성으로 gradient, shadow, 유색 노드 내부, 잘림과 겹침이 없다.

### 그림 2.5 — reaction to matrix column

- `ATP + 포도당 → ADP + G6P + H⁺`의 방향과 모든 물질명이 정확하다.
- 반응물 ATP·포도당은 `−1`, 생성물 ADP·G6P·H⁺는 `+1`로 대응하며, `계수 기록` 화살표가 변환 방향을 분명히 한다.
- 소비·생성 범례와 다섯 행이 모두 있고 추가 텍스트·숫자·기호가 없다.
- 표와 반응식이 잘림·겹침 없이 배치되었고 gradient와 shadow가 없다.

### 그림 2.6 — matrix balance ledger

- 3×3 행렬의 값이 장난감 네트워크와 일치하고, `R2` 열은 `B → C`, `B` 행은 물질수지 읽기 방향으로 정확히 강조되었다.
- 강조식은 B 행의 계수와 같은 열 플럭스를 대응해 합하는 관계를 보존한다.
- 행·열 이름, 반응식, 행렬 원소와 배지가 모두 있으며 환각 텍스트나 핵심 패널 누락이 없다.
- 4:3 원본에서 외곽 요소가 잘리지 않고 gradient, shadow와 장식성 채움이 없다.

### 그림 2.8 — bipartite graph and projection

- 패널 A는 `A + 2B → C + D`에서 `A → R1` 가중치 1, `B → R1` 가중치 2, `R1 → C`, `R1 → D` 가중치 1을 보존한다.
- 패널 B는 투영 후 `A → C`, `A → D`, `B → C`, `B → D`의 네 간선만 남긴다.
- 반응 노드·계수·다자 관계의 손실 표지가 있고, 패널·노드·간선·라벨 누락이나 명세 밖 텍스트가 없다.
- 화살표와 라벨이 겹치거나 잘리지 않으며 gradient와 shadow가 없다.

### 그림 2.9 — path versus feasible flux

- 두 패널의 경로는 동일한 `Aₑ → B꜀ → Cₑ` 순서를 유지한다.
- 플럭스 패널에서 `R2`가 차단되고 `v2 = 0`, `v1 − v2 = 0`, `v1 = 0`의 논리 관계가 정확하며 각 식은 한 번만 표시된다.
- 경로 존재와 비영 정상상태 플럭스 부재의 대비가 명확하고 핵심 패널·화살표·부호가 빠지지 않았다.
- 텍스트 잘림·겹침, gradient, shadow와 과도한 장식이 없다.

### 그림 2.10 — metabolite balance

- 위 비교는 생성 기여 `R1: +4`, `R2: +2`와 소비 기여 `R3: −6`을 합쳐 총생성 6, 총소비 6, 순생성률 0으로 표시한다.
- 아래 비교는 총생성 6, 총소비 5, 순생성률 +1이며 풀 높이가 위의 균형 상태보다 높아 축적을 나타낸다.
- 모든 화살표 방향, 부호, 합계와 두 비교 패널이 정확하며 추가 텍스트·기호가 없다.
- 풀, 화살표와 배지가 원본 프레임 안에 있고 gradient, shadow와 장식성 채움이 없다.

### 그림 2.11 — PSSA scope

- 패널 A는 생성률 8과 소비률 8, 일정한 풀을 나타내고 패널 B는 생성률 8과 소비률 5, 시간에 따라 증가하는 세 스냅샷을 나타낸다.
- 정상상태 근사와 동적 물질수지의 적용 범위가 생성·소비 차이 및 풀 변화로 정확히 구분된다.
- 지정 라벨·숫자·시간 순서가 정확하고 핵심 스냅샷이나 화살표가 누락되지 않았다.
- 모든 요소가 잘림·겹침 없이 보이며 gradient, shadow와 과도한 장식이 없다.

## 게시 자산

PASS한 위 8개 JPEG만 `.gitbook/assets/nano/ch2/`에 같은 파일명으로 게시했다.

## 최종 검증

- `python scripts/validate_figure_coverage.py --chapter 2`: PASS — 번호가 있는 4개 절에 시각자료가 각 2개 이상이며 총 10개
- `python scripts/validate_textbook.py`: PASS — 원고 구조, 장 링크와 supplement navigation
- `git diff --check`: PASS
