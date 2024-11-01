from fastapi import APIRouter
from app.routes.auth_routes import auth_router
from app.routes.embrapa_routes import embrapa_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(embrapa_router, prefix="/embrapa", tags=["Embrapa"])
