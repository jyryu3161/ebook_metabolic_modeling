# 마무리: 요약 · 스스로 점검 · 용어

## 한 장 요약

- **대사(Metabolism)**는 생명체가 에너지와 생체 분자를 생성·분해하는 모든 화학 반응의 총칭이며, 이들이 얽혀 만드는 **대사 네트워크**는 가장 단순한 자립 생존 세균에서도 수백 개 이상의 반응으로 구성되어 직관적 이해의 한계를 넘어선다. ATP·NADH 같은 **통화 대사물**은 네트워크 그래프에서 매우 높은 차수를 가진 허브로 작동하며, 대사 네트워크는 이런 소수의 허브와 다수의 저차수 대사물로 이루어진 구조를 갖는다.
- 이 복잡성 때문에 **예측(조합적 폭발) · 시스템적 이해(창발적 행동) · 응용**이라는 세 가지 필요에서 계산 모델, 즉 **게놈 규모 대사 모델(GEM)**이 요구된다.
- GEM은 화학량론 행렬, GPR, 생물량 반응, 교환 반응으로 구성되며, **의사-정상 상태 가정**($$\frac{d\mathbf{x}}{dt}=\mathbf{0}$$)을 핵심 전제로 삼는다. 모델을 만드는 과정은 "모델링"이 아니라 지식 조립으로서의 **재구축**이라 불린다.
- 대사를 계산적으로 다루는 두 축은 **제약 기반 모델링(CBM)**과 **동역학 모델링**이며, 전자는 게놈 규모 확장성을, 후자는 동적·농도 예측 능력을 제공하는 상호 보완 관계에 있다. 두 접근을 결합한 dFBA·ecGEM·ME-model 등 하이브리드 방법도 발전하고 있다.
- 대사 모델은 **범위**(경로 특이적 vs 게놈 규모 vs 커뮤니티), **수학적 프레임워크**(CBM vs 동역학 vs 효소 제약 vs 통합), **생물학적 대상**(미생물 vs 인체 vs 미생물군집)이라는 세 축으로 분류할 수 있다.
- 대사 모델링의 35년 역사는 **Pre-genome(1990–1997) → 게놈 시대(1998–2007) → 확장과 정제(2008–2017) → 현대(2018–현재)**의 4개 시대로 구분되며, 반응 수의 지수적 성장·정확도 향상·커뮤니티 주도 개발·자동화·생태계로의 확장이라는 패턴을 보인다.
- 하나의 GEM이 완성되어 응용되기까지는 **재구축 → 구조화 → 제약 설정 → 시뮬레이션 → 검증 → (조건 특이화) → 응용**의 반복적 워크플로를 거치며, 각 단계는 이 책의 Chapter 2~9가 각각 담당한다.
- COBRApy로 모델을 불러오는 한 줄의 코드(`cobra.io.load_model("textbook")`)는 이 모든 이론이 실제로 작동하는 소프트웨어로 구현되어 있음을 보여주는 첫걸음이며, 이렇게 불러온 `e_coli_core` 모델은 이 책 전체에서 계속 다시 만나게 될 동반 모델이다.

---

## 스스로 점검

1. **개념 확인**: "대사 네트워크의 중복성(redundancy)"이 세포에게 주는 이점을 한 문장으로 설명하고, 본문에서 다룬 대장균의 포도당→피루브산 경로 3가지 이름을 적어보세요.
   > *힌트*: §1.2를 참고하세요. 중복 경로가 있으면 한 경로가 막혀도 대안 경로로 생존할 수 있습니다(강건성).

2. **개념 확인**: "의사-정상 상태 가정"이 "대사가 멈췄다"는 뜻이 아닌 이유를 싱크대 비유를 들어 설명해 보세요.
   > *힌트*: §3.3의 hint 박스를 참고하세요. 유입량 = 유출량이면 농도는 일정하게 유지되지만 흐름 자체는 계속됩니다.

3. **비교/판단**: 어떤 연구팀이 "특정 항암제 후보 물질의 농도에 따라 암세포 내 대사물 농도가 시간에 따라 어떻게 변하는지"를 예측하고 싶어 합니다. 제약 기반 모델(GEM)과 동역학 모델 중 어느 쪽이 더 적합할까요? 이유는?
   > *힌트*: §4.3의 비교표에서 "대사물 농도 예측"과 "과도적 동역학 예측" 행을 확인하세요. 답: 동역학 모델. GEM은 통량만 예측하고 농도의 시간적 변화는 예측할 수 없기 때문입니다.

4. **역사 이해**: iJE660(2000) → iJR904(2003) → iAF1260(2007) → iJO1366(2011) → iML1515(2017)로 이어지는 *E. coli* 모델 계보에서, 반응 수는 어떻게 변했으며 그 사이 유전자 필수성 예측 정확도는 어떻게 달라졌나요?
   > *힌트*: §6.2~6.3의 각 모델 소개와 §6.5의 "정확도의 점진적 향상" 단락을 참고하세요.

