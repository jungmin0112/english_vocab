# 영어 단어 퀴즈

Python 3.11 콘솔 퀴즈 모듈입니다. JSON 단어 파일을 읽어 문제 진행·채점·결과·자기평가를 제공합니다.
출제 대상 선정, FSRS 계산, 학습 기록 저장은 연결 전입니다.

## 실행

외부 라이브러리 없이 Python 표준 라이브러리만 사용합니다.
Windows PowerShell에서 처음 한 번 가상환경을 생성합니다.

```powershell
py -3.11 -m venv .venv
```

샘플 단어로 실행:

```powershell
.\.venv\Scripts\python.exe -X utf8 quiz.py tests/fixtures/words.json --demo
```

출제할 영어 키를 직접 지정:

```powershell
.\.venv\Scripts\python.exe -X utf8 quiz.py tests/fixtures/words.json run apple
```

정답은 Good, 오답은 Again이 기본값입니다. 결과 화면에서 정답 번호를 선택해
Hard/Good/Easy를 변경하고 Enter로 확정합니다. Ctrl+C 또는 입력 종료는 회차를 취소합니다.
단독 CLI는 확정 평가를 화면에 표시하며 파일에 저장하지 않습니다.
개인 단어 파일은 Git에서 제외된 `data/` 안에 보관합니다.

## 검증과 설계

```powershell
.\.venv\Scripts\python.exe -X utf8 -m unittest discover -s tests -v
```

10개 테스트 통과. JSON 구조·함수 입출력·예외 처리·통합 대기 사항은
[퀴즈 설계](docs/quiz-design.md), 용어는 [용어집](GLOSSARY.md)을 참고하세요.
