"""
API 데이터 수집 시스템 - 애플리케이션 진입점

FastAPI 애플리케이션을 초기화하고 설정합니다.
"""
import logging
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from src.api.router import router as api_router
from src.common.config import Settings, get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    애플리케이션 라이프사이클 관리
    
    Args:
        app: FastAPI 애플리케이션
    """
    # 애플리케이션 시작 시 실행할 코드
    logger.info("애플리케이션 시작")
    yield
    # 애플리케이션 종료 시 실행할 코드
    logger.info("애플리케이션 종료")


# 로깅 설정
def setup_logging():
    """로깅 설정 초기화"""
    settings = get_settings()
    
    # Loguru 로거 설정
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )
    
    logger.remove()  # 기존 핸들러 제거
    logger.add(
        settings.LOG_FILE,
        format=log_format,
        level=settings.LOG_LEVEL,
        rotation="10 MB",
        retention="7 days",
        compression="zip"
    )
    logger.add(lambda msg: print(msg), format=log_format, level=settings.LOG_LEVEL)
    
    # FastAPI 로깅 통합
    logging.getLogger("uvicorn").handlers = []
    logging.getLogger("fastapi").handlers = []


# FastAPI 애플리케이션 생성
def create_app() -> FastAPI:
    """
    FastAPI 애플리케이션 생성
    
    Returns:
        FastAPI: 설정된 FastAPI 애플리케이션
    """
    try:
        settings = get_settings()
        
        # 애플리케이션 설정
        app = FastAPI(
            title="API 데이터 수집 시스템",
            description="startTime부터 현재 시간까지의 데이터를 조회하고 수집하는 API 시스템",
            version="0.1.0",
            lifespan=lifespan
        )
        
        # CORS 미들웨어 설정
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # 실제 환경에서는 특정 출처만 허용하도록 설정
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # 라우터 등록
        app.include_router(api_router)
        
        return app
    except FileNotFoundError as e:
        logger.error(f"설정 파일 오류: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"애플리케이션 생성 중 오류 발생: {str(e)}")
        sys.exit(1)


try:
    # 로깅 설정 초기화
    setup_logging()
    
    # FastAPI 애플리케이션 인스턴스 생성
    app = create_app()
except Exception as e:
    print(f"애플리케이션 초기화 중 오류 발생: {str(e)}")
    sys.exit(1)


if __name__ == "__main__":
    """직접 실행 시 uvicorn 서버 시작"""
    try:
        settings = get_settings()
        logger.info(f"서버 시작: http://{settings.API_HOST}:{settings.API_PORT}")
        uvicorn.run(
            "src.main:app",
            host=settings.API_HOST,
            port=settings.API_PORT,
            reload=True
        )
    except Exception as e:
        logger.error(f"서버 시작 중 오류 발생: {str(e)}")
        sys.exit(1) 