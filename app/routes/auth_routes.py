# app/routes/auth_routes.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import app.schemas.index_schemas as schemas
import app.db.models.index_models as models
from app.db.db import SessionLocal
from datetime import datetime, timezone
from passlib.context import CryptContext
from app.helpers.jwt_helper import create_jwt_token

auth_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_session_local():
    yield SessionLocal()

@auth_router.post("/register", response_model=schemas.Token)
def register(user: schemas.UserRegister, db: Session = Depends(get_session_local)):
    if user.password != user.password_confirm:
        raise HTTPException(status_code=400, detail="Passwords do not match.")

    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already in use.")

    new_user = models.User(
        name=user.name,
        email=user.email,
        password=pwd_context.hash(user.password),
        date=datetime.now(timezone.utc)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_jwt_token(data={"sub": user.email, "expires_delta": datetime.utcnow().timestamp() + 3600 })
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_session_local)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user is None or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
        
    access_token = create_jwt_token(data={ "sub": db_user.email, "expires_delta": datetime.utcnow().timestamp() + 3600 })
    return {"access_token": access_token, "token_type": "bearer"}
