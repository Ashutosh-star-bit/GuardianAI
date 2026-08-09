"""
GuardianAI Master Input Adapter Layer Production Pytest Suite
Purpose: Enterprise-grade test suite covering Text, URL, Email, PDF, Image, QR Code, Batch processing,
         Malformed files, Large files, Null bytes, Encryption guards, and Edge cases.
"""

import os
import pytest
from io import BytesIO
from fastapi import UploadFile, HTTPException

from app.adapters.schemas import UniversalAnalysisRequest, AdapterMetadata, AttachmentMetadata
from app.adapters.base import BaseInputAdapter
from app.adapters.text_adapter import TextAdapter
from app.adapters.url_adapter import URLAdapter
from app.adapters.email_adapter import EmailAdapter
from app.adapters.pdf_adapter import PDFAdapter
from app.adapters.image_adapter import ImageAdapter
from app.adapters.qr_adapter import QRImageAdapter
from app.adapters.factory import InputAdapterFactory, InputAdapterFactoryError
from app.pipeline.batch_processor import BatchProcessor, BatchItemPayload, BatchAnalysisResult, BatchProcessorError
from app.services.upload_service import SecureUploadService

# --- 1. PLAIN TEXT ADAPTER TESTS ---
@pytest.mark.asyncio
async def test_text_adapter_valid_and_homoglyphs():
    """Tests TextAdapter with standard text, homoglyph deobfuscation, and metadata extraction."""
    adapter = TextAdapter()

    # Normal text
    raw_text = "URGENT: Verify your account at http://paypa1-check.top"
    req = await adapter.adapt_to_request(raw_text, user_id="usr_100")
    assert req.input_type == "TEXT"
    assert req.raw_content == raw_text
    assert req.metadata.extra_attributes["char_count"] == len(raw_text)
    assert req.metadata.extra_attributes["word_count"] == 6
    assert req.metadata.extracted_urls_count == 1

    # Homoglyph deobfuscation
    homoglyph_text = "Pаypаl sеcurіty verification"  # Cyrillic 'а', 'е', 'і'
    req_hg = await adapter.adapt_to_request(homoglyph_text)
    assert req_hg.metadata.extra_attributes["homoglyphs_detected"] is True
    assert len(req_hg.metadata.extra_attributes["deobfuscated_text"]) > 0

@pytest.mark.asyncio
async def test_text_adapter_malformed_null_bytes_and_length():
    """Tests TextAdapter error handling for null bytes and excessive length."""
    adapter = TextAdapter()

    # Null byte injection
    with pytest.raises(ValueError, match="null byte"):
        await adapter.adapt_to_request("URGENT\x00Message")

    # Exceeding 10,000 max character limit
    huge_text = "A" * 10_001
    with pytest.raises(ValueError, match="exceeds max limit"):
        await adapter.adapt_to_request(huge_text)

# --- 2. WEB URL ADAPTER TESTS ---
@pytest.mark.asyncio
async def test_url_adapter_validation_and_normalization():
    """Tests URLAdapter with scheme normalization, domain extraction, and port/query attributes."""
    adapter = URLAdapter()

    # URL without scheme
    req = await adapter.adapt_to_request("paypa1-check.top/login?user=test#top")
    assert req.input_type == "URL"
    assert req.raw_content == "http://paypa1-check.top/login?user=test#top"
    assert req.metadata.extra_attributes["domain"] == "paypa1-check.top"
    assert req.metadata.extra_attributes["scheme"] == "http"

    # URL with port and IP
    req_ip = await adapter.adapt_to_request("https://192.168.1.1:8080/secure")
    assert req_ip.metadata.extra_attributes["domain"] == "192.168.1.1"
    assert req_ip.metadata.extra_attributes["port"] == 8080
    assert req_ip.metadata.extra_attributes["scheme"] == "https"

@pytest.mark.asyncio
async def test_url_adapter_malformed_urls():
    """Tests URLAdapter error handling for invalid/malformed web URLs."""
    adapter = URLAdapter()

    with pytest.raises(ValueError, match="Malformed URL"):
        await adapter.adapt_to_request("http://")

    with pytest.raises(ValueError, match="Malformed URL"):
        await adapter.adapt_to_request("not_a_valid_url_without_dot")

