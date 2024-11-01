from sqlalchemy.orm import Session
from shared.repositories.productions_repository import ProductionsRepository

class ProductionsService:
    @staticmethod
    def get_documents(db: Session):
        return ProductionsRepository.get_documents(db)

    @staticmethod
    def insert_many_documents(db: Session, documents):
        if not len(documents):
            return

        return ProductionsRepository.insert_many_documents(db, documents)
    
    @staticmethod
    def delete_documents(db: Session):
        return ProductionsRepository.delete_documents(db)
