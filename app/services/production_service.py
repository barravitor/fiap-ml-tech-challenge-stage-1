from sqlalchemy.orm import Session
from ..repositories.production_repository import ProductionRepository

class ProductionService:
    @staticmethod
    def get_productions(db: Session):
        return ProductionRepository.get_productions(db)

    @staticmethod
    def insert_many(db: Session, productions):
        return ProductionRepository.insert_many(db, productions)