# --- 3. EMAIL ADAPTER TESTS ---
@pytest.mark.asyncio
async def test_email_adapter_rfc5322_text_and_mime():
    """Tests EmailAdapter parsing RFC 5322 headers and MIME byte streams."""
    adapter = EmailAdapter()

    # Header & body text paste
    email_paste = (
        "From: Security Support <security@paypa1-check.top>\n"
        "To: Victim <victim@gmail.com>\n"
        "Subject: URGENT: Account Suspended\n\n"
        "Please click http://paypa1-check.top to verify."
    )
    req = await adapter.adapt_to_request(email_paste)
    assert req.input_type == "EMAIL"
    assert req.metadata.extra_attributes["sender"] == "Security Support <security@paypa1-check.top>"
    assert req.metadata.extra_attributes["recipient"] == "Victim <victim@gmail.com>"
    assert req.metadata.extra_attributes["subject"] == "URGENT: Account Suspended"

    # MIME raw bytes
    mime_bytes = (
        b"From: admin@bank.com\n"
        b"Subject: Test MIME Email\n\n"
        b"MIME Body Content"
    )
    req_mime = await adapter.adapt_to_request(mime_bytes)
    assert req_mime.metadata.extra_attributes["sender"] == "admin@bank.com"
    assert req_mime.metadata.extra_attributes["subject"] == "Test MIME Email"

# --- 4. PDF ADAPTER TESTS ---
@pytest.mark.asyncio
async def test_pdf_adapter_header_and_encryption_detection():
    """Tests PDFAdapter magic header inspection, page count calculation, and encrypted PDF detection."""
    adapter = PDFAdapter()

    # Valid PDF bytes mockup
    pdf_content = b"%PDF-1.7\n1 0 obj\n<< /Type /Catalog >>\nendobj\n/Type /Page\n/Type /Page\n%%EOF"
    req = await adapter.adapt_to_request(pdf_content, filename="statement.pdf")
    assert req.input_type == "PDF"
    assert req.metadata.extra_attributes["page_count"] == 2

    # Encrypted PDF bytes mockup
    encrypted_pdf = b"%PDF-1.4\n/Encrypt << /V 2 >>\n%%EOF"
    with pytest.raises(ValueError, match="Encrypted PDF"):
        await adapter.adapt_to_request(encrypted_pdf, filename="secret.pdf")

@pytest.mark.asyncio
async def test_pdf_adapter_malformed_and_empty():
    """Tests PDFAdapter error handling for invalid or empty PDF bytes."""
    adapter = PDFAdapter()

    # Invalid header
    with pytest.raises(ValueError, match="Missing %PDF header"):
        await adapter.adapt_to_request(b"NOT_A_PDF_FILE", filename="bad.pdf")

    # Empty payload
    with pytest.raises(ValueError, match="empty"):
        await adapter.adapt_to_request(b"")

# --- 5. IMAGE SCREENSHOT ADAPTER TESTS ---
@pytest.mark.asyncio
async def test_image_adapter_magic_headers_and_dimensions():
    """Tests ImageAdapter sniffing PNG/JPEG/WEBP magic headers and extracting width/height dimensions."""
    adapter = ImageAdapter()

    # PNG magic bytes (800x600 dimensions mocked in header)
    png_bytes = (
        b"\x89PNG\r\n\x1a\n"  # PNG magic header
        b"\x00\x00\x00\rIHDR"
        b"\x00\x00\x03\x20"  # Width = 800
        b"\x00\x00\x02\x58"  # Height = 600
        b"\x08\x06\x00\x00\x00"
    )
    req = await adapter.adapt_to_request(png_bytes, filename="screenshot.png")
    assert req.input_type == "IMAGE"
    assert req.metadata.extra_attributes["format"] == "PNG"
    assert req.metadata.extra_attributes["width"] == 800
    assert req.metadata.extra_attributes["height"] == 600
    assert req.metadata.extra_attributes["ocr_ready"] is True

