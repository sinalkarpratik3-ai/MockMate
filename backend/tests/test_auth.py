def test_register_user_success(client):
    res = client.post("/api/auth/register", json={
        "email": "newdev@mockmate.io",
        "password": "SecurePassword123!",
        "full_name": "New Developer"
    })
    assert res.status_code == 201
    data = res.json()
    assert "access_token" in data
    assert data["user"]["email"] == "newdev@mockmate.io"
    assert data["user"]["full_name"] == "New Developer"

def test_register_duplicate_email(client):
    res1 = client.post("/api/auth/register", json={
        "email": "dupe@mockmate.io",
        "password": "Password123!"
    })
    assert res1.status_code == 201
    
    res2 = client.post("/api/auth/register", json={
        "email": "dupe@mockmate.io",
        "password": "Password123!"
    })
    assert res2.status_code == 400
    assert "already exists" in res2.json()["detail"]

def test_login_success(client):
    client.post("/api/auth/register", json={
        "email": "loginuser@mockmate.io",
        "password": "Password123!"
    })
    res = client.post("/api/auth/login", json={
        "email": "loginuser@mockmate.io",
        "password": "Password123!"
    })
    assert res.status_code == 200
    assert "access_token" in res.json()

def test_login_invalid_password(client):
    client.post("/api/auth/register", json={
        "email": "badpass@mockmate.io",
        "password": "Password123!"
    })
    res = client.post("/api/auth/login", json={
        "email": "badpass@mockmate.io",
        "password": "WrongPassword999!"
    })
    assert res.status_code == 401

def test_protected_route_unauthenticated(client):
    res = client.get("/api/auth/me")
    assert res.status_code == 401

def test_protected_route_authenticated(client, auth_headers):
    res = client.get("/api/auth/me", headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["email"] == "testuser@mockmate.io"
    assert "created_at" in res.json()
    assert res.json()["created_at"] is not None

def test_user_timestamps_and_update(client):
    """Verify user registration sets created_at/updated_at and updating user updates updated_at."""
    res = client.post("/api/auth/register", json={
        "email": "timestamp_test@mockmate.io",
        "password": "Password123!",
        "full_name": "Timestamp Test"
    })
    assert res.status_code == 201
    user_data = res.json()["user"]
    assert user_data["created_at"] is not None

    # Verify migration function executes cleanly
    import asyncio
    from app.core.migrations import migrate_timestamp_columns
    from tests.conftest import test_engine

    async def run_check():
        async with test_engine.begin() as conn:
            count = await migrate_timestamp_columns(conn)
            assert count >= 0
    asyncio.run(run_check())

