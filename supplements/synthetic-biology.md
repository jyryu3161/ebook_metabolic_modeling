# 보충 학습. 합성생물학에서 GEM 기반 세포공장까지

> 합성생물학의 역사, 설계 원리, 대표 유전자 회로와 합성 게놈, 바이오센서·치료 미생물·biofoundry를 살펴보고 GEM 기반 균주 설계가 전체 DBTL 주기에서 맡는 역할을 연결합니다. 원 강의의 **Synthetic Biology**와 OT의 산업·지속가능성 내용을 통합했습니다.

## 1. 합성생물학은 무엇을 설계하는가

합성생물학(synthetic biology)은 자연에 없던 생물학적 **parts, devices, circuits, systems**를 설계·구축하거나 기존 시스템을 원하는 기능으로 재설계하는 분야입니다. 세포를 완벽한 디지털 컴퓨터로 볼 수는 없지만, 입력 신호를 감지하고 논리적으로 처리해 출력 분자를 만드는 “프로그래밍 가능한 시스템”으로 다룹니다.

```text
센서 promoter → 조절 회로 → effector gene/pathway → 측정 가능한 출력
       입력              계산                    출력
```

GEM은 이 가운데 대사 경로와 자원 배분을 계산하는 설계 모델입니다. “회로가 켜지는가?”뿐 아니라 “켜졌을 때 탄소·ATP·NADPH가 충분하고 세포가 계속 자랄 수 있는가?”를 묻습니다.

## 2. 역사: 자연 회로의 이해에서 게놈·진화 설계로

| 시기 | 이정표 | 남긴 개념 |
|:---|:---|:---|
| 1961 | Jacob–Monod의 lac operon | 유전자가 조절 회로처럼 상호작용한다는 토대 |
| 1970–1980년대 | recombinant DNA, gene cloning, PCR | DNA를 분리·증폭·재조합하는 제작 기술 |
| 1990년대 | genome sequencing과 omics | 시스템 전체를 측정하고 모델링하는 systems biology |
| 2000 | toggle switch, repressilator | 인공 회로가 기억과 진동을 구현할 수 있음을 입증 |
| 2010 | JCVI-syn1.0 | 합성한 게놈이 세포를 제어할 수 있음을 입증 |
| 2013 | artemisinic acid 생산 효모 | 합성생물학의 산업적 scale-up 사례 |
| 2016 | Cello, JCVI-syn3.0 | 회로 설계 자동화와 최소 게놈 |
| 2020년대 | ALE·biofoundry·continuous evolution | 대규모 자동화와 탐색·학습의 가속 |

### 2.1 lac operon: 자연의 조건부 스위치

lac operon에서 LacI 억제자는 유당이 없을 때 전사를 막고, 유당 유도체가 존재하면 억제가 풀립니다.

- `lacZ`: lactose를 분해하는 β-galactosidase
- `lacY`: lactose를 세포 안으로 들이는 permease
- `lacA`: transacetylase

이 회로는 센서·조절자·대사 효소가 하나의 기능 단위로 연결되는 원형을 보여줍니다.

### 2.2 toggle switch: 세포 기억

Gardner, Cantor, Collins(2000)의 toggle switch는 LacI와 TetR 같은 두 억제자가 서로의 발현을 억제하도록 구성합니다. 한쪽이 높고 다른 쪽이 낮은 두 안정 상태가 존재하며, 외부 유도 신호가 상태를 전환합니다. 신호가 사라져도 상태가 유지되므로 **bistability와 cellular memory**를 구현합니다.

### 2.3 repressilator: 합성 진동

Elowitz와 Leibler(2000)는 세 억제자가 고리 모양으로 다음 유전자를 억제하는 회로를 만들어 시간에 따른 단백질 발현 진동을 보였습니다. 이 연구는 음성 되먹임과 지연이 생물학적 리듬을 만들 수 있음을 보여주었지만, 세포 간 주기·진폭 변동도 함께 드러내 합성 회로의 noise 문제를 부각했습니다.

