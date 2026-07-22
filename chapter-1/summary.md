# Chapter 1 요약과 연습문제

## 핵심 정리

- 대사는 물질, 자유에너지와 환원력을 획득·전환·배분·배출하는 화학 반응의 총체이다. [GEM](../glossary.md)은 이 생화학 전체가 아니라 근거가 있는 대사·수송·경계·의사반응을 선택한 계산 표현이다.
- 대사물은 구분 가능한 화학종, 반응은 화학량론적 변환, [플럭스](../glossary.md)는 단위 시간당 반응 진행률이다. 플럭스와 대사물 농도, 화학량론 계수와 효소 활성은 서로 다른 양이다.
- 구조적 대체 경로는 잠재적 강건성을 제공하지만, 유전자 발현, 열역학, 보조인자 재생 및 효소 용량이 허용될 때만 실제 우회 플럭스를 형성한다.
- 네트워크의 degree와 essentiality는 동일하지 않으며, [통화 대사물](../glossary.md)의 포함과 그래프 투영법이 위상 지표에 큰 영향을 준다.
- [재구축](../glossary.md)은 반응·대사물·[GPR](../chapter-3/README.md)·[구획](../glossary.md)과 그 근거를 정리한 지식베이스이다. 여기에 배지, bounds, [대사 작업](../glossary.md)과 [목적함수](../glossary.md)를 부여하면 특정 질문에 대한 조건부 계산 모델이 된다.
- 표준 [FBA](../chapter-4/README.md)는 내부 대사물의 순축적을 무시하여 $$\mathbf S\mathbf v=\mathbf0$$을 적용한다. 이는 화학평형이나 영 플럭스를 뜻하지 않으며, 과도 상태와 저장물질 축적에는 별도의 동역학 표현이 필요하다.
- [제약 기반 모델](../glossary.md)은 가능한 정상 상태 집합을, [동역학 모델](../glossary.md)은 속도식과 초기조건 아래의 시간 궤적을 분석한다. [ecGEM](../glossary.md), ME-model, 오믹스 통합과 [dynamic FBA](../glossary.md)는 서로 다른 정보를 추가하는 방법이며 하나의 우열 순서가 아니다.
- 모델은 생화학적 범위, 시스템 경계, 수학적 형식과 맥락화 수준으로 기술한다. 반응·대사물 수는 생물 종의 고정 특성이 아니라 특정 릴리스와 집계 규칙의 속성이다.
- 대사모델링은 증거 수집, 재구축, 품질관리, 조건 설정, 분석, 독립 검증과 갱신이 반복되는 연구 절차이다. 계산 결과는 실험을 대체하지 않고 검증할 가설을 구조화한다.

## 연습문제

### 정의와 기호

1. 대사물, 반응, 화학량론 계수와 플럭스를 각각 한 문장으로 정의하고, GEM에서 대응하는 행렬·벡터 요소를 쓰시오.

2. 반응

   $$
   2A+B\rightarrow C+3D
   $$

   에 대해 대사물 순서가 $$(A,B,C,D)$$일 때 화학량론 열벡터를 작성하시오. 이 벡터의 숫자가 반응 속도를 나타내지 않는 이유도 설명하시오.

3. “정상 상태이므로 모든 반응의 순플럭스가 0이다”라는 주장의 오류를 화학평형과 개방계 정상 상태의 차이를 이용해 설명하시오.

### 계산과 비교

4. 모델 artifact에서 확인한 유전자 후보 수를 $$n$$이라고 하자. $$n=10$$인 교육용 예에서 가능한 이중 결손 조합 수를 계산하시오. 실제 GEM 스크리닝에서는 모델 릴리스·GPR·필수 유전자 사전 제외·조건별 실행 가능성에 따라 후보 수가 달라지는 이유를 각각 하나씩 제시하시오. 특정 iML1515 릴리스의 유전자 수를 쓰려면 먼저 모델 파일의 tag·checksum·집계 규칙을 기록하시오.

5. 다음 두 연구 질문에 적합한 1차 모델링 접근을 선택하고 필요한 추가 자료를 쓰시오.

   - 일정 배지에서 유전자 결손 후 가능한 성장률과 분비 플럭스 범위
   - 약물 투여 직후 30분 동안 세포 내 ATP와 젖산 농도의 시간 변화

6. 다음 세 모델을 생화학적 범위, 시스템 경계, 수학적 형식과 맥락화 수준으로 기술하시오.

   - COBRApy `textbook`
   - Human1에서 추출한 환자별 간세포 모델
   - AGORA2 재구축으로 구성한 표본별 장내 미생물군 모델

### 비판적 해석

7. “ATP는 대사 네트워크에서 degree가 가장 높은 대사물 중 하나이므로 ATP와 연결된 모든 반응은 필수이다”라는 주장을 비판하시오. 그래프 표현, 통화 대사물 및 조건부 필수성을 답에 포함하시오.

8. 어떤 연구가 “GEM으로 암세포의 대사물 농도를 정확히 예측했다”고 보고했다. 이 주장을 평가하기 위해 논문에서 확인해야 할 모델 종류, 입력 자료, 출력 단위와 검증 자료를 네 가지 이상 제시하시오.

9. 아래 코드를 실행하기 전에 예상되는 객체 수를 기록한 뒤 실제 출력과 비교하시오. 이어서 모델 ID, COBRApy 버전, solver와 목적함수를 함께 출력하도록 코드를 확장하시오.

   ```python
   import cobra

   model = cobra.io.load_model("textbook")
   print(len(model.reactions), len(model.metabolites), len(model.genes))
   ```

