# Nano Banana Pro 그림 생성 절차

각 `chN/figNN.json`은 `final_prompt_info.md`의 공통 스타일을 적용할 그림 명세다. API 키는 저장소에 커밋하지 않는다.

## 1. 명세 검사

```bash
python generate_all.py --dry-run
```

## 2. 그림 생성

프로젝트 루트의 `key.txt`에 Gemini API 키를 두거나 `GEMINI_API_KEY` 환경 변수를 설정한 뒤 실행한다.

```bash
python generate_all.py specs/ch4
```

기본 모델은 Nano Banana Pro인 `gemini-3-pro-image`이며, 각 명세는 2K 이미지를 요청한다. 생성물은 `figures/chN/`에 저장되고 사용량 메타데이터는 같은 디렉터리의 `_usage.jsonl`에 기록된다.

## 3. 그림 검수

각 이미지를 열어 다음을 확인한다.

1. 반응 방향, 화학량론 계수, 숫자와 패널 순서가 명세와 일치하는가?
2. 한글·영문 라벨이 빠지거나 깨지지 않았는가?
3. 화살표가 올바른 대상을 가리키고 겹치는 요소가 없는가?
4. 캡션·로고·워터마크가 이미지 안에 들어가지 않았는가?
5. `_placement.md`의 자립 캡션이 그림만 보아도 조건과 한계를 설명하는가?

검수에 실패한 명세만 수정한 뒤 `--force`로 다시 생성한다.

```bash
python gen_one.py specs/ch4/fig02.json --force
```

## 4. GitBook 자산으로 게시

검수를 통과한 이미지만 게시한다.

```bash
python scripts/publish_nano_figures.py specs/ch4
```

게시 위치는 `.gitbook/assets/nano/chN/`이다. 이후 각 장의 `_placement.md`에 적힌 위치에 이미지 링크와 캡션을 삽입하고 `FIGURE_SOURCES.md`를 갱신한다.

## 5. 최종 검사

```bash
python scripts/validate_figure_coverage.py
python scripts/validate_textbook.py
git diff --check
```
