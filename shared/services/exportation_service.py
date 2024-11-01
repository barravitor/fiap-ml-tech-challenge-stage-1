from sqlalchemy.orm import Session
from shared.repositories.exportation_repository import ExportationRepository

class ExportationService:
    @staticmethod
    def get_documents(db: Session):
        return ExportationRepository.get_documents(db)

    @staticmethod
    def insert_many_documents(db: Session, documents):
        if not len(documents):
            return

        return ExportationRepository.insert_many_documents(db, documents)
    
    @staticmethod
    def delete_documents(db: Session):
        return ExportationRepository.delete_documents(db)
