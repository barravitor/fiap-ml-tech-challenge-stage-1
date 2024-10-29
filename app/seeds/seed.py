from datetime import datetime
from ..db.db import SessionLocal 
from ..db.models.index_models import ScrapeStatusModelDb

def seed_db():
    db = SessionLocal()

    db.query(ScrapeStatusModelDb).delete()
    db.commit()

    scrape_status = [
        ScrapeStatusModelDb(name="productions", running=False, created_at=datetime.utcnow()),
        ScrapeStatusModelDb(name="processingn", running=False, created_at=datetime.utcnow()),
        ScrapeStatusModelDb(name="commercialization", running=False, created_at=datetime.utcnow()),
        ScrapeStatusModelDb(name="importation", running=False, created_at=datetime.utcnow()),
        ScrapeStatusModelDb(name="exportation", running=False, created_at=datetime.utcnow())
    ]

    db.add_all(scrape_status)
    
    db.commit()
    db.close()
    print("Seed finished!")

if __name__ == "__main__":
    seed_db()