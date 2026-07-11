# 그림 출처·재현성 장부

이 문서는 출판 원고가 직접 참조하는 raster 자산, 그에 대응하는 SVG 원본, 그리고 Chapter 1·5·8–10의 주요 Mermaid 도식을 추적합니다. 자산·링크·권리 문구의 최종 검증일은 **2026-07-10**입니다.

## 적용 원칙

- `출처: 저자 자체 제작`은 외부 논문의 그림 파일·레이아웃을 복제하거나 변형하지 않고, 본문 수식·코드·인용 문헌의 개념을 바탕으로 새로 그렸다는 뜻입니다.
- 개념 원출처의 라이선스는 **그 논문 자체**에 적용됩니다. 독립적으로 만든 본 교재 도식에 자동으로 이전되지 않습니다.
- 저장소 루트에는 별도의 `LICENSE`, `COPYING`, `NOTICE`가 없습니다. 따라서 저자 자체 제작 자산의 제3자 재사용 조건은 현재 **미선언** 상태이며, 공개 배포 전에 교재 전체 라이선스를 별도로 결정해야 합니다.
- 외부 논문의 그림은 현재 원고에 직접 포함하지 않습니다. CC BY-NC-ND 또는 출판사 저작권 자료는 사실·방법 인용에만 사용하며 번역·트레이싱·재구성하지 않습니다.
- 다만 퍼블릭 도메인(PD)·CC0 **실물 사진**은 출처와 라이선스를 표기하고 원고에 직접 포함합니다. 이는 저작권이 있는 논문 그림과 구별되며, 각 파일의 개별 검증 결과는 아래 「퍼블릭 도메인 실물 사진」 표에 기록합니다.
- `raw_data/`의 그림은 출판 원고에서 참조하지 않고 Git에서도 제외되므로 이 장부의 출판 자산으로 보지 않습니다. `.gitbook/assets/fig2_gem_workflow.png`도 현재 본문에서 참조하지 않으므로 제외했습니다.

## 공통 생성 환경

`assets/figures/`의 일곱 자산은 다음 명령으로 PNG와 SVG를 함께 다시 만듭니다.

```bash
python scripts/generate_optimization_figures.py
```

