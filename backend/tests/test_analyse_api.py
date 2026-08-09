"""
GuardianAI Scam Analysis REST API Endpoints Pytest Suite
Purpose: Tests REST endpoints (POST /api/v1/analyse/text, /url, /email, /qr, /document, /batch) with JWT authentication and OpenAPI schema validation.
"""

import sys
import os
import io
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app

def test_api_analyse_text(client: TestClient, auth_headers: dict):
    """Tests POST /api/v1/analyse/text endpoint."""
    response = client.post(
        "/api/v1/analyse/text",
        json={
            "text": "URGENT: Your PayPal account is suspended. Verify at http://paypa1-check.top",
            "target_persona": "SENIOR_CITIZENS",
            "locale": "en"
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    res_data = response.json()["data"]
    assert res_data["input_format"] == "TEXT"
    assert res_data["decision"]["final_scam_probability"] > 0

def test_api_analyse_url(client: TestClient, auth_headers: dict):
    """Tests POST /api/v1/analyse/url endpoint."""
    response = client.post(
        "/api/v1/analyse/url",
        json={"url": "http://paypa1-check.top/login"},
        headers=auth_headers
    )
    assert response.status_code == 200
    res_data = response.json()["data"]
    assert res_data["input_format"] == "URL"

def test_api_analyse_email(client: TestClient, auth_headers: dict):
    """Tests POST /api/v1/analyse/email endpoint."""
    response = client.post(
        "/api/v1/analyse/email",
        json={"email_text": "From: support@paypa1-check.top\nSubject: Account Locked\n\nVerify link"},
        headers=auth_headers
    )
    assert response.status_code == 200
    res_data = response.json()["data"]
    assert res_data["input_format"] == "EMAIL"

def test_api_analyse_qr(client: TestClient, auth_headers: dict):
    """Tests POST /api/v1/analyse/qr endpoint."""
    response = client.post(
        "/api/v1/analyse/qr",
        json={"qr_payload": "upi://pay?pa=merchant@okaxis"},
        headers=auth_headers
    )
    assert response.status_code == 200
    res_data = response.json()["data"]
    assert res_data["input_format"] == "QR"

def test_api_analyse_document(client: TestClient, auth_headers: dict):
    """Tests POST /api/v1/analyse/document endpoint executing OCRService pipeline."""
    png_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x04\x00\x00\x00\x03\x00"
    files = {"file": ("bank_alert.png", io.BytesIO(png_bytes), "image/png")}
    data = {"target_persona": "SENIOR_CITIZENS", "locale": "en"}

    response = client.post(
        "/api/v1/analyse/document",
        files=files,
        data=data,
        headers=auth_headers
    )
    assert response.status_code == 200
    res_json = response.json()
    assert res_json["success"] is True
    data_res = res_json["data"]
    assert "pipeline_result" in data_res
    assert "document_intelligence" in data_res
    assert data_res["ocr_processing_time_ms"] > 0

def test_api_analyse_batch(client: TestClient, auth_headers: dict):
    """Tests POST /api/v1/analyse/batch endpoint."""
    response = client.post(
        "/api/v1/analyse/batch",
        json={
            "items": [
                {"item_id": "i1", "raw_payload": "URGENT: Verify account", "format_type": "TEXT"},
                {"item_id": "i2", "raw_payload": "https://paypa1-check.top", "format_type": "URL"}
            ]
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    res_data = response.json()["data"]
    assert res_data["total_items"] == 2
    assert res_data["successful_items"] == 2
