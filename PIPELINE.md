# Nano Banana Pro 그림 파이프라인

이 파이프라인은 `final_prompt_info.md`의 모델·스타일·검수 규칙을 이 교재의 번호 절 그림에 적용한다.

## 입력과 출력

- 입력 명세: `specs/chN/figNN.json`
- 공통 스타일: `style_v2.txt`
- 생성 명령: `python gen_one.py specs/chN/figNN.json`
- 생성 결과: `figures/chN/`
- GitBook 게시 위치: `.gitbook/assets/nano/chN/`
- 배치·캡션 계획: `specs/chN/_placement.md`
- 사용량 기록: `figures/chN/_usage.jsonl`

기본 모델은 `gemini-3-pro-image`, 해상도는 2K다. 프로젝트 루트의 `key.txt` 또는 `GEMINI_API_KEY`를 사용하며 키를 저장소에 커밋하지 않는다.

## 이번 실행 결과

- 유지 장: Chapters 1–6·9–11
- JSON 명세와 최종 게시 자산: 100개
- 원고의 신규 자산 링크: 100개
- 기존 시각화와 합친 번호 절 시각화: 149개
- 수량 검사: 72개 번호 절 모두 2개 이상, PASS
- QA 기록: `figures/chN/_QA_REPORT.md`

API 키는 생성이 끝난 뒤 프로젝트 작업 파일에서 제거한다. 채팅이나 로그에 노출된 키는 공급자 콘솔에서 폐기·재발급해야 한다.

## 생성 정책

1. 기존 Markdown 이미지와 Mermaid를 먼저 세고, 번호 절마다 최종 2개가 되도록 부족분만 명세한다.
2. 개념도·모식도·공개 수치를 명시한 차트만 생성한다.
3. 실제 화면 캡처, 실사·현미경·젤 이미지와 출처 불명 실측 그래프는 생성 이미지로 대체하지 않는다.
4. 변동 가능한 소프트웨어·모델 목록은 정적 그림보다 본문 표와 공식 링크로 유지한다.
5. 원본을 참고하는 경우 정보 구조·수치·순서를 보존하되 로고·워터마크·출처 문구는 복제하지 않는다.

## 실행

```bash
python generate_all.py --dry-run
python generate_all.py specs/ch4
```

재생성이 필요한 한 그림만 덮어쓸 때에는 다음과 같이 실행한다.

```bash
python gen_one.py specs/ch4/fig02.json --force
```

## 생성 후 검수

각 결과는 다음 세 검사를 모두 통과해야 한다.

1. **과학 검수:** 반응 방향·수치·명칭·패널 순서·화살표 대상이 명세와 일치하는가?
2. **시각·한글 검수:** 한글을 음절 단위로 읽었을 때 깨짐·오타·환각 텍스트·잘림이 없는가?
3. **상세도 검수:** 원고와 명세가 요구한 핵심 관계·예외·패널이 빠지지 않았는가?

과학적 관계·오탈자·누락·잘림이 있는 이미지는 게시하지 않는다. 명세를 고쳐 다시 생성하고 재검수한다. 모델 특성상 미세한 색조 변화만 남고 내용·텍스트·배치가 정확한 경우에는 재시도 상한 뒤 조건부 PASS로 기록할 수 있다.

## 게시와 원고 반영

```bash
python scripts/publish_nano_figures.py specs/ch4
```

검수를 통과한 자산만 게시한 뒤 `_placement.md`에 적힌 위치에 링크와 자립 캡션을 넣고 그림 번호를 장 전역에서 다시 확인한다. 마지막으로 `FIGURE_SOURCES.md`와 `figures/_MASTER_REPORT.md`를 갱신한다.

## 최종 검사

```bash
python scripts/validate_figure_coverage.py
python scripts/validate_textbook.py
git diff --check
```
