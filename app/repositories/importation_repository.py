from sqlalchemy.orm import Session
from ..db.models.index_models import ImportationModelDb

class ImportationRepository:
    @staticmethod
    def get_documents(db: Session):
        try:
            results = db.query(ImportationModelDb).all()

            data = [prod.__dict__ for prod in results]

            for item in data:
                item.pop("_sa_instance_state", None)
                item.pop("id", None)

            return data
        except Exception as e:
            print(f"Error to get_documents: {e}")
    
    @staticmethod
    def insert_many_documents(db: Session, documents):
        try:
            db.bulk_insert_mappings(ImportationModelDb, documents)
            db.commit()
            return documents
        except Exception as e:
            print(f"Error to insert_many_documents: {e}")


    @staticmethod
    def delete_documents(db: Session):
        try:
            db.query(ImportationModelDb).delete()
            db.commit()
        except Exception as e:
            print(f"Error to delete_documents: {e}")