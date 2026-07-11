# 설치 가이드: 실습 환경 구축 (Linux · macOS)와 Gurobi 라이선스

> 이 장은 본문·[Chapter 10](chapter-10/README.md) 실습을 재현하기 위한 설치 절차를 정리한다. 기준 환경은 **Python 3.10 이상**과 **[COBRApy](https://opencobra.github.io/cobrapy/) 0.30.0**이다. 명령어의 세부는 배포판·버전에 따라 달라질 수 있으므로, 각 도구의 공식 문서를 함께 확인한다.

## 1. 무엇을, 왜 설치하는가

| 구성 요소 | 역할 | 필수 여부 |
|:---|:---|:---|
| Python 3.10+ | 실행 환경 | 필수 |
| 가상환경(venv 또는 conda) | 프로젝트별 의존성 격리 | 강력 권장 |
| [COBRApy](https://opencobra.github.io/cobrapy/) | 제약 기반 대사 모델링 라이브러리 | 필수 |
| GLPK (기본 LP/MILP 솔버) | COBRApy에 기본 포함되는 오픈소스 솔버 | 기본 포함 |
| [Gurobi](https://www.gurobi.com/) 또는 CPLEX | 대규모 모델·MILP를 빠르게 푸는 상용 솔버(학술 무료) | 선택(권장) |
| Jupyter | 노트북 실습 | 실습용 |

{% hint style="info" %}
**왜 가상환경인가:** 시스템 Python에 바로 설치하면 다른 프로젝트와 버전이 충돌하기 쉽다. 프로젝트마다 독립된 가상환경을 두면 `cobra==0.30.0`처럼 버전을 고정해 재현성을 확보할 수 있다.
{% endhint %}

## 2. 운영체제별 사전 준비

### Linux (Ubuntu/Debian 계열)

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip build-essential
python3 --version   # 3.10 이상인지 확인
```

- `build-essential`은 일부 패키지의 컴파일에 필요하다.
- Red Hat/Fedora 계열은 `sudo dnf install python3 python3-virtualenv gcc-c++`를 사용한다.
- **Windows 사용자**는 [WSL2](https://learn.microsoft.com/windows/wsl/install)로 Ubuntu를 설치하면 이 문서의 Linux 절차를 그대로 따를 수 있다.

### macOS (Intel · Apple Silicon)

```bash
# Homebrew가 없다면 먼저 설치: https://brew.sh
brew install python@3.12
python3 --version
```

- Apple Silicon(M1~)에서도 COBRApy와 GLPK는 네이티브로 동작한다.
- Xcode Command Line Tools가 없다면 `xcode-select --install`을 먼저 실행한다.

## 3. 가상환경 만들기

{% tabs %}
{% tab title="venv (표준 라이브러리)" %}
```bash
mkdir gem-lab && cd gem-lab
python3 -m venv .venv
source .venv/bin/activate        # 활성화 (프롬프트 앞에 (.venv) 표시)
python -m pip install --upgrade pip
# 작업이 끝나면: deactivate
```
{% endtab %}

{% tab title="conda / mamba" %}
```bash
conda create -n gem-lab python=3.12
conda activate gem-lab
python -m pip install --upgrade pip
```
{% endtab %}
{% endtabs %}

## 4. COBRApy와 실습 패키지 설치

```bash
python -m pip install "cobra==0.30.0"
# 실습에 쓰는 보조 패키지
python -m pip install jupyterlab numpy pandas matplotlib scipy scikit-learn networkx plotly ipywidgets
python -m pip check     # 의존성 충돌 여부 확인
```

설치 직후 최소 검증:

```python
import cobra
model = cobra.io.load_model("textbook")   # e_coli_core (반응 95 · 대사물 72 · 유전자 137)
print(cobra.__version__)
print(len(model.reactions), len(model.metabolites), len(model.genes))
print(model.optimize().objective_value)   # ≈ 0.8739 h^-1
# 기대 출력 예:
# 0.30.0
# 95 72 137
# 0.8739215069684307
```

{% hint style="info" %}
**기본 솔버(GLPK)** 는 COBRApy 설치 시 `optlang`·`swiglpk`를 통해 함께 들어오므로 별도 설치가 필요 없다. 작은/중간 모델에는 충분하다. 대규모 모델이나 MILP(예: [OptKnock](chapter-8/06.md), [ROOM](supplements/perturbation-analysis.md))에서는 Gurobi/CPLEX가 훨씬 빠르다.
{% endhint %}

## 5. Gurobi 설치와 학술 라이선스 취득

Gurobi는 상용 솔버이지만 **학생·교직원에게 무료 학술 라이선스**를 제공한다. 절차는 (1) 계정 등록 → (2) 라이선스 요청 → (3) 라이선스 파일 설치 → (4) Python 연동 순서다.

### 5.1 계정 등록과 라이선스 요청

1. [Gurobi 계정 페이지](https://portal.gurobi.com/iam/register/)에서 **학교 이메일**로 무료 계정을 만든다.
2. 로그인 후 [User Portal → Licenses → Request](https://portal.gurobi.com/iam/licenses/request)에서 라이선스 종류를 고른다.
   - **Named-User Academic**: 개인 학습·연구용. 한 사용자·한 기기에 설치. 학교 네트워크에서 검증한다.
   - **Academic WLS (Web License Service)**: 컨테이너·클라우드·CI·공용 서버용. 네트워크 검증 없이 토큰으로 인증한다.
3. 라이선스를 요청하면 설치 명령(예: `grbgetkey <라이선스키>`)이나 WLS 자격 증명이 발급된다.

{% hint style="warning" %}
❓ **흔한 오해:** `pip install gurobipy`만 하면 바로 대규모 모델을 풀 수 있다고 생각하기 쉽다. `gurobipy`에 기본 포함된 것은 **크기 제한이 있는 평가판**이다(변수·제약 수 제한). 제한을 없애려면 아래의 **학술 라이선스**를 반드시 설치해야 한다.
{% endhint %}

### 5.2 설치와 라이선스 적용

가장 간단한 방법은 Python 패키지로 설치하는 것이다.

```bash
python -m pip install gurobipy
```

**Named-User Academic** 라이선스는 학교 네트워크(또는 학교 VPN)에 연결한 상태에서 발급받은 명령을 실행해 적용한다.

```bash
# User Portal에서 발급된 실제 키로 <KEY>를 대체한다.
grbgetkey <KEY>
# 성공하면 홈 디렉터리 등에 gurobi.lic 파일이 생성된다.
```

**Academic WLS** 라이선스(컨테이너·클라우드)는 발급된 자격 증명으로 `gurobi.lic`을 직접 만든다.

```text
WLSACCESSID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
WLSSECRET=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
LICENSEID=1234567
```

Gurobi는 `GRB_LICENSE_FILE` 환경변수나 표준 경로(`~/gurobi.lic`)에서 라이선스를 찾는다.

### 5.3 COBRApy에서 Gurobi 사용

```python
import cobra
model = cobra.io.load_model("textbook")
model.solver = "gurobi"          # 이 한 줄로 솔버 전환 (glpk / gurobi / cplex)
solution = model.optimize()
print(model.solver.interface.__name__)   # optlang.gurobi_interface 확인
print(solution.objective_value)
```

{% hint style="success" %}
**설치가 잘 되었는지 확인:** 위 코드가 오류 없이 `objective_value`를 출력하면 Gurobi 연동이 완료된 것이다. 라이선스 문제가 있으면 `GurobiError: ... size-limited license` 또는 `No Gurobi license found` 메시지가 나오므로, 5.1~5.2를 다시 확인한다.
{% endhint %}

- **CPLEX**(IBM ILOG)도 [학술 프로그램](https://www.ibm.com/academic)으로 무료 제공되며, 설치 후 `model.solver = "cplex"`로 사용한다.
- 공식 문서: [Gurobi 학술 라이선스 안내](https://www.gurobi.com/academia/academic-program-and-licenses/), [Gurobi Quickstart](https://docs.gurobi.com/current/#quickstart.html).

## 6. Jupyter 커널 등록과 실습 실행

```bash
python -m ipykernel install --user --name gem-lab --display-name "GEM Lab (Python 3.12)"
jupyter lab      # 브라우저에서 노트북 실행
```

[Chapter 10](chapter-10/README.md)의 preflight 셀을 먼저 실행해 Python·COBRApy·솔버·모델 checksum을 고정한 뒤 실습을 진행한다. 대화형 그래프([Plotly](https://plotly.com/python/)·[ipywidgets](https://ipywidgets.readthedocs.io/))는 GitBook 지면이 아니라 **Jupyter에서 실행할 때** 상호작용한다.

## 7. 설치 검증 체크리스트

```python
import sys, cobra
print("python", sys.version.split()[0])          # 3.10 이상
print("cobra", cobra.__version__)                # 0.30.0
m = cobra.io.load_model("textbook")
for s in ("glpk", "gurobi", "cplex"):
    try:
        m.solver = s
        print(f"{s}: OK ({m.optimize().objective_value:.4f})")
    except Exception as e:
        print(f"{s}: 사용 불가 ({type(e).__name__})")
```

- `glpk: OK`가 나오면 본문 대부분의 실습을 실행할 수 있다.
- `gurobi: OK`가 나오면 대규모 모델·MILP 실습이 빨라진다.

## 8. 자주 겪는 문제

| 증상 | 원인·해결 |
|:---|:---|
| `pip install cobra`가 컴파일 오류 | Linux에서 `build-essential`, macOS에서 Command Line Tools 설치 후 재시도 |
| `No Gurobi license found` | 5.2의 `grbgetkey` 미실행 또는 `gurobi.lic` 경로 문제. `GRB_LICENSE_FILE` 확인 |
| `size-limited license` 경고 | 평가판 상태. 학술 라이선스(5.1) 발급·적용 필요 |
| `grbgetkey`가 실패 | Named-User 라이선스는 학교 네트워크/VPN에서 실행해야 함. 컨테이너면 WLS로 전환 |
| Jupyter에서 커널이 안 보임 | 6절의 `ipykernel install`을 가상환경을 활성화한 상태에서 실행했는지 확인 |
| 대화형 차트가 GitBook에서 안 움직임 | 정상 동작이다. GitBook 지면은 정적이며, 상호작용은 Jupyter 또는 [대화형 탐색기](https://jyryu3161.github.io/ebook_metabolic_modeling/interactive/index.html)에서 확인한다 |

---

*설치 이후의 첫 실습은 [Chapter 10. COBRApy 완전 실행 튜토리얼](chapter-10/README.md)에서 이어진다. 개념적 출발점은 [Chapter 1](chapter-1/README.md)이다.*
