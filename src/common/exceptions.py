"""
사용자 정의 예외 모듈

애플리케이션에서 사용하는 커스텀 예외 클래스를 정의합니다.
"""
from fastapi import HTTPException, status


class APIError(Exception):
    """API 관련 기본 예외 클래스"""
    
    def __init__(self, message: str = "API 오류가 발생했습니다"):
        self.message = message
        super().__init__(self.message)


class DataCollectionError(APIError):
    """데이터 수집 중 발생하는 예외"""
    
    def __init__(self, message: str = "데이터 수집 중 오류가 발생했습니다"):
        super().__init__(message)


class APIConnectionError(APIError):
    """API 연결 관련 예외"""
    
    def __init__(self, message: str = "API 서버에 연결할 수 없습니다"):
        super().__init__(message)


class InvalidResponseError(APIError):
    """잘못된 API 응답 예외"""
    
    def __init__(self, message: str = "잘못된 API 응답을 받았습니다"):
        super().__init__(message)


class DataStorageError(APIError):
    """데이터 저장 관련 예외"""
    
    def __init__(self, message: str = "데이터를 저장하는 중 오류가 발생했습니다"):
        super().__init__(message)


class InvalidDateTimeFormatError(APIError):
    """잘못된 날짜/시간 형식 예외"""
    
    def __init__(self, message: str = "잘못된 날짜/시간 형식입니다"):
        super().__init__(message)


def http_exception_handler(status_code: int, detail: str) -> HTTPException:
    """HTTP 예외 핸들러"""
    return HTTPException(
        status_code=status_code,
        detail=detail
    ) 