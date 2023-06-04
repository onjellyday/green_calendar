# 환경 문제점

- . 가상환경 .venv의 부재

  - requirement.txt가 없어서 pip install -r requirements.txt를 할 수 없었음
  - .venv를 만들고 pip install -r requirements.txt를 통해 필요한 패키지를 설치함

- .gitignore도 없음
  - .gitignore : git에 올리지 않을 파일들을 명시하는 파일
- 보통 readme.md에 프로젝트에 대한 설명을 적는데, 해당 프로젝트에는 readme.md비어있다. (파이썬 버전 정보 및, 필요한 패키지들을 적어놓는 것이 좋음)
  - 아니면 requirement.txt로 대신하던가

---

## venv

- 파이썬의 패키지들은 무겁다. 그래서 가상환경을 만들어서 프로젝트마다 필요한 패키지만 설치해서 사용한다.
- 가상환경을 만들어서 사용하면, 프로젝트마다 필요한 패키지만 설치해서 사용할 수 있고, 프로젝트마다 다른 버전의 패키지를 사용할 수 있다.
- 윈도우 터미널에서 python -m venv .venv로 가상환경 폴더를 만든다. 그리고 .gitignore에 .venv를 추가한다.
- 이렇게되면, .venv에 패키지들이 설치되고, 이를 requirement.txt로 만들어서 다른 사람들이 설치할 수 있게 한다.
- pip freeze > requirements.txt로 requirement.txt를 만들 수 있다.
