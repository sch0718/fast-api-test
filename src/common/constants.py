"""
상수 정의 모듈

애플리케이션 전반에서 사용되는 상수들을 정의합니다.
"""
from enum import Enum, IntEnum


class ResponseCode(str, Enum):
    """API 응답 코드"""
    SUCCESS = "200"
    BAD_REQUEST = "400"
    UNAUTHORIZED = "401"
    NOT_FOUND = "404"
    SERVER_ERROR = "500"


class ResponseMessage(str, Enum):
    """API 응답 메시지"""
    SUCCESS = "성공"
    BAD_REQUEST = "잘못된 요청"
    UNAUTHORIZED = "인증 실패"
    NOT_FOUND = "리소스를 찾을 수 없음"
    SERVER_ERROR = "서버 오류"
    MISSING_START_TIME = "startTime이 필요합니다"
    NO_DATA = "데이터가 없습니다"


class Status(str, Enum):
    """데이터 상태"""
    SUCCESS = "SUCCESS"
    PENDING = "PENDING"
    FAILED = "FAILED"


class DateTimeFormat:
    """날짜/시간 형식"""
    API_DATETIME = "%Y-%m-%dT%H:%M:%S"
    LEGACY_DATETIME = "%Y-%m-%d %H:%M:%S"
    DATE_ONLY = "%Y%m%d"
    FILENAME = "%Y-%m-%d_%H-%M-%S"


# 파일 관련 상수
FILE_ENCODING = "utf-8"
JSON_INDENT = 2 