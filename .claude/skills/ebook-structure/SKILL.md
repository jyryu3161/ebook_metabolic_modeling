---
name: ebook-structure
description: Create or restructure a chapter, section, lab, or summary in the Korean genome-scale metabolic modeling textbook, following the repository's file layout, chapter opening pattern, learning objectives, GitBook hint blocks, and SUMMARY.md navigation. Use when adding a new chapter or section, splitting/merging files, scaffolding a lab, or wiring navigation. Triggers - 장 구성, 챕터, 절 추가, 목차, 구조, 스캐폴드, chapter, section, scaffold, outline, navigation, SUMMARY, 학습목표. Do NOT use for prose wording (use ebook-prose) or QA (use ebook-review).
---

# 장·절 구조 규약

## 1. 장 디렉터리 구성

```
chapter-N/
  README.md    장 도입 — 개관, 표기 원칙, 대화형 도해
  01.md … NN.md  번호 절 (이론 본문, 다체)
  lab.md       실습 (습니다체)
  summary.md   마무리 — 요약·자가점검·용어
```

절 파일은 두 자리 연번(`01.md`, `02.md`, …)이다. 장의 절 개수는 고정이 아니다(Chapter 3은 7개, Chapter 9는 11개).

## 2. `README.md` 필수 구성

순서대로 배치한다.

1. `# Chapter N. 제목`
2. 인용 블록(`>`)으로 **이전 장과의 연결 + 이 장의 질문**
3. `## 표기와 읽기 원칙` — 이 장에서 쓰는 핵심 용어의 한국어/영어 병기와 정의, 계산 조건과 생물학적 사실의 구분
4. GitBook 경고 블록 — 예측의 조건부성 고지

   ```
   {% hint style="warning" %}
   본문의 “예측”은 명시된 모델·배지·경계조건·목적함수 아래의 계산 결과다. 실험 관찰이나 인과적 효과와 혼용하지 않는다.
   {% endhint %}
   ```

5. `## 이 장을 시작하며` — 학술적 문제 제기에서 출발
6. `## 대화형 도해: 핵심 가정과 결과 해석` — **필수**

   ```
   {% hint style="info" %}
   아래 도해는 **교육용 개념·모의 데이터**를 조작하여 … 실제 GEM 결과로 인용할 수 없으며 …
   {% endhint %}

   {% embed url="https://jyryu3161.github.io/ebook_metabolic_modeling/interactive/index.html?chapter=N" %}

   [새 창에서 대화형 도해 열기](https://jyryu3161.github.io/ebook_metabolic_modeling/interactive/index.html?chapter=N)
   ```

   `interactive/index.html?chapter=N` 링크가 없으면 [`scripts/validate_textbook.py`](../../../scripts/validate_textbook.py)가 **실패**한다. 장 번호를 반드시 맞춘다.

## 3. 학습목표

측정 가능한 동사만 쓴다: **정의한다 · 유도한다 · 비교한다 · 계산한다 · 비판적으로 평가한다**.

- ✗ `FBA를 이해한다`, `~에 대해 알아본다`
- ✓ `FBA의 세 가정을 정의하고, 장난감 LP의 최적 꼭짓점을 손으로 계산한다`

## 4. `summary.md` 구성

```markdown
# 마무리: 요약 · 스스로 점검 · 용어

## 한 장 요약
- (핵심 명제를 불릿으로. 각 항목은 조건과 한계를 포함한다)

## 스스로 점검
1. **손 계산:** …
   > **힌트:** …
2. **개념 확인:** …
3. **계산:** …
```

문제는 **정의 확인 · 손 계산 · 결과 해석 · 가정 비판**의 네 수준을 균형 있게 포함한다. 정답을 질문 바로 뒤에 그대로 노출하지 않는다(힌트는 사고 경로를 주되 결론을 대신하지 않게 쓴다).

요약의 표는 `Table S.x`로 번호를 붙인다.

## 5. 본문 블록 관례

- 조건·가정·절차 → 번호 목록
- 결과의 범위와 예외 → `해석상의 주의` 블록 (`흔한 오해`라는 이름은 쓰지 않는다)
- 주의·경고 → `{% hint style="warning" %}`, 보조 설명 → `{% hint style="info" %}`
- 확인문제는 개념 전개를 끊지 않도록 **절 말미나 장 요약**에 배치

## 6. 상호 참조

- 장 참조: `[Chapter 2](../chapter-2/README.md)`
- 용어집: `[화학량론 행렬](../glossary.md)`
- 방법 논문: `[FBA](../landmark-papers.md)`
- 보충: `[SBML 보충](../supplements/sbml-practical.md)`

## 7. 네비게이션 등록

새 장·절·보충 자료는 [`SUMMARY.md`](../../../SUMMARY.md)에 추가한다. `textbook-completeness-supplement.md` 항목이 빠지면 검증 스크립트가 실패한다. 장을 추가하면 [`README.md`](../../../README.md)의 「책의 구성」 표에도 행을 추가한다.

## 8. 작업 절차

1. 장 디렉터리와 파일을 §1대로 만든다.
2. `README.md`를 §2 순서로 채우고 `?chapter=N`을 장 번호에 맞춘다.
3. 절 파일은 다체, `lab.md`는 습니다체로 쓴다([[ebook-prose]]).
4. `summary.md`를 §4 형식으로 작성한다.
5. `SUMMARY.md`와 루트 `README.md` 표를 갱신한다.
6. `python scripts/validate_textbook.py`로 PASS를 확인한다.

관련: [[ebook-prose]] 문체, [[ebook-review]] 검수, [[ebook-figure]] 그림.
