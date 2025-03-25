# FastAPI 코딩 규칙 (FastAPI Coding Rules)

## 기본 원칙
- 효율적이고 유지보수가 용이한 API 설계를 지향한다
- 타입 힌트와 Pydantic 모델을 적극 활용한다
- 문서화와 자동 검증 기능을 최대한 활용한다
- 비동기 프로그래밍의 장점을 적절히 활용한다

## 프로젝트 구조
- 기능별 모듈화 구조를 사용한다 (권장)
  ```
  src/
  ├── auth/
  │   ├── router.py
  │   ├── schemas.py
  │   ├── models.py
  │   ├── dependencies.py
  │   └── service.py
  ├── users/
  │   ├── router.py
  │   ├── schemas.py
  │   └── ... 
  ├── config.py
  └── main.py
  ```
- 각 도메인 디렉토리는 다음 구성요소를 포함한다:
  - `router.py`: 엔드포인트 정의
  - `schemas.py`: Pydantic 모델
  - `models.py`: 데이터베이스 모델
  - `dependencies.py`: 의존성 함수
  - `service.py`: 비즈니스 로직
  - `constants.py`: 상수 및 에러 코드
  - `exceptions.py`: 사용자 정의 예외

## 라우팅 및 API 설계
- REST 원칙을 따른다:
  - GET: 리소스 조회
  - POST: 리소스 생성
  - PUT: 리소스 전체 업데이트
  - PATCH: 리소스 부분 업데이트
  - DELETE: 리소스 삭제
- 명확하고 일관된 URL 패턴을 사용한다 (예: `/users/{user_id}/posts/{post_id}`)
- APIRouter를 사용하여 관련 엔드포인트를 그룹화한다
- 적절한 상태 코드를 반환한다 (201 Created, 204 No Content 등)
- 경로 매개변수와 쿼리 매개변수를 적절히 구분하여 사용한다

## Pydantic 모델
- 요청과 응답에 각각 별도의 Pydantic 모델을 정의한다
- 모든 데이터 검증은 Pydantic 모델을 통해 수행한다
- `response_model`을 사용하여 응답 스키마를 명시한다
- 공통 기능을 가진 기본 모델 클래스를 만들어 재사용한다
- 복잡한 검증 로직은 validator 데코레이터를 사용한다
- 선택적 필드에는 기본값을 제공하거나 Optional 타입을 사용한다

## 의존성 주입
- 공통 기능은 의존성 함수로 분리하여 재사용한다
- 의존성 함수는 작은 단위로 분리하고 체이닝을 통해 조합한다
- 데이터베이스 검증 로직은 의존성 함수를 통해 구현한다
- 가능한 비동기 의존성 함수를 사용한다
- 전역 의존성은 라우터 수준에서 적용한다
- 의존성 결과는 기본적으로 캐시되므로 이를 활용한다

## 데이터베이스 통합
- SQLAlchemy를 사용할 때는 비동기 API(asyncio)를 활용한다
- 데이터베이스 키와 테이블에 일관된 명명 규칙을 적용한다
- Alembic을 사용하여 마이그레이션을 관리한다
- 복잡한 쿼리는 SQL-first, Pydantic-second 접근 방식을 사용한다
- ORM 모델과 Pydantic 모델을 명확히 구분한다
- 데이터베이스 연결 풀을 적절히 설정한다

## 테스트 및 문서화
- 테스트 클라이언트는 처음부터 비동기로 설정한다
- 각 엔드포인트에 대한 단위 테스트와 통합 테스트를 작성한다
- OpenAPI 문서에 적절한 설명과 예시를 추가한다
- Swagger UI와 ReDoc을 활용하여 API 문서화를 개선한다
- 주요 함수와 클래스에 독스트링을 작성한다
- 예외 처리 시 명확한 에러 메시지를 제공한다

## 성능 최적화
- I/O 작업에는 비동기 함수(`async def`)를 사용한다
- CPU 집약적 작업은 별도의 스레드 풀에서 실행한다
- 동기 라이브러리를 사용할 때는 `run_in_threadpool`을 활용한다
- 백그라운드 작업은 `BackgroundTasks`를 사용하여 구현한다
- 대용량 파일 처리 시 청크 단위로 처리한다
- 캐싱 전략을 적용하여 반복 작업의 성능을 향상시킨다

## 보안
- 사용자 입력은 항상 Pydantic 모델로 검증한다
- JWT나 OAuth2를 사용한 인증을 구현한다
- CORS 설정을 적절히 구성한다
- 환경 변수와 시크릿은 `pydantic_settings.BaseSettings`를 통해 관리한다
- URL 호스트 검증을 구현하여 SSRF 공격을 방지한다
- 민감한 정보는 응답에서 제외한다

## 개발 환경 설정
- 코드 포맷팅에는 Black과 isort를 사용한다
- Ruff 같은 린터를 사용하여 코드 품질을 유지한다
- 의존성 관리는 Poetry를 사용한다
- 개발, 테스트, 프로덕션 환경에 대한 별도의 설정을 유지한다
- docker-compose를 사용하여 개발 환경을 표준화한다
- pre-commit 훅을 설정하여 코드 품질을 자동으로 검사한다
