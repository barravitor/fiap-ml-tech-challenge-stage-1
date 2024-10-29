# app/routes/embrapa_routes.py
import io
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
import httpx
from app.helpers.jwt_helper import get_current_user
from app.schemas.index_schemas import Filters
from sqlalchemy.orm import Session
import pandas as pd
from app.db.db import SessionLocal
from app.services.index_service import ProductionsService, ProcessingnService, ExportationService, CommercializationService, ImportationService, check_if_file_exists
from app.config import CACHED_TAB_PRODUCTIONS_FILE_NAME, CACHED_TAB_PROCESSINGN_FILE_NAME, CACHED_TAB_COMMERCIALIZATION_FILE_NAME, CACHED_TAB_IMPORTATION_FILE_NAME, CACHED_TAB_EXPORTATION_FILE_NAME

def get_session_local():
    yield SessionLocal()

embrapa_router = APIRouter()

def get_data_filtered(df, filters: Filters):
    df['date'] = pd.to_datetime(df['date'])

    if filters.category:
        df = df[df["category"] == filters.category]

    if filters.min_year_date:
        df = df[df['date'] >= pd.Timestamp(f"{filters.min_year_date}-12-21")]

    if filters.max_year_date:
        df = df[df['date'] <= pd.Timestamp(f"{filters.max_year_date}-12-31")]

    return df

@embrapa_router.get("/productions", response_class=StreamingResponse)
async def get_productions(filters: Filters = Depends(), current_user: dict = Depends(get_current_user), db: Session = Depends(get_session_local)):
    try:
        file_name = CACHED_TAB_PRODUCTIONS_FILE_NAME

        if not check_if_file_exists(f"./tmp/{file_name}"):
            data = ProductionsService.get_documents(db)

            if not data:
                print("ERROR")
                return

            df = pd.DataFrame(data[0:], columns=data[0])
            df.to_csv(f"./tmp/{file_name}", index=False, header=True, sep=',', encoding='utf-8')

        df = pd.read_csv(f"./tmp/{file_name}")

        df = get_data_filtered(df, filters)
        
        buffer = io.StringIO()

        df.to_csv(buffer, index=False)
        buffer.seek(0)

        return StreamingResponse(
            iter([buffer.getvalue()]),
            media_type="text/csv",
            headers={ "Content-Disposition": f"attachment; filename={file_name}" },
        )
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error to find data: {str(e)}")

@embrapa_router.get("/processingn", response_class=StreamingResponse)
async def get_processingn(filters: Filters = Depends(), current_user: dict = Depends(get_current_user), db: Session = Depends(get_session_local)):
    try:
        file_name = CACHED_TAB_PROCESSINGN_FILE_NAME

        if not check_if_file_exists(f"./tmp/{file_name}"):
            data = ProcessingnService.get_documents(db)

            if not data:
                print("ERROR")
                return

            df = pd.DataFrame(data[0:], columns=data[0])
            df.to_csv(f"./tmp/{file_name}", index=False, header=True, sep=',', encoding='utf-8')

        df = pd.read_csv(f"./tmp/{file_name}")

        df = get_data_filtered(df, filters)
        
        buffer = io.StringIO()

        df.to_csv(buffer, index=False)
        buffer.seek(0)

        return StreamingResponse(
            iter([buffer.getvalue()]),
            media_type="text/csv",
            headers={ "Content-Disposition": f"attachment; filename={file_name}" },
        )
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error to find data: {str(e)}")

@embrapa_router.get("/commercialization", response_class=StreamingResponse)
async def get_commercialization(filters: Filters = Depends(), current_user: dict = Depends(get_current_user), db: Session = Depends(get_session_local)):
    try:
        file_name = CACHED_TAB_COMMERCIALIZATION_FILE_NAME

        if not check_if_file_exists(f"./tmp/{file_name}"):
            data = CommercializationService.get_documents(db)

            if not data:
                print("ERROR")
                return

            df = pd.DataFrame(data[0:], columns=data[0])
            df.to_csv(f"./tmp/{file_name}", index=False, header=True, sep=',', encoding='utf-8')

        df = pd.read_csv(f"./tmp/{file_name}")

        df = get_data_filtered(df, filters)
        
        buffer = io.StringIO()

        df.to_csv(buffer, index=False)
        buffer.seek(0)

        return StreamingResponse(
            iter([buffer.getvalue()]),
            media_type="text/csv",
            headers={ "Content-Disposition": f"attachment; filename={file_name}" },
        )
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error to find data: {str(e)}")
    
@embrapa_router.get("/importation", response_class=StreamingResponse)
async def get_importation(filters: Filters = Depends(), current_user: dict = Depends(get_current_user), db: Session = Depends(get_session_local)):
    try:
        file_name = CACHED_TAB_IMPORTATION_FILE_NAME

        if not check_if_file_exists(f"./tmp/{file_name}"):
            data = ImportationService.get_documents(db)

            if not data:
                print("ERROR")
                return

            df = pd.DataFrame(data[0:], columns=data[0])
            df.to_csv(f"./tmp/{file_name}", index=False, header=True, sep=',', encoding='utf-8')

        df = pd.read_csv(f"./tmp/{file_name}")

        df = get_data_filtered(df, filters)
        
        buffer = io.StringIO()

        df.to_csv(buffer, index=False)
        buffer.seek(0)

        return StreamingResponse(
            iter([buffer.getvalue()]),
            media_type="text/csv",
            headers={ "Content-Disposition": f"attachment; filename={file_name}" },
        )
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error to find data: {str(e)}")
    
@embrapa_router.get("/exportation", response_class=StreamingResponse)
async def get_exportation(filters: Filters = Depends(), current_user: dict = Depends(get_current_user), db: Session = Depends(get_session_local)):
    try:
        file_name = CACHED_TAB_EXPORTATION_FILE_NAME

        if not check_if_file_exists(f"./tmp/{file_name}"):
            data = ExportationService.get_documents(db)

            if not data:
                print("ERROR")
                return

            df = pd.DataFrame(data[0:], columns=data[0])
            df.to_csv(f"./tmp/{file_name}", index=False, header=True, sep=',', encoding='utf-8')

        df = pd.read_csv(f"./tmp/{file_name}")

        df = get_data_filtered(df, filters)
        
        buffer = io.StringIO()

        df.to_csv(buffer, index=False)
        buffer.seek(0)

        return StreamingResponse(
            iter([buffer.getvalue()]),
            media_type="text/csv",
            headers={ "Content-Disposition": f"attachment; filename={file_name}" },
        )
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error to find data: {str(e)}")

