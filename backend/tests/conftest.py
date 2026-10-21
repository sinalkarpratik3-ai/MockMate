import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool
import sys
import os
import asyncio

# Add app to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.core.database import Base, get_db

# Use in-memory SQLite database for isolated fast testing with async driver
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingAsyncSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    async def init_models():
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    loop.run_until_complete(init_models())
    yield
    async def drop_models():
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await test_engine.dispose()
    loop.run_until_complete(drop_models())
    loop.close()

@pytest.fixture
def client():
    async def override_get_db():
        async with TestingAsyncSessionLocal() as session:
            try:
                yield session
            finally:
                await session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def auth_headers(client):
    """Registers and authenticates a user, returning Authorization header."""
    user_data = {
        "email": "testuser@mockmate.io",
        "password": "Password123!",
        "full_name": "Test Engineer"
    }
    client.post("/api/auth/register", json=user_data)
    login_res = client.post("/api/auth/login", json={
        "email": user_data["email"],
        "password": user_data["password"]
    })
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def auth_headers_user2(client):
    """Second user for data isolation tests."""
    user_data = {
        "email": "user2@mockmate.io",
        "password": "Password456!",
        "full_name": "Second User"
    }
    client.post("/api/auth/register", json=user_data)
    login_res = client.post("/api/auth/login", json={
        "email": user_data["email"],
        "password": user_data["password"]
    })
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
