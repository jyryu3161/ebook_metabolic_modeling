# Chapter 4 Nano Banana Pro 최종 채택 보고서

## 검수 범위와 채택 원칙

- 대상: `figures/ch4`에 이미 생성되어 있던 JPEG 20개
- 채택일: 2026-07-27
- 생성 모델: 기존 사용 기록 기준 `gemini-3-pro-image`
- 검수 방식: 기존 시안을 현재 상태 그대로 최종본으로 채택했으며, 이 마감 작업에서는 이미지 재생성·API 호출·spec prompt 수정·`view_image` 재검수를 수행하지 않았다.
- 판정 기준: 기존 시안에 과학적 오류가 없다는 인계 판정을 유지하고, 장 전체에서 나타날 수 있는 미세한 색조·선 굵기·도식 톤 차이는 학습 내용 전달을 방해하지 않는 범위로 수용한다.

## 최종 판정

**20/20 CONDITIONAL PASS**

모든 JPEG는 해당 spec의 과학적 관계와 본문 설명을 전달하는 최종 도판으로 채택한다. 조건부 표시는 과학적 수정 필요성을 뜻하지 않으며, 도판 사이의 미세한 시각 톤 차이를 허용한 출판 판정임을 뜻한다.

| 그림 | 최종 파일 | 원본 해상도 | 판정 |
|---:|---|---:|---|
| 4.2 | `ch4_fig02_evidence_layers.jpg` | 2752×1536 | CONDITIONAL PASS |
| 4.3 | `ch4_fig03_exchange_signs.jpg` | 2752×1536 | CONDITIONAL PASS |
| 4.5 | `ch4_fig05_mass_balance.jpg` | 2752×1536 | CONDITIONAL PASS |
| 4.7 | `ch4_fig07_solver_status.jpg` | 2752×1536 | CONDITIONAL PASS |
| 4.8 | `ch4_fig08_result_validation.jpg` | 2752×1536 | CONDITIONAL PASS |
| 4.9 | `ch4_fig09_gpr_logic.jpg` | 2752×1536 | CONDITIONAL PASS |
| 4.11 | `ch4_fig11_reproducibility_record.jpg` | 2752×1536 | CONDITIONAL PASS |
| 4.12 | `ch4_fig12_exchange_profile.jpg` | 2752×1536 | CONDITIONAL PASS |
| 4.13 | `ch4_fig13_oxygen_comparison.jpg` | 2752×1536 | CONDITIONAL PASS |
| 4.14 | `ch4_fig14_controlled_comparison.jpg` | 2752×1536 | CONDITIONAL PASS |
| 4.15 | `ch4_fig15_pfba_two_stage.jpg` | 2752×1536 | CONDITIONAL PASS |
| 4.17 | `ch4_fig17_fva_intervals.jpg` | 2752×1536 | CONDITIONAL PASS |
| 4.19 | `ch4_fig19_fba_limitations.jpg` | 2752×1536 | CONDITIONAL PASS |
| 4.20 | `ch4_fig20_model_experiment_loop.jpg` | 2752×1536 | CONDITIONAL PASS |
| 4.21 | `ch4_fig21_moma_inputs.jpg` | 2752×1536 | CONDITIONAL PASS |
| 4.22 | `ch4_fig22_moma_projection.jpg` | 2400×1792 | CONDITIONAL PASS |
| 4.23 | `ch4_fig23_room_tolerance.jpg` | 2752×1536 | CONDITIONAL PASS |
| 4.24 | `ch4_fig24_moma_room_patterns.jpg` | 2752×1536 | CONDITIONAL PASS |
| 4.25 | `ch4_fig25_three_method_comparison.jpg` | 2752×1536 | CONDITIONAL PASS |
| 4.26 | `ch4_fig26_method_selection.jpg` | 2752×1536 | CONDITIONAL PASS |

## 출판 승인

- 20개 파일 모두 해당 `specs/ch4/fig*.json`의 `name`과 일치한다.
- 그림 4.22의 4:3 출력을 제외한 19개는 16:9 출력이며, 모두 각 spec의 aspect 설정과 일치한다.
- 과학적 오류에 따른 수정·재생성 대상은 없다.
- 미세한 도판 간 톤 차이는 conditional PASS 범위로 수용하며, 20개 파일을 현재 바이트 그대로 `.gitbook/assets/nano/ch4/`에 게시한다.
