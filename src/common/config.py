"""
공통 설정 모듈

YAML 설정 파일에서 애플리케이션 설정을 로드하는 기능을 제공합니다.
"""
import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings


class YamlConfigSettings(BaseSettings):
    """YAML 설정 파일을 로드하는 클래스"""
    
    @classmethod
    def from_yaml(cls, yaml_file: str) -> "YamlConfigSettings":
        """
        YAML 파일에서 설정 값을 로드
        
        Args:
            yaml_file: YAML 파일 경로
            
        Returns:
            YamlConfigSettings: 설정 객체
        """
        yaml_path = Path(yaml_file)
        if not yaml_path.exists():
            raise FileNotFoundError(f"설정 파일을 찾을 수 없습니다: {yaml_file}")

        with open(yaml_path, "r", encoding="utf-8") as f:
            config_values = yaml.safe_load(f)
            
        return cls(**config_values)


class Settings(YamlConfigSettings):
    """애플리케이션 설정 클래스"""

    # API 서버 설정
    api: Dict[str, Any] = Field(
        default_factory=lambda: {
            "host": "localhost",
            "port": 8000,
        }
    )
    
    # 데이터 수집 설정
    collection: Dict[str, Any] = Field(
        default_factory=lambda: {
            "interval": 300,
            "max_records": 50000,
        }
    )
    
    # 로깅 설정
    logging: Dict[str, Any] = Field(
        default_factory=lambda: {
            "level": "INFO",
            "file": "logs/api_service.log",
        }
    )
    
    # 데이터 저장 경로
    data_directory: str = "data/collected"
    
    @property
    def API_HOST(self) -> str:
        """API 호스트"""
        return self.api.get("host", "localhost")
    
    @property
    def API_PORT(self) -> int:
        """API 포트"""
        return self.api.get("port", 8000)
    
    @property
    def API_BASE_URL(self) -> str:
        """API 기본 URL"""
        return f"http://{self.API_HOST}:{self.API_PORT}"
    
    @property
    def API_DATA_PATH(self) -> str:
        """API 데이터 경로"""
        return "/api/data"
    
    @property
    def COLLECTION_INTERVAL(self) -> int:
        """데이터 수집 간격 (초)"""
        return self.collection.get("interval", 300)
    
    @property
    def MAX_RECORDS(self) -> int:
        """최대 레코드 수"""
        return self.collection.get("max_records", 50000)
    
    @property
    def LOG_LEVEL(self) -> str:
        """로그 레벨"""
        return self.logging.get("level", "INFO")
    
    @property
    def LOG_FILE(self) -> str:
        """로그 파일 경로"""
        return self.logging.get("file", "logs/api_service.log")
    
    @property
    def DATA_DIRECTORY(self) -> str:
        """데이터 저장 디렉토리"""
        return self.data_directory


@lru_cache
def get_settings() -> Settings:
    """
    설정 객체를 반환하는 함수
    
    환경 변수로 설정 파일 경로를 지정할 수 있습니다.
    기본값은 config/config.yaml 입니다.
    
    Returns:
        Settings: 설정 객체
    """
    config_file = os.environ.get("CONFIG_FILE", "config/config.yaml")
    return Settings.from_yaml(config_file) 