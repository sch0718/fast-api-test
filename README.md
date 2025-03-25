# API 데이터 수집 시스템

## 요구사항

1. HTTP 프로토콜을 이용한 API 통신
2. 데이터는 표준 JSON 형식 사용
3. Source(서버)와 Target(클라이언트) 구조 구현
4. Source
    - FastAPI를 사용하여 데이터를 API를 통해 전달하는 역할
    - 응답 예시:
    ```json
    {
        "startTime": "2025-02-27T15:00:00",
        "res_code": "200",
        "res_msg": "성공",
        "dataCnt": 1,
        "data": [
            { "tfservicedtime": "20240220", ... },
            ...
        ]
    }
    ```
5. Target
    - API를 호출하여 데이터를 수집하는 역할
    - 요청 예시:
    ```json
    {
        "startTime": "2025-02-27T15:00:00",
        "limitYn": "Y"
    }
    ```
6. Python 3.11+ 기반으로 구현
7. startTime 기준으로 현재 시간까지의 데이터 조회 (최대 50,000건)
8. 5분 단위로 API 호출 (비동기 작업 스케줄러 사용)

## 프로젝트 구조

```
src/
├── api/
│   ├── router.py      # FastAPI 라우터 정의
│   ├── schemas.py     # Pydantic 모델 정의
│   ├── service.py     # 비즈니스 로직
│   └── dependencies.py # 의존성 함수
├── client/
│   ├── collector.py   # API 호출 및 데이터 수집
│   └── scheduler.py   # 작업 스케줄러
├── common/
│   ├── config.py      # 공통 설정
│   ├── constants.py   # 상수 정의
│   └── exceptions.py  # 사용자 정의 예외
├── data/
│   └── models.py      # 데이터 모델 (필요시)
├── tests/             # 테스트 코드
├── main.py            # 애플리케이션 진입점
├── pyproject.toml     # 프로젝트 설정 및 의존성
└── config/
    └── config.yaml    # YAML 설정 파일
```

## 개발 환경 설정

### 1. 파이썬 설치

- Python 3.11 이상 버전 필요
- [공식 파이썬 웹사이트](https://www.python.org/downloads/)에서 다운로드

### 2. Poetry 설치

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 3. 프로젝트 의존성 설치

```bash
poetry install
```

### 4. 설정 파일 구성

`config/config.yaml` 파일을 생성하고 필요한 설정을 구성:

```yaml
# API 서버 설정
api:
  host: localhost
  port: 8000

# 데이터 수집 설정
collection:
  interval: 300
  max_records: 50000

# 로깅 설정
logging:
  level: INFO
  file: logs/api_service.log
```

환경 변수 `CONFIG_FILE`을 설정하여 다른 설정 파일을 지정할 수 있습니다:

```bash
export CONFIG_FILE=/path/to/your/config.yaml
```

## 코드 스타일

- 코드 형식: Black과 isort 사용
- 린팅: Ruff 사용
- 타입 검사: mypy 사용

```bash
# 코드 포맷팅
poetry run black .
poetry run isort .

# 린팅
poetry run ruff check .

# 타입 검사
poetry run mypy .
```

## 실행 방법

### 방법 1: 개발 모드

```bash
# Source 서버 실행
poetry run python -m src.main

# Target 클라이언트 실행
poetry run python -m src.client.collector
```

### 방법 2: 프로덕션 모드

```bash
# 서버 실행
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4

# 클라이언트 스케줄러 실행
poetry run python -m src.client.scheduler
```

### API 문서

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 테스트

```bash
poetry run pytest
```

## 수집된 데이터

- 수집된 데이터는 `data/collected` 디렉토리에 JSON 파일로 저장
- 파일명 형식: `{YYYY-MM-DD}_{HH-MM-SS}.json`
- 중복 데이터는 자동으로 필터링되며 로그에 기록