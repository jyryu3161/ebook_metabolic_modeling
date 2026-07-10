# 마무리: 요약 · 스스로 점검 · 용어

## 한 장 요약

- GEM의 "해부학(anatomy)"은 [Chapter 2](../chapter-2/README.md)의 화학량론 행렬 $$\mathbf{S}$$ 위에 얹히는 네 가지 구조 요소 — **GPR**, **구획과 운송**, **경계 반응(exchange/demand/sink)**, **바이오매스 목적함수** — 로 구성된다.
- **GPR**은 유전자-반응 관계를 AND(효소 복합체)·OR(동위 효소) Boolean 논리로 인코딩하며, 이를 통해 유전자 결실을 반응 통량 제약으로 변환하고 유전자 필수성을 예측할 수 있다. 2.3절의 손 계산이 보여주듯, AND/OR의 **중첩 순서**에 따라 같은 세 유전자라도 결과가 달라진다. 인체 GPR은 아이소자임·대안적 스플라이싱·다중 서브유닛 복합체로 인해 원핵생물보다 훨씬 복잡하다(LDH, PDC, Hexokinase 사례).
- **세포 구획**은 서로 다른 화학적 환경을 물리적으로 분리해 상반된 반응의 공존과 정교한 조절을 가능케 한다. 전체 규모의 그람음성 대장균 모델은 `c`, `p`, `e`를, 이 책의 축소 `textbook` 모델은 `c`, `e`만을 가지며, 인체 모델은 여러 세포소기관 구획을 구분한다. 구획화는 $$\mathbf{S}$$를 블록 구조로 만든다.
- **운송 반응**은 확산·촉진확산·능동수송(PTS, ABC transporter 등)으로 구획 간 물질을 이동시키며, GPR과 아세포위 국소화 예측을 통해 구축된다. 구획·운송체의 기능 장애는 다양한 대사 질병(Zellweger, Gaucher, Pompe 등)으로 이어진다.
- **경계 반응**은 exchange(세포외 대사물-환경), demand(세포내 대사물의 비가역적 배출), sink(세포내 대사물의 가역적 공급/배출) 세 종류로 나뉘며, 이들의 bounds 설정이 곧 모델의 성장 조건(배지)을 정의한다.
- **바이오매스 목적함수**는 단백질·RNA·DNA·지질 등 대분자 조성비로 계산된 계수를 가진 특수 반응이며, GAM/NGAM으로 성장 관련/비성장 관련 에너지 요구를 반영한다. NGAM은 모델마다 다르게 큐레이션되므로(`e_coli_core`의 8.39 vs 문헌의 3.15), 항상 그 모델 자신의 값을 확인해야 한다.
- 이 네 요소를 종합하면, 인체 GEM이 미생물 GEM보다 훨씬 큰 이유는 "화학이 더 복잡해서"가 아니라 **GPR의 조직 특이성과 구획·운송의 다층 구조** 때문임을 알 수 있다. `e_coli_core`·iML1515·Recon3D 삼자를 나란히 놓은 7.2절의 표는 이 결론을 세 가지 규모에서 동시에 확인시켜 준다.
- 구획이 늘어나는 계산적 대가는 조합론으로도 셀 수 있다(3.6절): $$n$$개 구획을 완전 연결하려면 $$\binom{n}{2}$$개의 연결이 필요하지만, 실제 세포는 세포질을 중심으로 한 허브-스포크 구조($$n-1$$개)를 택해 배관을 절약한다.
- 이 구조를 게놈 서열로부터 실제로 채워 넣는 재구축(reconstruction) 절차와 품질 관리(QC)는 [Chapter 5](../chapter-5/README.md)에서, 발현 데이터를 GPR·구획에 통합하는 맥락-특이적 모델링(iMAT, GIMME, tINIT)은 [Chapter 6](../chapter-6/README.md)에서 다룬다.

### 이 장에서 익힌 손 계산 도구 모음

| 도구 | 핵심 공식 | 어디서 배웠나 |
|:---|:---|:---:|
| GPR AND/OR 평가 | $$r_{\text{AND}} = \min(g_A,g_B)$$, $$r_{\text{OR}} = \max(g_C,g_D)$$ | 2.1·2.3·2.8절 |
| 이소자임 필수성 조합론 | $$k$$개 동위 효소 중 반응을 끄는 조합은 $$2^k-1$$가지 중 1가지 | 2.8절 |
| 구획 연결 토폴로지 | 완전 연결 $$\binom{n}{2}$$ vs 허브-스포크 $$n-1$$ | 3.6절 |
| 예측 도구 정확도 분해 | 정확도·민감도·정밀도(혼동행렬) | 3.7절 |
| 교환 반응 부호 규약 | $$v<0$$ 흡수, $$v>0$$ 분비 | 5.1b절 |
| BOF 계수 계산 | $$c_i = f_{\text{macro}} \times w_{\text{DW}} / M_i$$ | 6.2절 |
| GAM/NGAM 회귀 | 기울기=GAM, 절편=NGAM | 6.3절 |

