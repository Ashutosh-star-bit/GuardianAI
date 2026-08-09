"""
GuardianAI Scan API Tests
Purpose: Tests POST /api/v1/scan/text payload analysis, threat score evaluation, and validation handling.
"""

import pytest
from fastapi.testclient import TestClient

@pytest.mark.unit
def test_scan_text_safe_payload(client: TestClient):
    """Tests scan endpoint with a benign text payload."""
    payload = {"payload": "Hello, meeting is confirmed for 3 PM tomorrow.", "zeroKnowledge": True}
    response = client.post("/api/v1/scan/text", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["threatScore"] < 30
    assert data["riskBand"] == "safe"
    assert "scanId" in data

@pytest.mark.unit
def test_scan_text_dangerous_payload(client: TestClient):
    """Tests scan endpoint with urgent demand and typosquatted URL."""
    payload = {"payload": "URGENT: Your account is locked! Verify at http://paypa1-check.com", "zeroKnowledge": True}
    response = client.post("/api/v1/scan/text", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["threatScore"] >= 70
    assert data["riskBand"] == "dangerous"
    assert len(data["highlights"]) >= 1

@pytest.mark.unit
def test_scan_text_invalid_empty_payload(client: TestClient):
    """Verifies 422 Unprocessable Entity error envelope when empty payload is posted."""
    payload = {"payload": "", "zeroKnowledge": True}
    response = client.post("/api/v1/scan/text", json=payload)
    assert response.status_code == 422

    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "UNPROCESSABLE_ENTITY"
    assert "requestId" in data["error"]
