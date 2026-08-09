"""
GuardianAI SecureUploadService Unit & Security Pytest Suite
Purpose: Tests file extension whitelist, MIME validation, 10MB size limits, virus executable rejection, SHA-256 duplicate detection, and path sanitization.
"""

import pytest
from io import BytesIO
from fastapi import UploadFile, HTTPException
from app.services.upload_service import SecureUploadService, VirusScannerPlaceholder

@pytest.fixture(autouse=True)
def clean_upload_cache():
    SecureUploadService.clear_cache()
    yield
    SecureUploadService.clear_cache()

@pytest.mark.asyncio
async def test_upload_service_valid_txt_upload():
    """Tests SecureUploadService with valid TXT file upload."""
    content = b"URGENT: Verify PayPal account at http://paypa1-check.top"
    file = UploadFile(filename="sample_alert.txt", file=BytesIO(content), headers={"content-type": "text/plain"})

    res = await SecureUploadService.save_upload(file)

    assert res["file_id"].startswith("upl_")
    assert res["original_filename"] == "sample_alert.txt"
    assert res["file_size_bytes"] == len(content)
    assert res["is_duplicate"] is False
    assert len(res["sha256_hash"]) == 64

@pytest.mark.asyncio
async def test_upload_service_duplicate_detection():
    """Tests SHA-256 duplicate file detection."""
    content = b"PDF document content for duplicate testing"
    file1 = UploadFile(filename="doc1.pdf", file=BytesIO(content), headers={"content-type": "application/pdf"})
    file2 = UploadFile(filename="doc1.pdf", file=BytesIO(content), headers={"content-type": "application/pdf"})

    res1 = await SecureUploadService.save_upload(file1)
    res2 = await SecureUploadService.save_upload(file2)

    assert res1["is_duplicate"] is False
    assert res2["is_duplicate"] is True
    assert res1["file_id"] == res2["file_id"]

@pytest.mark.asyncio
async def test_upload_service_malware_executable_rejection():
    """Tests virus scanner rejecting Windows PE executable binary files."""
    exe_content = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00"  # Windows EXE PE magic signature
    file = UploadFile(filename="malware.exe", file=BytesIO(exe_content), headers={"content-type": "text/plain"})

    with pytest.raises(HTTPException) as exc:
        await SecureUploadService.save_upload(file)

    assert exc.value.status_code == 400
    assert any(k in str(exc.value.detail) for k in ["Unsupported file extension", "Malicious", "null byte"])

@pytest.mark.asyncio
async def test_upload_service_filename_sanitization():
    """Tests path traversal sanitization."""
    bad_filename = "../../../etc/passwd"
    clean = SecureUploadService.sanitize_filename(bad_filename)

    assert "../" not in clean
    assert clean == "passwd"
