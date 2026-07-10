# 보충 학습. 오믹스 데이터 분석과 기초 통계

> RNA-seq 값을 GEM 제약으로 바꾸기 전에 알아야 할 데이터 유형, 정규화, 차등발현, 가설검정과 다중검정을 정리합니다. 원 강의의 **데이터분석 및 기초통계** 57개 슬라이드를 Chapter 6의 실제 의사결정에 맞게 재구성했습니다.

## 1. 데이터에서 모델 제약까지

데이터는 관찰·실험·조사로 얻은 사실이나 측정값입니다. 분석과 맥락 해석을 거쳐야 정보가 되고, 그 정보가 모델의 반응 포함 여부·flux bound·가중치로 번역됩니다.

```text
raw data → 품질관리 → 정규화 → 통계 추론 → 생물학적 해석
         → 유전자 점수 → GPR 집계 → 반응 점수/제약 → GEM 분석
```

통계적으로 유의하다는 사실만으로 생물학적으로 중요하거나 좋은 약물 표적이라는 결론을 낼 수는 없습니다. 효과 크기, 재현성, 기전, 모델 민감도를 함께 봐야 합니다.

## 2. 데이터 유형을 먼저 구분하기

| 구분 | 유형 | 오믹스 예 |
|:---|:---|:---|
| 구조 | 정형 데이터 | 유전자×샘플 count/TPM 행렬, 임상 메타데이터 |
|  | 비정형 데이터 | 논문 텍스트, 병리 이미지, 분자 그래프 |
| 측정척도 | 정량형 | 발현량, 대사물 농도, IC₅₀ |
|  | 범주형 | 암종, 처리군, 성별 |
| 범주 순서 | 명목형 | 혈액형, 세포주 이름 |
|  | 서열형 | 암 병기, 반응 confidence score |
| 수치 범위 | 이산형 | RNA-seq raw count, 돌연변이 수 |
|  | 연속형 | TPM, 단백질 농도, flux |

유전체·전사체·단백질체·대사체는 서로 다른 생물학 층위를 측정합니다. 전사체 행렬의 행은 유전자/전사체, 열은 샘플, 셀은 raw count 또는 정규화된 발현량입니다. 이 구조를 뒤집거나 샘플 메타데이터 순서를 어긋나게 하는 것이 가장 흔한 분석 오류 중 하나입니다.

## 3. RNA-seq 측정과 정량화

전형적인 RNA-seq 흐름은 RNA 추출 → library 제작 → sequencing → read QC → genome/transcriptome 정렬 또는 pseudo-alignment → 유전자/전사체별 정량화입니다.

### 3.1 WGS와 RNA-seq는 서로 다른 질문에 답한다

| 구분 | WGS(whole-genome sequencing) | RNA-seq |
|:---|:---|:---|
| 측정 물질 | genomic DNA | 시점·조건별 RNA |
| 주된 결과 | SNV/indel, copy-number 및 구조 변이 등 | 유전자·전사체 abundance, splice isoform 등 |
| 시간적 성격 | 체세포 변이를 제외하면 비교적 안정적인 유전 정보 | 환경·조직·처리에 따라 동적으로 변하는 세포 상태 |
| 직접 답하지 못하는 것 | 해당 유전자가 현재 발현·활성인지 | genome 전체의 변이와 결실을 완전하게 규명하는 것 |
| GEM 연결 | 기능상실 변이·gene copy 변화 등을 GPR 또는 효소 가용성 가설에 반영 | 맥락별 반응 점수, 포함 우선순위 또는 flux bound의 증거로 사용 |

두 데이터는 대체 관계가 아닙니다. 예를 들어 WGS가 효소 유전자의 기능상실 가능성을 제시하고 RNA-seq가 해당 조건의 발현 상태를 보완할 수 있습니다. 다만 DNA 변이와 RNA abundance 어느 쪽도 반응 flux를 직접 측정하지 않으므로, GPR 해석·단백질체·대사체·flux 실험과 함께 검증해야 합니다.

raw count에는 적어도 두 가지 크기 효과가 섞여 있습니다.

1. **sequencing depth**: 더 깊게 읽은 샘플은 대부분의 유전자 count가 커집니다.
2. **gene length**: 같은 발현 수준이라도 긴 유전자는 더 많은 read를 받습니다.

정규화법은 연구 질문에 맞게 선택해야 합니다.

