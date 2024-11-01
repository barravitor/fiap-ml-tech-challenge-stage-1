# app/routes/embrapa_routes.py
import io
import os
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
import httpx
from app.helpers.jwt_helper import get_current_user
from app.schemas.index_schemas import FiltersSchema
from sqlalchemy.orm import Session
import pandas as pd
from shared.db.database import SessionLocal
from app.services.index_service import check_if_file_exists
from shared.services.index_service import ProductionsService, ProcessingnService, ExportationService, CommercializationService, ImportationService
from shared.config import CACHED_TAB_PRODUCTIONS_FILE_NAME, CACHED_TAB_PROCESSINGN_FILE_NAME, CACHED_TAB_COMMERCIALIZATION_FILE_NAME, CACHED_TAB_IMPORTATION_FILE_NAME, CACHED_TAB_EXPORTATION_FILE_NAME

def get_session_local():
    yield SessionLocal()

embrapa_router = APIRouter()

def get_data_filtered(df, filters: FiltersSchema):
    df['date'] = pd.to_datetime(df['date'])

    if filters.category:
        df = df[df["category"] == filters.category]

    if filters.min_year_date:
        df = df[df['date'] >= pd.Timestamp(f"{filters.min_year_date}-12-21")]

    if filters.max_year_date:
        df = df[df['date'] <= pd.Timestamp(f"{filters.max_year_date}-12-31")]

    return df

def save_data_on_cache(data, directory_path, file_name):
    os.makedirs(directory_path, exist_ok=True)

    df = pd.DataFrame(data[0:], columns=data[0])
    df.to_csv(f"{directory_path}/{file_name}", index=False, header=True, sep=',', encoding='utf-8')

