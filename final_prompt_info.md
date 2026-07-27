# final_prompt_info.md — 전자책 과학 인포그래픽 생성 종합 정보 (모델 + 프롬프트 + 파이프라인)

이 파일 하나로 **현재 그림을 만드는 방법 전체**(모델·API·비용·프롬프트·규칙·검수·재현)를 재현한다.
최종 갱신: 2026-07 · 대체: `AI-프롬프트.md`(v2)·`AI-프롬프트_최종.md`

---

## 0. 모델 정보 (MODEL)

| 항목 | 값 |
|---|---|
| 제품명 | **Google Nano Banana Pro** (= "Nano Banana 2") |
| 모델 ID (기본) | **`gemini-3-pro-image`** |
| 폴백 순서 | `gemini-3-pro-image` → `nano-banana-pro-preview` → `gemini-3-pro-image-preview` → `gemini-2.5-flash-image` |
| 제공처 | Google Gemini API (`generativelanguage.googleapis.com`) |
| 강점 | 이미지 내 **한글·영문 텍스트 렌더링 우수**, 인포그래픽·도식, 원본 참조 리드로우(이미지+텍스트 입력) |
| 인증 | API 키 파일 `key.txt` (형식 `AIza...`, 39자) |
| 해상도 | **2K**(인쇄 적합) — `imageConfig.imageSize:"2K"` |
| 반환 형식 | inlineData base64, **mimeType `image/jpeg`** (2K, 가로세로비별 대략 롱변 ~2048px 내외; 예 16:9 → 2752×1536) |
| 지원 비율 | 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 (원본에 근접값 선택) |

### API 호출 규격
```
POST https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={KEY}
Content-Type: application/json

{
  "contents": [{ "role": "user", "parts": [
    { "inlineData": { "mimeType": "image/png", "data": "<원본 base64>" } },   // 리드로우 시(선택)
    { "text": "<STYLE 프리앰블 + 리드로우 지시 + 그림별 내용>" }
  ]}],
  "generationConfig": {
    "responseModalities": ["IMAGE"],
    "imageConfig": { "aspectRatio": "16:9", "imageSize": "2K" }   // gemini-3 / nano-banana 계열
  }
}
```
- 응답: `candidates[0].content.parts[].inlineData.data`(base64) → 파일 저장. `usageMetadata`로 토큰 사용량 확인.
- 원본 이미지를 `inlineData`로 함께 넣으면 **리드로우(원본 반영)**, 없으면 텍스트만으로 신규 생성.

### 비용 (확인일 2026-07)
| 항목 | 단가 | 비고 |
|---|---|---|
| 이미지 출력 | **1,120 토큰/장 (1K·2K 동일)** × **$120 / 1M** = **$0.134/장** | 4K는 2,000토큰 = $0.24 |
| 입력 이미지 | ~258 토큰/장 × $2/1M ≈ $0.0005 | 레퍼런스 원본 |
| 텍스트 입력 | ~1,500–2,000 토큰 × $2/1M | 프롬프트 |
| 텍스트 출력(사고 포함) | 가변 × $12/1M | |
| **실측 유효 단가** | **≈ $0.15/장 (2K, ₩약 210)** | 본 프로젝트 평균 |
- 참고 실적: 최종 REDRAW 83장 + 다회 재생성 = 생성호출 157회, 누적 **$23.75 (₩32,890)**.

---

## 1. [기계 투입용] 공통 STYLE 프리앰블 (그대로 복사 = `style_v2.txt`)