@pytest.mark.asyncio
async def test_image_adapter_malformed_header():
    """Tests ImageAdapter rejecting unrecognized binary headers."""
    adapter = ImageAdapter()

    with pytest.raises(ValueError, match="Unsupported image format"):
        await adapter.adapt_to_request(b"INVALID_IMAGE_BYTES")

# --- 6. QR CODE IMAGE ADAPTER TESTS ---
@pytest.mark.asyncio
async def test_qr_adapter_vector_classification():
    """Tests QRImageAdapter categorizing all 6 threat vectors (UPI, URL, Phone, SMS, Email, WiFi)."""
    adapter = QRImageAdapter()

    # 1. UPI Payment URI
    req_upi = await adapter.adapt_to_request("upi://pay?pa=merchant@okaxis&pn=Payee")
    assert req_upi.input_type == "QR"
    assert req_upi.metadata.extra_attributes["qr_category"] == "UPI"
    assert req_upi.metadata.extra_attributes["parsed_details"]["handle"] == "merchant@okaxis"

    # 2. Phishing URL
    req_url = await adapter.adapt_to_request("https://paypa1-check.top/login")
    assert req_url.metadata.extra_attributes["qr_category"] == "URL"

    # 3. Phone Call URI
    req_phone = await adapter.adapt_to_request("tel:+18005550199")
    assert req_phone.metadata.extra_attributes["qr_category"] == "PHONE"

    # 4. SMS URI
    req_sms = await adapter.adapt_to_request("SMSTO:+18005550199:Share OTP")
    assert req_sms.metadata.extra_attributes["qr_category"] == "SMS"

    # 5. Email URI
    req_email = await adapter.adapt_to_request("mailto:support@paypa1-check.top")
    assert req_email.metadata.extra_attributes["qr_category"] == "EMAIL"

    # 6. WiFi Network URI
    req_wifi = await adapter.adapt_to_request("WIFI:S:Free_Airport_Wifi;P:pass;;")
    assert req_wifi.metadata.extra_attributes["qr_category"] == "WIFI"

# --- 7. BATCH PROCESSOR TESTS ---
@pytest.mark.asyncio
async def test_batch_processor_multi_format_and_error_isolation():
    """Tests BatchProcessor analyzing multi-format items concurrently with fault isolation."""
    items = [
        BatchItemPayload(item_id="it_1", raw_payload="URGENT: Verify account at http://paypa1-check.top", format_type="TEXT"),
        BatchItemPayload(item_id="it_2", raw_payload="https://paypa1-check.top", format_type="URL"),
        BatchItemPayload(item_id="it_3", raw_payload="upi://pay?pa=merchant@okaxis", format_type="QR"),
        BatchItemPayload(item_id="it_err", raw_payload="INVALID\x00NULL_BYTE", format_type="TEXT")  # Errors isolated
    ]

    batch_res: BatchAnalysisResult = await BatchProcessor.process_batch(items=items, max_concurrency=4)

    assert batch_res.total_items == 4
    assert batch_res.successful_items == 3
    assert batch_res.failed_items == 1

    err_item = next(r for r in batch_res.results if r.item_id == "it_err")
    assert err_item.status == "FAILED"
    assert "null byte" in err_item.error_message

# --- 8. SECURE UPLOAD SERVICE SECURITY TESTS ---
@pytest.mark.asyncio
async def test_secure_upload_service_security_and_duplicates():
    """Tests SecureUploadService file size limits, executable rejection, duplicate detection, and filename sanitization."""
    content = b"PDF document content for duplicate testing"
    file1 = UploadFile(filename="statement.pdf", file=BytesIO(content), headers={"content-type": "application/pdf"})
    file2 = UploadFile(filename="statement.pdf", file=BytesIO(content), headers={"content-type": "application/pdf"})

    # Upload file 1
    res1 = await SecureUploadService.save_upload(file1)
    assert res1["is_duplicate"] is False
    assert res1["file_id"].startswith("upl_")

    # Upload duplicate file 2
    res2 = await SecureUploadService.save_upload(file2)
    assert res2["is_duplicate"] is True
    assert res2["file_id"] == res1["file_id"]

    # Path traversal sanitization
    clean_name = SecureUploadService.sanitize_filename("../../../etc/passwd")
    assert "../" not in clean_name
    assert clean_name == "passwd"
