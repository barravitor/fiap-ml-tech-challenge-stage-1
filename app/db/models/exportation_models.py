# app/models/exportation_models.py
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from ..db import Base, create_table

class ExportationModelDb(Base):
    __tablename__ = 'exportation'

    id = Column(Integer, index=True, primary_key=True)
    country = Column(String, index=False, nullable=False)
    category = Column(String, index=True, nullable=False)
    amount_kg = Column(String, index=False, nullable=False)
    price_us = Column(String, index=False, nullable=False)
    date = Column(DateTime, index=True, nullable=False)
    created_at = Column(DateTime, index=True, nullable=False, default=lambda: datetime.now(datetime.timezone.utc))

create_table()