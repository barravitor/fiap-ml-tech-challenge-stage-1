# app/models/user_models.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, index=True, primary_key=True)
    name = Column(String, index=False, nullable=False)
    email = Column(String, index=True, nullable=False, unique=True)
    password = Column(String, index=False, nullable=False)
    created_at = Column(DateTime, index=False, nullable=False, default=lambda: datetime.now(datetime.timezone.utc))

    def __repr__(self):
        return f"<User(name={self.name}, email={self.email})>"