5. **코드 예측**: 아래 코드를 실행하면 무엇이 출력될지 실행 전에 예측해 보세요. (힌트: 본문의 실습 코드와 §3.1의 e_coli_core 통계를 참고하세요.)
   ```python
   import cobra
   model = cobra.io.load_model("textbook")
   print(len(model.reactions), len(model.metabolites), len(model.genes))
   ```
   > *힌트*: §9(실습)의 기대 출력과 동일해야 합니다 — `95 72 137`.

6. **계산 연습**: 대장균 유전자가 4,400개라 할 때, 서로 다른 두 유전자를 동시에 없애는 조합(이중 결손)의 총 가짓수를 직접 계산해 보세요.
   > *힌트*: §2.1의 $$\binom{n}{2} = \frac{n(n-1)}{2}$$ 공식을 사용하세요. 답: 약 970만 가지.

7. **개념 확인**: "통화 대사물(currency metabolite)"이 무엇이며, 이런 대사물의 차수(degree)가 왜 다른 대사물보다 높은지 설명해 보세요.
   > *힌트*: §1.3(그래프로 본 대사 네트워크)의 ATP·NADH 예시를 참고하세요.

---

## 다음 장 예고

이 장에서 우리는 대사가 무엇인지, 왜 이를 모델링해야 하는지, GEM이 무엇이고 어떤 가정 위에 서 있는지, 그리고 이 분야가 지난 35년간 어떻게 발전해 왔는지를 큰 그림으로 살펴보았습니다. 아직 우리는 실제로 계산을 해본 적이 없습니다 — 반응 목록과 개수만 확인했을 뿐입니다.

생명체의 대사 지도를 컴퓨터가 실제로 다루려면, 먼저 이 수천 개의 반응을 사람의 언어(화학식)가 아니라 **숫자와 행렬**로 옮겨야 합니다. 다음 [Chapter 2. 생화학 반응과 대사 네트워크 표현](../chapter-2/README.md)에서는, 오늘 만난 `e_coli_core` 모델의 반응들을 화학량론 행렬 $$\mathbf{S}$$(72개 대사물 × 95개 반응)로 바꾸는 법을 배우고, PGI 반응 하나가 이 행렬의 한 열로 어떻게 표현되는지 직접 확인해 봅니다. 그 다음에야 비로소 $$\mathbf{S}\mathbf{v}=\mathbf{0}$$이라는, 이 책 전체를 관통하는 핵심 방정식의 의미를 제대로 이해할 수 있게 됩니다.

---

## 핵심 용어 정리

| 용어 (한글) | 용어 (English) | 정의 | 관련 챕터 |
|:---|:---|:---|:---|
| 대사 | Metabolism | 생명체가 영양분을 에너지와 세포 구성 성분으로 전환하는 모든 화학 반응의 총칭 | Ch1 |
| 대사 네트워크 | Metabolic Network | 반응과 대사물이 상호 연결되어 형성하는 네트워크 | Ch1, Ch2 |
| 강건성 | Robustness | 경로 중복 등으로 인해 외부 교란에도 기능을 유지하는 성질 | Ch1 |
| 게놈 규모 대사 모델 | Genome-scale Metabolic Model (GEM) | 게놈에서 추론된 모든 대사 반응을 수학적으로 표현한 모델 | Ch1, Ch3 |
| 재구축 | Reconstruction | 게놈 주석·데이터베이스·문헌·실험 데이터를 통합해 대사 모델을 조립하는 과정 | Ch1, Ch5 |
| 의사-정상 상태 가정 | Pseudo-Steady-State Assumption | 관심 시간 척도에서 세포 내 대사물 농도의 순 변화가 0이라는 가정 | Ch1, Ch2 |
| 제약 기반 모델링 | Constraint-Based Modeling (CBM) | 물리화학적·생물학적 제약을 통해 대사 네트워크를 분석하는 방법론 | Ch1, Ch4 |
| 동역학 모델링 | Kinetic Modeling | 반응 속도를 효소·기질 농도의 함수로 표현하는 ODE 기반 모델링 | Ch1 |
| 통량 균형 분석 | Flux Balance Analysis (FBA) | 선형 계획법을 이용해 정상 상태 통량 분포를 예측하는 CBM 방법 | Ch1, Ch4 |
| 효소 제약 GEM | enzyme-constrained GEM (ecGEM) | 효소 농도·회전수를 추가 제약으로 통합한 GEM (예: GECKO) | Ch1 |
| 미생물군집 모델 | Community Metabolic Model | 여러 종/균주의 GEM을 연결해 상호작용을 모사하는 모델 (예: AGORA2) | Ch1, Ch6 |
| 통화 대사물 | Currency Metabolite | ATP, NADH 등 다수의 반응에 반복해서 관여하는 고차수(high-degree) 대사물 | Ch1, Ch2 |
| 창발적 행동 | Emergent Behavior | 개별 구성 요소의 성질만으로는 예측할 수 없는, 시스템 전체 수준에서만 나타나는 성질(예: 아세테이트 오버플로) | Ch1 |
| 조합적 폭발 | Combinatorial Explosion | 결손 유전자 수가 늘어날 때 검토해야 할 조합 수가 곱셈적으로 급증하는 현상 | Ch1 |

---

## 참고문헌 / 더 읽을거리

