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

    def to_dict(self):
        return {
            "id": self.id,
            "country": self.country,
            "category": self.category,
            "amount_kg": self.amount_kg,
            "price_us": self.price_us,
            "date": self.date,
            "created_at": self.created_at
        }

create_table()