"""
GuardianAI Real-Time System Metrics Pytest Suite
"""

import pytest
from fastapi.testclient import TestClient
from main import app
from app.core.system_metrics_collector import system_metrics_collector

@pytest.fixture
def client():
    return TestClient(app)

def test_system_metrics_collector_engine():
    data = system_metrics_collector.collect_realtime_metrics()
    assert "cpu" in data
    assert "memory" in data
    assert "latency" in data
    assert "tokens" in data
    assert "scans_by_channel" in data
    assert data["scans_by_channel"]["url"] == 54200

def test_system_metrics_api_endpoint(client):
    response = client.get("/api/v1/system/metrics")
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True
    assert "cpu" in res["data"]
    assert "tokens" in res["data"]
