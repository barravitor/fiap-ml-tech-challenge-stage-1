# app/models/user_models.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db import Base, create_table

class ScrapeStatusModelDb(Base):
    __tablename__ = 'scrape_status'

    id = Column(Integer, index=True, primary_key=True)
    name = Column(String, index=True, nullable=False, unique=True)
    running = Column(Boolean, index=False, nullable=False)
    start_date = Column(DateTime, index=False, nullable=True)
    end_date = Column(DateTime, index=False, nullable=True)
    updated_at = Column(DateTime, index=False, nullable=True)
    created_at = Column(DateTime, index=False, nullable=False, default=lambda: datetime.now(datetime.timezone.utc))

create_table()
