"""
GuardianAI Public Developer REST API Pytest Suite
"""

import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_public_scan_text(client):
    payload = {"text": "URGENT: Your HDFC netbanking is locked. Verify at http://hdfc-verify.top"}
    response = client.post("/api/v1/public/scan/text", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True
    assert "decision" in res["data"]

def test_public_scan_url(client):
    payload = {"url": "http://hdfc-bank-login.top"}
    response = client.post("/api/v1/public/scan/url", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True

def test_public_scan_email(client):
    payload = {"subject": "Urgent Wire Transfer Authorization", "body": "Please wire $50,000 immediately."}
    response = client.post("/api/v1/public/scan/email", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True

def test_public_scan_ocr(client):
    payload = {"document_text": "POLICE NOTICE: Digital arrest warrant issued by Cyber Cell."}
    response = client.post("/api/v1/public/scan/ocr", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True

def test_public_scan_voice(client):
    payload = {"audio_transcript": "This is Officer Sharma. Pay fine immediately via UPI."}
    response = client.post("/api/v1/public/scan/voice", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True

def test_public_threat_intel(client):
    response = client.get("/api/v1/public/threat-intel?indicator=hdfc-verify.top")
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True

def test_public_decision_engine(client):
    payload = {"text": "Urgent wire transfer"}
    response = client.post("/api/v1/public/decision", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True

def test_public_community_reports(client):
    response = client.get("/api/v1/public/community/reports?limit=10")
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True
    assert isinstance(res["data"], list)
