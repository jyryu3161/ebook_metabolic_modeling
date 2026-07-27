# 전 장 시각화 최종 현황

이 보고서는 유지되는 번호 절의 기존 Markdown 이미지·Mermaid와 Nano Banana Pro 신규 도판을 합산한 최종 현황이다. 표와 코드 블록, 장 도입 `README.md`의 시각화는 절별 수량에 포함하지 않았다.

| 장 | 번호 절 | 기존 시각화 | 신규 도판 | 최종 합계 | 절별 최소 2개 |
|:---:|---:|---:|---:|---:|:---:|
| 1 | 8 | 9 | 7 | 16 | PASS |
| 2 | 4 | 2 | 8 | 10 | PASS |
| 3 | 7 | 2 | 12 | 14 | PASS |
| 4 | 13 | 6 | 20 | 26 | PASS |
| 5 | 6 | 5 | 7 | 12 | PASS |
| 6 | 9 | 6 | 12 | 18 | PASS |
| 9 | 3 | 4 | 3 | 7 | PASS |
| 10 | 15 | 5 | 26 | 31 | PASS |
| 11 | 7 | 10 | 5 | 15 | PASS |
| **합계** | **72** | **49** | **100** | **149** | **PASS** |

## 완료 상태

- `final_prompt_info.md`와 `style_v2.txt`를 기준으로 JSON 명세 100개를 실제 생성했다.
- 장별 최종 JPEG 100개와 `.gitbook/assets/nano/chN/` 게시본 100개가 일치하며, 원고에는 실제 자산 링크 100개가 들어 있다.
- 각 장의 `_QA_REPORT.md`에 모델·해상도·재시도와 과학·텍스트·배치 판정을 기록했다. 미세한 색조 차이만 남은 도판은 조건부 PASS로 명시했고, 과학적 관계 오류는 수정 후에만 채택했다.
- `python scripts/validate_figure_coverage.py` 결과, 유지되는 72개 번호 절 모두 시각화 2개 이상이며 총 149개다.
- `python scripts/validate_textbook.py`, 생성 스크립트 구문 검사, Markdown 로컬 링크 검사, 대화형 JavaScript 구문 검사와 `git diff --check`를 통과했다.

## 재검증 명령

```bash
python generate_all.py --dry-run
python scripts/validate_figure_coverage.py
python scripts/validate_textbook.py
git diff --check
```
