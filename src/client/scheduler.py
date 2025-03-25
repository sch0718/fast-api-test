"""
작업 스케줄러 모듈

주기적인 데이터 수집을 위한, 비동기 스케줄러를 구현합니다.
"""
import asyncio
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from loguru import logger

from src.client.collector import DataCollector
from src.common.config import Settings, get_settings
from src.common.exceptions import DataCollectionError


class DataCollectionScheduler:
    """데이터 수집 스케줄러 클래스"""
    
    def __init__(self, settings: Settings = None):
        """
        초기화
        
        Args:
            settings: 설정 객체 (기본값: None, None인 경우 기본 설정 사용)
        """
        self.settings = settings or get_settings()
        self.collector = DataCollector(self.settings)
        self.scheduler = AsyncIOScheduler()
        self.job = None
    
    def start(self):
        """스케줄러 시작"""
        # 스케줄러가 이미 실행 중인지 확인
        if self.scheduler.running:
            logger.warning("스케줄러가 이미 실행 중입니다.")
            return
        
        # 스케줄러에 작업 추가
        self.job = self.scheduler.add_job(
            self._collect_data_task,
            IntervalTrigger(seconds=self.settings.COLLECTION_INTERVAL),
            id="data_collection",
            replace_existing=True,
            next_run_time=datetime.now()  # 즉시 첫 실행
        )
        
        # 스케줄러 시작
        self.scheduler.start()
        logger.info(f"데이터 수집 스케줄러 시작 - 수집 간격: {self.settings.COLLECTION_INTERVAL}초")
    
    def stop(self):
        """스케줄러 중지"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("데이터 수집 스케줄러 중지")
        else:
            logger.warning("스케줄러가 실행 중이 아닙니다.")
    
    async def _collect_data_task(self):
        """데이터 수집 작업"""
        try:
            logger.info(f"데이터 수집 작업 시작: {datetime.now().isoformat()}")
            await self.collector.collect_data()
            logger.info(f"데이터 수집 작업 완료: {datetime.now().isoformat()}")
        except DataCollectionError as e:
            logger.error(f"데이터 수집 실패: {str(e)}")
        except Exception as e:
            logger.error(f"예상치 못한 오류 발생: {str(e)}")


async def run_scheduler():
    """스케줄러 실행 함수"""
    scheduler = DataCollectionScheduler()
    scheduler.start()
    
    try:
        # 스케줄러가 계속 실행되도록 유지
        while True:
            await asyncio.sleep(60)
    except KeyboardInterrupt:
        logger.info("키보드 인터럽트 감지, 스케줄러 종료")
        scheduler.stop()
    except Exception as e:
        logger.error(f"스케줄러 실행 중 오류 발생: {str(e)}")
        scheduler.stop()
        raise


if __name__ == "__main__":
    """스케줄러 직접 실행"""
    logger.info("데이터 수집 스케줄러 모듈 직접 실행")
    asyncio.run(run_scheduler()) 