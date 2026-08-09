"""
GuardianAI Developer API Usage Analytics Pytest Suite
"""

import pytest
from fastapi.testclient import TestClient
from main import app
from app.developer_platform.usage_analytics import developer_usage_analytics

@pytest.fixture
def client():
    return TestClient(app)

def test_developer_usage_analytics_engine():
    summary = developer_usage_analytics.get_developer_analytics_summary()
    assert summary["total_requests"] > 100000
    assert summary["latency"]["avg_ms"] < 200.0
    assert summary["tokens"]["total_tokens"] > 2000000
    assert len(summary["top_endpoints"]) == 4

def test_developer_analytics_api(client):
    response = client.get("/api/v1/developer/analytics")
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True
    assert "latency" in res["data"]
    assert "top_endpoints" in res["data"]
