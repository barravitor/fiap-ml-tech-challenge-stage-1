from sqlalchemy.orm import Session
from ..repositories.commercialization_repository import CommercializationRepository

class CommercializationService:
    @staticmethod
    def get_documents(db: Session):
        return CommercializationRepository.get_documents(db)

    @staticmethod
    def insert_many_documents(db: Session, documents):
        return CommercializationRepository.insert_many_documents(db, documents)
    
    @staticmethod
    def delete_documents(db: Session):
        return CommercializationRepository.get_documents(db)
