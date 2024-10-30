from datetime import datetime, timezone
from typing import Dict, Optional
from sqlalchemy.orm import Session
from ..repositories.scrape_status_repository import ScrapeStatusRepository

class ScrapeStatusService:
    @staticmethod
    def get_document_by_name(db: Session, name: str):
        return ScrapeStatusRepository.get_document_by_name(db=db, name=name)

    @staticmethod
    def get_documents(db: Session, filters = None):
        return ScrapeStatusRepository.get_documents(db=db, filters=filters)
    
    @staticmethod
    def start_scrape(name: str, db: Session):
        return ScrapeStatusRepository.update_document_by_name(db=db, name=name, update_fields={
            "running": True,
            "start_date": datetime.now(timezone.utc)
        })
    
    @staticmethod
    def finished_scrape(name: str, db: Session):
        return ScrapeStatusRepository.update_document_by_name(db=db, name=name, update_fields={
            "running": False,
            "end_date": datetime.now(timezone.utc)
        })
