# Chapter 10 그림 최종 QA 보고서

검수일: 2026-07-27
검수 범위: `specs/ch10/fig*.json`, `figures/ch10/*.jpg`, `.gitbook/assets/nano/ch10/*.jpg`
최종 판정: **PASS 1개, 조건부 PASS 25개**

## 마감 원칙

- `figures/ch10/_attempts/attempt1/`의 최초본 26개를 먼저 `figures/ch10/`에 복원했다.
- 그림 10.16을 제외한 최초본 25개는 기존 과학 검수 결과를 그대로 채택했다. 재생성·반복 시각 검수를 하지 않았으며, 배경 온도·채도·명암의 미세한 톤 차이는 개념 전달과 판독을 훼손하지 않는 잔여 조건으로 보고 **조건부 PASS**했다.
- 모든 spec에서 일괄 추가되었던 `SECOND ATTEMPT CORRECTION` 문단을 제거했다.
- 그림 10.16은 같은 모델·기본 배지에서 결손 전 WT flux를 먼저 계산하고, 이 참조를 MOMA와 ROOM에만 넣으며, 별도의 `tpiA` 결손 mutant를 FBA·MOMA·ROOM 모두에 넣는 구조로 spec을 수정했다.
- 최초 단일 생성본은 WT 참조 화살표가 ROOM에만 연결되어 과학 검수에서 탈락했다. coordinator의 명시적 예외 승인으로 prompt를 강화해 마지막 1회 추가 생성했으며, 최종본에서 WT→MOMA/ROOM의 얇은 직접 화살표 2개와 mutant→FBA/MOMA/ROOM의 굵은 직접 화살표 3개가 분리되어 있음을 확인했다.

## 자산별 판정

모든 최종 파일은 JPEG, 2752×1536 px, 300 DPI 메타데이터를 갖는다.

| 그림 | 파일 | 과학 판정 | 시각 조건 | 최종 판정 |
|:---:|:---|:---:|:---|:---:|
| 10.2 | `ch10_fig02_notebook_cell_contracts.jpg` | 기존 검수 채택 | 미세 톤 차이 허용 | 조건부 PASS |
| 10.3 | `ch10_fig03_unexpected_output_diagnosis.jpg` | 기존 검수 채택 | 미세 톤 차이 허용 | 조건부 PASS |
| 10.4 | `ch10_fig04_preflight_environment_contract.jpg` | 기존 검수 채택 | 미세 톤 차이 허용 | 조건부 PASS |
| 10.5 | `ch10_fig05_textbook_to_user_sbml.jpg` | 기존 검수 채택 | 미세 톤 차이 허용 | 조건부 PASS |
| 10.6 | `ch10_fig06_cobrapy_object_connections.jpg` | 기존 검수 채택 | 미세 톤 차이 허용 | 조건부 PASS |
| 10.7 | `ch10_fig07_exchange_bounds_and_medium.jpg` | 기존 검수 채택 | 미세 톤 차이 허용 | 조건부 PASS |
| 10.8 | `ch10_fig08_fba_input_code_output.jpg` | 기존 검수 채택 | 미세 톤 차이 허용 | 조건부 PASS |
| 10.9 | `ch10_fig09_mass_balance_residual.jpg` | 기존 검수 채택 | 미세 톤 차이 허용 | 조건부 PASS |
| 10.10 | `ch10_fig10_context_manager_restore.jpg` | 기존 검수 채택 | 미세 톤 차이 허용 | 조건부 PASS |
| 10.11 | `ch10_fig11_objective_switch_outputs.jpg` | 기존 검수 채택 | 미세 톤 차이 허용 | 조건부 PASS |
| 10.12 | `ch10_fig12_pfba_two_stage_readout.jpg` | 기존 검수 채택 | 미세 톤 차이 허용 | 조건부 PASS |
| 10.13 | `ch10_fig13_fva_independent_ranges.jpg` | 기존 검수 채택 | 미세 톤 차이 허용 | 조건부 PASS |
| 10.14 | `ch10_fig14_gene_deletion_pipeline.jpg` | 기존 검수 채택 | 미세 톤 차이 허용 | 조건부 PASS |
| 10.15 | `ch10_fig15_status_aware_nonfinite_policy.jpg` | 기존 검수 채택 | 미세 톤 차이 허용 | 조건부 PASS |
| 10.16 | `ch10_fig16_tpia_three_method_inputs.jpg` | WT 참조·mutant 입력 분리 확인 | 잘림·겹침·오탈자 없음 | PASS |
| 10.17 | `ch10_fig17_method_objective_vs_growth.jpg` | 기존 검수 채택 | 미세 톤 차이 허용 | 조건부 PASS |
| 10.19 | `ch10_fig19_gapfill_before_candidate_after.jpg` | 기존 검수 채택 | 미세 톤 차이 허용 | 조건부 PASS |
| 10.20 | `ch10_fig20_gapfill_evidence_gate.jpg` | 기존 검수 채택 | 미세 톤 차이 허용 | 조건부 PASS |
| 10.22 | `ch10_fig22_production_envelope_reading.jpg` | 기존 검수 채택 | 미세 톤 차이 허용 | 조건부 PASS |
| 10.24 | `ch10_fig24_widget_explore_then_record.jpg` | 기존 검수 채택 | 미세 톤 차이 허용 | 조건부 PASS |
| 10.25 | `ch10_fig25_sbml_roundtrip_checks.jpg` | 기존 검수 채택 | 미세 톤 차이 허용 | 조건부 PASS |
| 10.26 | `ch10_fig26_checksum_vs_model_meaning.jpg` | 기존 검수 채택 | 미세 톤 차이 허용 | 조건부 PASS |
| 10.27 | `ch10_fig27_provenance_json_layers.jpg` | 기존 검수 채택 | 미세 톤 차이 허용 | 조건부 PASS |
| 10.28 | `ch10_fig28_reproducibility_handoff.jpg` | 기존 검수 채택 | 미세 톤 차이 허용 | 조건부 PASS |
| 10.29 | `ch10_fig29_mini_project_workflow.jpg` | 기존 검수 채택 | 미세 톤 차이 허용 | 조건부 PASS |
| 10.30 | `ch10_fig30_final_evidence_chain.jpg` | 기존 검수 채택 | 미세 톤 차이 허용 | 조건부 PASS |

## 동일성·출판 확인

- 최초본 25개는 `figures/ch10/_attempts/attempt1/`의 대응 JPEG와 SHA-256이 일치한다.
- 그림 10.16 최종 SHA-256: `a4315c476a628c3540d81756cf9d30646933364e7109d57bd03c7b884c1763c9`
- 원본 26개와 `.gitbook/assets/nano/ch10/` 게시본 26개의 파일별 SHA-256이 모두 일치한다.
- 본문에는 그림 10.1–10.30이 결번·중복 없이 순서대로 배치되며, 신규 JPEG 26개 링크와 각 대체 텍스트·자립 캡션이 포함된다.

## 마감 검증

- `python scripts/validate_figure_coverage.py --chapter 10` — PASS, 15개 번호 절에 시각화 31개
- `python scripts/validate_textbook.py` — PASS
- `git diff --check -- chapter-10 specs/ch10 figures/ch10 .gitbook/assets/nano/ch10` — PASS