@embrapa_router.get("/productions", response_class=StreamingResponse,
    responses={
        200: {
            "description": "CSV file with production data.",
            "content": {
                "text/csv": {
                    "example": "category,date\nVinhos de mesa,1970-12-21\nVinhos de mesa,1971-12-21\n"
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
        },
        404: {
            "description": "Data not found."
        },
        422: {
            "description": "Unprocessable Entity. Validation error in provided filters."
        },
    }
)
async def get_productions(filters: FiltersSchema = Depends(), current_user: dict = Depends(get_current_user), db: Session = Depends(get_session_local)):
    """
    Retrieve production data in CSV format.

    - **Return**: A CSV file with production data.

    ## Possible Errors:
    - **401 Unauthorized**: If the JWT token is not provided or is invalid.
    - **422 Unprocessable Entity**: If the provided filter data does not pass validation.
    """
    try:
        file_name = CACHED_TAB_PRODUCTIONS_FILE_NAME

        if not check_if_file_exists(f"./tmp/{file_name}"):
            data = ProductionsService.get_documents(db)

            if not data:
                raise HTTPException(status_code=404, detail="Data not found.")

            save_data_on_cache(data=data, directory_path="./tmp", file_name=file_name)

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

@embrapa_router.get("/processingn", response_class=StreamingResponse,
    responses={
        200: {
            "description": "CSV file with processingn data.",
            "content": {
                "text/csv": {
                    "example": "category,date\nVinhos de mesa,1970-12-21\nVinhos de mesa,1971-12-21\n"
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
        },
        404: {
            "description": "Data not found."
        },
        422: {
            "description": "Unprocessable Entity. Validation error in provided filters."
        },
    }
)
async def get_processingn(filters: FiltersSchema = Depends(), current_user: dict = Depends(get_current_user), db: Session = Depends(get_session_local)):
    """
    Retrieve processingn data in CSV format.

    - **Return**: A CSV file with processingn data.

    ## Possible Errors:
    - **401 Unauthorized**: If the JWT token is not provided or is invalid.
    - **422 Unprocessable Entity**: If the provided filter data does not pass validation.
    """
    try:
        file_name = CACHED_TAB_PROCESSINGN_FILE_NAME

        if not check_if_file_exists(f"./tmp/{file_name}"):
            data = ProcessingnService.get_documents(db)

            if not data:
                raise HTTPException(status_code=404, detail="Data not found.")

            save_data_on_cache(data=data, directory_path="./tmp", file_name=file_name)

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

@embrapa_router.get("/commercialization", response_class=StreamingResponse,
    responses={
        200: {
            "description": "CSV file with commercialization data.",
            "content": {
                "text/csv": {
                    "example": "category,date\nVinhos de mesa,1970-12-21\nVinhos de mesa,1971-12-21\n"
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
        },
        404: {
            "description": "Data not found."
        },
        422: {
            "description": "Unprocessable Entity. Validation error in provided filters."
        },
    }
)
async def get_commercialization(filters: FiltersSchema = Depends(), current_user: dict = Depends(get_current_user), db: Session = Depends(get_session_local)):
    """
    Retrieve commercialization data in CSV format.

    - **Return**: A CSV file with commercialization data.

    ## Possible Errors:
    - **401 Unauthorized**: If the JWT token is not provided or is invalid.
    - **422 Unprocessable Entity**: If the provided filter data does not pass validation.
    """
    try:
        file_name = CACHED_TAB_COMMERCIALIZATION_FILE_NAME

        if not check_if_file_exists(f"./tmp/{file_name}"):
            data = CommercializationService.get_documents(db)

            if not data:
                raise HTTPException(status_code=404, detail="Data not found.")

            save_data_on_cache(data=data, directory_path="./tmp", file_name=file_name)

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
    
@embrapa_router.get("/importation", response_class=StreamingResponse,
    responses={
        200: {
            "description": "CSV file with importation data.",
            "content": {
                "text/csv": {
                    "example": "category,date\nVinhos de mesa,1970-12-21\nVinhos de mesa,1971-12-21\n"
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
        },
        404: {
            "description": "Data not found."
        },
        422: {
            "description": "Unprocessable Entity. Validation error in provided filters."
        },
    }
)
async def get_importation(filters: FiltersSchema = Depends(), current_user: dict = Depends(get_current_user), db: Session = Depends(get_session_local)):
    """
    Retrieve importation data in CSV format.

    - **Return**: A CSV file with importation data.

    ## Possible Errors:
    - **401 Unauthorized**: If the JWT token is not provided or is invalid.
    - **422 Unprocessable Entity**: If the provided filter data does not pass validation.
    """
    try:
        file_name = CACHED_TAB_IMPORTATION_FILE_NAME

        if not check_if_file_exists(f"./tmp/{file_name}"):
            data = ImportationService.get_documents(db)

            if not data:
                raise HTTPException(status_code=404, detail="Data not found.")

            save_data_on_cache(data=data, directory_path="./tmp", file_name=file_name)

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

@embrapa_router.get("/exportation", response_class=StreamingResponse,
    responses={
        200: {
            "description": "CSV file with exportation data.",
            "content": {
                "text/csv": {
                    "example": "category,date\nVinhos de mesa,1970-12-21\nVinhos de mesa,1971-12-21\n"
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
        },
        404: {
            "description": "Data not found."
        },
        422: {
            "description": "Unprocessable Entity. Validation error in provided filters."
        },
    }
)
async def get_exportation(filters: FiltersSchema = Depends(), current_user: dict = Depends(get_current_user), db: Session = Depends(get_session_local)):
    """
    Retrieve exportation data in CSV format.

    - **Return**: A CSV file with exportation data.

    ## Possible Errors:
    - **401 Unauthorized**: If the JWT token is not provided or is invalid.
    - **422 Unprocessable Entity**: If the provided filter data does not pass validation.
    """
    try:
        file_name = CACHED_TAB_EXPORTATION_FILE_NAME

        if not check_if_file_exists(f"./tmp/{file_name}"):
            data = ExportationService.get_documents(db)

            if not data:
                raise HTTPException(status_code=404, detail="Data not found.")
            
            save_data_on_cache(data=data, directory_path="./tmp", file_name=file_name)

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

