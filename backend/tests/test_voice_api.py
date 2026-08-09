"""
GuardianAI Voice Intelligence REST API & End-to-End Pipeline Pytest Suite
Testing POST /api/v1/voice/analyse and POST /api/v1/voice/batch
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def sample_wav_bytes():
    return b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x80\x3e\x00\x00\x00\x7d\x00\x00\x02\x00\x10\x00data\x00\x00\x00\x00"

def test_voice_analyse_endpoint(sample_wav_bytes):
    response = client.post(
        "/api/v1/voice/analyse",
        files={"file": ("fraud_call.wav", sample_wav_bytes, "audio/wav")},
        params={"target_persona": "SENIOR_CITIZENS", "locale": "en"}
    )

    assert response.status_code == 200
    json_resp = response.json()
    assert json_resp["success"] is True
    data = json_resp["data"]
    assert "scan_id" in data
    assert "transcript" in data
    assert data["pipeline_result"]["decision"]["risk_level"] in ["SAFE", "LOW", "MEDIUM", "HIGH", "CRITICAL", "CAUTION", "DANGEROUS"]

def test_voice_analyse_missing_file():
    response = client.post("/api/v1/voice/analyse")
    assert response.status_code == 400

def test_voice_batch_endpoint():
    batch_payload = {
        "items": [
            {
                "item_id": "item_001",
                "filename": "scam_call_1.wav"
            },
            {
                "item_id": "item_002",
                "filename": "scam_call_2.wav"
            }
        ],
        "target_persona": "SENIOR_CITIZENS",
        "locale": "en"
    }

    response = client.post(
        "/api/v1/voice/batch",
        json=batch_payload
    )

    assert response.status_code == 200
    json_resp = response.json()
    assert json_resp["success"] is True
    data = json_resp["data"]
    assert data["total_processed"] == 2
    assert data["successful_count"] == 2
    assert len(data["items"]) == 2
    assert data["items"][0]["item_id"] == "item_001"
