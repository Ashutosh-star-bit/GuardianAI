"""
GuardianAI JWT Authentication & User Registration Test Suite
Purpose: Tests user signup, BCrypt login, JWT access/refresh token generation, and current profile retrieval.
"""

from fastapi.testclient import TestClient

def test_signup_success(client: TestClient):
    """Tests successful user account registration via POST /api/v1/auth/signup."""
    payload = {
        "email": "newuser@guardianai.io",
        "password": "SecurePassword123!",
        "full_name": "New Test User"
    }
    response = client.post("/api/v1/auth/signup", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@guardianai.io"
    assert data["full_name"] == "New Test User"
    assert "id" in data
    assert "hashed_password" not in data

def test_signup_duplicate_email_fails(client: TestClient):
    """Tests registration with duplicate email address fails with HTTP 400."""
    payload = {
        "email": "duplicate@guardianai.io",
        "password": "SecurePassword123!",
        "full_name": "Duplicate User"
    }
    res1 = client.post("/api/v1/auth/signup", json=payload)
    assert res1.status_code == 201

    res2 = client.post("/api/v1/auth/signup", json=payload)
    assert res2.status_code == 400
    assert "already exists" in res2.json()["detail"]

def test_login_success(client: TestClient):
    """Tests user authentication returning valid JWT Access & Refresh Tokens."""
    # 1. Register user
    signup_payload = {
        "email": "loginuser@guardianai.io",
        "password": "ValidPassword123!",
        "full_name": "Login User"
    }
    client.post("/api/v1/auth/signup", json=signup_payload)

    # 2. Login
    login_payload = {
        "email": "loginuser@guardianai.io",
        "password": "ValidPassword123!"
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_password_fails(client: TestClient):
    """Tests login with wrong password fails with HTTP 401 Unauthorized."""
    signup_payload = {
        "email": "wrongpwd@guardianai.io",
        "password": "CorrectPassword123!"
    }
    client.post("/api/v1/auth/signup", json=signup_payload)

    login_payload = {
        "email": "wrongpwd@guardianai.io",
        "password": "WrongPassword123!"
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 401

def test_get_me_success(client: TestClient, auth_headers: dict):
    """Tests GET /api/v1/auth/me returns authenticated user profile."""
    response = client.get("/api/v1/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "testuser@guardianai.io"
    assert data["role"] == "user"

def test_get_me_unauthorized_fails(client: TestClient):
    """Tests GET /api/v1/auth/me without Bearer token fails with HTTP 401."""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401
