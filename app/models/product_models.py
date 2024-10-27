# app/models/product_models.py
from sqlalchemy import Column, Float, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, index=True, primary_key=True)
    name = Column(String, index=False, nullable=False)
    category = Column(String, index=True, nullable=False)
    amount = Column(Float, index=False, nullable=True)
    date = Column(DateTime, index=True, nullable=False)
    created_at = Column(DateTime, index=True, nullable=False, default=lambda: datetime.now(datetime.timezone.utc)) 

    def __repr__(self):
        return f"<User(name={self.name}, email={self.email})>"
