from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
import app.models  # Ensures all models are registered
from app.api import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure database tables exist asynchronously on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        from sqlalchemy import text
        for sql in [
            "ALTER TABLE interviews ADD COLUMN current_round INTEGER DEFAULT 1",
            "ALTER TABLE interviews ADD COLUMN current_difficulty VARCHAR(50) DEFAULT 'Easy'",
            "ALTER TABLE questions ADD COLUMN round_number INTEGER DEFAULT 1",
        ]:
            try:
                await conn.execute(text(sql))
            except Exception:
                pass  # Column already exists
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

# CORS Middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production config allows full web client interaction
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