## 3. 합성 게놈과 최소 세포

- **JCVI-syn1.0(2010)**은 약 1.08 Mb의 *Mycoplasma mycoides* 게놈을 합성해 수용 세포에 이식하고, 합성 게놈이 세포의 자기복제와 표현형을 제어함을 보였습니다. 핵심은 “완전히 새로운 생명 설계”보다 genome-scale DNA synthesis와 transplantation의 원리 증명입니다.
- **JCVI-syn3.0(2016)**은 생존 가능한 최소 유전자 집합을 찾는 반복적 설계로 531 kb, 473개 유전자의 세포를 만들었습니다. 그러나 분열 이상은 “생존에 필수”와 “정상 형태·강건성에 필요”가 다름을 보여주었습니다.
- **JCVI-syn3A**는 일부 유전자를 되돌려 정상적인 형태와 분열을 회복한 최소 세포 계열입니다.

최소 게놈 연구는 유전자 필수성이 배지·환경·상호작용에 조건부라는 GEM의 핵심 교훈과 맞닿습니다. 모델에서 필수라고 해도 배지에 대사물을 보충하면 비필수가 될 수 있습니다.

## 4. 세 가지 공학 원리

### 4.1 추상화(abstraction)

불필요한 세부를 숨기고 적절한 계층에서 설계합니다.

```text
DNA sequence → part → device → circuit → cell/system → bioprocess
```

GEM도 모든 원자 운동을 계산하지 않고 반응 화학량론·bounds·목적함수로 대사를 추상화합니다.

### 4.2 표준화(standardization)

공통 측정 단위, 조립 규격, 데이터 형식과 성능 보고법을 사용해 다른 실험실의 부품과 모델을 교환합니다. BioBricks는 promoter, RBS, coding sequence, terminator 같은 DNA part를 표준화해 조립·재사용하려는 대표적 운동입니다. GEM에서는 SBML, BiGG ID, MIRIAM, MEMOTE가 같은 역할을 합니다.

### 4.3 모듈성(modularity)

복잡한 시스템을 상대적으로 독립적인 모듈로 나누고 조합합니다. 하지만 생물학적 모듈은 완전히 독립적이지 않습니다. ribosome, ATP, NADPH, membrane space를 공유하는 **resource competition**과 host burden 때문에 단독으로 잘 작동한 회로가 조합 후 실패할 수 있습니다. GEM과 enzyme-constrained model은 이 숨은 결합을 점검하는 데 유용합니다.

## 5. Parts → devices → systems

| 계층 | 정의 | 예 |
|:---|:---|:---|
| Part | 정의된 기본 DNA 기능 | promoter, RBS, CDS, terminator |
| Device | 여러 part가 만든 기능 단위 | biosensor, toggle switch |
| Circuit | 여러 device의 논리·동적 연결 | oscillator, AND gate |
| System | 회로·대사·숙주·공정의 통합 | 치료 미생물, 생산 세포공장 |

BioBricks의 LEGO 비유는 재사용성을 설명하지만, 실제 part의 동작은 서열 주변부, copy number, 숙주, 성장 단계와 배지에 따라 달라집니다. 따라서 표준 part라도 새로운 맥락에서 다시 특성화해야 합니다.

## 6. DBTL과 설계 자동화

합성생물학의 기본 작업 주기는 다음과 같습니다.

1. **Design**: 목표 기능, 회로, 대사 경로와 조작 후보를 설계합니다.
2. **Build**: DNA를 합성·조립하고 숙주에 도입합니다.
3. **Test**: 성장, 발현, titer, rate, yield, 안정성을 측정합니다.
4. **Learn**: 실패와 성공 데이터를 모델에 반영해 다음 설계를 개선합니다.

**Cello**는 논리 회로 사양과 특성화된 gate library를 받아 DNA 회로를 자동 설계하는 전자설계자동화(EDA)식 접근을 보여주었습니다. GEM 기반 OptKnock·FSEOF는 대사 경로의 Design 단계를, 오믹스·flux 측정은 Test와 Learn을 지원합니다.

