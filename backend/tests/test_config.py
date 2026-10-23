import os
import pytest
from app.core.config import Settings

def test_sqlite_url_normalization():
    s = Settings(DATABASE_URL="sqlite:///./mockmate.db")
    assert s.ASYNC_DATABASE_URL == "sqlite+aiosqlite:///./mockmate.db"

def test_postgres_url_normalization():
    s = Settings(DATABASE_URL="postgres://mockuser:secret@db.mockmate.com:5432/mockmatedb")
    assert s.ASYNC_DATABASE_URL == "postgresql+asyncpg://mockuser:secret@db.mockmate.com:5432/mockmatedb"

def test_postgresql_sslmode_conversion():
    s = Settings(DATABASE_URL="postgresql://mockuser:secret@rds-host.amazonaws.com:5432/mockmate?sslmode=require")
    assert "ssl=require" in s.ASYNC_DATABASE_URL
    assert "sslmode=" not in s.ASYNC_DATABASE_URL
    assert s.ASYNC_DATABASE_URL.startswith("postgresql+asyncpg://")

def test_asyncpg_url_idempotence():
    s = Settings(DATABASE_URL="postgresql+asyncpg://mockuser:secret@host:5432/mockmate")
    assert s.ASYNC_DATABASE_URL == "postgresql+asyncpg://mockuser:secret@host:5432/mockmate"

def test_cors_origin_parsing():
    s = Settings(BACKEND_CORS_ORIGINS="https://app.mockmate.com, https://d12345.cloudfront.net/ ")
    assert "https://app.mockmate.com" in s.BACKEND_CORS_ORIGINS
    assert "https://d12345.cloudfront.net" in s.BACKEND_CORS_ORIGINS

def test_production_sqlite_rejected(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "production")
    with pytest.raises(ValueError, match="Production environment detected"):
        Settings(DATABASE_URL="sqlite:///./mockmate.db")
