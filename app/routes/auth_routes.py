# app/routes/auth_routes.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.index_schemas import UserRegisterSchema, UserLoginSchema, TokenSchema
from app.db.models.index_models import UserModelDb
from app.db.db import SessionLocal
from datetime import datetime, timezone
from passlib.context import CryptContext
from app.helpers.jwt_helper import create_jwt_token

auth_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_session_local():
    yield SessionLocal()

@auth_router.post("/register", response_model=TokenSchema,
    responses={
        200: {
            "description": "User registered successfully. Returns an access token.",
            "content": {
                "application/json": {
                    "schema": TokenSchema.model_json_schema(),
                    "example": {
                        "access_token": "token_jwt_generated",
                        "token_type": "bearer"
                    }
                }
            }
        },
        400: {
            "description": "Bad Request.",
            "content": {
                "application/json": {
                    "examples": {
                        "email_already_registered": {
                            "summary": "Email already registered",
                            "value": {
                                "detail": "Email already registered. Please choose another valid email."
                            }
                        }
                    }
                }
            }
        },
        422: {
            "description": "Erro de validação. Os dados fornecidos não estão corretos.",
            "content": {
                "application/json": {
                    "examples": {
                        "wrong_password": {
                            "summary": "Unprocessable Entity",
                            "value": {
                                "detail": "The password entered does not match the password confirmation"
                            }
                        }
                    }
                }
            }
        }
    }
)
def register(user: UserRegisterSchema, db: Session = Depends(get_session_local)):
    """
    Register a new user on the platform.
    
    - **Return**: An access token on success.

    ## Possible Errors:
    - **400 Bad Request**: If the email has already been registered.
    - **422 Unprocessable Entity**: If the data provided does not pass validation..
    """
    if user.password != user.password_confirm:
        raise HTTPException(status_code=422, detail="The password entered does not match the password confirmation")

    existing_user = db.query(UserModelDb).filter(UserModelDb.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered. Please choose another email.")
    
    new_user = UserModelDb(
        name=user.name,
        email=user.email,
        password=pwd_context.hash(user.password),
        created_at=datetime.now(timezone.utc)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_jwt_token(data={"sub": user.email, "expires_delta": datetime.now(timezone.utc).timestamp() + 3600 })
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.post("/login", response_model=TokenSchema,
    responses={
        200: {
            "description": "Returns an access token.",
            "content": {
                "application/json": {
                    "schema": TokenSchema.model_json_schema(),
                    "example": {
                        "access_token": "token_jwt_generated",
                        "token_type": "bearer"
                    }
                }
            }
        },
        400: {
            "description": "Bad Request.",
            "content": {
                "application/json": {
                    "examples": {
                        "incorrect_email_or_password": {
                            "summary": "Incorrect email or password",
                            "value": {
                                "detail": "Incorrect email or password"
                            }
                        }
                    }
                }
            }
        }
    }
)
def login(user: UserLoginSchema, db: Session = Depends(get_session_local)):
    """
    Log the user into the platform.
    
    - **Return**: An access token on success.

    ## Possible Errors:
    - **400 Bad Request**: If are incorrect email or password.
    """
    db_user = db.query(UserModelDb).filter(UserModelDb.email == user.email).first()

    if db_user is None or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
        
    access_token = create_jwt_token(data={ "sub": db_user.email, "expires_delta": datetime.now(timezone.utc).timestamp() + 3600 })
    return {"access_token": access_token, "token_type": "bearer"}