*Table S.1: 이 장에서 등장한 손 계산 공식 전체 목록. 다음 장부터는 이 공식들을 이미 안다고 가정하고 이야기를 진행합니다.*

---

## 스스로 점검

1. **GPR 손 계산**: GPR 규칙이 $$(\text{geneX OR geneY}) \; \text{AND} \; \text{geneZ}$$일 때, (a) geneX만 결손, (b) geneY와 geneZ를 함께 결손시킨 경우 각각 반응이 ON인지 OFF인지 2.3절의 방법으로 직접 계산해 보시오.
   > 힌트: 먼저 괄호 안 OR을 계산한 뒤, 그 결과와 geneZ를 AND로 묶으세요. (a) geneX 결손 → (0 OR 1)=1, 1 AND geneZ(1)=1 → **ON**. (b) geneY, geneZ 결손 → (1 OR 0)=1, 1 AND 0(geneZ 결손)=0 → **OFF**.

2. **구획 개수 비교**: `e_coli_core`, iML1515, Recon3D는 각각 몇 개의 구획을 가지는가? 구획 수 차이가 반응 수 차이에 어떻게 기여하는지 1.2절과 7절의 논리로 설명하시오.
   > 힌트: `e_coli_core`는 2개(`c`, `e`, 축소 모델), iML1515는 3개(`c`, `p`, `e`), Recon3D는 8개 이상. 구획이 늘어날수록 같은 화학종이 여러 노드로 쪼개지고, 이를 잇는 운송 반응이 새로 필요해진다.

3. **경계 반응 구분**: 어떤 대사물 X가 모델 안에서 다른 반응에 의해 소비만 되고 생성되지는 않는데, 그 합성 경로가 아직 모델에 없다고 하자. 이 문제를 풀기 위해 exchange, demand, sink 중 무엇을 추가해야 하며 그 이유는?
   > 힌트: X는 세포내 대사물이므로 exchange(세포외 전용)는 쓸 수 없다. X가 공급도 배출도 필요할 수 있다면 **sink**가 적절하다(5.2절 heme 예시 참고). 만약 X를 생성만 확인하면 되는 "테스트용 배출구"라면 **demand**가 더 적절하다.

4. **BOF 계수 계산**: 어떤 미생물의 단백질 질량 비율이 50%이고, Glycine이 단백질에서 차지하는 질량 비율이 8%, Glycine의 몰 질량이 75.07 g/mol이라면 6.2절의 공식으로 Glycine의 BOF 계수(mmol/gDW)를 계산하시오.
   > 힌트: $$c_{\text{Gly}} = \frac{0.50 \times 0.08}{75.07} \times 1000 \approx 0.533\ \text{mmol/gDW}$$.

5. **원핵 vs 진핵 비교**: Recon3D가 iML1515보다 반응 수가 약 4배 많은 이유를 "화학의 복잡성"이 아니라 이 장에서 배운 **구조적** 이유로 설명하시오. (최소 두 가지 이상 근거를 드시오.)
   > 힌트: 1.2절과 7절 참고 — 구획 수 증가(3개→8개 이상)에 따른 운송 반응 급증, 조직 특이적 아이소자임의 별도 GPR 등록, 복잡한 지질 대사 등을 근거로 들 수 있다.

6. **중첩 GPR 트리 평가(2.8절)**: GPR 규칙이 $$\big[(\text{geneA AND geneB}) \text{ OR geneC}\big] \text{ AND } \big[\text{geneD OR geneE}\big]$$일 때, geneB와 geneD를 함께 결손시키면 반응은 ON인가 OFF인가? 안쪽 괄호부터 차례로 접어 계산하시오.
   > 힌트: 좌측 $$(\text{geneA AND geneB}) = \min(1, 0) = 0$$, 이를 geneC(1)와 OR: $$\max(0,1)=1$$. 우측 $$(\text{geneD OR geneE}) = \max(0,1)=1$$. 마지막으로 좌우를 AND: $$\min(1,1)=1$$ → **ON**.

7. **구획 연결의 조합론(3.6절)**: 어떤 진핵 미생물 GEM이 5개의 구획을 가지고, 모든 구획 간 운송을 세포질을 거치는 허브-스포크 구조로만 구현한다고 하자. 이 경우 필요한 구획-쌍 연결의 최소 개수는 몇 개이며, 만약 완전 연결 구조였다면 몇 개가 필요했겠는가?
   > 힌트: 허브-스포크는 $$n - 1 = 5 - 1 = 4$$개, 완전 연결은 $$\binom{5}{2} = \frac{5 \times 4}{2} = 10$$개. 구획 수가 늘어날수록 완전 연결과 허브-스포크의 격차가 더 벌어진다.

---

## 다음 장 예고

