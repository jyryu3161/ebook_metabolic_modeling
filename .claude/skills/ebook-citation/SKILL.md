---
name: ebook-citation
description: Add, verify, or repair citations, sources, licenses, and reuse rights for the Korean genome-scale metabolic modeling textbook, including the figure rights ledger. Use when citing a paper, adding a quantitative claim that needs a source, checking whether an external figure may be reused, recording a license, or updating FIGURE_SOURCES.md rights entries. Triggers - 인용, 출처, 참고문헌, 저작권, 라이선스, 권리, DOI, citation, license, copyright, reuse, attribution, CC BY. Do NOT use for figure generation mechanics (use ebook-figure) or prose tone (use ebook-prose).
---

# 인용·출처·권리 규약

정본 기준: [`docs/textbook-editorial-standard.md`](../../../docs/textbook-editorial-standard.md) §4, 권리 장부는 [`FIGURE_SOURCES.md`](../../../FIGURE_SOURCES.md), 방법론 비교는 [`landmark-papers.md`](../../../landmark-papers.md).

## 1. 인용이 반드시 필요한 진술

다음에는 **일차 문헌 또는 공식 데이터베이스**를 인용한다.

- 정량값(성장률, 반응 수, 성능 수치)
- 역사적 최초성(`처음 제안된`, `최초의`)
- 성능 비교(`A가 B보다 정확하다`)
- 임상·산업적 효과

방법론은 **제안 논문**과 **현재 구현을 설명하는 공식 문서**를 구분해 인용한다.

- FBA 개념 → [Orth et al. (2010)](https://doi.org/10.1038/nbt.1614)
- 구현 → [COBRApy 공식 문서](https://opencobra.github.io/cobrapy/)

## 2. 링크 우선순위

장기 추적이 가능한 주소만 쓴다.

1. DOI (`https://doi.org/...`)
2. PubMed / PMC
3. 공식 프로젝트 저장소, 모델 데이터베이스(BiGG 등)
4. 그 외 웹 자료는 가급적 피한다

출처가 확인되지 않은 이미지·수치, 그리고 **논문 결론보다 강한 표현**은 삭제하거나 검증 가능한 수준으로 낮춘다.

## 3. 라이선스별 취급 — 그림 재사용 판단

이 교재는 **외부 논문의 그림을 원고에 직접 포함하지 않는다.** 필요한 관계는 재현 가능한 코드나 벡터 도식으로 새로 그리고 원개념을 인용한다.

| 라이선스 | 그림 재사용 | 이 교재의 처리 |
|---|---|---|
| **CC BY-NC-ND** | ✗ 수정·번역·재구성 금지 | 사실·방법·보고 수치만 인용. 트레이싱·재구성 금지 |
| **출판사 저작권(PNAS·Wiley 등)** | ✗ 별도 허락 필요 | 수식·논리만 인용하고 독립 도식 제작 |
| **CC BY 4.0** | 조건부 가능 | 허용되더라도 **원 그림은 가져오지 않는 것이 이 저장소의 방침** |
| **PD / CC0 실물 사진** | ✓ 포함 가능 | 출처·라이선스 표기 후 직접 포함. 장부의 「퍼블릭 도메인 실물 사진」 표에 개별 검증 결과 기록 |

핵심 원칙 두 가지:

- **개념 원출처의 라이선스는 그 논문에만 적용된다.** 독립적으로 새로 그린 이 교재 도식에 자동으로 이전되지 않는다.
- 저장소 루트에 `LICENSE`/`COPYING`/`NOTICE`가 없으므로 **자체 제작 자산의 제3자 재사용 조건은 현재 미선언 상태**다. 공개 배포 전 교재 전체 라이선스를 별도로 결정해야 한다. 장부의 권리 열에 이 사실을 그대로 적는다.

## 4. 출처 표기 형식

본문 그림 캡션 끝에 붙인다.

```
저자 작성; 개념 근거: [Orth et al. (2010)](https://doi.org/10.1038/nbt.1614)
```

```
출처: 저자 계산; 생성: [`scripts/generate_optimization_figures.py`](../scripts/generate_optimization_figures.py)의 `draw_production_envelope()`; 조건: COBRApy 0.30.0, e_coli_core, GLPK
```

논문 그림을 변형·재작성한 경우에만 `~에서 수정·재구성`을 쓰고, 원출처 DOI와 라이선스를 확인해 함께 적는다. **이 교재에서는 이 경우가 발생하지 않도록 독립 제작을 우선한다.**

## 5. 장부 갱신

[`FIGURE_SOURCES.md`](../../../FIGURE_SOURCES.md)를 갱신할 때:

- 자산 표에 행 추가/갱신 — `ID`·`자산 파일`·`최초·재사용 위치`·`제작·생성 조건`·`개념·데이터 원출처`·`권리 상태`·`검증일`
- 새 외부 문헌을 인용했다면 「외부 문헌 권리 확인」 표에도 `문헌군`·`확인한 라이선스·권리`·`이 원고에서의 사용`을 추가한다
- 문서 상단의 **최종 검증일**을 갱신한다
- 확인하지 못한 항목은 추정해 채우지 말고 결손으로 명시한다(예: "GLPK 세부 버전과 모델 checksum은 생성 당시 기록되지 않았습니다")

## 6. 작업 절차

1. 진술 유형을 판별한다 — §1에 해당하면 인용 필수.
2. 일차 문헌을 찾아 DOI를 확보한다. 방법 제안 논문과 구현 문서를 분리한다.
3. 그림이 관련되면 §3 표로 재사용 가능 여부를 판정한다. 불확실하면 **재사용하지 않고 독립 제작**한다.
4. 캡션·본문에 §4 형식으로 표기한다.
5. 그림이면 §5에 따라 장부를 갱신하고 검증일을 적는다.

관련: [[ebook-figure]] 그림 제작, [[ebook-review]] 인용 누락 검수, [[ebook-prose]] 조건부 진술 표현.
