# app/routes/scrape_routes.py
from fastapi import APIRouter, Depends, HTTPException
import httpx
from sqlalchemy.orm import Session
from app.db.db import get_session_local
from app.helpers.jwt_helper import get_current_user
from app.services.index_service import scrape_data
import threading
from ..services.scrapre_status_service import ScrapeStatusService

scrape_route = APIRouter()

@scrape_route.get("/status")
async def get_status(current_user: dict = Depends(get_current_user), db: Session = Depends(get_session_local)):
    try:
        documents = ScrapeStatusService.get_documents(db)

        db.close()

        return list(map(lambda document: {
            "name": document['name'],
            "running": document['running']
        }, documents))
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error to find data: {str(e)}")

@scrape_route.get("/rescrape")
async def get_rescrape(current_user: dict = Depends(get_current_user)):
    threading.Thread(target=scrape_data).start()

    return { "message": "The scraping process has started. The data will be processed." }