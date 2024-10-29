# app/models/commercialization_models.py
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from ..db import Base, create_table

class CommercializationModelDb(Base):
    __tablename__ = 'commercialization'

    id = Column(Integer, index=True, primary_key=True)
    name = Column(String, index=False, nullable=False)
    category = Column(String, index=True, nullable=False)
    amount_liters = Column(String, index=False, nullable=False)
    date = Column(DateTime, index=True, nullable=False)
    created_at = Column(DateTime, index=True, nullable=False, default=lambda: datetime.now(datetime.timezone.utc))

create_table()