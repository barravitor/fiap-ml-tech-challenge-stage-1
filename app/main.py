# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routes.index_routes import router
from app.db.db import create_table

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting the application...")
    create_table()
    yield
    print("Closing the application...")

app = FastAPI(lifespan=lifespan)

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the API!"}
