# app/schemas/user_register_schemas.py
from pydantic import BaseModel, EmailStr, Field

class UserRegisterSchema(BaseModel):
    name: str = Field(..., example="Your Name", description="Your full name")
    email: EmailStr = Field(..., example="youremail@example.com", description="Your valid email")
    password: str = Field(..., example="yourpassword", min_length=8, description="The user's password. Must be at least 8 characters long.")
    password_confirm: str = Field(..., example="yourpassword", min_length=8, description="Confirm user password.")

    class Config:
        from_attributes = True