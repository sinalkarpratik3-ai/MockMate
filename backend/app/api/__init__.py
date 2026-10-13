from fastapi import APIRouter
from app.api.auth import router as auth_router
from app.api.interviews import router as interviews_router
from app.api.bookmarks import router as bookmarks_router
from app.api.daily import router as daily_router
from app.api.dashboard import router as dashboard_router
from app.api.health import router as health_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(interviews_router)
api_router.include_router(bookmarks_router)
api_router.include_router(daily_router)
api_router.include_router(dashboard_router)
