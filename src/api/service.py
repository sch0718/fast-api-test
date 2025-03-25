"""
API 서비스 모듈

비즈니스 로직을 처리하는 서비스 함수들을 제공합니다.
"""
import random
from datetime import datetime, timedelta
from typing import List, Optional

from loguru import logger

from src.api.schemas import DataItem, DataRequest
from src.common.constants import DateTimeFormat, Status
from src.common.exceptions import InvalidDateTimeFormatError


async def generate_sample_data(
    request: DataRequest, max_count: int = 100
) -> List[DataItem]:
    """
    샘플 데이터 생성 함수
    
    Args:
        request: 데이터 요청 객체
        max_count: 최대 데이터 수
        
    Returns:
        List[DataItem]: 생성된 데이터 목록
        
    Raises:
        InvalidDateTimeFormatError: 날짜 형식이 잘못된 경우
    """
    try:
        # 시작 시간 파싱
        start_time = datetime.strptime(request.startTime, DateTimeFormat.API_DATETIME)
    except ValueError:
        try:
            # 기존 형식 지원
            start_time = datetime.strptime(request.startTime, DateTimeFormat.LEGACY_DATETIME)
        except ValueError:
            logger.error(f"잘못된 시간 형식: {request.startTime}")
            raise InvalidDateTimeFormatError(f"잘못된 시간 형식: {request.startTime}")
    
    data_list: List[DataItem] = []
    current_time = datetime.now()
    
    # 데이터 수 결정 (limitYn=Y인 경우 적은 수의 데이터 반환)
    data_count = 15 if request.limitYn == "Y" else max_count
    
    # 현재 날짜 기준으로 샘플 데이터 생성
    for i in range(data_count):
        sample_time = start_time + timedelta(minutes=i*10)
        
        # 현재 시간을 초과하는 데이터는 생성하지 않음
        if sample_time > current_time:
            break
            
        # 데이터 생성
        data = DataItem(
            tfservicedtime=sample_time.strftime(DateTimeFormat.DATE_ONLY),
            timestamp=sample_time.strftime(DateTimeFormat.API_DATETIME),
            value=random.randint(1000, 9999),
            status=random.choice([s for s in Status]),
            id=f"DATA_{i}_{sample_time.strftime('%Y%m%d%H%M%S')}"
        )
        data_list.append(data)
    
    logger.info(f"생성된 데이터 수: {len(data_list)}")
    return data_list 