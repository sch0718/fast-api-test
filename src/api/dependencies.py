"""
API 의존성 모듈

FastAPI 의존성 주입을 위한 함수들을 정의합니다.
"""
from typing import Callable, Dict, Optional, Type

from fastapi import Depends, HTTPException, status
from loguru import logger

from src.api.schemas import DataRequest
from src.common.config import Settings, get_settings


async def get_request_data(
    request: DataRequest,
    settings: Settings = Depends(get_settings)
) -> DataRequest:
    """
    요청 데이터 검증 의존성
    
    Args:
        request: API 요청 데이터
        settings: 애플리케이션 설정
        
    Returns:
        DataRequest: 검증된 요청 데이터
        
    Raises:
        HTTPException: 요청 데이터가 유효하지 않은 경우
    """
    try:
        logger.debug(f"요청 데이터: {request.dict()}")
        return request
    except Exception as e:
        logger.error(f"요청 데이터 검증 실패: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"잘못된 요청 데이터: {str(e)}"
        )


async def validate_max_records(
    max_records: Optional[int] = None,
    settings: Settings = Depends(get_settings)
) -> int:
    """
    최대 레코드 수 검증 의존성
    
    Args:
        max_records: 최대 레코드 수 (None인 경우 설정값 사용)
        settings: 애플리케이션 설정
        
    Returns:
        int: 검증된 최대 레코드 수
    """
    if max_records is None:
        max_records = settings.MAX_RECORDS
    
    # 최대값이 설정 값을 초과하지 않도록 제한
    return min(max_records, settings.MAX_RECORDS) 