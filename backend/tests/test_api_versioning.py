"""
GuardianAI API Versioning Pytest Suite
"""

import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_v1_version_header(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.headers["x-api-version"] == "v1.0.0"

def test_v2_status_endpoint(client):
    response = client.get("/api/v2/status")
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True
    assert res["data"]["version"] == "v2.0.0-alpha"
    assert response.headers["x-api-version"] == "v2.0.0-alpha"
