from sqlalchemy.orm import Session
from ..repositories.exportation_repository import ExportationRepository

class ExportationService:
    @staticmethod
    def get_documents(db: Session):
        return ExportationRepository.get_documents(db)

    @staticmethod
    def insert_many_documents(db: Session, documents):
        return ExportationRepository.insert_many_documents(db, documents)
    
    @staticmethod
    def delete_documents(db: Session):
        return ExportationRepository.get_documents(db)
