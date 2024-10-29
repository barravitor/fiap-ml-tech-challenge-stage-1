# app/schemas/scrape_schemas.py
from pydantic import BaseModel, Field

class StatusResponseSchema(BaseModel):
    name: str = Field(..., example="commercialization", description="The name of the tab execution")
    running: bool = Field(..., example="False", description="Tells if scrape is running")

    class Config:
        from_attributes = True
