"""
GuardianAI Developer API Key REST API Pytest Suite
"""

import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_create_and_list_api_keys(client):
    payload = {"name": "Staging Backend Key", "environment": "LIVE", "tier": "PRO"}
    res_create = client.post("/api/v1/api-keys", json=payload)
    assert res_create.status_code == 201
    created = res_create.json()["data"]
    assert "raw_key_secret" in created
    key_id = created["key_id"]

    res_list = client.get("/api/v1/api-keys")
    assert res_list.status_code == 200
    listed_keys = res_list.json()["data"]
    assert len(listed_keys) >= 1
    # Secret omitted in list response!
    assert "raw_key_secret" not in listed_keys[0]

def test_rotate_api_key(client):
    payload = {"name": "Key To Rotate", "environment": "LIVE", "tier": "FREE"}
    res_create = client.post("/api/v1/api-keys", json=payload)
    key_id = res_create.json()["data"]["key_id"]

    res_rotate = client.post(f"/api/v1/api-keys/{key_id}/rotate")
    assert res_rotate.status_code == 200
    rotated = res_rotate.json()["data"]
    assert "raw_key_secret" in rotated

def test_toggle_and_delete_api_key(client):
    payload = {"name": "Key To Delete", "environment": "TEST", "tier": "FREE"}
    res_create = client.post("/api/v1/api-keys", json=payload)
    key_id = res_create.json()["data"]["key_id"]

    # Toggle Disable
    res_toggle = client.post(f"/api/v1/api-keys/{key_id}/toggle?is_active=false")
    assert res_toggle.status_code == 200
    assert res_toggle.json()["data"]["is_active"] is False

    # Delete
    res_delete = client.delete(f"/api/v1/api-keys/{key_id}")
    assert res_delete.status_code == 200
