---
name: ebook-figure
description: Create, regenerate, or caption figures for the Korean genome-scale metabolic modeling textbook, following the repository's matplotlib generation pipeline, asset paths, caption format, and figure-ledger requirements. Use when adding a new figure, rebuilding existing assets, writing or fixing a caption, or drawing a Mermaid schematic. Triggers - 그림, 그림 생성, 도식, 캡션, figure, diagram, plot, mermaid, 자산, assets, 그래프. Do NOT use for prose style (use ebook-prose) or license/rights research (use ebook-citation).
---

# 그림 제작·캡션 규약

정본 기준: [`docs/textbook-editorial-standard.md`](../../../docs/textbook-editorial-standard.md) §3, 권리 장부는 [`FIGURE_SOURCES.md`](../../../FIGURE_SOURCES.md).

## 1. 그림의 두 종류 — 반드시 구분

| 종류 | 정의 | 캡션에 명시할 것 |
|---|---|---|
| **모식도** | 본문 수식·좌표에서 직접 그림. solver·GEM 미사용 | "…교육용 기하 도식이며 solver나 실제 GEM 계산을 투영한 결과가 아니다." |
| **계산 그림** | 실제 모델을 solver로 풀어 얻은 결과 | 모델 ID·버전, 배지·경계조건, 목적함수, solver, 허용오차 |

이 구분을 캡션에서 생략하면 안 된다. 모식도를 계산 결과처럼 읽히게 두는 것이 이 교재에서 가장 경계하는 오류다.

## 2. 생성 파이프라인

계산·기하 그림은 [`scripts/generate_optimization_figures.py`](../../../scripts/generate_optimization_figures.py) 한 파일에 모은다. 새 그림은 이 스크립트에 `draw_*()` 함수로 추가하고 `main()`에 등록한다.

```bash
python scripts/generate_optimization_figures.py
```

스크립트가 고정하는 규약을 그대로 따른다:

- 백엔드 `matplotlib.use("Agg")`
- 팔레트 — `BLUE #2563EB`, `ORANGE #EA580C`, `GREEN #059669`, `PURPLE #7C3AED`, `GRAY #64748B`, `LIGHT_BLUE #DBEAFE`, `LIGHT_ORANGE #FFEDD5`
- `rcParams`: `figure.dpi 140`, `savefig.dpi 180`, `font.size 10`, `axes.titlesize 12`, `axes.labelsize 10`, `legend.fontsize 8`, `svg.hashsalt "gem-ebook-figures"`
- 저장은 반드시 공용 `save(fig, stem)` 사용 — 투명 SVG + 흰 배경 PNG를 함께 쓰고, SVG 줄 끝 공백을 제거해 `git diff --check`가 깨끗하게 유지된다

계산 그림은 COBRApy 0.30.0 `cobra.io.load_model("textbook")`(BiGG `e_coli_core`, 대사물 72·반응 95·유전자 137), 모델 기본 배지와 biomass 목적함수, GLPK, `Configuration().processes = 1`을 기준 환경으로 한다.

## 3. 자산 경로 — 2단 구조

```
assets/figures/<stem>.png   ← 생성 출력(PNG)
assets/figures/<stem>.svg   ← 생성 출력(SVG, 벡터 원본)
.gitbook/assets/<stem>.png  ← 본문이 참조하는 PNG 사본
```

스크립트는 `assets/figures/`에만 쓴다. 새 그림을 추가하거나 재생성한 뒤 **PNG를 `.gitbook/assets/`로 복사하는 단계를 잊지 말 것.**

```bash
cp assets/figures/<stem>.png .gitbook/assets/<stem>.png
```

본문에서의 참조는 항상 `.gitbook/assets` 기준 상대경로다: `../.gitbook/assets/<stem>.png`

## 4. 캡션 형식

```markdown
![축·대상·핵심 구조를 서술한 대체 텍스트](../.gitbook/assets/lp-feasible-region.png)

_그림 4.3:_ 가로축은 $$v_1$$, 세로축은 $$v_2$$이며 … 본 절의 수치로 생성한 2변수 교육용 기하 도식이며 solver나 실제 GEM 계산을 투영한 결과가 아니다. 저자 작성; 개념 근거: [Cottle (2004), pp. 41–42](https://web.stanford.edu/class/msande311/000311.pdf).
```

규칙:

- 이미지 다음에 **빈 줄**, 그 다음 `_그림 N.x:_ `(이탤릭 라벨). 번호는 **장 기준 전역 연번**(그림 4.1, 4.2, …).
- 대체 텍스트에는 그림 번호를 넣지 않는다. 축·대상·핵심 구조를 서술한다.
- 캡션은 **자립적**이어야 한다. 캡션만 읽고 대상·축·기호·조건·핵심 해석이 파악되어야 한다.
- 캡션 끝에 출처를 붙인다. 자체 제작도 예외 없이 개념 근거를 인용한다 — `저자 작성; 개념 근거: [저자 (연도)](DOI)`.
- 계산 그림은 `출처: 저자 계산; 생성: [scripts/generate_optimization_figures.py](...)의 draw_xxx(); 조건: COBRApy 0.30.0, e_coli_core, GLPK, …` 형식으로 생성 함수와 조건을 밝힌다.
- 표 캡션은 `Table N.x`, 장 요약의 표는 `Table S.x`를 쓴다.

## 5. Mermaid 도식

Chapter 1·5·8–10의 흐름도는 Mermaid로 직접 작성한다. 외부 논문 그림을 트레이싱·재구성하지 않고 개념만 인용해 새로 그리는 것이 이 교재의 원칙이다. Mermaid 도식도 캡션과 출처 표기 대상이며 `FIGURE_SOURCES.md`에 등록한다.

## 6. 장부 등록 — 생략 불가

새 그림·재생성 그림은 [`FIGURE_SOURCES.md`](../../../FIGURE_SOURCES.md)의 표에 행을 추가하거나 갱신한다. 필수 열:

`ID` · `자산 파일` · `최초·재사용 위치` · `제작·생성 조건` · `개념·데이터 원출처` · `권리 상태` · `검증일`

권리 문구를 판단할 때는 [[ebook-citation]]을 따른다. 특히 **CC BY-NC-ND 문헌의 그림은 번역·트레이싱·재구성 모두 금지**이며 사실·방법 인용만 허용된다.

## 7. 작업 절차

1. 그림이 모식도인지 계산 그림인지 먼저 결정한다.
2. `generate_optimization_figures.py`에 `draw_*()`를 추가하고 `save()`로 저장한다.
3. 스크립트를 실행하고 PNG를 `.gitbook/assets/`로 복사한다.
4. §4 형식으로 캡션을 쓴다 — 자립성과 모식도/계산 구분을 점검한다.
5. `FIGURE_SOURCES.md`에 등록하고 검증일을 적는다.
6. `python scripts/validate_textbook.py`로 구조 검사를 통과시킨다.

관련: [[ebook-citation]] 권리·출처, [[ebook-prose]] 캡션 문체, [[ebook-review]] 최종 검수.
