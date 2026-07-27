# Chapter 11 그림 최종 QA 보고서

## 최종 판정

**조건부 PASS — 현재 JPEG 5개를 재생성 없이 최종본으로 채택한다.**

기존 과학·시각 검수 결과를 인수한 결과, 재현 가능한 실행 기록의 구성 요소, GLPK·Gurobi의 LP·QP·MILP 지원 관계, 교환 반응의 음수 흡수·양수 분비 부호, pFBA·FVA가 답하는 질문의 차이, CarveMe 초안 생성과 별도 품질 검증의 흐름에서 과학적 오류가 보고되지 않았다. 그림 사이에 채도·명암과 배경 온도의 미세한 톤 차이가 있으나 개념 전달, 라벨 판독과 장 전역의 시각적 일관성을 훼손하지 않는 비본질적 편차이므로 조건부 PASS로 기록한다.

본 마감에서는 기존 판정을 존중해 `figures/ch11`의 JPEG를 다시 열어 반복 검수하지 않았고, 이미지 생성·API 호출·재생성, `gen_one.py` 실행 및 spec prompt 수정도 수행하지 않았다. 아래 SHA-256은 채택한 현재 파일의 동일성을 고정하기 위한 기록이다.

## 자산별 판정

모든 파일은 JPEG, 2752×1536 px, 300 DPI이다.

| 그림 | 파일 | 과학 검수 | 시각 검수 | 최종 판정 | SHA-256 |
|:---:|:---|:---:|:---|:---:|:---|
| 11.2 | `ch11_fig02_reproducible_run_record.jpg` | 오류 없음 | 미세 톤 차이 허용 | 조건부 PASS | `5dc81a7d060e861645378a45b2b1f5abb6eff0122e0fdc11df6b1f9d151b5880` |
| 11.3 | `ch11_fig03_solver_capability_choice.jpg` | 오류 없음 | 미세 톤 차이 허용 | 조건부 PASS | `4c963a4654b3a29fad47facea140d6b67a60c442114c07c4ab49c0cb11ebccd1` |
| 11.5 | `ch11_fig05_exchange_flux_signs.jpg` | 오류 없음 | 미세 톤 차이 허용 | 조건부 PASS | `500cfac85da97dbbfa2dda16547f5ea77208ece4ae3d9eb0f0bb4f6dc1265470` |
| 11.7 | `ch11_fig07_pfba_fva_questions.jpg` | 오류 없음 | 미세 톤 차이 허용 | 조건부 PASS | `4866137f24646754ae67ebb04929569c86d079392f3bfd7ee5b0bcebc461505b` |
| 11.11 | `ch11_fig11_carveme_draft_to_validation.jpg` | 오류 없음 | 미세 톤 차이 허용 | 조건부 PASS | `d857fa240c91d44087fcbd8e143935145139635f2683c2e22a0ec73ab85e0f9c` |

## 출판 조건

- 본문에는 `specs/ch11/_placement.md`의 위치·대체 텍스트·자립 캡션을 사용한다.
- 기존 Mermaid 1개, 기존 계산 그림 10개와 신규 JPEG 5개를 합쳐 그림 11.1–11.16을 결번·중복 없이 배치한다.
- 미세 톤 차이는 허용된 잔여 조건이며 재생성 조건으로 사용하지 않는다.
- 게시본은 원본과 같은 파일 내용인지 SHA-256으로 확인한다.

## 마감 검증

- 원본 5개와 `.gitbook/assets/nano/ch11/` 게시본 5개의 SHA-256 일치
- `python scripts/validate_figure_coverage.py --chapter 11` — PASS, 본절 7개에 그림 15개
- `python scripts/validate_textbook.py` — PASS
- `git diff --check -- chapter-11 figures/ch11 specs/ch11 .gitbook/assets/nano/ch11` — PASS