```mermaid
flowchart LR
    A[Design<br/>GEM·회로 모델] --> B[Build<br/>DNA 조립·편집]
    B --> C[Test<br/>성장·발현·titer·yield]
    C --> D[Learn<br/>통계·ML·모델 갱신]
    D --> A
```

## 7. 적응진화와 연속 진화

**ALE(Adaptive Laboratory Evolution)**는 원하는 선택압 아래 세포를 여러 세대 배양해 성장·내성·기질 이용을 개선합니다. 계산 설계가 “어떤 변화가 유리한가”를 제안한다면 ALE는 세포가 미처 모델링하지 못한 조절·돌연변이 공간을 탐색합니다. 결과 변이가 인과적인지는 역유전학 검증이 필요합니다.

**T7-ORACLE(2025)**은 숙주 게놈과 분리된 T7 기반 복제계가 원형 plasmid의 목표 유전자만 빠르게 돌연변이시키는 연속진화 플랫폼입니다. 보고된 돌연변이율은 숙주 게놈 배경보다 약 100,000배 높았고, TEM-1 β-lactamase의 새로운 기질 활성을 1주 이내에 크게 향상시켰습니다. 중요한 점은 “수십만 년을 정확히 시뮬레이션”한 것이 아니라, 매 세포 분열마다 목표 서열의 mutation–selection 주기를 반복해 실험실 탐색을 가속했다는 것입니다.

## 8. 대표 응용

### 8.1 의약품과 비천연 화합물 생산

Paddon et al.(2013)은 효모의 mevalonate·artemisinic acid 경로를 공학적으로 개선해 반합성 artemisinin 공급을 산업 규모로 확장했습니다. Galanie et al.(2015)은 식물 효소 경로를 효모에 이식해 opioid 계열 생합성의 가능성을 보였습니다.

비천연 화합물 설계는 보통 다음 순서로 진행됩니다.

```text
목표 화합물
 → retrosynthesis로 가능한 반응 경로 탐색
 → 효소 후보·EC·서열 선택
 → 숙주 대사망에 경로 삽입
 → GEM으로 전구체/보조인자/성장 trade-off 평가
 → 유전자 편집·배양 최적화
```

### 8.2 whole-cell biosensor

센서 회로는 arsenic, 중금속, 독소, 병원체 신호나 질병 biomarker를 감지해 색·빛·전기화학 신호를 냅니다. 예를 들어 ArsR 기반 회로는 arsenic이 억제자를 해제하면 `lacZ`를 발현하고, β-galactosidase가 전기화학적으로 측정 가능한 산물을 생성하도록 설계할 수 있습니다.

### 8.3 동적 대사 제어

성장기에는 biomass를, 생산기에는 목표 경로를 켜는 toggle이나 sensor-actuator 회로를 사용하면 성장–생산 충돌을 시간적으로 분리할 수 있습니다. oscillator는 효소 발현을 주기화해 독성 또는 부담을 낮출 수 있지만, 진동의 동기화와 공정 scale-up이 과제입니다.

### 8.4 병원체 감지·살상 치료 미생물

engineered probiotic은 병원체의 quorum-sensing 신호를 감지하고 lysis·bacteriocin 같은 effector를 방출하도록 설계할 수 있습니다. *P. aeruginosa*의 AHL을 감지해 pyocin을 방출하는 *E. coli* 회로가 대표적 개념입니다. 실제 치료로 옮기려면 off-target, 진화적 안정성, 생물안전, containment를 검증해야 합니다.

## 9. Biofoundry와 산업화

**biofoundry**는 자동화된 설계·DNA 제작·배양·고속 측정·데이터 분석을 연결해 수많은 설계를 병렬로 DBTL하는 시설·플랫폼입니다. Ginkgo Bioworks 같은 기업형 foundry는 다양한 고객의 설계를 공통 자동화 인프라에서 실행한다는 점에서 반도체 foundry와 비슷하지만, 생물학적 변이와 맥락 의존성을 다뤄야 한다는 차이가 있습니다.

