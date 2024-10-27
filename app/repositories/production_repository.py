from sqlalchemy.orm import Session
from ..db.models.index_models import Production

class ProductionRepository:
    @staticmethod
    def get_productions(db: Session):
        results = db.query(Production).all()

        data = [prod.__dict__ for prod in results]

        for item in data:
            item.pop("_sa_instance_state", None)
            item.pop("id", None)

        return data
    
    @staticmethod
    def insert_many(db: Session, productions):
        try:
            db.bulk_insert_mappings(Production, productions)
            db.commit()
            return productions
        except Exception as e:
            print(f"Error to insert_many productions: {e}")