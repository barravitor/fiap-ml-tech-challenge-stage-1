from sqlalchemy.orm import Session
from shared.repositories.processingn_repository import ProcessingnRepository

class ProcessingnService:
    @staticmethod
    def get_documents(db: Session):
        return ProcessingnRepository.get_documents(db)

    @staticmethod
    def insert_many_documents(db: Session, documents):
        if not len(documents):
            return

        return ProcessingnRepository.insert_many_documents(db, documents)
    
    @staticmethod
    def delete_documents(db: Session):
        return ProcessingnRepository.delete_documents(db)
