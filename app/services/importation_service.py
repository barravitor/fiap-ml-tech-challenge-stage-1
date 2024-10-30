from sqlalchemy.orm import Session
from ..repositories.importation_repository import ImportationRepository

class ImportationService:
    @staticmethod
    def get_documents(db: Session):
        return ImportationRepository.get_documents(db)

    @staticmethod
    def insert_many_documents(db: Session, documents):
        if not len(documents):
            return

        return ImportationRepository.insert_many_documents(db, documents)
    
    @staticmethod
    def delete_documents(db: Session):
        return ImportationRepository.delete_documents(db)
