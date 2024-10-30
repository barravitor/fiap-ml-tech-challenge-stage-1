# app/routes/scrape_routes.py
from fastapi import APIRouter, Depends, HTTPException
import httpx
from sqlalchemy.orm import Session
from app.db.db import get_session_local
from app.helpers.jwt_helper import get_current_user
from app.services.index_service import scrape_data
import threading
from ..services.scrapre_status_service import ScrapeStatusService
from app.schemas.scrape_schemas import StatusResponseSchema

scrape_route = APIRouter()

@scrape_route.get("/status", response_model=list[StatusResponseSchema],
    dependencies=[Depends(get_current_user)],
    responses={
        200: {
            "description": "List of operations status.",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "name": "commercialization",
                            "running": True
                        },
                        {
                            "name": "importation",
                            "running": False
                        }
                    ]
                }
            }
        },
        401: {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "examples": {
                        "invalid_token": {
                            "summary": "Unauthorized",
                            "value": {
                                "detail": "Unauthorized: Invalid Token"
                            }
                        },
                        "not_authenticated": {
                            "summary": "Unauthorized",
                            "value": {
                                "detail": "Not authenticated"
                            }
                        }
                    }
                }
            }
        }
    }
)
async def get_status(current_user: dict = Depends(get_current_user), db: Session = Depends(get_session_local)):
    """
    Returns a status about the scrape execution.
    
    - **Return**: List of operations status.
    """
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

@scrape_route.get("/rescrape",
    dependencies=[Depends(get_current_user)],
    responses={
        200: {
            "description": "Scrape the Embrapa website.",
            "content": {
                "application/json": {
                    "example": { "message": "The scraping process has started. The data will be processed." }
                }
            }
        },
        401: {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "examples": {
                        "invalid_token": {
                            "summary": "Unauthorized",
                            "value": {
                                "detail": "Unauthorized: Invalid Token"
                            }
                        },
                        "not_authenticated": {
                            "summary": "Unauthorized",
                            "value": {
                                "detail": "Not authenticated"
                            }
                        }
                    }
                }
            }
        }
    }
)
async def get_rescrape(current_user: dict = Depends(get_current_user)):
    """
    Scrape the Embrapa website.
    
    - **Return**: The scraping process has started. The data will be processed.
    """
    threading.Thread(target=scrape_data).start()

    return { "message": "The scraping process has started. The data will be processed." }