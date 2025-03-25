"""
API 데이터 수집 모듈

API를 호출하여 데이터를 수집하는 기능을 제공합니다.
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional

import httpx
from loguru import logger

from src.common.config import Settings, get_settings
from src.common.constants import DateTimeFormat, FILE_ENCODING, JSON_INDENT
from src.common.exceptions import (APIConnectionError, DataCollectionError,
                                  DataStorageError, InvalidResponseError)
from src.data.models import CollectedData


class DataCollector:
    """데이터 수집기 클래스"""
    
    def __init__(self, settings: Optional[Settings] = None):
        """
        초기화
        
        Args:
            settings: 설정 객체 (기본값: None, None인 경우 기본 설정 사용)
        """
        self.settings = settings or get_settings()
        self.last_run_time: Optional[datetime] = None
        self.data_directory = self.settings.DATA_DIRECTORY
        
        # 데이터 저장 디렉토리 생성
        if not os.path.exists(self.data_directory):
            os.makedirs(self.data_directory)
            logger.info(f"데이터 디렉토리 생성: {self.data_directory}")
    
    def _get_start_time(self) -> str:
        """
        시작 시간 결정
        
        Returns:
            str: 데이터 조회 시작 시간 (ISO 형식)
        """
        # 마지막 실행 기록이 없으면 1시간 전부터 데이터 수집
        if not self.last_run_time:
            start_time = datetime.now() - timedelta(hours=1)
        else:
            # 마지막 실행 시간부터 데이터 수집
            start_time = self.last_run_time
        
        return start_time.strftime(DateTimeFormat.API_DATETIME)
    
    async def collect_data(self) -> CollectedData:
        """
        API를 호출하여 데이터 수집
        
        Returns:
            CollectedData: 수집된 데이터 객체
            
        Raises:
            DataCollectionError: 데이터 수집 중 오류 발생 시
        """
        try:
            start_time = self._get_start_time()
            logger.info(f"데이터 수집 시작 - 시작 시간: {start_time}")
            
            # API 요청 데이터 준비
            request_data = {
                "startTime": start_time,
                "limitYn": "Y"  # 데이터 수 제한 여부
            }
            
            # API 호출 URL 생성
            api_url = f"{self.settings.API_BASE_URL}{self.settings.API_DATA_PATH}"
            logger.debug(f"API URL: {api_url}")
            
            # API 호출
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    api_url,
                    json=request_data,
                    timeout=30.0
                )
            
            # 응답 확인
            if response.status_code == 200:
                result = response.json()
                
                # 응답 결과 확인
                if result.get("res_code") == "200":
                    data_count = result.get("dataCnt", 0)
                    
                    if data_count > 0:
                        # 데이터 객체 생성
                        collected_data = CollectedData.from_api_response(result)
                        
                        # 데이터 저장
                        await self._save_data(collected_data)
                        logger.info(f"데이터 수집 완료 - {data_count}건")
                        
                        # 데이터가 MAX_RECORDS를 초과하면 추가 데이터를 수집하지 않음
                        if data_count >= self.settings.MAX_RECORDS:
                            logger.warning(f"최대 데이터 수 도달: {data_count}")
                        
                        # 현재 시간을 마지막 실행 시간으로 저장
                        self.last_run_time = datetime.now()
                        
                        return collected_data
                    else:
                        logger.info("새로운 데이터가 없습니다.")
                        # 현재 시간을 마지막 실행 시간으로 저장
                        self.last_run_time = datetime.now()
                        # 빈 데이터 객체 반환
                        return CollectedData(
                            start_time=start_time,
                            collection_time=datetime.now(),
                            data_count=0,
                            data=[]
                        )
                else:
                    error_msg = f"API 오류: {result.get('res_msg', '알 수 없는 오류')}"
                    logger.error(error_msg)
                    raise InvalidResponseError(error_msg)
            else:
                error_msg = f"API 호출 실패 - 상태 코드: {response.status_code}"
                logger.error(error_msg)
                raise APIConnectionError(error_msg)
                
        except httpx.RequestError as e:
            error_msg = f"API 연결 오류: {str(e)}"
            logger.error(error_msg)
            raise APIConnectionError(error_msg)
        except Exception as e:
            error_msg = f"데이터 수집 중 오류 발생: {str(e)}"
            logger.error(error_msg)
            raise DataCollectionError(error_msg)
    
    async def _save_data(self, data: CollectedData) -> str:
        """
        수집한 데이터 저장
        
        Args:
            data: 수집한 데이터
            
        Returns:
            str: 저장된 파일 경로
            
        Raises:
            DataStorageError: 데이터 저장 중 오류 발생 시
        """
        try:
            # 현재 시간으로 파일명 생성
            timestamp = data.collection_time.strftime(DateTimeFormat.FILENAME)
            filename = f"{self.data_directory}/data_{timestamp}.json"
            
            # 데이터를 dict로 변환
            data_dict = {
                "startTime": data.start_time,
                "collectionTime": data.collection_time.isoformat(),
                "dataCnt": data.data_count,
                "data": data.data
            }
            
            # JSON 파일로 저장
            with open(filename, 'w', encoding=FILE_ENCODING) as f:
                json.dump(data_dict, f, ensure_ascii=False, indent=JSON_INDENT)
                
            logger.info(f"데이터 저장 완료: {filename}")
            return filename
        except Exception as e:
            error_msg = f"데이터 저장 중 오류 발생: {str(e)}"
            logger.error(error_msg)
            raise DataStorageError(error_msg) 