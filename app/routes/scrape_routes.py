# app/routes/scrape_routes.py
from fastapi import APIRouter, Depends
from app.helpers.jwt_helpers import get_current_user
from app.services.index_services import scrape_data
import threading

scrape_route = APIRouter()

@scrape_route.get("/rescrape")
async def get_rescrape(current_user: dict = Depends(get_current_user)):
    threading.Thread(target=scrape_data).start()

    return { "message": "The scraping process has started. The data will be processed." }