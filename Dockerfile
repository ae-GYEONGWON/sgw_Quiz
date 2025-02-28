# FastAPI 기반 컨테이너 이미지 생성
FROM python:3.12

# 작업 디렉토리 설정
WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client

# Poetry 설치
RUN pip install poetry

# Poetry 가상환경을 사용하지 않도록 설정
ENV POETRY_VIRTUALENVS_CREATE=false

# 프로젝트 의존성 파일 복사 (✅ `poetry.lock` 포함!)
COPY pyproject.toml poetry.lock ./

# Poetry를 사용하여 의존성 설치
RUN poetry install --no-root

# 앱 소스 코드 복사
COPY src src

# Entrypoint 스크립트 복사 (✅ 추가)
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 컨테이너 시작 시 `entrypoint.sh` 실행 (✅ 변경)
ENTRYPOINT ["/entrypoint.sh"]
