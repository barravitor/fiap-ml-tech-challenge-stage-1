# app/routes/embrapa_routes.py
import io
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
import httpx
from app.helpers.jwt_helpers import get_current_user
from app.schemas.index_schemas import Filters
from sqlalchemy.orm import Session
import pandas as pd
from app.db.db import SessionLocal
from app.services.index_services import ProductionService, check_if_file_exists

def get_session_local():
    yield SessionLocal()

CACHE_FILE_NAME = "productions.csv"

embrapa_router = APIRouter()

@embrapa_router.get("/productions", response_class=StreamingResponse)
async def get_productions(filters: Filters = Depends(), current_user: dict = Depends(get_current_user), db: Session = Depends(get_session_local)):
    try:
        if not check_if_file_exists(f"./tmp/{CACHE_FILE_NAME}"):
            data = ProductionService.get_productions(db)

            if not data:
                print("ERROR")

            df = pd.DataFrame(data[0:], columns=data[0])
            df.to_csv(f"./tmp/{CACHE_FILE_NAME}", index=False, header=True, sep=',', encoding='utf-8')
        else:
            df = pd.read_csv(f"./tmp/{CACHE_FILE_NAME}")

        df['date'] = pd.to_datetime(df['date'])
        
        if filters.category:
            df = df[df["category"] == filters.category]

        if filters.min_year_date:
            df = df[df['date'] >= pd.Timestamp(f"{filters.min_year_date}-12-21")]

        if filters.max_year_date:
            df = df[df['date'] <= (f"{filters.max_year_date}-12-31")]
        
        buffer = io.StringIO()

        df.to_csv(buffer, index=False)
        buffer.seek(0)

        return StreamingResponse(
            iter([buffer.getvalue()]),
            media_type="text/csv",
            headers={ "Content-Disposition": f"attachment; filename={CACHE_FILE_NAME}" },
        )
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error to find data: {str(e)}")
