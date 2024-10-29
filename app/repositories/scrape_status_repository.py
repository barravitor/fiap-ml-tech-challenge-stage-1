from datetime import datetime
from typing import Dict, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..db.models.index_models import ScrapeStatusModelDb

class ScrapeStatusRepository:
    @staticmethod
    def get_document_by_name(db: Session, name: str):
        try:
            document = db.query(ScrapeStatusModelDb).filter(ScrapeStatusModelDb.name == name).first()
            return document
        except Exception as e:
            print(f"Error to get_document_by_name: {e}")

    @staticmethod
    def get_documents(db: Session, filters: dict = None):
        try:
            query = db.query(ScrapeStatusModelDb)

            if filters:
                for key, value in filters.items():
                    if value is not None:
                        query = query.filter(getattr(ScrapeStatusModelDb, key) == value)

            results = query.all()
            data = [element.__dict__ for element in results]

            return data
        except Exception as e:
            print(f"Error to get_documents: {e}")

    @staticmethod
    def update_document_by_name(db: Session, name: str, update_fields: Dict[str, Optional[str]]):
        try:
            document = db.query(ScrapeStatusModelDb).filter(ScrapeStatusModelDb.name == name).first()

            if not document:
                raise HTTPException(status_code=404, detail="Document not found")

            for field, value in update_fields.items():
                if value is not None:
                    setattr(document, field, value)

            setattr(document, "updated_at", datetime.utcnow())

            db.commit()
        except Exception as e:
            print(f"Error to update_document_by_name: {e}")