# Chapter 8. 미생물·세포공장·합성생물학 응용

> 유전자 하나를 껐을 때 세포는 무엇을 할까요? 이 장에서는 유전자 결손(gene knockout)이 대사 흐름에 미치는 영향을 예측하는 세 방법(FBA·MOMA·ROOM)을 손으로 계산하며 배우고, 이를 발판으로 미생물을 유용 물질 **세포 공장(cell factory)**으로 재설계하는 **균주 설계(strain design)** 알고리듬과 여러 미생물이 대사를 나누는 **커뮤니티(community) 모델링**까지 나아갑니다. 이 장을 마치면 여러분은 `e_coli_core`로 단일·이중 결손, MOMA/ROOM, production envelope를 직접 실행하고 그 결과를 해석할 수 있게 됩니다.

{% hint style="info" %}
유전자 회로·표준 부품·ALE·바이오센서에서 세포공장 설계로 이어지는 큰 그림은 준비 학습 C: 합성생물학에서 GEM 기반 세포공장까지를 함께 보십시오.
{% endhint %}

## 이 장을 시작하며

여러분이 맥주 양조장을 운영한다고 상상해 봅시다. 효모는 포도당을 먹고 열심히 에탄올을 뱉어냅니다. 그런데 어느 날 이런 생각이 듭니다 — "효모가 에너지를 자기 몸집 불리는 데 그만 쓰고, 내가 팔고 싶은 물질을 더 많이 만들게 할 수는 없을까?" 세포를 마치 **공장의 생산 라인처럼 개조**하는 것, 이것이 이 장의 핵심 질문입니다.

[Chapter 4](../chapter-4/README.md)에서 우리는 [FBA](../chapter-4/README.md)로 "세포가 최적으로 행동할 때 어떤 flux 분포를 택하는가"를 계산했습니다. [Chapter 7](../chapter-7/README.md)에서는 그 도구를 질병에 겨눠, "어떤 유전자를 **끄면**(knockout) 암세포를 굶겨 죽일 수 있는가"를 물었습니다. 이제 산업 현장으로 무대를 옮기면 질문의 방향이 정반대가 됩니다 — "어떤 유전자를 끄고 켜야 세포가 **더 많이 만들어낼까**?" MOMA·ROOM의 핵심만 먼저 복습하려면 [Perturbation 분석 보충](../supplements/perturbation-analysis.md), 원 논문을 순서대로 읽으려면 [필독 논문 통합 가이드](../landmark-papers.md)를 참고하십시오.

> **잠깐, 생각해보기:** 암 표적 발굴(Ch7)과 세포 공장 설계(Ch8)는 정반대의 목적을 가지는데, 왜 같은 유전자 결손·FBA 도구를 쓸 수 있을까요? 힌트: 두 경우 모두 "유전자를 껐을 때 대사 흐름이 어떻게 재배치되는가"라는 **동일한 예측 문제**를 풀며, 다만 그 예측을 "생장 억제"에 쓰느냐 "생산 증대"에 쓰느냐만 다릅니다.

하지만 곧바로 곤란한 사실과 마주합니다. Ch4의 FBA는 돌연변이도 지정한 목적을 재최적화한다고 가정하지만, 결손 직후 세포가 새 최적 상태에 도달한다는 보장은 없습니다. 이 차이를 시험하기 위해 **MOMA**와 **ROOM**이라는 두 대안 가설이 등장했습니다. 뒤에서는 FBA·FVA 또는 MOMA·ROOM을 평가 층으로 활용하는 균주 설계 알고리듬(OptKnock, OptForce, OptGene, FSEOF)으로 확장합니다. 실행 예제는 [Chapter 1](../chapter-1/README.md)의 `e_coli_core`(반응 95, 대사물 72, 유전자 137)를 사용합니다.

---
## 학습 목표

이 장을 마치면 학습자는 다음을 할 수 있게 됩니다.

**이론적 목표**
1. Perturbation(섭동) 분석의 대수적 기초 — null space, feasible space, 세 가지 제약(화학량론적·열역학적·perturbation-specific) — 을 설명할 수 있다.
2. **GPR (Gene-Protein-Reaction)** 규칙의 Boolean 평가를 통해 유전자 결손이 반응 비활성화로 이어지는 메커니즘을 손으로 추론하고, 단일/이중 결손 결과를 essential/growth-reduced/non-essential로 분류할 수 있다.
3. MOMA의 이차계획법(QP) 정형화와 ROOM의 혼합정수선형계획법(MILP) 정형화를 수식으로 설명하고 두 방법을 비교할 수 있다.
4. OptKnock, OptForce, OptGene, FSEOF 등 균주 설계 알고리듬의 수학적 정형화와 적용 맥락의 차이를 설명할 수 있다.
5. Production envelope와 phenotype phase plane이 생산-생장 트레이드오프를 어떻게 시각화하는지 꼭짓점을 손으로 읽으며 설명할 수 있다.
6. 커뮤니티 대사 모델링의 개념(cross-feeding, competition, mutualism)과 대표 프레임워크(MICOM, SteadyCom, OptCom, COMETS)의 차이를 설명할 수 있다.

**실습적 목표**
7. COBRApy로 단일/이중 유전자 결손, `moma()`, `room()`을 실행하고 결과를 비교·시각화할 수 있다.
8. `production_envelope()`로 생산 포락선을 계산하고 growth-coupled 여부를 판정할 수 있다.
9. 두 개의 최소 모델을 이어 붙여 cross-feeding 커뮤니티 모델을 만들고 FBA로 분석할 수 있다.

**통합적 목표**
10. 연구 질문(과도 상태 vs. 안정 상태, 약물 표적 스크리닝 vs. 균주 설계, 단일 종 vs. 커뮤니티)에 따라 이 장에서 다룬 방법 중 적절한 것을 선택하는 기준을 제시할 수 있다.

---