```
PROFESSIONAL FLAT VECTOR INFOGRAPHIC for a university science textbook, in the polished style of premium editorial / scientific-journal graphics. Sole purpose: clear information delivery. Restrained, not decorative.

RENDERING (obey strictly):
- Flat 2D vector illustration. Each shape = ONE solid muted fill + a clean crisp outline. NO gradient fills, NO drop shadows, NO 3D/bevel/gloss, NO texture, NO photorealism, NO gradient background.
- Background: plain warm off-white #FCFCFA (not pure white). Keep calm whitespace; do NOT fill it with clutter. Align everything to a shared baseline / tidy grid. Flow left-to-right, top-to-bottom.

PROFESSIONAL COLOR SYSTEM — deeper, calmer, editorial (NOT candy pastel). Every colored shape uses a {darker outline stroke / calmer light fill} PAIR (fill light, outline = a darker version of the same hue). This tonal outlining is the key to the professional look.
Semantic colors (fixed to a concept, reused everywhere):
- Structure / actor (protein, enzyme, receptor, cell, organ, system): outline #33526F, fill #C4D4E6
- Input / activation / positive (substrate, agonist, ON, normal): outline #43704E, fill #C6DCC3
- Secondary / competitive molecule: outline #8E5877, fill #E3C3D4
- Inhibitor / antagonist / blocked / negative / OFF: outline #9E3B34, fill #E4A69F
Categorical / stage colors (assign in order to any undefined category/stage; solid fill with white text): #35507E, #6A5399, #C2912E, #4E8C57, #2C6E6A, slate #4A5A6A.
Neutrals: ink outlines & body text #1F242B; secondary lines/text graphite #3C444D; English academic terms & captions warm-grey #7C838C; inactive fill #E4E7EA with #AAB0B7 outline; hairline grid/guides #E1E4E8.
Emphasis color #9E2B25 — use ONCE per image only, for the single most important marker/label.

LINE-WEIGHT HIERARCHY (organize information by stroke weight — do NOT draw everything at one weight):
- Main silhouette (key shapes): ~3px, in the shape's outline color or ink.
- Interior detail / secondary shapes: ~1.5px, graphite.
- Process arrow (next step): ~2.5px straight, ink #1F242B, filled triangular arrowhead.
- Binding / action arrow: ~2px curved, SAME color as the molecule it connects.
- Axis / grid / guides: ~1px hairline #E1E4E8.
Consistent corner radius (containers 12-16px; stage tags fully rounded pills). Uniform arrowhead & line-cap style throughout.

HANDLING UNSPECIFIED ELEMENTS (general-purpose): classify EVERY element into a role and style it consistently — structure->blue, input/positive->green, block/negative->red (+red X or grey-out), secondary->mauve, stage/category->categorical palette in order, data->slate bars/points/lines on a hairline grid with only the key series in the emphasis color, annotation/key->emphasis (once), inactive->grey. If a concept has no color yet, take the next unused categorical hue and reuse it.

TYPOGRAPHY HIERARCHY: clean geometric sans-serif. Title heavy (800) Korean + smaller English academic term in warm-grey (600). Panel labels: bold categorical-colored A/B/C + Korean subtitle. Body labels 600; values/annotations smaller. Keep all text minimal, EXACT spelling as given, fully legible, high contrast, no gibberish, no stray numbers/letters. Technical terms (Agonist, Allosteric...) stay in English.

LAYOUT: outer margin generous. Time/value axis only may use a color transition (light pink #F3CFCB -> emphasis #9E2B25); nowhere else.
NO CAPTION: Do NOT add any caption, description, footnote, or explanatory sentence anywhere in the image. The image contains ONLY the figure itself — title, panel labels, axis/data labels, legend. No full-sentence text at the bottom or elsewhere.
KOREAN TEXT SAFETY: Render Korean EXACTLY as given, syllable by syllable. Avoid rare/complex final consonants (e.g. 묾, 풂) — they garble easily; prefer common wording. Do NOT invent words, English fragments, or layout words like "COLUMN"/"PANEL" (use only "A"/"B" as panel markers). Every Hangul syllable must be a real, correctly-spelled character.
DON'T: gradient bg/fills, shadows, 3D, emoji, decorative icons, meaningless numbers, outline-less blurry shapes, logos/watermarks, any caption/description sentence, time-stamped "as-of" single-point values, or drawing everything at the same weight/saturation.
```

## 2. [기계 투입용] 원본 리드로우 지시문 (원본 이미지를 함께 입력할 때)

```
You are given the ORIGINAL textbook figure as a reference image. REDRAW it as a NEW flat vector infographic in the house style described above.
- PRESERVE the same information, overall structure/layout, data values, ordering and meaning, so it is clearly recognizable as the same figure.
- RE-EXPRESS every shape cleanly in the house style; do NOT copy the original's photographic/screenshot look, its colors, and DO NOT reproduce any logo, watermark, or source stamp from the original.
- Replace ALL text with the exact Korean (+English term) labels specified below, correctly spelled, fully legible, no gibberish.
- Keep the same composition/aspect so it reads as a faithful redraw, not a different figure.

=== THIS FIGURE (labels & content) ===
[여기에 그림별 내용·정확한 한글 라벨·데이터값을 적는다]
```

---

## 3. 반드시 지킬 규칙 (프로젝트에서 확립한 9원칙)

