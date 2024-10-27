from fastapi import APIRouter
from .auth_routes import auth_router
from .embrapa_routes import embrapa_router
from .scrape_routes import scrape_route

router = APIRouter()

router.include_router(auth_router, prefix="/auth")
router.include_router(scrape_route, prefix="/scrape")
router.include_router(embrapa_router, prefix="/embrapa")
