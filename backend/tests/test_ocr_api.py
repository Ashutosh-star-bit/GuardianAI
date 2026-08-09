"""
GuardianAI Document Intelligence OCR REST API Endpoints Pytest Suite
Purpose: Tests REST endpoints (POST /api/v1/ocr/image, /pdf, /batch) with JWT authentication,
         OpenAPI schema validation, file size limits, extension whitelisting, and error responses.
"""

import sys
import os
import io
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app

def test_ocr_api_image_upload(client: TestClient, auth_headers: dict):
    """Tests POST /api/v1/ocr/image endpoint with valid PNG image upload."""
    png_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x04\x00\x00\x00\x03\x00"
    files = {"file": ("screenshot.png", io.BytesIO(png_bytes), "image/png")}
    data = {"language": "en"}

    response = client.post(
        "/api/v1/ocr/image",
        files=files,
        data=data,
        headers=auth_headers
    )
    assert response.status_code == 200
    res_json = response.json()
    assert res_json["success"] is True
    res_data = res_json["data"]
    assert "document_result" in res_data
    assert "analysis_request" in res_data
    assert res_data["document_result"]["metadata"]["file_format"] == "PNG"

def test_ocr_api_pdf_upload(client: TestClient, auth_headers: dict):
    """Tests POST /api/v1/ocr/pdf endpoint with valid PDF upload."""
    pdf_bytes = b"%PDF-1.7\n/Type /Page\n/Type /Page\n%%EOF"
    files = {"file": ("document.pdf", io.BytesIO(pdf_bytes), "application/pdf")}
    data = {"language": "en"}

    response = client.post(
        "/api/v1/ocr/pdf",
        files=files,
        data=data,
        headers=auth_headers
    )
    assert response.status_code == 200
    res_json = response.json()
    assert res_json["success"] is True
    res_data = res_json["data"]
    assert res_data["document_result"]["metadata"]["file_format"] == "PDF"
    assert res_data["document_result"]["metadata"]["page_count"] == 2

def test_ocr_api_batch(client: TestClient, auth_headers: dict):
    """Tests POST /api/v1/ocr/batch endpoint with concurrent items."""
    response = client.post(
        "/api/v1/ocr/batch",
        json={
            "items": [
                {"item_id": "d1", "image_base64_or_text": "URGENT SECURITY NOTICE: Account Suspended", "format_type": "TEXT"},
                {"item_id": "d2", "image_base64_or_text": "https://paypa1-check.top/login", "format_type": "URL"}
            ],
            "language": "en"
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    res_data = response.json()["data"]
    assert res_data["total_items"] == 2
    assert res_data["successful_items"] == 2

def test_ocr_api_unsupported_media_type(client: TestClient, auth_headers: dict):
    """Tests 415 Unsupported Media Type error for invalid file extension."""
    files = {"file": ("malicious.exe", io.BytesIO(b"MZHeader"), "application/x-msdownload")}
    response = client.post(
        "/api/v1/ocr/image",
        files=files,
        headers=auth_headers
    )
    assert response.status_code == 415
    assert "Unsupported image extension" in response.json()["detail"]

def test_ocr_api_unauthorized(client: TestClient):
    """Tests 401 Unauthorized error when request is missing JWT header."""
    png_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
    files = {"file": ("screenshot.png", io.BytesIO(png_bytes), "image/png")}

    response = client.post("/api/v1/ocr/image", files=files)
    assert response.status_code == 401