1. **캡션 금지** — 이미지에 설명 문장/하단 캡션 없음(제목·라벨·범례·축만).
2. **시점 의존 라벨 금지** — 특정 '현재 연도' 값 강조·"as of"·단일시점 마커 금지. 예측/추세는 축·추세만.
3. **주석 포인터 정확성** — 지시선·화살표는 정확한 대상을 가리킴(예: 알로스테릭 부위=활성부위와 다른 별도 포켓).
4. **과학적 정확성 우선** — 원본과 비슷하되 사실이 우선. 원본이 틀렸으면 바로잡음(명칭·순서·방향·위치·수치·기전). 교육적 단순화는 로그에 표기.
5. **스킵 정책("데이터 공개 시에만 리드로우")** — 실제 화면 캡처·실사·현미경/젤/실측 이미지·출처불명 실측 그래프는 생성하지 않고 제외(가짜 데이터·가짜 화면 방지). 개념도·모식도·공개/표기 데이터 차트만 REDRAW.
6. **시점·팩트 변동 표는 SKIP** — 소프트웨어/모델 목록·도구 비교표는 정적 이미지 대신 본문 유지보수형 표 + 공식 링크 + 확인일.
7. **로고·워터마크·출처문구 제거** (저작권·상표 회피).
8. **한글 오타 강건성** — 정확한 철자 명시. 반복해 깨지는 드문 받침 음절(묾·풂 등)은 **같은 뜻의 흔한 표현으로 치환**(예: "드묾"→"거의 없음"). "COLUMN/PANEL" 골격 단어가 리터럴로 찍히지 않게 마커는 "A/B"만.
9. **비율은 원본에 맞춤** — 원본 px로 근접 비율 선택. 초광폭(2.36:1)·세로 긴 표는 모바일 가독성 저하 → 분할 고려.

---

## 4. 그림별 spec 템플릿 (JSON — `gen_one.py` 입력)

```json
{
  "name": "chN_figMM_slug",
  "out_dir": "figures/chN",
  "aspect": "16:9",
  "size": "2K",
  "ref_image": "<원본 이미지 절대경로 (없으면 생략 → 텍스트만 생성)>",
  "prompt": "Title (top): \"<한글 제목>\" + smaller warm-grey \"<English>\". <패널·도형·데이터·정확한 한글 라벨. 과학적으로 정확하게. 캡션·시점라벨·로고 없이.>"
}
```
- JSON 저장은 `json.dump(..., ensure_ascii=False)`로 이스케이프 안전. `name`=이미지 파일명(2자리 그림번호).

## 5. 2단계(+상세) 검수 체크리스트 — 생성 후 필수

- **A. 과학 검수**: 수치·명칭·순서·방향·위치·주석 포인터가 사실과 일치? 원본 오류를 바로잡았나?
- **B. 시각·한글 검수**: 한글을 **한 음절씩** 판독 → 깨짐/근접 오타(묾↔풂), 환각 텍스트(COLUMN·없는 영단어), 도형 깨짐·라벨 누락·잘림 없나?
- **C. 원본 대비 상세도**: 원본이 전달하던 핵심 정보·패널이 과하게 축소되지 않았나?
→ 결함 시 spec 보완 후 재생성(보통 1~2회, 깨지는 단어는 표현 치환). 셋 다 통과해야 완료.

## 6. 재현 파이프라인

```bash
# 1) key.txt 에 Google Gemini API 키 (AIza...)
# 2) 그림별 spec 작성 → specs/chN/figMM.json  (④ 템플릿)
# 3) 생성 (STYLE 자동 전치 + 원본 레퍼런스 리드로우 + 2K + 사용량 기록)
python3 gen_one.py specs/chN/figMM.json
# 4) 결과 figures/chN/chN_figMM_slug.jpg → ⑤ 검수(A·B·C) → 필요시 재생성
```
- `gen_one.py`: STYLE(`style_v2.txt`) 자동 전치 → (원본 있으면) 리드로우 지시 결합 → `imageConfig.aspectRatio/imageSize:2K` → base64 저장 → `figures/chN/_usage.jsonl` 기록.
- 관련 파일: `style_v2.txt`(STYLE 블록), `gen_one.py`(생성기), `PIPELINE.md`(전체 규칙), `figures/CAPTION_GUIDANCE.md`(출처·기준일 등 저자 캡션 사항), `figures/_MASTER_REPORT.md`(전 과정 기록).

---
> 유의: 이 스타일은 개념도·모식도·차트에 최적. 화학구조식·염기서열·정밀 수치플롯은 최종 인쇄 시 벡터/코드(matplotlib·SVG)로 조판하면 더 정확·강건. 시장규모·모델목록 등 변동 정보는 기준일 표기 또는 본문 표로.
