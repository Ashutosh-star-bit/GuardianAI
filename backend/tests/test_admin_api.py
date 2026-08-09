"""
GuardianAI Enterprise Admin REST API Pytest Suite
"""

import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_command_center_telemetry_api(client):
    response = client.get("/api/v1/admin/command-center")
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True
    assert res["data"]["system_health"] == "HEALTHY"

def test_ai_metrics_api(client):
    response = client.get("/api/v1/admin/ai-metrics")
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True
    assert res["data"]["total_tokens_consumed_today"] > 0

def test_audit_logs_api(client):
    response = client.get("/api/v1/admin/audit-logs")
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True
    assert isinstance(res["data"], list)

def test_create_broadcast_api(client):
    payload = {
        "title": "Emergency Threat Advisory",
        "message": "High volume fake police calls detected in Delhi region",
        "severity": "CRITICAL"
    }
    response = client.post("/api/v1/admin/broadcast", json=payload)
    assert response.status_code == 201
    res = response.json()
    assert res["success"] is True
    assert res["data"]["severity"] == "CRITICAL"

def test_list_admin_roles_api(client):
    response = client.get("/api/v1/admin/roles")
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True
    assert len(res["data"]) >= 6

def test_create_custom_role_api(client):
    payload = {
        "name": "SOC Manager",
        "description": "Custom SOC Lead Role",
        "permissions": ["threat:intel:read", "analytics:view"]
    }
    response = client.post("/api/v1/admin/roles", json=payload)
    assert response.status_code == 201
    res = response.json()
    assert res["success"] is True
    assert res["data"]["role_id"] == "CUSTOM_SOC_MANAGER"

def test_export_dataset_api(client):
    response = client.post("/api/v1/admin/export?dataset=REPORTS&format_type=CSV")
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    assert "Digital Arrest Scam" in response.text
