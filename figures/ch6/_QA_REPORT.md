# Chapter 6 그림 최종 QA 보고서

## 최종 판정

**조건부 PASS — 현재 JPEG 12개를 재생성 없이 최종본으로 채택한다.**

기존 과학·시각 검수 결과를 인수한 결과, 반응 방향, GPR의 AND·OR 및 min·max 해석, 임계값 분류, 방법별 제약 의미, TPM 정규화 순서, RNA-seq 관측 단위와 다중 오믹스 충돌 분류에서 과학적 오류가 보고되지 않았다. 그림 사이에 채도·명암과 배경 온도의 미세한 톤 차이가 있으나 개념 전달, 라벨 판독과 장 전역의 시각적 일관성을 훼손하지 않는 비본질적 편차이므로 조건부 PASS로 기록한다.

본 마감에서는 기존 판정을 존중해 `figures/ch6`의 JPEG를 다시 열어 반복 검수하지 않았고, 이미지 생성·API 호출·재생성 및 spec prompt 수정도 수행하지 않았다. 아래 SHA-256은 채택한 현재 파일의 동일성을 고정하기 위한 기록이다.

## 자산별 판정

모든 파일은 JPEG, 2752×1536 px, 300 DPI이다.

| 그림 | 파일 | 과학 검수 | 시각 검수 | 최종 판정 | SHA-256 |
|:---:|:---|:---:|:---|:---:|:---|
| 6.2 | `ch6_fig02_evidence_decision_ledger.jpg` | 오류 없음 | 미세 톤 차이 허용 | 조건부 PASS | `0f943fa3057bacfe2d4232a45f5b30393f3b9607689f7123cf9de86529f9dc90` |
| 6.4 | `ch6_fig04_release_identity.jpg` | 오류 없음 | 미세 톤 차이 허용 | 조건부 PASS | `7af1f9509da0ba8dd5d22801720fbfe5438bc035e2c0a41ae386da8d9a086d97` |
| 6.6 | `ch6_fig06_curation_assurance_layers.jpg` | 오류 없음 | 미세 톤 차이 허용 | 조건부 PASS | `25a60e91665f73deedd613ac3ff0fd9d9daa9ccc711822b5ade445d5ddbcf647` |
| 6.8 | `ch6_fig08_generic_to_context_choices.jpg` | 오류 없음 | 미세 톤 차이 허용 | 조건부 PASS | `98eba4e03e9d2faa999bdc5f94264cfcb1af6ab088c86103c5afa25a71c44b1a` |
| 6.10 | `ch6_fig10_task_protected_path.jpg` | 오류 없음 | 미세 톤 차이 허용 | 조건부 PASS | `7009a589f8f928ab0186065e051f40db85ecc72e857468af032b72c8bce00fb5` |
| 6.11 | `ch6_fig11_gpr_ras_logic.jpg` | 오류 없음 | 미세 톤 차이 허용 | 조건부 PASS | `bbd4317622c351288dcc0e7dd8608290a90035915f4d2675755cc35f70445cad` |
| 6.12 | `ch6_fig12_threshold_sensitivity.jpg` | 오류 없음 | 미세 톤 차이 허용 | 조건부 PASS | `cc3ddb3a773d0fad98e5a00357b5aaf100c8c2372c65058b9ab4188ec647f09b` |
| 6.13 | `ch6_fig13_four_method_translation.jpg` | 오류 없음 | 미세 톤 차이 허용 | 조건부 PASS | `b9ed27509a76d7e6a256775ed81528a756b27876fe9fc582014a5ea081cae61e` |
| 6.14 | `ch6_fig14_method_selection_tree.jpg` | 오류 없음 | 미세 톤 차이 허용 | 조건부 PASS | `289e6f3220e46d6e07f294cee8f7b54e67ac176a627a3035d1a1665c07aabf37` |
| 6.15 | `ch6_fig15_counts_to_tpm.jpg` | 오류 없음 | 미세 톤 차이 허용 | 조건부 PASS | `103e8ca6dfbfeaab0695538baac439a1527cba60d926db899fe6974ecbce82f9` |
| 6.16 | `ch6_fig16_rnaseq_observation_units.jpg` | 오류 없음 | 미세 톤 차이 허용 | 조건부 PASS | `a2e771611d62ad755148ba9734381dfcd98fd8931c1d308773c19dab9cdd31d4` |
| 6.18 | `ch6_fig18_multiomics_conflict_matrix.jpg` | 오류 없음 | 미세 톤 차이 허용 | 조건부 PASS | `ff2eb440e68f577b2d86be6eee4ddb44277b9c9b3f9fd930162ed9603dd0e88e` |

## 출판 조건

- 본문에는 `specs/ch6/_placement.md`의 위치·대체 텍스트·자립 캡션을 사용한다.
- 기존 Mermaid 6개와 신규 JPEG 12개를 합쳐 그림 6.1–6.18을 결번·중복 없이 배치한다.
- 미세 톤 차이는 허용된 잔여 조건이며 재생성 조건으로 사용하지 않는다.
- 게시본은 원본과 같은 파일 내용인지 SHA-256으로 확인한다.

## 마감 검증

- 원본 12개와 `.gitbook/assets/nano/ch6/` 게시본 12개의 SHA-256 일치
- `python scripts/validate_figure_coverage.py --chapter 6` — PASS, 본절 9개에 그림 18개
- `python scripts/validate_textbook.py` — PASS
- `git diff --check -- chapter-6 figures/ch6 specs/ch6 .gitbook/assets/nano/ch6` — PASS
