from sqlalchemy.orm import Session
from shared.repositories.commercialization_repository import CommercializationRepository

class CommercializationService:
    @staticmethod
    def get_documents(db: Session):
        return CommercializationRepository.get_documents(db)

    @staticmethod
    def insert_many_documents(db: Session, documents):
        if not len(documents):
            return

        return CommercializationRepository.insert_many_documents(db, documents)
    
    @staticmethod
    def delete_documents(db: Session):
        return CommercializationRepository.delete_documents(db)
