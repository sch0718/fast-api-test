"""
데이터 모델 모듈

데이터 모델을 정의합니다. 확장 시 필요한 ORM 모델도 여기에 추가할 수 있습니다.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

from src.common.constants import Status


@dataclass
class CollectedData:
    """수집된 데이터 클래스"""
    
    start_time: str
    collection_time: datetime
    data_count: int
    data: List[Dict]
    
    @classmethod
    def from_api_response(cls, response_data: Dict, collection_time: Optional[datetime] = None) -> "CollectedData":
        """
        API 응답에서 CollectedData 객체 생성
        
        Args:
            response_data: API 응답 데이터
            collection_time: 수집 시간 (기본값: 현재 시간)
            
        Returns:
            CollectedData: 수집된 데이터 객체
        """
        if collection_time is None:
            collection_time = datetime.now()
            
        return cls(
            start_time=response_data.get("startTime", ""),
            collection_time=collection_time,
            data_count=response_data.get("dataCnt", 0),
            data=response_data.get("data", [])
        ) 