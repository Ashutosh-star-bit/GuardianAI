"""
GuardianAI Feature Flag REST API Pytest Suite
"""

import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_list_feature_flags_api(client):
    response = client.get("/api/v1/feature-flags")
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True
    assert len(res["data"]) == 7

def test_toggle_feature_flag_api(client):
    response = client.put("/api/v1/feature-flags/feature:ocr_processor?is_enabled=false")
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True
    assert res["data"]["is_enabled"] is False

    # Re-enable
    response_enable = client.put("/api/v1/feature-flags/feature:ocr_processor?is_enabled=true")
    assert response_enable.status_code == 200
    res_enable = response_enable.json()
    assert res_enable["data"]["is_enabled"] is True
