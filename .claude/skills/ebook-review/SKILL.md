---
name: ebook-review
description: Proofread and QA a manuscript file or chapter of the Korean genome-scale metabolic modeling textbook against the editorial standard, running mechanical checks for mixed sentence endings, banned expressions, unconditioned claims, missing citations, and structural validation. Use before committing a chapter, after drafting or importing content, or when asked to check/verify/review the manuscript. Triggers - 검수, 교정, 검토, 점검, 확인, 리뷰, 품질, review, proofread, QA, check, verify, lint. Do NOT use for writing new prose (use ebook-prose) or creating figures (use ebook-figure).
---

# 원고 검수 절차

정본 기준: [`docs/textbook-editorial-standard.md`](../../../docs/textbook-editorial-standard.md) 전체. 이 스킬은 그 기준을 기계 검사 + 판독 검사로 나누어 실행한다.

## 0. 검수 범위 확정

대상 파일 목록을 먼저 확정한다. 장 단위 검수라면 `chapter-N/` 전체(`README.md`, `01.md`~`NN.md`, `lab.md`, `summary.md`).

## 1. 기계 검사 — 먼저 돌린다

### 1-1. 구조 검증

```bash
python scripts/validate_textbook.py
```

백슬래시가 빠진 `\qquad`·`\left\{` 이스케이프 오류, `SUMMARY.md`의 보충자료 링크, 10개 장 README의 대화형 도해 링크를 검사한다. **PASS가 아니면 다른 검수를 진행하지 않는다.**

> 이 스크립트는 저장소의 모든 `*.md`를 훑으므로 `.claude/skills/`의 문서도 검사 대상이다. 스킬 문서에서 이스케이프 예시를 들 때는 반드시 백슬래시를 붙여 쓴다.

### 1-2. 종결 어미 혼용

이론 본문(`README.md`, 번호 절)은 다체, 실습(`lab.md`, `chapter-10/*`, `chapter-11/*`)은 습니다체다. 한 파일 안에 섞이면 위반이다.

```bash
# 이론 본문에 습니다체가 섞였는지
rg -n "(습니다|입니다)\." chapter-*/README.md chapter-*/0*.md chapter-*/1*.md 2>/dev/null | rg -v "chapter-1[01]/"

# 실습 파일에 다체가 섞였는지
rg -n "(한다|이다|된다)\." chapter-*/lab.md chapter-10/*.md chapter-11/*.md 2>/dev/null
```

인용문·표 안의 문장은 예외일 수 있으므로 히트는 눈으로 확인한다.

### 1-3. 금지 표현

```bash
rg -n "여러분|기억하십시오|왜 이걸 배우나요|아주 쉬운 비유|흔한 오해" chapter-*/ supplements/ 2>/dev/null
rg -n "^#{1,6} .*(할까요|일까요|하는가)\?" chapter-*/ 2>/dev/null   # 수사적 질문형 제목
rg -n "[\x{1F300}-\x{1FAFF}\x{2600}-\x{27BF}]" chapter-*/ 2>/dev/null  # 이모지
```

`흔한 오해`는 `해석상의 주의`로 교체한다.

### 1-4. 조건 없는 정량 진술

수치가 나오는 줄을 뽑아 모델·배지·목적함수·solver 조건이 함께 적혔는지 확인한다.

```bash
rg -n "[0-9]+\.[0-9]+\s*(h\$\$\^\{-1\}\$\$|h⁻¹|mmol)" chapter-*/ 2>/dev/null
```

## 2. 판독 검사 — 사람이 읽어야 하는 항목

기계로 못 잡는다. 항목마다 위반 위치를 `파일:줄` 로 기록한다.

**서술 (§1)**
- [ ] 절이 학술적 문제·정의·분석 범위로 시작하는가 (동기 부여 훅으로 시작하지 않는가)
- [ ] 핵심 주장이 `정의 → 가정 → 수식/근거 → 해석 범위와 한계` 순인가
- [ ] 비유를 썼다면 **성립하지 않는 지점**을 함께 밝혔는가
- [ ] 소제목이 서술형 명제인가

**개념·수치 (§2)**
- [ ] 새 용어가 처음 등장할 때만 영어·약어를 병기하고 이후 표기가 일관되는가
- [ ] 수식에 기호 정의·단위·적용 가정이 붙었는가
- [ ] 반응·대사물·유전자 수가 **모델 릴리스의 속성**으로 기록되었는가 (종의 고정 특성으로 쓰지 않았는가)
- [ ] 예측 / 실험 관찰 / 저자 해석이 구분되는가
- [ ] 단일 연구·단일 조건 결과를 일반 법칙으로 확장하지 않았는가

**그림·표 (§3)** — 상세는 [[ebook-figure]]
- [ ] 모든 주요 그림에 번호와 **자립적** 캡션이 있는가
- [ ] 모식도와 계산 그림이 캡션에서 명시적으로 구분되는가
- [ ] 계산 그림에 생성 스크립트와 계산 조건이 있는가
- [ ] `FIGURE_SOURCES.md`에 등록·갱신되었는가

**인용 (§4)** — 상세는 [[ebook-citation]]
- [ ] 정량값·최초성·성능 비교·임상 효과에 일차 문헌이 붙었는가
- [ ] 링크가 DOI/PMC/공식 저장소인가
- [ ] 논문 결론보다 강한 표현이 없는가

**학습 요소 (§5)**
- [ ] 학습목표가 측정 가능한 동사(정의한다·유도한다·비교한다·계산한다·비판적으로 평가한다)인가
- [ ] 확인문제가 개념 전개를 끊지 않고 절 말미나 장 요약에 있는가
- [ ] 연습문제가 정의 확인·손 계산·결과 해석·가정 비판의 네 수준을 포함하는가

## 3. 보고 형식

발견 항목을 심각도 순으로 정리한다. 추측이 아니라 **위치와 근거**를 적는다.

```
[치명] chapter-7/03.md:112 — "대장균의 성장률은 0.9 h⁻¹이다"
        모델·배지·목적함수 조건 없이 단정. §2 위반.
        → "…모델의 기본 배지와 biomass 목적함수를 GLPK로 풀면 …" 으로 조건 명시

[경미] chapter-7/README.md:24 — 소제목 "왜 암 대사를 모델링하는가?"
        수사적 질문형 제목. §1 위반. → 서술형 명제로 교체
```

수정까지 요청받은 경우에만 고친다. 검수 요청이면 보고에서 멈춘다.

## 4. 마무리

수정했다면 `python scripts/validate_textbook.py`를 다시 돌려 PASS를 확인하고, 어미·금지 표현 검사를 재실행한다.

관련: [[ebook-prose]] 문체 수정, [[ebook-figure]] 그림 검수, [[ebook-citation]] 인용 검수, [[ebook-structure]] 구조 검수.