산업화에서 동시에 최적화할 지표는 다음과 같습니다.

- titer: 최종 산물 농도
- rate/productivity: 시간당 생산량
- yield: 기질 대비 산물 수율
- growth·stability: 숙주 생존과 장기 유전적 안정성
- downstream recovery와 원가

## 10. 바이오기술의 색과 지속가능성

색상 분류는 문헌마다 조금 다르지만, 흔히 red biotechnology는 의료, green은 농업, white는 산업, blue는 해양 생명공학을 가리킵니다. GEM과 합성생물학은 이 모든 분야에 쓰이므로 색을 고정된 경계보다 응용 지형으로 이해하는 편이 낫습니다.

미생물 세포공장은 재생 가능한 탄소원, 낮은 온도·압력, 효소 선택성, 자기복제라는 장점이 있어 SDG의 건강·청정에너지·책임 있는 생산·기후 대응과 연결될 수 있습니다. 그러나 feedstock의 토지·물 사용, 에너지 믹스, 정제 공정, biosafety까지 포함한 life-cycle assessment 없이 “bio-based = 자동으로 지속가능”이라고 결론 내리면 안 됩니다.

## 11. GEM이 맡는 역할과 맡지 못하는 역할

| 질문 | GEM의 기여 | 추가로 필요한 것 |
|:---|:---|:---|
| 목표 산물 최대 이론수율 | carbon·redox·energy balance | kinetic·toxicity 정보 |
| KO/증폭 후보 | OptKnock, FSEOF, MCS | 조절·편집 가능성 검증 |
| 배지와 기질 선택 | exchange bound, production envelope | 공정 전달·원가 모델 |
| 회로가 대사 부담을 만드는가 | enzyme/resource constraint로 일부 평가 | transcription/translation model |
| 진화적 안정성 | 대체 경로와 성장 결합 분석 | 장기 ALE·population model |

## 다음 읽기

- 세포공장 균주 설계와 production envelope: [Chapter 8](../chapter-8..md)
- 재구축·효소 기능 주석: [Chapter 5](../chapter-5..md)
- 오믹스와 AI 기반 Learn 단계: [Chapter 6](../chapter-6.-omics.md), [Chapter 9](../chapter-9.-ai.md)
- 미생물 생장과 flux 단위: [준비 학습 A](microbial-growth-metabolism.md)

## 대표 논문

1. Gardner, T. S., Cantor, C. R., & Collins, J. J. (2000). [Construction of a genetic toggle switch in *Escherichia coli*](https://doi.org/10.1038/35002131). *Nature*, 403, 339–342.
2. Elowitz, M. B., & Leibler, S. (2000). [A synthetic oscillatory network of transcriptional regulators](https://doi.org/10.1038/35002125). *Nature*, 403, 335–338.
3. Gibson, D. G. et al. (2010). [Creation of a bacterial cell controlled by a chemically synthesized genome](https://doi.org/10.1126/science.1190719). *Science*, 329, 52–56.
4. Hutchison, C. A. et al. (2016). [Design and synthesis of a minimal bacterial genome](https://doi.org/10.1126/science.aad6253). *Science*, 351, aad6253.
5. Paddon, C. J. et al. (2013). [High-level semi-synthetic production of the potent antimalarial artemisinin](https://doi.org/10.1038/nature12051). *Nature*, 496, 528–532.
6. Nielsen, A. A. K. et al. (2016). [Genetic circuit design automation](https://doi.org/10.1126/science.aac7341). *Science*, 352, aac7341.
7. Diercks, C. S. et al. (2025). [An orthogonal T7 replisome for continuous hypermutation and accelerated evolution in *E. coli*](https://doi.org/10.1126/science.adp9583). *Science*, 389, 618–622.
