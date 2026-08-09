"""
GuardianAI API Gateway Middleware Pytest Suite
"""

import pytest
from fastapi.testclient import TestClient
from main import app
from app.developer_platform.api_key_service import api_key_service

@pytest.fixture
def client():
    return TestClient(app)

def test_gateway_correlation_id_headers(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert "x-correlation-id" in response.headers
    assert "x-process-time-ms" in response.headers
    assert "x-api-version" in response.headers

def test_gateway_invalid_api_key(client):
    response = client.get("/api/v1/health", headers={"Authorization": "Bearer gai_live_invalid_key"})
    assert response.status_code == 401
    assert response.json()["code"] == "UNAUTHORIZED_KEY"

def test_gateway_valid_api_key(client):
    key_rec = api_key_service.create_api_key("Test App", environment="LIVE", tier="PRO")
    response = client.get("/api/v1/health", headers={"Authorization": f"Bearer {key_rec.raw_key_secret}"})
    assert response.status_code == 200

def test_gateway_sqli_payload_screening(client):
    response = client.get("/api/v1/health?query=SELECT+*+FROM+users+--")
    assert response.status_code == 400
    assert response.json()["code"] == "SECURITY_VIOLATION"
