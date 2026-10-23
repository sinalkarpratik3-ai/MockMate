import os
from pathlib import Path
from typing import List, Any
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # backend/
ROOT_DIR = BASE_DIR.parent  # MockMate/

class Settings(BaseSettings):
    PROJECT_NAME: str = "MockMate - Interview Preparation Platform"
    API_V1_STR: str = "/api"
    ENVIRONMENT: str = "development"
    AUTO_MIGRATE_ON_STARTUP: bool = True
    
    # Security
    SECRET_KEY: str = "super-secret-jwt-key-for-mockmate-dev-2026-secure"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    
    # Database & Async Connection Pooling
    DATABASE_URL: str = "sqlite:///./mockmate.db"
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800
    
    @property
    def ASYNC_DATABASE_URL(self) -> str:
        url = self.DATABASE_URL.strip()
        if url.startswith("sqlite:///"):
            return url.replace("sqlite:///", "sqlite+aiosqlite:///", 1)
        if url.startswith("sqlite://"):
            return url.replace("sqlite://", "sqlite+aiosqlite://", 1)
        if url.startswith("postgresql+asyncpg://"):
            pass
        elif url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        
        # asyncpg does not accept libpq 'sslmode=' parameter; convert to asyncpg-supported 'ssl='
        import re
        if "sslmode=" in url:
            url = re.sub(r'([?&])sslmode=([^&]+)', r'\1ssl=\2', url)

        return url

    # Gemini Integration
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.0-flash"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Any) -> List[str]:
        if isinstance(v, str):
            import json
            v_trimmed = v.strip()
            if v_trimmed.startswith("[") and v_trimmed.endswith("]"):
                try:
                    return json.loads(v_trimmed)
                except Exception:
                    pass
            return [origin.strip().rstrip("/") for origin in v.split(",") if origin.strip()]
        elif isinstance(v, list):
            return [str(origin).strip().rstrip("/") for origin in v if str(origin).strip()]
        return v

    @field_validator("DATABASE_URL", mode="before")
    def assemble_db_connection(cls, v: str) -> str:
        # Prevent silent SQLite fallback on production (AWS ECS, or ENVIRONMENT=production)
        is_production = (
            os.getenv("ENVIRONMENT", "").lower() == "production"
            or os.getenv("ENV", "").lower() == "production"
            or bool(os.getenv("AWS_EXECUTION_ENV"))
            or bool(os.getenv("ECS_CONTAINER_METADATA_URI"))
        )
        if is_production and (not v or "sqlite" in v.lower()):
            raise ValueError(
                "Production environment detected, but no valid PostgreSQL DATABASE_URL was configured. "
                "SQLite is disabled in production to prevent silent data loss across container restarts."
            )
        if v and v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql://", 1)
        return v

    model_config = SettingsConfigDict(
        case_sensitive=True, 
        env_file=[str(BASE_DIR / ".env"), str(ROOT_DIR / ".env"), ".env"], 
        extra="allow"
    )

settings = Settings()