## 다음 장과의 연결

[Chapter 2](../chapter-2/README.md)는 반응식을 화학량론 행렬 $$\mathbf S$$로 변환하고, 내부 물질수지 $$\mathbf S\mathbf v=\mathbf0$$의 선형대수적 의미와 bounds를 적용한 가능 영역을 분석한다. Chapter 1에서 구분한 대사물·반응·플럭스의 단위와 모델 경계가 이후 모든 계산의 출발점이다.

## 핵심 용어

| 용어 | 정의 | 해석상의 주의 |
|:---|:---|:---|
| 대사(metabolism) | 생명체의 물질·에너지·환원력 전환 반응의 총체 | 영양분 분해에 한정되지 않음 |
| 대사물(metabolite) | 구획·전하 등을 포함해 구분한 화학종 | 동일 분자도 구획별로 별도 객체가 될 수 있음 |
| 반응(reaction) | 정해진 화학량론을 갖는 변환 또는 수송 | 효소·유전자와 일대일 대응하지 않음 |
| 플럭스(flux) | 단위 시간당 반응 진행률 | 농도나 분자 수가 아님 |
| 재구축(reconstruction) | 근거와 주석을 포함한 대사 네트워크 지식베이스 | 조건부 목적함수를 반드시 포함하는 것은 아님 |
| GEM | 유전체 범위의 대사 재구축을 계산 가능하게 형식화한 모델 | “모든 반응의 완전한 목록”을 뜻하지 않음 |
| GPR | 유전자 산물과 반응 가용성의 불리언 연관 | 유전자 발현량·효소 활성을 직접 뜻하지 않음 |
| [의사-정상 상태](../glossary.md) | 내부 대사물의 순축적을 무시하는 근사 | 화학평형과 구별해야 함 |
| FBA | 정상 상태와 bounds 아래 선형 목적을 최적화하는 방법 | 목적함수 가설과 대안 최적해가 존재함 |
| 동역학 모델 | 속도식과 초기조건으로 상태의 시간 변화를 계산하는 모델 | 매개변수 식별과 불확실성 검증이 필요함 |
| 구조적 대체성 | 같은 기능을 수행할 수 있는 둘 이상의 반응 집합 | 실제 우회 사용을 보장하지 않음 |
| 통화 대사물 | 많은 반응에서 에너지·환원력·화기를 전달하는 대사물 | 그래프 분석에서 연결성을 왜곡할 수 있음 |

## 참고문헌과 더 읽을거리

1. Savinell JM, Palsson BO (1992). Network analysis of intermediary metabolism using linear optimization. I. Development of mathematical formalism. *Journal of Theoretical Biology* 154, 421–454. [doi:10.1016/S0022-5193(05)80161-4](https://doi.org/10.1016/S0022-5193(05)80161-4).
2. Varma A, Palsson BO (1994). Stoichiometric flux balance models quantitatively predict growth and metabolic by-product secretion in wild-type *Escherichia coli* W3110. *Applied and Environmental Microbiology* 60, 3724–3731. [PubMed 7986045](https://pubmed.ncbi.nlm.nih.gov/7986045/).
3. Orth JD, Thiele I, Palsson BØ (2010). What is flux balance analysis? *Nature Biotechnology* 28, 245–248. [doi:10.1038/nbt.1614](https://doi.org/10.1038/nbt.1614).
4. Thiele I, Palsson BØ (2010). A protocol for generating a high-quality genome-scale metabolic reconstruction. *Nature Protocols* 5, 93–121. [doi:10.1038/nprot.2009.203](https://doi.org/10.1038/nprot.2009.203).
5. Monk JM et al. (2017). iML1515, a knowledgebase that computes *Escherichia coli* traits. *Nature Biotechnology* 35, 904–908. [doi:10.1038/nbt.3956](https://doi.org/10.1038/nbt.3956).
6. Robinson JL et al. (2020). An atlas of human metabolism. *Science Signaling* 13, eaaz1482. [doi:10.1126/scisignal.aaz1482](https://doi.org/10.1126/scisignal.aaz1482).
7. Lieven C et al. (2020). MEMOTE for standardized genome-scale metabolic model testing. *Nature Biotechnology* 38, 272–276. [doi:10.1038/s41587-020-0446-y](https://doi.org/10.1038/s41587-020-0446-y).
8. Heinken A et al. (2023). Genome-scale metabolic reconstruction of 7,302 human microorganisms for personalized medicine. *Nature Biotechnology* 41, 1320–1332. [doi:10.1038/s41587-022-01628-0](https://doi.org/10.1038/s41587-022-01628-0).
9. Chen Y et al. (2024). Reconstruction, simulation and analysis of enzyme-constrained metabolic models using GECKO Toolbox 3.0. *Nature Protocols* 19, 629–667. [doi:10.1038/s41596-023-00931-7](https://doi.org/10.1038/s41596-023-00931-7).
10. Luo J et al. (2026). Reconstruction of human metabolic models with large language models. *PNAS* 123, e2516511123. [doi:10.1073/pnas.2516511123](https://doi.org/10.1073/pnas.2516511123).

온라인 자료: [COBRApy documentation](https://cobrapy.readthedocs.io/) · [BiGG Models](https://bigg.ucsd.edu/) · [Human-GEM](https://github.com/SysBioChalmers/Human-GEM) · [MEMOTE](https://memote.io/)
