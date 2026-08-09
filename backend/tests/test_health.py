"""
GuardianAI Health & System Diagnostic Endpoints Test Suite
Purpose: Tests root welcome endpoint, liveness probe (/health), readiness probe (/ready), and version info (/version).
"""

from fastapi.testclient import TestClient

def test_root_endpoint(client: TestClient):
    """Tests GET / returns API welcome metadata."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data
    assert data["data"]["name"] == "GuardianAI"
    assert data["data"]["status"] == "online"

def test_health_liveness_endpoint(client: TestClient):
    """Tests GET /api/v1/health returns system liveness status."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "healthy"
    assert "uptime_seconds" in data["data"]

def test_health_readiness_endpoint(client: TestClient):
    """Tests GET /api/v1/ready executes database query and returns readiness status."""
    response = client.get("/api/v1/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "ready"
    assert data["data"]["components"]["database"]["status"] == "healthy"

def test_version_endpoint(client: TestClient):
    """Tests GET /api/v1/version returns version info."""
    response = client.get("/api/v1/version")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["version"] == "1.0.0"
    assert "python_version" in data["data"]
