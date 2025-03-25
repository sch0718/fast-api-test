"""
API 스키마 모듈

API 요청 및 응답을 위한 Pydantic 모델을 정의합니다.
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator

from src.common.constants import DateTimeFormat, ResponseCode, ResponseMessage, Status


class DataItem(BaseModel):
    """단일 데이터 항목 모델"""
    
    tfservicedtime: str = Field(..., description="서비스 날짜")
    timestamp: str = Field(..., description="타임스탬프")
    value: int = Field(..., description="값")
    status: Status = Field(..., description="상태")
    id: str = Field(..., description="고유 ID")
    
    @validator("tfservicedtime")
    def validate_service_date(cls, v: str) -> str:
        """서비스 날짜 형식 검증"""
        try:
            datetime.strptime(v, DateTimeFormat.DATE_ONLY)
            return v
        except ValueError:
            raise ValueError("올바른 날짜 형식이 아닙니다. (YYYYMMDD)")
    
    @validator("timestamp")
    def validate_timestamp(cls, v: str) -> str:
        """타임스탬프 형식 검증"""
        try:
            datetime.strptime(v, DateTimeFormat.LEGACY_DATETIME)
            return v
        except ValueError:
            try:
                datetime.strptime(v, DateTimeFormat.API_DATETIME)
                return v
            except ValueError:
                raise ValueError("올바른 시간 형식이 아닙니다. (YYYY-MM-DD HH:MM:SS)")


class DataRequest(BaseModel):
    """API 요청 모델"""
    
    startTime: str = Field(..., description="데이터 조회 시작 시간 (YYYY-MM-DDThh:mm:ss)")
    limitYn: str = Field("Y", description="데이터 수 제한 여부 (Y/N)")
    
    @validator("startTime")
    def validate_start_time(cls, v: str) -> str:
        """시작 시간 형식 검증"""
        try:
            datetime.strptime(v, DateTimeFormat.API_DATETIME)
            return v
        except ValueError:
            try:
                # 기존 형식도 지원
                dt = datetime.strptime(v, DateTimeFormat.LEGACY_DATETIME)
                # API 형식으로 변환하여 반환
                return dt.strftime(DateTimeFormat.API_DATETIME)
            except ValueError:
                raise ValueError("올바른 시간 형식이 아닙니다. (YYYY-MM-DDThh:mm:ss)")
    
    @validator("limitYn")
    def validate_limit_yn(cls, v: str) -> str:
        """제한 여부 값 검증"""
        if v not in ["Y", "N"]:
            raise ValueError("limitYn은 'Y' 또는 'N'이어야 합니다.")
        return v


class DataResponse(BaseModel):
    """API 응답 모델"""
    
    startTime: str = Field(..., description="요청된 시작 시간")
    res_code: str = Field(ResponseCode.SUCCESS.value, description="응답 코드")
    res_msg: str = Field(ResponseMessage.SUCCESS.value, description="응답 메시지")
    dataCnt: int = Field(0, description="데이터 개수")
    data: List[DataItem] = Field([], description="데이터 목록")
    
    class Config:
        """Pydantic 설정"""
        json_schema_extra = {
            "example": {
                "startTime": "2025-02-27T15:00:00",
                "res_code": "200",
                "res_msg": "성공",
                "dataCnt": 1,
                "data": [
                    {
                        "tfservicedtime": "20240220",
                        "timestamp": "2024-02-20T12:00:00",
                        "value": 1234,
                        "status": "SUCCESS",
                        "id": "DATA_0_20240220120000"
                    }
                ]
            }
        } 