생성 코드는 [`scripts/generate_optimization_figures.py`](scripts/generate_optimization_figures.py)입니다. 모식도 네 종은 스크립트에 적힌 좌표·수식에서 직접 그리며 solver를 호출하지 않습니다. 계산 그림 세 종은 COBRApy 0.30.0의 `cobra.io.load_model("textbook")`으로 불러온 [BiGG `e_coli_core`](http://bigg.ucsd.edu/models/e_coli_core)(72 metabolites, 95 reactions, 137 genes), 모델의 기본 배지와 biomass 목적함수, GLPK, `Configuration().processes = 1`을 사용합니다. GLPK의 세부 버전과 모델 파일 checksum은 생성 당시 기록되지 않았으므로, 다음 재생성 때 함께 고정해야 합니다.

COBRApy 코드는 [GPL/LGPL v2 이상 이중 라이선스](https://github.com/opencobra/cobrapy)입니다. [BiGG License](http://bigg.ucsd.edu/license)는 © 2019 The Regents of the University of California로, 저작권·라이선스 문구를 사본에 포함하는 조건 아래 교육·연구·비영리 목적의 사용·복사·수정·배포를 무상 허용하고 상업적 사용에는 별도 연락을 요구합니다. 본 저장소의 그래프는 모델 파일을 복사한 것이 아니라 계산 결과를 저자가 시각화한 것이지만, `e_coli_core` 모델을 배포물에 직접 포함할 때는 이 조건을 적용해야 합니다.

### 외부 문헌 권리 확인

| 문헌군 | 확인한 라이선스·권리 | 이 원고에서의 사용 |
|:---|:---|:---|
| MOMA([Segrè et al., 2002](https://doi.org/10.1073/pnas.232349399)), ROOM([Shlomi et al., 2005](https://doi.org/10.1073/pnas.0406346102)) | 공개 페이지에서 CC 재사용 라이선스를 확인하지 못한 PNAS 저작권 자료 | 수식·방법을 인용하고 독립 도식을 새로 제작. 원 그림 복제·변형 없음. |
| OptKnock([Burgard et al., 2003](https://doi.org/10.1002/bit.10803)) | Wiley 저작권 자료. 그림 재사용·변형에는 출판사 허락이 필요합니다. | 이중 수준 문제의 논리를 인용하고 독립 Mermaid를 제작. 원 그림 복제·변형 없음. |
| AMN, FlowGAT, FluxGAT, CHESHIRE | 각 논문 페이지의 [AMN CC BY 4.0](https://www.nature.com/articles/s41467-023-40380-0), [FlowGAT CC BY 4.0](https://www.nature.com/articles/s41540-024-00348-2), [FluxGAT CC BY 4.0](https://www.nature.com/articles/s41540-026-00738-8), [CHESHIRE CC BY 4.0](https://www.nature.com/articles/s41467-023-38110-7) 권리 문구 확인 | 개념과 사실만 인용. 허용 라이선스가 있더라도 논문 그림 자체는 가져오지 않았습니다. |
| CLOSEgaps([arXiv:2409.13259](https://arxiv.org/abs/2409.13259)), MuSHIN([Zhao et al., 2026](https://doi.org/10.1038/s42003-026-09761-1)) | **CC BY-NC-ND 4.0**. 비상업적 원문 공유는 허용하지만 수정·번역한 파생 자료 배포는 허용하지 않습니다. | 사실·방법·보고 수치만 인용. 그림·표를 번역, 트레이싱, 재구성하지 않았습니다. |
| Human2([Luo et al., 2026](https://doi.org/10.1073/pnas.2516511123)), ftINIT([Gustafsson et al., 2023](https://doi.org/10.1073/pnas.2217868120)) | **CC BY-NC-ND 4.0**. 수정·번역·도식 재구성에는 ND 제한이 적용됩니다. | 보고된 사실과 방법만 인용하고, 원 논문의 패널·레이아웃·그림을 사용하지 않은 독립 흐름도를 제작했습니다. |
| 균주 설계 RL([Sabzevari et al., 2022](https://doi.org/10.1371/journal.pcbi.1010177)) | **CC BY 4.0** | DBTL과 RL 개념만 인용하고 독립 Mermaid를 제작. |

FBA·pFBA·FVA 및 `e_coli_core` 논문도 개념·계산 입력의 서지 출처일 뿐 외부 그림을 재사용하지 않습니다. 따라서 해당 논문의 그림 라이선스를 본 교재 자산의 라이선스로 표기하지 않습니다.

## 출판 raster/SVG 자산

| ID | 자산 파일 | 최초·재사용 위치 | 제작·생성 조건 | 개념·데이터 원출처 | 권리 상태 | 검증일 |
|:---|:---|:---|:---|:---|:---|:---:|
| A-01 | [`.gitbook/assets/fig2_2_fba_lp.png`](.gitbook/assets/fig2_2_fba_lp.png) | [`chapter-4/02.md`](chapter-4/02.md) | 저자 자체 제작 FBA–LP 모식도. PNG 메타데이터는 Matplotlib 3.10.3을 기록하지만 원 생성 스크립트와 정확한 명령은 보존되지 않았습니다. 수치 GEM 계산이 아닙니다. | FBA 개념: [Orth et al. (2010)](https://doi.org/10.1038/nbt.1614) | 외부 그림 재사용 없음. 저장소의 자체 자산 라이선스는 미선언. 스크립트 부재는 재현성 결손으로 남아 있습니다. | 2026-07-10 |
| A-02 | [`lp-feasible-region.png`](assets/figures/lp-feasible-region.png) · [`lp-feasible-region.svg`](assets/figures/lp-feasible-region.svg) | 최초 [`chapter-4/03.md`](chapter-4/03.md); 재사용 [`chapter-10/09.md`](chapter-10/09.md) 그림 10.2 왼쪽 | `draw_lp_geometry()`. 꼭짓점 $$(0,0),(6,0),(6,4),(2,8),(0,8)$$, 제약 $$v_1+v_2\le10$$, 목적함수 $$0.5v_1+0.8v_2$$ 및 대안 최적 변을 그린 모식도. solver·GEM 미사용. | 선형 FBA 개념: [Orth et al. (2010)](https://doi.org/10.1038/nbt.1614) | 저자 자체 제작; 외부 그림 재사용 없음; 자체 자산 라이선스 미선언. | 2026-07-10 |
| A-03 | [`l1-l2-norm-geometry.png`](assets/figures/l1-l2-norm-geometry.png) · [`l1-l2-norm-geometry.svg`](assets/figures/l1-l2-norm-geometry.svg) | [`chapter-4/08.md`](chapter-4/08.md) | `draw_norm_geometry()`. 원점 중심 단위원 $$\lVert v\rVert_1=1$$과 $$\lVert v\rVert_2=1$$을 비교하는 수학 모식도. solver·GEM 미사용. | pFBA: [Lewis et al. (2010)](https://doi.org/10.1038/msb.2010.47); quadratic MOMA: [Segrè et al. (2002)](https://doi.org/10.1073/pnas.232349399) | 저자 자체 제작; 두 논문의 그림 재사용 없음; 자체 자산 라이선스 미선언. | 2026-07-10 |
| A-04 | [`fva-intervals.png`](assets/figures/fva-intervals.png) · [`fva-intervals.svg`](assets/figures/fva-intervals.svg) | [`chapter-4/09.md`](chapter-4/09.md) | `draw_fva_intervals()`. 기본 `textbook` 모델, `fraction_of_optimum=0.9`, GLPK, `processes=1`; `PGI`, `PFK`, `PYK`, `G6PDH2r`, `EX_ac_e`, `EX_etoh_e`, `EX_for_e`의 FVA min–max와 한 pFBA 해. | FVA: [Mahadevan & Schilling (2003)](https://doi.org/10.1016/j.ymben.2003.09.002); 모델: [BiGG `e_coli_core`](http://bigg.ucsd.edu/models/e_coli_core) | 저자 계산·시각화; 외부 그림 재사용 없음. COBRApy와 BiGG 조건은 위 공통 환경 참조; 자체 자산 라이선스 미선언. | 2026-07-10 |
| A-05 | [`glucose-robustness.png`](assets/figures/glucose-robustness.png) · [`glucose-robustness.svg`](assets/figures/glucose-robustness.svg) | 최초 [`chapter-4/05.md`](chapter-4/05.md); 재사용 [`chapter-10/12.md`](chapter-10/12.md) 그림 10.4 | `draw_robustness_curve()`. glucose uptake cap 0.5–20을 40점으로 스캔; oxygen uptake cap 1000과 10; 각 점에서 biomass 최대화. 아래 Chapter 10 위젯의 단일 조건 출력과 동일 화면이 아닙니다. | 모델: [BiGG `e_coli_core`](http://bigg.ucsd.edu/models/e_coli_core), 원 모델 논문 [Orth et al. (2010)](https://doi.org/10.1128/ecosalplus.10.2.1) | 저자 계산·시각화; 외부 그림 재사용 없음. COBRApy와 BiGG 조건은 위 공통 환경 참조; 자체 자산 라이선스 미선언. | 2026-07-10 |
| A-06 | [`qp-moma-projection.png`](assets/figures/qp-moma-projection.png) · [`qp-moma-projection.svg`](assets/figures/qp-moma-projection.svg) | 최초 [`chapter-8/03.md`](chapter-8/03.md) 그림 8.3; 재사용 [`chapter-10/09.md`](chapter-10/09.md) 그림 10.2 가운데 | `draw_moma_projection()`. 임의 polygon, WT $$(7,7)$$, MOMA $$(4,4)$$, FBA $$(2,6)$$인 2차원 투영 모식도. solver·`e_coli_core` 미사용. | MOMA: [Segrè et al. (2002)](https://doi.org/10.1073/pnas.232349399) | 저자 자체 제작. PNAS 원 논문의 그림을 복제·트레이싱·변형하지 않았으며 해당 논문은 개념 인용에만 사용. 자체 자산 라이선스 미선언. | 2026-07-10 |
| A-07 | [`milp-room-tolerance.png`](assets/figures/milp-room-tolerance.png) · [`milp-room-tolerance.svg`](assets/figures/milp-room-tolerance.svg) | 최초 [`chapter-8/04.md`](chapter-8/04.md) 그림 8.4; 재사용 [`chapter-10/09.md`](chapter-10/09.md) 그림 10.2 오른쪽 | `draw_room_tolerance()`. WT $$(2,5,-3,0.2)$$, mutant $$(2.1,8,-2.8,1.5)$$와 임의 tolerance half-width를 사용한 이진 판정 모식도. solver·`e_coli_core` 미사용. | ROOM: [Shlomi et al. (2005)](https://doi.org/10.1073/pnas.0406346102) | 저자 자체 제작. PNAS 원 논문의 그림을 복제·트레이싱·변형하지 않았으며 해당 논문은 개념 인용에만 사용. 자체 자산 라이선스 미선언. | 2026-07-10 |
| A-08 | [`acetate-production-envelope.png`](assets/figures/acetate-production-envelope.png) · [`acetate-production-envelope.svg`](assets/figures/acetate-production-envelope.svg) | 최초 [`chapter-8/07.md`](chapter-8/07.md) 그림 8.7; 동일 파일 재사용 [`chapter-10/11.md`](chapter-10/11.md) 그림 10.3 | `draw_production_envelope()`. 기본 `textbook` 모델, reactions=`Biomass_Ecoli_core`, objective=`EX_ac_e`, 30점, GLPK, `processes=1`; 가로축 biomass, 세로축 acetate min–max. Chapter 10의 21점·전치 축 Plotly 자료와 동일 화면이 아닙니다. | 모델: [BiGG `e_coli_core`](http://bigg.ucsd.edu/models/e_coli_core), 원 모델 논문 [Orth et al. (2010)](https://doi.org/10.1128/ecosalplus.10.2.1) | 저자 계산·시각화; 외부 그림 재사용 없음. COBRApy와 BiGG 조건은 위 공통 환경 참조; 자체 자산 라이선스 미선언. | 2026-07-10 |

SVG 일곱 개는 현재 Markdown에 직접 삽입되지 않지만 각 PNG와 같은 스크립트 호출에서 함께 생성되는 출판용 벡터 원본이므로 동일 논리 자산으로 관리합니다.

## 퍼블릭 도메인 실물 사진

아래 두 사진은 저자 자체 제작 도식이 전달할 수 없는 실제 형태(morphology)를 보여 주기 위해 포함한 외부 실물 사진이다. 두 파일 모두 Wikimedia Commons의 파일 페이지에서 라이선스 템플릿을 직접 확인했으며 미국 연방기관 저작물로 퍼블릭 도메인이다. 캡션의 출처 표기는 PD상 법적 의무는 아니나 본 교재의 인용 방침에 따라 제공한다.

| ID | 자산 파일 | 위치 | 대상·조건 | 출처·원저작자 | 라이선스·검증 | 검증일 |
|:---|:---|:---|:---|:---|:---|:---:|
| P-01 | [`.gitbook/assets/ecoli-sem-usda-ars.jpg`](.gitbook/assets/ecoli-sem-usda-ars.jpg) | [`chapter-1/02.md`](chapter-1/02.md) 사진 1.1 | 대장균 저온 SEM(약 10,000배) | Eric Erbe 촬영, Christopher Pooley 디지털 컬러화, 미국 농무부 농업연구청(USDA ARS), 이미지 K11077-1 | Public Domain (PD-USGov-USDA-ARS). Wikimedia Commons [File:E coli at 10000x, original.jpg](https://commons.wikimedia.org/wiki/File:E_coli_at_10000x,_original.jpg) 파일 페이지 라이선스 템플릿 확인 | 2026-07-11 |
| P-02 | [`.gitbook/assets/biofilm-sem-cdc.jpg`](.gitbook/assets/biofilm-sem-cdc.jpg) | [`chapter-8/09.md`](chapter-8/09.md) 사진 8.1 | 포도상구균 biofilm SEM(카테터 표면) | Rodney M. Donlan·Janice Carr, 미국 질병통제예방센터(CDC), PHIL #7488 | Public Domain (PD-USGov-HHS-CDC). Wikimedia Commons [File:Staphylococcus aureus biofilm 01.jpg](https://commons.wikimedia.org/wiki/File:Staphylococcus_aureus_biofilm_01.jpg) 파일 페이지 라이선스 템플릿 확인 | 2026-07-11 |

사진 8.1의 biofilm 예시는 임상 표면(카테터)의 포도상구균 사례로, 특정 장내 미생물군집이나 커뮤니티 대사 모델의 결과가 아니라 공간적 군집 구조 일반을 예시한다.

## Chapter 11 실습 계산 그림

아래 계산 그림은 제11장 실습에서 **실제로 실행한 계산 결과**를 matplotlib로 렌더한 것이다(모식도가 아님). 계산 환경은 macOS, Python 3.10, COBRApy 0.30.0, GLPK/Gurobi(학술 라이선스)이며 한글 렌더는 AppleGothic을 사용했다. CarveMe 관련 입력은 UniProt proteome UP000000625, CarveMe 1.6.6, diamond 2.2.3, 번들 BiGG universe이다. GUI 화면(`tracegem_gui.png`, `cmm_gui.png`)은 저자가 개발·공개한 도구([TRACE-GEM](https://github.com/jyryu3161/TRACE-GEM), [CMM](https://github.com/jyryu3161/CMM), MIT) 저장소의 자작 스크린샷이므로 제3자 저작권 문제가 없다.

| ID | 자산 파일 | 위치 | 생성 조건 | 데이터 원출처 | 권리 상태 | 검증일 |
|:---|:---|:---|:---|:---|:---|:---:|
| L-01 | [`.gitbook/assets/lab11/fig_fba_exchanges.png`](.gitbook/assets/lab11/fig_fba_exchanges.png) | [`chapter-11/02.md`](chapter-11/02.md) 그림 11.2 | `e_coli_core` FBA 최적해의 주요 교환 flux; GLPK, 기본 배지, biomass 최대화 | [BiGG `e_coli_core`](http://bigg.ucsd.edu/models/e_coli_core) | 저자 계산·시각화; 외부 그림 재사용 없음 | 2026-07-11 |
| L-02 | [`.gitbook/assets/lab11/fig_fva_intervals.png`](.gitbook/assets/lab11/fig_fva_intervals.png) | [`chapter-11/03.md`](chapter-11/03.md) 그림 11.3 | 선택 반응 FVA(fraction\_of\_optimum=0.90, processes=1)와 pFBA 해 | [BiGG `e_coli_core`](http://bigg.ucsd.edu/models/e_coli_core) | 저자 계산·시각화 | 2026-07-11 |
| L-03 | [`.gitbook/assets/lab11/fig_moma_scatter.png`](.gitbook/assets/lab11/fig_moma_scatter.png) | [`chapter-11/04.md`](chapter-11/04.md) 그림 11.4 | PGI 결손 후 WT pFBA 대비 FBA·선형 MOMA flux 산점도; GLPK/Gurobi | [BiGG `e_coli_core`](http://bigg.ucsd.edu/models/e_coli_core) | 저자 계산·시각화 | 2026-07-11 |
| L-04 | [`.gitbook/assets/lab11/fig_prod_envelope.png`](.gitbook/assets/lab11/fig_prod_envelope.png) | [`chapter-11/04.md`](chapter-11/04.md) 그림 11.5 | biomass–acetate production envelope(25점); GLPK | [BiGG `e_coli_core`](http://bigg.ucsd.edu/models/e_coli_core) | 저자 계산·시각화 | 2026-07-11 |
| L-05 | [`.gitbook/assets/lab11/fig_carveme_compare.png`](.gitbook/assets/lab11/fig_carveme_compare.png) | [`chapter-11/05.md`](chapter-11/05.md) 그림 11.6 | `e_coli_core`·CarveMe 초안·iML1515의 반응·대사물·유전자 수 비교 | BiGG `e_coli_core`·iML1515, CarveMe 1.6.6 초안(UP000000625) | 저자 계산·시각화 | 2026-07-11 |
| L-06 | [`.gitbook/assets/lab11/fig_mmplatform_ladfit.png`](.gitbook/assets/lab11/fig_mmplatform_ladfit.png) | [`chapter-11/06.md`](chapter-11/06.md) 그림 11.7 | mmplatform 데모의 표본별 LAD 적합 목적값; expression_only, scipy-highs | mmplatform 0.3.0 `make-demo` fixture | 저자 계산·시각화 | 2026-07-11 |
| L-07 | [`.gitbook/assets/lab11/tracegem_gui.png`](.gitbook/assets/lab11/tracegem_gui.png) | [`chapter-11/07.md`](chapter-11/07.md) 그림 11.8 | TRACE-GEM 데스크톱 GUI(iML1515·52 task) | 저자 도구 [TRACE-GEM](https://github.com/jyryu3161/TRACE-GEM) 저장소 이미지 | 저자 도구 GUI 자작 스크린샷 | 2026-07-11 |
| L-08 | [`.gitbook/assets/lab11/fig_cmm_eflux_lad.png`](.gitbook/assets/lab11/fig_cmm_eflux_lad.png) | [`chapter-11/08.md`](chapter-11/08.md) 그림 11.9 | CMM E-Flux2 vs LAD 예측 flux 산점도; 합성 발현 | CMM 0.3.0, BiGG `e_coli_core` | 저자 계산·시각화 | 2026-07-11 |
| L-09 | [`.gitbook/assets/lab11/cmm_gui.png`](.gitbook/assets/lab11/cmm_gui.png) | [`chapter-11/08.md`](chapter-11/08.md) 그림 11.10 | CMM 데스크톱 GUI 시뮬레이션 화면 | 저자 도구 [CMM](https://github.com/jyryu3161/CMM)(MIT) 저장소 이미지 | 저자 도구 GUI 자작 스크린샷 | 2026-07-11 |
| L-10 | [`.gitbook/assets/lab11/fig_cmig_community.png`](.gitbook/assets/lab11/fig_cmig_community.png) | [`chapter-11/09.md`](chapter-11/09.md) 그림 11.11 | CMIG 3-구성원 군집의 구성원 성장률과 교환 프로파일 | CMIG 0.1.0, MICOM 0.39.0, 합성 fixture | 저자 계산·시각화 | 2026-07-11 |
| L-11 | [`.gitbook/assets/lab11/fig_cmig_dfba.png`](.gitbook/assets/lab11/fig_cmig_dfba.png) | [`chapter-11/09.md`](chapter-11/09.md) 그림 11.12 | CMIG 동적 FBA 시간경과(바이오매스·포도당); t≈5.36 고갈 | CMIG 0.1.0, Gurobi, dt=0.1 | 저자 계산·시각화 | 2026-07-11 |
| L-12 | [`.gitbook/assets/lab11/fig_cmig_spatial.png`](.gitbook/assets/lab11/fig_cmig_spatial.png) | [`chapter-11/09.md`](chapter-11/09.md) 그림 11.13 | CMIG 2D 공간 미리보기 포도당 확산 히트맵 | CMIG 0.1.0 spatial-preview | 저자 계산·시각화 | 2026-07-11 |

## Chapter 1 Mermaid 도식

아래 도식은 Markdown의 Mermaid source가 원본인 저자 자체 제작물이다. 개념 문헌의 원 그림과 패널·레이아웃을 복제하지 않았다.

| 그림 | Mermaid 원본 위치 | 대상 | 개념 원출처와 권리 처리 | 검증일 |
|:---:|:---|:---|:---|:---:|
| 1.1 | [`chapter-1/README.md`](chapter-1/README.md) | 제1장의 개념 의존 관계 | 저자 교육용 종합; 특정 외부 그림 없음. | 2026-07-10 |
| 1.2 | [`chapter-1/01.md`](chapter-1/01.md) | 분해대사–합성대사의 물질·에너지 결합 | [OpenStax Biology 2e §6.1](https://openstax.org/books/biology-2e/pages/6-1-energy-and-metabolism), CC BY-NC-SA 4.0의 개념을 인용하고 독립 도식 제작. | 2026-07-10 |
| 1.3 | [`chapter-1/01.md`](chapter-1/01.md) | 대장균 중심탄소대사의 분기·재합류 | [Long et al. (2016)](https://doi.org/10.1016/j.ymben.2016.05.006), [Hollinshead et al. (2016)](https://doi.org/10.1186/s13068-016-0630-y)의 실험 사실만 인용. | 2026-07-10 |
| 1.4 | [`chapter-1/02.md`](chapter-1/02.md) | 모델–실험 반복 | [Orth et al. (2010)](https://doi.org/10.1038/nbt.1614)의 제약 기반 분석 개념만 인용. | 2026-07-10 |
| 1.5 | [`chapter-1/03.md`](chapter-1/03.md) | reconstruction–model–validation 관계 | [Thiele & Palsson (2010)](https://doi.org/10.1038/nprot.2009.203)의 절차 개념만 인용. | 2026-07-10 |
| 1.6 | [`chapter-1/04.md`](chapter-1/04.md) | FBA 확장의 서로 다른 설계축 | FBA·dFBA·GECKO의 방법 사실을 인용하고 독립 taxonomy 제작. | 2026-07-10 |
| 1.7 | [`chapter-1/05.md`](chapter-1/05.md) | 모델 기술의 네 기준 | 저자 교육용 taxonomy; 특정 외부 그림 없음. | 2026-07-10 |
| 1.8 | [`chapter-1/07.md`](chapter-1/07.md) | 연구 대상별 응용과 검증 | 저자 교육용 종합; 원 논문 그림 재사용 없음. | 2026-07-10 |
| 1.9 | [`chapter-1/08.md`](chapter-1/08.md) | 재구축·분석의 반복 절차 | Thiele–Palsson와 MEMOTE의 절차를 사실로 인용하고 독립 도식 제작. | 2026-07-10 |

## Chapter 2–4 Mermaid 도식

아래 도식은 각 Markdown의 Mermaid source가 원본인 저자 자체 제작물이다. 외부 문헌의 그림이나 레이아웃을 복제하지 않았다.

| 그림 | Mermaid 원본 위치 | 대상 | 개념 원출처와 권리 처리 | 검증일 |
|:---:|:---|:---|:---|:---:|
| 2.1 | [`chapter-2/README.md`](chapter-2/README.md) | 화학량론 행렬에서 제약 기반 분석으로의 흐름 | 저자 교육용 종합; 특정 외부 그림 없음. | 2026-07-10 |
| 2.2 | [`chapter-2/01.md`](chapter-2/01.md) | 반응·대사물·flux·bound의 관계 | [Orth et al. (2010)](https://doi.org/10.1038/nbt.1614)의 FBA 개념을 인용한 독립 도식. | 2026-07-10 |
| 2.3 | [`chapter-2/03.md`](chapter-2/03.md) | 대사 네트워크의 행렬·이분 그래프·투영 표현 | [Poupin et al. (2020)](https://doi.org/10.1371/journal.pcbi.1007645)의 네트워크 표현 개념만 인용. | 2026-07-10 |
| 3.1 | [`chapter-3/README.md`](chapter-3/README.md) | GEM의 구성 요소와 검증 단계 | 저자 교육용 종합; 특정 외부 그림 없음. | 2026-07-10 |
| 3.2 | [`chapter-3/04.md`](chapter-3/04.md) | 수송 반응의 에너지 구동과 화학량론 결합 | [Wright et al. (2011)](https://doi.org/10.1152/physrev.00055.2009), [Ruprecht & Kunji (2020)](https://doi.org/10.1016/j.tibs.2019.11.001)의 사실을 인용한 독립 도식. | 2026-07-10 |
| 3.3 | [`chapter-3/07.md`](chapter-3/07.md) | 모델 규모와 주석·검증 정보의 분리 | BiGG `textbook`과 iML1515의 모델 메타데이터를 저자가 독립적으로 종합. | 2026-07-10 |
| 4.1 | [`chapter-4/01.md`](chapter-4/01.md) | FBA 장의 분석 흐름 | [Orth et al. (2010)](https://doi.org/10.1038/nbt.1614)의 개념을 인용한 독립 도식. | 2026-07-10 |

## Chapter 5 Mermaid 도식

| 그림 | Mermaid 원본 위치 | 대상 | 개념 원출처와 권리 처리 | 검증일 |
|:---:|:---|:---|:---|:---:|
| 5.1 | [`chapter-5/README.md`](chapter-5/README.md) | GEM 재구축의 증거 흐름 | Thiele–Palsson와 MEMOTE의 절차를 독립적으로 종합. | 2026-07-10 |
| 5.2 | [`chapter-5/01.md`](chapter-5/01.md) | 재구축–검증 생명주기 | Thiele–Palsson와 MEMOTE의 개념을 인용; 외부 그림 없음. | 2026-07-10 |
| 5.3 | [`chapter-5/02.md`](chapter-5/02.md) | BLASTP 검색 흐름 | [Altschul et al. (1990)](https://doi.org/10.1016/S0022-2836(05)80360-2)와 NCBI 문서의 알고리즘 사실을 독립 도식화. | 2026-07-10 |
| 5.4 | [`chapter-5/02.md`](chapter-5/02.md) | 기능 주석에서 반응·GPR로의 변환 | 저자 교육용 종합; 특정 외부 그림 없음. | 2026-07-10 |
| 5.5 | [`chapter-5/04.md`](chapter-5/04.md) | Top-down과 bottom-up 재구축 | CarveMe·ModelSEED 방법을 사실로 인용하고 독립 도식 제작. | 2026-07-10 |
| 5.6 | [`chapter-5/05.md`](chapter-5/05.md) | 학습 점수와 제약 기반 gap-filling | CHESHIRE(CC BY 4.0)의 방법 개념을 일반화; 원 그림 없음. | 2026-07-10 |
| 5.7 | [`chapter-5/07.md`](chapter-5/07.md) | 범용 인체 재구축의 증거 층 | Recon1·Human1의 재구축 사실을 독립 도식화. | 2026-07-10 |
| 5.8 | [`chapter-5/08.md`](chapter-5/08.md) | 인체 GEM release 계보 | Recon3D·Human1·Human2의 provenance를 바탕으로 독립 genealogy 제작. | 2026-07-10 |
| 5.9 | [`chapter-5/09.md`](chapter-5/09.md) | Human2 LLM screening 흐름 | Human2는 CC BY-NC-ND 4.0. 수치·범주 사실만 사용하고 원 그림의 패널·레이아웃을 복제·변형하지 않음. | 2026-07-10 |
| 5.10 | [`chapter-5/10.md`](chapter-5/10.md) | tINIT task 보존 절차 | [Agren et al. (2014)](https://doi.org/10.1002/msb.145122)의 방법 사실을 독립 흐름도로 제작. | 2026-07-10 |

## Chapter 8–10 Mermaid 도식

Mermaid 도식은 각 Markdown의 fenced source가 원본이며 GitBook/Mermaid 렌더러가 빌드 시 출력합니다. 별도 raster 파일이나 외부 생성 명령은 없습니다. 아래 도식은 모두 저자 자체 제작이고, 외부 논문의 패널·레이아웃·아이콘을 재사용하지 않습니다.

| 그림 | Mermaid 원본 위치 | 대상·재사용 | 개념 원출처와 외부 권리 | 검증일 |
|:---:|:---|:---|:---|:---:|
| 8.1 | [`chapter-8/README.md`](chapter-8/README.md) | 섭동 예측에서 균주·커뮤니티 설계로 이어지는 장 지도; 재사용 없음 | MOMA·ROOM·OptKnock을 사실·개념으로만 인용. 원 논문 그림 재사용 없음. | 2026-07-10 |
| 8.2 | [`chapter-8/01.md`](chapter-8/01.md) | perturbation→feasible-space 축소→FBA/MOMA/ROOM; 재사용 없음 | MOMA([DOI](https://doi.org/10.1073/pnas.232349399)), ROOM([DOI](https://doi.org/10.1073/pnas.0406346102)); PNAS 그림 재사용 없음. | 2026-07-10 |
| 8.5 | [`chapter-8/04.md`](chapter-8/04.md) | ROOM MILP의 branch-and-bound 개념; 재사용 없음 | ROOM([DOI](https://doi.org/10.1073/pnas.0406346102)); 특정 solver·논문 그림 재사용 없음. | 2026-07-10 |
| 8.6 | [`chapter-8/06.md`](chapter-8/06.md) | OptKnock 이중 수준 문제와 production-envelope 검증; 재사용 없음 | OptKnock([DOI](https://doi.org/10.1002/bit.10803))은 Wiley 출판물이며 그림을 재사용하지 않고 방법만 인용. | 2026-07-10 |
| 8.8 | [`chapter-8/lab.md`](chapter-8/lab.md) | 제8장 실습 흐름; 재사용 없음 | 로컬 COBRApy 실습을 저자가 요약; 외부 시각물 없음. | 2026-07-10 |
| 9.1 | [`chapter-9/01.md`](chapter-9/01.md) | GEM 한계와 AI 보완 경로 지도; 재사용 없음 | AMN([CC BY 4.0](https://www.nature.com/articles/s41467-023-40380-0)), FlowGAT([CC BY 4.0](https://www.nature.com/articles/s41540-024-00348-2)), CHESHIRE([CC BY 4.0](https://www.nature.com/articles/s41467-023-38110-7)); 개념 인용만 사용. | 2026-07-10 |
| 9.2 | [`chapter-9/02.md`](chapter-9/02.md) | 데이터→특징→학습→검증→적용의 일반 ML 흐름; 재사용 없음 | 저자 교육용 종합; 특정 외부 그림 없음. | 2026-07-10 |
| 9.3 | [`chapter-9/02.md`](chapter-9/02.md) | 70:15:15 예시의 train/validation/test 역할; 재사용 없음 | 저자 교육용 종합; 특정 외부 그림 없음. | 2026-07-10 |
| 9.4 | [`chapter-9/02.md`](chapter-9/02.md) | stratified 5-fold 평가 순환; 재사용 없음 | 저자 교육용 종합; 특정 외부 그림 없음. | 2026-07-10 |
| 9.5 | [`chapter-9/04.md`](chapter-9/04.md) | GEM→반응 그래프→GNN→예측; 재사용 없음 | FlowGAT([CC BY 4.0](https://www.nature.com/articles/s41540-024-00348-2)), FluxGAT([CC BY 4.0](https://www.nature.com/articles/s41540-026-00738-8)); 논문 그림 재사용 없음. | 2026-07-10 |
| 9.6 | [`chapter-9/05.md`](chapter-9/05.md) | CHESHIRE·CLOSEgaps·MuSHIN의 발표 순서와 입력 표현. 서로 다른 benchmark F1의 시계열이 아님. | CHESHIRE [CC BY 4.0](https://www.nature.com/articles/s41467-023-38110-7); CLOSEgaps [CC BY-NC-ND 4.0](https://arxiv.org/abs/2409.13259); MuSHIN [CC BY-NC-ND 4.0](https://www.nature.com/articles/s42003-026-09761-1). 두 ND 자료의 그림·표는 번역·변형하지 않고 사실만 인용. | 2026-07-10 |
| 9.7 | [`chapter-9/06.md`](chapter-9/06.md) | 서로게이트 선별→원모델·실험 재검산; 재사용 없음 | Neural–mechanistic 결합의 사례 AMN([CC BY 4.0](https://www.nature.com/articles/s41467-023-40380-0)); 논문 그림 재사용 없음. | 2026-07-10 |
| 9.8 | [`chapter-9/07.md`](chapter-9/07.md) | 물리적 Build/Test를 포함한 DBTL 순환; 재사용 없음 | 균주 설계 RL [Sabzevari et al. (2022)](https://doi.org/10.1371/journal.pcbi.1010177), CC BY 4.0; 논문 그림 재사용 없음. | 2026-07-10 |
| 9.9 | [`chapter-9/lab.md`](chapter-9/lab.md) | 그래프 특징→필수성 RF→평가→PCA/K-Means 실습; 재사용 없음 | 로컬 COBRApy·NetworkX·scikit-learn 코드를 저자가 요약; 외부 시각물 없음. | 2026-07-10 |
| 10.1 | [`chapter-10/README.md`](chapter-10/README.md) | preflight부터 JSON provenance까지의 튜토리얼 의존 흐름; 재사용 없음 | 이 저장소의 장·셀 구조를 저자가 요약; 외부 시각물 없음. | 2026-07-10 |

### 대화형 도해

| ID | 자산·최초 위치 | 내용·생성 조건 | 출처·권리 상태 |
|:---|:---|:---|:---|
| I-01 | [`interactive/index.html`](interactive/index.html); Chapters 1–10 각 `README.md` | 순수 HTML/SVG/JavaScript로 제작한 10개 조작형 교육 도해. Chapter 1–10의 모델 경계, S 행렬, GPR, FBA 가능영역, 재구축 근거, 오믹스 임계값, 선택성, production envelope, ROC, provenance를 각각 다룬다. 표본 점·수치·곡선은 **모의값**이며 외부 데이터 또는 실제 GEM 결과가 아니다. | 저자 자체 제작. 외부 그림·아이콘·데이터셋을 포함하지 않음. 개념 근거는 각 장의 본문 인용 문헌과 [대표 논문 가이드](landmark-papers.md)를 따른다. CDN 배포는 GitHub 저장소의 `main` 브랜치를 jsDelivr가 제공하는 방식이며, 네트워크 비가용 시 각 장의 정적 본문과 실습 코드를 대체하지 않는다. |

## 출판 전 남은 권리·재현성 조치

1. 교재와 저자 자체 제작 자산에 적용할 저장소 차원의 라이선스를 저자가 결정하고 루트에 명시합니다.
2. `.gitbook/assets/fig2_2_fba_lp.png`의 생성 코드를 복원하거나, [`scripts/generate_optimization_figures.py`](scripts/generate_optimization_figures.py)로 재작성해 추적 불가능한 raster를 제거합니다.
3. 계산 그림을 다시 만들 때 Python·NumPy·Matplotlib·GLPK 세부 버전, 실제로 로드된 모델 파일의 SHA-256, 기본 배지와 반응 bound를 함께 기록합니다.
4. BiGG 모델을 원고 배포물에 직접 포함할 경우 현재 [BiGG License](http://bigg.ucsd.edu/license)의 허용 범위를 별도로 확인합니다.
