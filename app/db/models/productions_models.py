# app/models/production_models.py
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from ..db import Base, create_table

class ProductionsModelDb(Base):
    __tablename__ = 'productions'

    id = Column(Integer, index=True, primary_key=True)
    name = Column(String, index=False, nullable=False)
    category = Column(String, index=True, nullable=False)
    amount_liters = Column(String, index=False, nullable=False)
    date = Column(DateTime, index=True, nullable=False)
    created_at = Column(DateTime, index=True, nullable=False, default=lambda: datetime.now(datetime.timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "amount_liters": self.amount_liters,
            "date": self.date,
            "created_at": self.created_at
        }

create_table()