이 장에서 우리는 [Chapter 2](../chapter-2/README.md)의 화학량론 행렬 $$\mathbf{S}$$ 위에 GPR·구획·운송·경계 반응·바이오매스 목적함수라는 네 가지 구조를 입혀, 마침내 **완전한 모델 구조**를 갖췄습니다. 이제 남은 질문은 하나입니다 — 이 모델로 **세포의 성장·플럭스를 실제로 예측**하려면 어떻게 해야 할까요? [Chapter 4. Flux Balance Analysis(FBA)](../chapter-4/README.md)에서는 이 장에서 완성한 구조($$\mathbf{S}$$, bounds, 바이오매스 목적함수)를 **선형 계획법(Linear Programming, LP)** 문제로 바꾸어, `e_coli_core`가 실제로 μ ≈ 0.874 h⁻¹의 속도로 자란다는 것을 직접 계산해 봅니다.

---

## 핵심 용어 정리

| 용어(한글) | English | 정의 |
|:---|:---|:---|
| 유전자-단백질-반응 연관 | Gene-Protein-Reaction (GPR) | 유전자와 반응의 관계를 AND(복합체)·OR(동위 효소) Boolean 논리로 인코딩한 규칙 |
| 효소 복합체 | Enzyme Complex | 여러 유전자 산물이 AND로 결합해야 작동하는 효소 |
| 동위 효소 | Isozyme | 동일 반응을 촉매하는, 서로 다른 유전자가 만드는 여러 효소(OR 관계) |
| 유전자 필수성 | Gene Essentiality | 특정 유전자 결실 시 성장이 임계치 이하로 떨어지는지 여부 |
| 합성 치사 | Synthetic Lethality | 개별 결손으로는 생존하지만 두 유전자를 함께 결손시키면 치사에 이르는 현상 |
| 세포 구획 | Compartment | 막으로 구분된, 독립적인 화학적 환경을 갖는 세포 내 공간 |
| 운송 반응 | Transport Reaction | 같은 화학종을 한 구획에서 다른 구획으로 옮기는 반응 |
| 단일수송체 · 공동수송체 · 역수송체 | Uniporter · Symporter · Antiporter | 운송체가 옮기는 분자 수와 방향 조합에 따른 분류(4.1b절) |
| 아세포위 국소화 | Subcellular Localization | 단백질(효소)이 어느 구획에서 작용하는지를 나타내는 위치 정보 |
| 교환 반응 | Exchange Reaction (`EX_`) | 세포외 대사물과 환경 사이의 경계 조건을 정의하는 의사-반응 |
| 요구 반응 | Demand Reaction (`DM_`) | 세포 내부 대사물을 비가역적으로 배출하는 경계 반응 |
| 싱크 반응 | Sink Reaction (`SK_`) | 세포 내부 대사물을 가역적으로 공급/배출하는 경계 반응 |
| 바이오매스 목적함수 | Biomass Objective Function (BOF) | 세포 조성비대로 전구체를 소비해 1 gDW를 생성하는 의사-반응 |
| 성장 관련 유지 에너지 | Growth-Associated Maintenance (GAM) | 성장률에 비례해 소비되는 ATP (BOF 계수에 내장) |
| 비성장 관련 유지 에너지 | Non-Growth-Associated Maintenance (NGAM) | 성장률 0에서도 필요한 기저 ATP 요구량 |

---

## 참고문헌 / 더 읽을거리

- Monk, J. M. et al. (2017). *iML1515, a knowledgebase that computes Escherichia coli traits.* Nature Biotechnology, 35(10), 904–908.
- Brunk, E. et al. (2018). *Recon3D enables a three-dimensional view of gene variation in human metabolism.* Nature Biotechnology, 36(3), 272–281.
- Thiele, I. et al. (2013). *A community-driven global reconstruction of human metabolism (Recon 2).* Nature Biotechnology, 31(5), 419–425.
- Robinson, J. L. et al. (2020). *An atlas of human metabolism.* Science Signaling, 13(624), eaaz1482.
- Duarte, N. C. et al. (2007). *Global reconstruction of the human metabolic network based on genomic and bibliomic data.* PNAS, 104(6), 1777–1782.
- Feist, A. M., & Palsson, B. O. (2010). *The biomass objective function.* Current Opinion in Microbiology, 13(3), 344–349.
- Thiele, I., & Palsson, B. Ø. (2010). *A protocol for generating a high-quality genome-scale metabolic reconstruction.* Nature Protocols, 5(1), 93–121.
- Palsson, B. Ø. (2015). *Systems Biology: Constraint-based Reconstruction and Analysis.* Cambridge University Press.
- Ebrahim, A. et al. (2013). *COBRApy: COnstraints-Based Reconstruction and Analysis for Python.* BMC Systems Biology, 7, 74.
- 본 챕터의 실습 코드 전체: `raw_data/GEM_lecture_notes/gem9_w02_lab.ipynb`