| 값 | 계산·보정 | 적절한 용도 | 부적절한 용도 |
|:---|:---|:---|:---|
| raw count | 정수 read 수 | DESeq2/edgeR 차등발현 입력 | 샘플 깊이가 다른 값의 직접 비교 |
| CPM | library size 보정 | 같은 유전자의 대략적 샘플 비교·필터 | 유전자 간 비교, 정식 DEG 검정 |
| RPKM/FPKM | depth+gene length | 한 샘플 내 유전자 간 상대량의 역사적 지표 | raw count 기반 DEG 대체 |
| TPM | 길이를 먼저 보정한 뒤 합을 10⁶으로 고정 | 한 샘플의 구성, GEM 활성 임계값 입력 | RNA composition 차이가 큰 샘플의 무비판적 DEG 검정 |
| DESeq2 size factor | median-of-ratios | 샘플 간 DEG | 한 샘플 내 서로 다른 유전자 양 비교 |
| edgeR TMM | 조성 편향을 trimmed mean으로 보정 | 샘플 간 DEG | 원래 count 없이 임의 역변환 |

### 3.2 CPM, RPKM/FPKM, TPM

유전자 $$g$$의 count를 $$C_g$$, 전체 mapped count를 $$N$$, 길이를 kb 단위 $$L_g$$라고 하면:

$$
CPM_g=\frac{C_g}{N}\times10^6
$$

$$
RPKM_g=\frac{C_g}{L_gN}\times10^6
$$

TPM은 먼저 $$R_g=C_g/L_g$$를 계산한 뒤 전체 합으로 나눕니다.

$$
TPM_g=\frac{R_g}{\sum_h R_h}\times10^6
$$

따라서 각 샘플의 TPM 합은 항상 $$10^6$$입니다. 이는 해석을 편하게 하지만, 소수의 매우 강한 전사체가 전체 구성비를 바꾸는 **compositional effect**까지 제거한다는 뜻은 아닙니다.

{% hint style="danger" %}
차등발현 검정에는 TPM/FPKM을 t-test에 바로 넣지 말고 raw count와 DESeq2·edgeR 같은 negative-binomial 모델을 사용하십시오. TPM은 GEM에 발현 증거를 매핑할 때 유용하지만, “TPM 합이 같으므로 모든 샘플 간 비교가 자동으로 공정하다”는 뜻은 아닙니다.
{% endhint %}

## 4. 차등발현과 negative binomial 모델

RNA-seq count는 이산형이며, 같은 평균에서도 생물학적 변동 때문에 분산이 평균보다 커지는 **과산포(overdispersion)**가 흔합니다. DESeq2와 edgeR은 이를 negative binomial(NB) 분포와 generalized linear model로 다룹니다.

| 항목 | DESeq2 | edgeR |
|:---|:---|:---|
| 정규화 | median-of-ratios | TMM |
| 분산 | 평균–분산 추세와 shrinkage | empirical Bayes shrinkage |
| 대표 검정 | Wald, likelihood-ratio | exact test, quasi-likelihood/LRT |
| log₂FC 안정화 | shrinkage 도구 제공 | 별도 절차·설정 사용 |

두 도구 모두 입력으로 정수 raw count와 올바른 design matrix가 필요합니다. batch, sex, paired sample 같은 실험 설계 변수를 무시하면 생물학적 차이와 교란이 섞입니다.

## 5. 기술통계와 추론통계

- **기술통계(descriptive statistics)**는 평균·중앙값·분산·분포·그림으로 관측 데이터를 요약합니다.
- **추론통계(inferential statistics)**는 표본으로 모집단의 차이와 불확실성을 추정합니다.

모집단 특성을 수로 나타낸 것을 **모수(parameter)**, 표본에서 계산한 값을 **통계량(statistic)**이라고 합니다. 예를 들어 모집단 평균은 $$\mu$$, 표본 평균은 $$\bar x$$로 구분합니다.

### 5.1 평균만 보면 안 되는 이유

두 집단 평균 차이가 2라고 해도 표준편차가 0.1인 경우와 10인 경우의 증거 강도는 전혀 다릅니다. 따라서 다음을 함께 보고해야 합니다.

- 중심: 평균 또는 중앙값
- 산포: 표준편차, 사분위범위, 신뢰구간
- 표본 수와 결측치
- 효과 크기와 방향
- p-value와 다중검정 보정값

## 6. 정규분포, 표준화와 t 분포

정규분포는 평균 $$\mu$$와 분산 $$\sigma^2$$로 결정되는 대칭 연속분포입니다.

$$
X\sim N(\mu,\sigma^2)
$$

z-score는 관측값을 평균 0, 표준편차 1의 척도로 바꿉니다.

