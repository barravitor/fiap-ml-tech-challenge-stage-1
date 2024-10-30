from datetime import datetime, timezone
from ..db.db import SessionLocal, create_table
from ..db.models.index_models import ScrapeStatusModelDb

def seed_db():
    db = SessionLocal()

    create_table()

    db.query(ScrapeStatusModelDb).delete()
    db.commit()

    scrape_status = [
        ScrapeStatusModelDb(name="productions", running=False, created_at=datetime.now(timezone.utc)),
        ScrapeStatusModelDb(name="processingn", running=False, created_at=datetime.now(timezone.utc)),
        ScrapeStatusModelDb(name="commercialization", running=False, created_at=datetime.now(timezone.utc)),
        ScrapeStatusModelDb(name="importation", running=False, created_at=datetime.now(timezone.utc)),
        ScrapeStatusModelDb(name="exportation", running=False, created_at=datetime.now(timezone.utc))
    ]

    db.add_all(scrape_status)
    
    db.commit()
    db.close()
    print("Seed finished!")

if __name__ == "__main__":
    seed_db()