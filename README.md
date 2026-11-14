# 영어 단어 암기 수준 분석 및 맞춤 복습 추천

학생이 직접 등록한 영어 단어로 퀴즈를 풀고, 정오 판정과 자기평가를 바탕으로 FSRS를 활용해 다음 복습 시기를 관리하는 Python 프로젝트입니다. 복습 계획을 스스로 관리하기 어려운 학생이 복습할 단어를 우선 학습하도록 돕는 것을 목표로 합니다.

Python 공동교육과정 수행평가를 위한 2인 개발 프로젝트이며, 최종발표 예정일은 2026-12-05입니다. 콘솔 기반 MVP를 먼저 개발합니다.

## 현재 상태

2026-11-14 현재 이 작업 트리에는 프로젝트 문서, 의존성 설정과 로컬 가상환경이 있습니다. Python 소스와 프로젝트 테스트는 아직 없으며 아래 기능은 구현 계획입니다. 다른 브랜치·작업 트리의 구현 여부는 확인하지 않았습니다.

| 요구 ID | 개발할 기능 | 이 작업 트리의 상태 |
| --- | --- | --- |
| F-01 | 영어 단어·여러 한국어 뜻 등록 및 중복 처리 | 코드 없음 |
| F-02 | 등록 목록 조회 및 내부 검색 필터 | 코드 없음 |
| F-03 | 한 회 최대 15문제의 주관식 퀴즈 | 코드 없음 |
| F-04 | 등록된 뜻을 기준으로 자동 채점·즉시 피드백 | 코드 없음 |
| F-05 | 회차 및 단어별 결과 표시 | 코드 없음 |
| F-06 | 정오 결과에 따른 기본 자기평가 및 평가 확정 | 코드 없음 |
| F-07 | FSRS 학습 상태 갱신 및 복습 일정 계산 | 코드 없음 |
| F-08 | 단어·학습 기록 자동 저장 및 복원 | 코드 없음 |
| F-09 | 복습 예정 단어 우선 선정 후 신규 단어로 보충 | 코드 없음 |

상세 동작과 검증 기준은 [요구 사항](docs/requirements.md)을 따릅니다. GUI, 통계, 외부 사전·단어장, 계정 관리 등은 MVP 이후 검토합니다.

## 개발 환경 준비

공통 개발 기준은 Python 3.11 계열이며, 콘솔 인터페이스와 JSON 저장을 우선 적용합니다. 외부 의존성은 `requirements.txt`의 `fsrs==6.3.2`입니다. JSON 처리와 기본 테스트에는 Python 표준 라이브러리를 사용합니다.

Windows PowerShell에서 저장소 또는 개발할 작업 트리의 루트로 이동한 뒤 실행합니다. Python 3.11이 설치되어 있어야 합니다.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip check
```

가상환경 생성은 해당 위치의 최초 설정 시에만 필요합니다. 의존성 파일이 바뀌면 설치 명령을 다시 실행합니다. 가상환경 활성화 없이 전용 Python 경로를 사용하므로 PowerShell 실행 정책을 변경할 필요가 없습니다. 이 컴퓨터에서는 `python`과 `py`의 기본 버전이 달라 생성 시 `-3.11`을 명시합니다.

VS Code에서는 `Python: Select Interpreter`에서 해당 작업 트리의 `.venv\Scripts\python.exe`를 선택합니다. 팀원과 다른 작업 트리에서도 각각 `.venv`를 새로 생성하며, 기존 가상환경을 복사하지 않습니다.

macOS/Linux 팀원은 Python 3.11 설치 후 `python3.11 -m venv .venv`로 만들고 `.venv/bin/python -m pip install -r requirements.txt`로 설치할 수 있습니다. 이 절차는 이번 Windows 환경에서 실행 검증한 범위에는 포함되지 않습니다.

`requirements.txt`는 라이브러리 설치 목록이고, `docs/requirements.md`는 기능 요구 사항입니다. 전역 환경의 패키지 목록을 그대로 설치 목록으로 가져오지 않습니다.

현재 실행 가능한 앱과 프로젝트 테스트는 없습니다. TODO: 기능 구현 후 검증한 앱 실행·테스트 명령을 추가합니다. FSRS 라이브러리 검증 결과와 범위는 [설계 문서](docs/design.md)의 환경 검증 기록에 남깁니다.

## 현재 파일 구조

```text
.
├── .gitignore
├── .venv/             # 로컬 전용, Git 제외
├── README.md
├── AGENTS.md
├── requirements.txt
└── docs/
    ├── requirements.md
    └── design.md
```

`main.py`, `words.py`, `quiz.py`, `review.py`, `storage.py`는 [설계 문서](docs/design.md)에 설명한 초기 구성안이며 아직 생성되지 않았습니다.

`tests/`는 첫 테스트 작성 시, 개인 기록 전용 `data/`는 저장 기능 구현 시 생성합니다. `/data/`는 Git에서 제외하며 공유 테스트 데이터가 필요하면 `tests/fixtures/`에 따로 둡니다.

## 협업과 학습 방식

- GitHub 저장소: [jungmin0112/english_vocab](https://github.com/jungmin0112/english_vocab)
- 현재 기록된 분담: 정민 — 퀴즈 모듈, 이연우 — 단어 저장·관리 모듈. 담당별 실제 완료 여부는 미확인입니다.
- 기능 브랜치·워크트리에서 작업하고 코드 검토 후 변경을 통합합니다. 커밋·푸시·PR 생성·병합은 사용자 요청 또는 승인에 따라 진행합니다.
- Codex로 작은 기능의 초안을 만든 뒤 개발자가 함수의 역할·입출력·제어 흐름을 읽고 직접 실행·수정·검증하며 학습합니다.
- 모듈 통합 전 두 팀원이 공통 데이터 구조와 함수 호출 계약을 확인합니다.
- 팀원은 공유된 브랜치를 내려받아 위 절차로 환경을 구성합니다. 소스·문서·`requirements.txt`·`.gitignore`는 Git으로 공유하고 `.venv`·개인 학습 기록·인증 정보는 각자 관리합니다. 로컬 절대 경로를 공통 설정에 넣지 않습니다.

## 문서

- [AGENTS.md](AGENTS.md): 에이전트의 공통 작업 지침
- [docs/requirements.md](docs/requirements.md): 실제 적용할 요구 사항 및 검증 기준
- [docs/design.md](docs/design.md): 초기 모듈 설계와 상세 설계 과제

문서 작성 근거는 [노션 문서 생성 기준](https://app.notion.com/p/418097f2b03b81d38877c2c3baef84e1), [1차 개발 계획서](https://app.notion.com/p/409097f2b03b81b1b2e4d270524e0288), [1차 요구 분석 명세서](https://app.notion.com/p/409097f2b03b81f59a0cc114c25dff4a)입니다. 요구 사항 적용 상태는 사용자의 최신 지시를 반영합니다.
