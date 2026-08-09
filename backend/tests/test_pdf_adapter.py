"""
GuardianAI PDFAdapter Unit & Document Parsing Pytest Suite
Purpose: Tests PDF header validation, page counting, text extraction, encrypted PDF handling, and error cases for PDFAdapter.
"""

import pytest
from app.adapters.pdf_adapter import PDFAdapter, PDFAdapterError
from app.adapters.schemas import UniversalAnalysisRequest

def create_sample_pdf_bytes() -> bytes:
    """Helper creating minimal PDF byte stream for testing."""
    return (
        b"%PDF-1.4\n"
        b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n"
        b"2 0 obj << /Type /Pages /Kinds [3 0 R] /Count 1 >> endobj\n"
        b"3 0 obj << /Type /Page /Parent 2 0 R >> endobj\n"
        b"stream\nBT (URGENT: Verify PayPal account at http://paypa1-check.top) ET\nendstream\n"
        b"%%EOF\n"
    )

@pytest.mark.asyncio
async def test_pdf_adapter_valid_pdf():
    """Tests PDFAdapter parsing valid PDF bytes."""
    adapter = PDFAdapter()
    pdf_bytes = create_sample_pdf_bytes()

    req: UniversalAnalysisRequest = await adapter.adapt_to_request(raw_payload=pdf_bytes, source="WEB_APP")

    assert req.input_type == "PDF"
    assert req.metadata.extra_attributes["page_count"] >= 1
    assert "paypa1-check.top" in req.raw_content
    assert req.metadata.file_size_bytes == len(pdf_bytes)

@pytest.mark.asyncio
async def test_pdf_adapter_encrypted_pdf():
    """Tests PDFAdapter graceful handling of encrypted PDFs."""
    adapter = PDFAdapter()
    encrypted_bytes = b"%PDF-1.4\n1 0 obj << /Encrypt 2 0 R >> endobj\n%%EOF\n"

    with pytest.raises(PDFAdapterError, match="Encrypted PDF document"):
        await adapter.adapt_to_request(encrypted_bytes)

@pytest.mark.asyncio
async def test_pdf_adapter_errors():
    """Tests PDFAdapter error handling for empty, None, and corrupted PDF bytes."""
    adapter = PDFAdapter()

    # None Rejection
    with pytest.raises(PDFAdapterError, match="cannot be None"):
        await adapter.adapt_to_request(None)

    # Empty Bytes Rejection
    with pytest.raises(PDFAdapterError, match="empty"):
        await adapter.adapt_to_request(b"")

    # Corrupted PDF Bytes Rejection
    with pytest.raises(PDFAdapterError, match="Missing %PDF header"):
        await adapter.adapt_to_request(b"NOT_A_PDF_FILE")