$$
z=\frac{x-\mu}{\sigma}
$$

모집단 분산을 모르고 표본으로 추정하면 평균 차이의 표준화 통계량은 t 분포를 따릅니다. 표본이 작을수록 꼬리가 두껍고, 자유도가 커질수록 정규분포에 가까워집니다. “표본이 30개면 무조건 z-test” 같은 규칙보다 분산을 알고 있는지, 분포와 표본 설계가 무엇인지가 더 중요합니다.

## 7. 가설과 p-value

- **귀무가설 $$H_0$$**: 차이 또는 효과가 없습니다.
- **대립가설 $$H_1$$**: 차이 또는 방향성 있는 효과가 있습니다.
- **단측 검정**은 사전에 정한 한 방향만, **양측 검정**은 양방향 차이를 봅니다.

**p-value**는 $$H_0$$가 참이라고 가정했을 때 관측한 검정통계량과 같거나 더 극단적인 값을 얻을 확률입니다.

{% hint style="warning" %}
p-value는 “귀무가설이 참일 확률”, “결과가 우연일 확률”, “재현될 확률”이 아닙니다. 또한 p<0.05가 큰 효과나 생물학적 중요성을 보장하지 않습니다.
{% endhint %}

## 8. t-test를 고르는 법

| 검정 | 질문 | 예 |
|:---|:---|:---|
| one-sample t-test | 한 집단 평균이 기준값과 다른가? | 평균 ATP flux가 기준 10과 다른가 |
| independent t-test | 서로 독립인 두 집단 평균이 다른가? | 암군과 정상군 발현 차이 |
| Welch t-test | 독립 두 집단이며 분산이 다를 수 있는가? | 표본 수·분산이 다른 두 환자군 |
| paired t-test | 같은 대상의 전후 차이가 있는가? | 약물 전후 같은 환자 |

독립성은 설계에서 확보해야 하며 검정으로 “고칠” 수 없습니다. 정규성은 원자료 자체보다 검정이 사용하는 잔차 또는 paired difference에 대해 판단해야 합니다. 독립 두 집단에서 등분산이 확실하지 않다면 기본적으로 Welch 검정이 안전합니다.

분포가 심하게 치우치거나 순서형 자료이고 표본이 작다면 Mann–Whitney U, Wilcoxon signed-rank 같은 **비모수 검정**을 고려합니다. 비모수 검정도 독립성·분포 모양에 대한 조건과 구체적 귀무가설이 있으므로 “가정이 전혀 없는 검정”은 아닙니다.

## 9. 1종·2종 오류와 검정력

| 실제 상태 / 판단 | 유의하다고 판단 | 유의하지 않다고 판단 |
|:---|:---|:---|
| 실제 효과 없음 | 1종 오류(false positive), 확률 $$\alpha$$ | 올바른 판단 |
| 실제 효과 있음 | 올바른 검출, power $$1-\beta$$ | 2종 오류(false negative), 확률 $$\beta$$ |

검정력은 효과 크기, 산포, 표본 수, 유의수준에 좌우됩니다. “p>0.05”는 효과가 없다는 증명이 아니라, 현재 설계로 충분히 검출하지 못했다는 뜻일 수 있습니다.

## 10. 수천 유전자를 검사할 때의 다중검정

10,000개 유전자를 각각 $$\alpha=0.05$$로 검사하면 모두 귀무가설이어도 기대상 약 500개의 false positive가 생깁니다.

### 10.1 Bonferroni

family-wise error rate를 강하게 통제하려면 기준을 $$\alpha/m$$으로 낮춥니다. 검정 수 $$m$$이 크면 매우 보수적이어서 true positive를 많이 놓칠 수 있습니다.

### 10.2 Benjamini–Hochberg FDR

BH 방법은 유의하다고 선언한 결과 중 기대되는 false discovery 비율을 통제합니다.

1. p-value를 $$p_{(1)}\le\cdots\le p_{(m)}$$으로 정렬합니다.
2. 원하는 FDR $$Q$$에 대해 $$p_{(i)}\le(i/m)Q$$를 만족하는 가장 큰 $$i$$를 찾습니다.
3. 그 지점까지를 유의하다고 판단합니다.

용어를 구분해야 합니다.

