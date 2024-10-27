# app/schemas/user_login_schemas.py
from pydantic import BaseModel, EmailStr, Field

class UserLogin(BaseModel):
    email: EmailStr = Field(..., example="youremail@example.com", description="Your valid email")
    password: str = Field(..., example="yourpassword", description="The user's password.")

    class Config:
        from_attributes = True