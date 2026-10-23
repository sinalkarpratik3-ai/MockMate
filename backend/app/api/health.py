import logging
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_db

logger = logging.getLogger("uvicorn.error")
router = APIRouter(tags=["Health"])

@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        logger.error(f"[Health Check DB Error] Database connection probe failed: {e}")
        db_status = "unhealthy"

    return {
        "status": "online",
        "service": "MockMate API",
        "database": db_status
    }