- **FDR**은 반복적으로 같은 절차를 적용했을 때 유의하다고 선언한 결과 중 false discovery가 차지하는 비율의 기댓값으로, 분석 절차가 통제하려는 오류율입니다. 개별 유전자의 값이 아닙니다.
- **BH-adjusted p-value(`padj`)**는 BH 절차 아래에서 각 가설을 기각할 수 있는 최소 FDR 유의수준으로 해석합니다.
- **q-value**는 보통 각 특징을 포함해 유의하다고 선언할 때의 최소 추정 FDR을 뜻합니다. 추정 방식과 null 비율 $$\pi_0$$ 처리에 따라 BH `padj`와 같지 않을 수 있습니다.

따라서 결과표에는 `p-value`, 사용한 방법의 `padj` 또는 `q-value`, 선택한 FDR 통제 수준을 이름 그대로 구분해 보고해야 합니다.

## 11. GEM 통합 전 권장 의사결정

| 목적 | 권장 입력·절차 |
|:---|:---|
| 두 조건의 DEG 탐색 | raw count → DESeq2/edgeR → log₂FC + BH `padj`(선택한 FDR 수준 명시) |
| 한 샘플에서 반응 활성 증거 | TPM 또는 적절히 정규화한 abundance → 임계값/확률 모델 |
| 여러 샘플의 맥락 특이 모델 비교 | 동일 파이프라인·batch 보정·공통 ID·민감도 분석 |
| GPR 반응 점수 | AND=min/limiting subunit, OR=max 또는 sum 등 규칙을 명시 |
| 모델 예측 차이 | flux 하나만 비교하지 말고 FVA·sampling·효과 크기 포함 |

임계값 하나로 유전자를 on/off하면 측정 오차가 반응 제거로 증폭될 수 있습니다. 적어도 여러 threshold에서 결과가 유지되는지, metabolic task와 gene essentiality가 보존되는지 확인해야 합니다.

## 12. 작은 실습

```python
import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests

control = np.array([8.1, 8.5, 7.9, 8.3, 8.0])
treated = np.array([9.4, 9.0, 9.8, 9.2, 9.7])

# 독립 두 집단, 등분산을 가정하지 않는 Welch t-test
t, p = stats.ttest_ind(treated, control, equal_var=False)

# 실제 오믹스에서는 유전자별 p-value 전체를 함께 보정
p_values = np.array([p, 0.20, 0.003, 0.80, 0.041])
reject, p_adjusted_bh, _, _ = multipletests(
    p_values, alpha=0.05, method="fdr_bh"
)

print(t, p)
print(p_adjusted_bh)
print(reject)
```

이 코드는 통계 개념 시연용입니다. RNA-seq raw count에 유전자별 Welch t-test를 적용하는 예가 아닙니다. 실제 DEG에는 NB 기반 DESeq2/edgeR를 사용하십시오.

## 13. 스스로 점검

1. TPM과 DESeq2 normalized count가 각각 적합한 질문은 무엇입니까?
2. paired design을 independent t-test로 분석하면 어떤 정보가 사라집니까?
3. p=0.03, log₂FC=0.05인 유전자를 바로 모델의 핵심 반응으로 판단하면 안 되는 이유는 무엇입니까?
4. 20,000개 유전자에서 raw p<0.05만 적용할 때 예상되는 false positive 문제를 설명하십시오.
5. threshold를 바꿀 때 맥락 특이 모델의 핵심 결론이 뒤집히면 어떻게 보고해야 합니까?

## 다음 읽기

- 정규화 값을 GPR과 반응 점수로 변환하는 법: [Chapter 6](../chapter-6/README.md)
- 통계적 예측 성능(MCC, ROC-AUC, PR-AUC): [Chapter 7](../chapter-7/README.md), [Chapter 9](../chapter-9/README.md)
- Human2 범용 GEM과 그로부터 구축한 연령·성별 기관 파생 모델의 구분: [Chapter 5](../chapter-5/README.md)

## 참고문헌 / 공식 문서

1. Love, M. I., Huber, W., & Anders, S. (2014). [Moderated estimation of fold change and dispersion for RNA-seq data with DESeq2](https://doi.org/10.1186/s13059-014-0550-8). *Genome Biology*, 15, 550.
2. Robinson, M. D., McCarthy, D. J., & Smyth, G. K. (2010). [edgeR: a Bioconductor package for differential expression analysis of digital gene expression data](https://doi.org/10.1093/bioinformatics/btp616). *Bioinformatics*, 26, 139–140.
3. Benjamini, Y., & Hochberg, Y. (1995). [Controlling the false discovery rate](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x). *Journal of the Royal Statistical Society B*, 57, 289–300.
4. [DESeq2 Bioconductor documentation](https://bioconductor.org/packages/DESeq2/) · [edgeR Bioconductor documentation](https://bioconductor.org/packages/edgeR/)
