# Chapter 10. COBRApy 완전 실행 튜토리얼

> 지금까지 배운 FBA·pFBA·FVA·유전자 결손·MOMA·ROOM·gap-filling을 하나의 재현 가능한 노트북 흐름으로 연결합니다. 모든 기준값은 **COBRApy 0.30.0 + GLPK + `textbook`(`e_coli_core`) 모델**에서 검산했습니다. 이 장을 위에서 아래로 실행하면 모델을 불러오는 데서 시작해 결과와 환경 정보를 JSON으로 남기는 데까지 한 번에 도달합니다.

이 장의 목적은 API 이름을 외우는 것이 아닙니다. 각 계산에서 다음 네 질문에 답하는 습관을 만드는 것이 목적입니다.

1. 지금 바꾼 것은 모델, 배지, 목적함수 중 무엇인가?
2. solver가 반환한 상태는 정말 `optimal`인가?
3. 목적함수 값 외에 질량보존과 수치 유한성도 확인했는가?
4. 다른 사람이 같은 모델과 조건을 복원할 기록을 남겼는가?

## 학습 목표

이 장을 마치면 다음을 할 수 있습니다.

- COBRApy 객체 모델과 GPR 규칙을 탐색하고 exchange flux의 부호를 해석한다.
- `model.medium`과 context manager로 조건을 안전하게 바꾼다.
- FBA 결과의 solver 상태와 $$\mathbf{S}\mathbf{v}=\mathbf{0}$$ 잔차를 검산한다.
- pFBA와 FVA가 각각 답하는 질문을 구분한다.
- infeasible/`NaN`을 안전하게 처리하며 유전자 결손을 분류한다.
- `tpiA` 결손을 FBA, 선형 MOMA, 선형 ROOM으로 비교한다.
- `optlang`으로 작은 GLPK MILP를 만들고 binary variable의 역할을 설명한다.
- 장난감 모델에서 gap-filling, production envelope, SBML 왕복 검증을 수행한다.
- Plotly와 ipywidgets로 조건을 대화형으로 탐색하고 실행 기록을 저장한다.

---