1. **Varma A, Palsson BO** (1994). "Stoichiometric flux balance models quantitatively predict growth and metabolic by-product secretion in wild-type Escherichia coli W3110." *Applied and Environmental Microbiology*, 60(10), 3724–3731.
2. **Edwards JS, Palsson BO** (2000). "The Escherichia coli MG1655 in silico metabolic genotype: Its definition, characteristics, and capabilities." *Proceedings of the National Academy of Sciences*, 97(10), 5528–5533. — iJE660
3. **Reed JL, Vo TD, Schilling CH, Palsson BO** (2003). "An expanded genome-scale model of Escherichia coli K-12 (iJR904 GSM/GPR)." *Genome Biology*, 4(9), R54.
4. **Forster J, Famili I, Fu P, Palsson BO, Nielsen J** (2003). "Genome-scale reconstruction of the Saccharomyces cerevisiae metabolic network." *Genome Research*, 13(2), 244–253. — iFF708
5. **Feist AM, Henry CS, Reed JL, et al.** (2007). "A genome-scale metabolic reconstruction for Escherichia coli K-12 MG1655 that accounts for 1260 ORFs and thermodynamic information." *Molecular Systems Biology*, 3, 121. — iAF1260
6. **Duarte NC, Becker SA, Jamshidi N, et al.** (2007). "Global reconstruction of the human metabolic network based on genomic and bibliomic data." *Proceedings of the National Academy of Sciences*, 104(6), 1777–1782. — Recon 1
7. **Orth JD, Conrad TM, Na J, et al.** (2011). "A comprehensive genome-scale reconstruction of Escherichia coli metabolism–2011." *Molecular Systems Biology*, 7, 535. — iJO1366
8. **Thiele I, Palsson BØ** (2010). "A protocol for generating a high-quality genome-scale metabolic reconstruction." *Nature Protocols*, 5(1), 93–121. — 96단계 재구축 프로토콜
9. **Thiele I, Swainston N, Fleming RMT, et al.** (2013). "A community-driven global reconstruction of human metabolism." *Nature Biotechnology*, 31(5), 419–425. — Recon 2
10. **Monk JM, Lloyd CJ, Brunk E, et al.** (2017). "iML1515, a knowledgebase that computes Escherichia coli traits." *Nature Biotechnology*, 35(10), 904–908.
11. **Brunk E, Sahoo S, Zielinski DC, et al.** (2018). "Recon3D enables a three-dimensional view of gene variation in human metabolism." *Nature Biotechnology*, 36(3), 272–281.
12. **Lu H, Li F, Sánchez BJ, et al.** (2019). "A consensus S. cerevisiae metabolic model Yeast8 and its ecosystem for comprehensively probing cellular metabolism." *Nature Communications*, 10, 3586.
13. **Robinson JL, Kocabas P, Wang H, et al.** (2020). "An atlas of human metabolism." *Science Signaling*, 13(624), eaaz1482. — Human1
14. **Ebrahim A, Lerman JA, Palsson BO, Hyduke DR** (2013). "COBRApy: Constraints-Based Reconstruction and Analysis for Python." *BMC Systems Biology*, 7, 74.
15. **Lieven C, Beber ME, Olivier BG, et al.** (2020). "MEMOTE for standardized genome-scale metabolic model testing." *Nature Biotechnology*, 38(3), 272–276.
16. **Palsson BØ** (2015). *Systems Biology: Constraint-based Reconstruction and Analysis*, 2nd Edition, Cambridge University Press. — 대사 모델링의 바이블
17. **Klipp E, et al.** (2016). *Systems Biology in Practice: Concepts, Implementation and Application*, Wiley-VCH.
18. **Stephanopoulos G, Aristidou AA, Nielsen J** (1998). *Metabolic Engineering: Principles and Methodologies*, Academic Press.
19. **Savinell JM, Palsson BO** (1992). "Network analysis of intermediary metabolism using linear optimization. I. Development of mathematical formalism." *Journal of Theoretical Biology*, 154, 421–454. DOI: [10.1016/S0022-5193(05)80161-4](https://doi.org/10.1016/S0022-5193(05)80161-4).
20. **Chen Y, Gustafsson J, Rangel AET, et al.** (2024). "Reconstruction, simulation and analysis of enzyme-constrained metabolic models using GECKO Toolbox 3.0." *Nature Protocols*, 19, 629–667. DOI: [10.1038/s41596-023-00931-7](https://doi.org/10.1038/s41596-023-00931-7).
21. **Luo J, et al.** (2026). "Reconstruction of human metabolic models with large language models." *PNAS*, 123(15), e2516511123. DOI: [10.1073/pnas.2516511123](https://doi.org/10.1073/pnas.2516511123). — Human2

> 온라인 자료: [COBRApy 문서](https://cobrapy.readthedocs.io) · [BiGG Models](http://bigg.ucsd.edu) · [Human-GEM (Human1/Human2) GitHub](https://github.com/SysBioChalmers/Human-GEM) · [yeast-GEM GitHub](https://github.com/SysBioChalmers/yeast-GEM) · [MEMOTE](https://memote.io)
