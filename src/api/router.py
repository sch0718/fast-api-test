"""
API 라우터 모듈

API 엔드포인트를 정의합니다.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger

from src.api.dependencies import get_request_data, validate_max_records
from src.api.schemas import DataRequest, DataResponse
from src.api.service import generate_sample_data
from src.common.config import Settings, get_settings
from src.common.constants import ResponseCode, ResponseMessage
from src.common.exceptions import InvalidDateTimeFormatError

# API 라우터 생성
router = APIRouter(prefix="/api", tags=["data"])


@router.post("/data", response_model=DataResponse, status_code=status.HTTP_200_OK)
async def get_data(
    request: DataRequest = Depends(get_request_data),
    max_records: int = Depends(validate_max_records),
    settings: Settings = Depends(get_settings)
) -> DataResponse:
    """
    데이터 API 엔드포인트
    
    startTime부터 현재 시간까지의 데이터를 반환합니다.
    
    Args:
        request: 데이터 요청 객체
        max_records: 최대 데이터 수
        settings: 애플리케이션 설정
        
    Returns:
        DataResponse: 데이터 응답
        
    Raises:
        HTTPException: API 오류 발생 시
    """
    try:
        logger.info(f"데이터 요청 수신: startTime={request.startTime}, limitYn={request.limitYn}")
        
        # 데이터 생성
        data_items = await generate_sample_data(request, max_records)
        
        # 응답 생성
        response = DataResponse(
            startTime=request.startTime,
            res_code=ResponseCode.SUCCESS.value,
            res_msg=ResponseMessage.SUCCESS.value,
            dataCnt=len(data_items),
            data=data_items
        )
        
        logger.info(f"응답 데이터 개수: {len(data_items)}")
        return response
        
    except InvalidDateTimeFormatError as e:
        logger.error(f"날짜 형식 오류: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"날짜 형식 오류: {str(e)}"
        )
    except Exception as e:
        logger.error(f"API 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"서버 오류: {str(e)}"
        ) 