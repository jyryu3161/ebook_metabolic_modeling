# Chapter 5 Nano Banana Pro 이미지 QA 보고서

- 검수일: 2026-07-27
- 생성 모델: `gemini-3-pro-image`
- 검수 방법: 생성된 JPEG 7개를 각각 원본 해상도(`2752 × 1536`)로 열어 직접 확인했다.
- 판정 기준: 과학적 화살표·부호·관계, 명세에 지정된 한글·영문, 명세 외 텍스트·숫자·기호, 잘림·겹침, gradient·shadow, 핵심 패널 누락 여부를 모두 점검했다.
- 게시 기준: 아래 최종본은 모두 PASS이며, 실패한 중간 생성물은 게시 대상에서 제외했다.

| Spec | 최종 파일 | 모델 | 해상도 | 재시도 | PASS 근거 |
|---|---|---|---:|---:|---|
| `fig03.json` | `ch5_fig03_validation_data_split.jpg` | `gemini-3-pro-image` | 2752 × 1536 | 6회 | 조건별 표현형 자료가 구축·큐레이션 자료와 독립 hold-out으로 분기되고, 내부 시험은 별도 경로로 출력에 연결된다. 붉은 점선 leakage 경로가 붉은 X에서 차단되며, 지정 문구 외 텍스트가 없고 잘림·겹침·gradient·shadow가 없다. |
| `fig06.json` | `ch5_fig06_reaction_curation_record.jpg` | `gemini-3-pro-image` | 2752 × 1536 | 1회 | 중앙 반응 `A + B → C`에 ID, 화학량론, 방향성, 구획, GPR, DOI, confidence, 변경 이력의 여덟 기록 필드가 연결되고 include·hold·exclude·unresolved 상태가 모두 보인다. 지정 문구 외 텍스트와 불필요한 카드가 없고 잘림·겹침·gradient·shadow가 없다. |
| `fig07.json` | `ch5_fig07_function_failure_diagnosis.jpg` | `gemini-3-pro-image` | 2752 × 1536 | 0회 | 실패에서 A–E 진단 단계를 순서대로 거쳐 gap-filling 가설과 독립 검증으로 이동하며, A–D에는 수정 후 재시험 회귀가 표시된다. 단계·화살표·문구가 명세와 일치하고 잘림·겹침·gradient·shadow가 없다. |
| `fig09.json` | `ch5_fig09_automated_draft_layers.jpg` | `gemini-3-pro-image` | 2752 × 1536 | 4회 | 후보 반응 지식베이스에서 서열 지지 초안, gap-filling 가설이 포함된 배지별 초안으로 이어지는 세 패널과 패널 사이 화살표가 모두 있다. provenance 행의 DB release·입력 checksum·도구·solver·배지·과제만 표기되며 잘림·겹침·gradient·shadow가 없다. |
| `fig11.json` | `ch5_fig11_gapfill_alternative_hypotheses.jpg` | `gemini-3-pro-image` | 2752 × 1536 | 1회 | 끊어진 `A → B → C → D` 경로에 두 반응짜리 총 비용 2 해와 직접 반응 비용 5 해가 대안으로 제시되고, 두 해 모두 공통의 세 검토 관문과 열린 판정 상태로 이어진다. 비용 관계와 화살표가 정확하며 지정 외 문구, 잘림·겹침·gradient·shadow가 없다. |
| `fig12.json` | `ch5_fig12_quality_control_questions.jpg` | `gemini-3-pro-image` | 2752 × 1536 | 2회 | A–D 패널이 반응 균형, 화학량론적 일관성, flux consistency, energy-cycle test를 각각 나타내고 B·D에만 붉은 X가 있다. 하단 독립 표현형 검증은 내부 검사와 분리되어 있으며 원소 문자나 Energy 같은 명세 외 표기, 잘림·겹침·gradient·shadow가 없다. |
| `fig13.json` | `ch5_fig13_release_bundle.jpg` | `gemini-3-pro-image` | 2752 × 1536 | 0회 | GEM release 폴더에 SBML+checksum부터 license·변경 이력까지 여덟 산출물이 모두 있고, 재실행과 해석 범위 확인으로 분기된다. `model.xml만`은 붉은 X로 격리되며 지정 외 문구, 잘림·겹침·gradient·shadow가 없다. |

## 최종 판정

7개 최종 이미지 모두 원본 해상도 직접 검수에서 PASS했다. 게시에는 위 표의 최종 파일만 사용한다.
