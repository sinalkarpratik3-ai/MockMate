from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.core.migrations import migrate_timestamp_columns
import app.models  # Ensures all models are registered
from app.api import api_router

import os
import logging
import traceback
from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger("uvicorn.error")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure database tables exist and schema migrations are applied on startup if enabled
    if settings.AUTO_MIGRATE_ON_STARTUP:
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
                if conn.dialect.name == "postgresql":
                    await migrate_timestamp_columns(conn)
        except Exception as e:
            logger.error(f"[Startup Database Error] Failed to initialize database schema: {e}")
            raise
    yield
    # Graceful connection pool disposal on shutdown
    await engine.dispose()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global unhandled error at {request.method} {request.url.path}: {exc}")
    logger.error(traceback.format_exc())
    is_prod = (
        getattr(settings, "ENVIRONMENT", "").lower() == "production"
        or os.getenv("ENVIRONMENT", "").lower() == "production"
    )
    detail = "An internal server error occurred. Please try again later." if is_prod else f"Internal Server Error: {str(exc)}"
    return JSONResponse(
        status_code=500,
        content={"detail": detail}
    )


# CORS Middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$|^https://.*\.amplifyapp\.com$|^https://.*\.elb\.[a-z0-9-]+\.amazonaws\.com$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "message": "Welcome to MockMate - Interview Preparation Platform API",
        "docs": f"{settings.API_V1_STR}/docs",
        "health": f"{settings.API_V1_STR}/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
