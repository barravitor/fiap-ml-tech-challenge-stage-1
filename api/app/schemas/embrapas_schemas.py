import datetime
from pydantic import BaseModel, Field
from typing import Optional

class FiltersSchema(BaseModel):
    category: Optional[str] = Field(None, description="Register category")
    min_year_date: Optional[str] = Field(None, description="Minimum year of register")
    max_year_date: Optional[str] = Field(None, description="Maximum year of register")
    min_price: Optional[float] = Field(None, gt=0, description="Minimum register price")
    max_price: Optional[float] = Field(None, gt=0, description="Maximum register price")

    class Config:
        from_attributes = True