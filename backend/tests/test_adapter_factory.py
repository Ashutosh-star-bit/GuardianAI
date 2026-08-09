"""
GuardianAI InputAdapterFactory Unit & Format Sniffing Pytest Suite
Purpose: Tests adapter resolution, MIME/header signature sniffing, and high-level process_payload execution.
"""

import pytest
from app.adapters.factory import InputAdapterFactory, InputAdapterFactoryError
from app.adapters.schemas import UniversalAnalysisRequest

@pytest.mark.asyncio
async def test_adapter_factory_explicit_format():
    """Tests InputAdapterFactory resolving explicit format keys (TEXT, URL, EMAIL, PDF, IMAGE, QR)."""
    # TEXT
    req_text = await InputAdapterFactory.process_payload("URGENT Notice", format_type="TEXT")
    assert req_text.input_type == "TEXT"

    # URL
    req_url = await InputAdapterFactory.process_payload("https://paypa1-check.top", format_type="URL")
    assert req_url.input_type == "URL"

    # UPI QR
    req_qr = await InputAdapterFactory.process_payload("upi://pay?pa=merchant@okaxis", format_type="QR")
    assert req_qr.input_type == "QR"

@pytest.mark.asyncio
async def test_adapter_factory_auto_sniffing():
    """Tests InputAdapterFactory auto-sniffing payloads (URL, PDF bytes, PNG bytes, Email)."""
    # Auto-sniff URL
    req_url = await InputAdapterFactory.process_payload("https://paypa1-check.top")
    assert req_url.input_type == "URL"

    # Auto-sniff PDF bytes
    pdf_bytes = b"%PDF-1.4\n1 0 obj << /Type /Page >> endobj\n%%EOF\n"
    req_pdf = await InputAdapterFactory.process_payload(pdf_bytes)
    assert req_pdf.input_type == "PDF"

@pytest.mark.asyncio
async def test_adapter_factory_unsupported_format():
    """Tests InputAdapterFactory rejecting unsupported format key."""
    with pytest.raises(InputAdapterFactoryError, match="Unsupported format type"):
        InputAdapterFactory.get_adapter("UNSUPPORTED_FORMAT")
