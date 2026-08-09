"""
GuardianAI ImageAdapter Unit & Image Header Sniffing Pytest Suite
Purpose: Tests header sniffing (PNG, JPEG), dimension extraction, OCR placeholder text, and error handling for ImageAdapter.
"""

import pytest
from app.adapters.image_adapter import ImageAdapter, ImageAdapterError
from app.adapters.schemas import UniversalAnalysisRequest

def create_sample_png_bytes() -> bytes:
    """Helper creating minimal PNG byte stream with IHDR 100x100 dimensions."""
    header = b"\x89PNG\r\n\x1a\n"
    ihdr = b"\x00\x00\x00\x0dIHDR\x00\x00\x00\x64\x00\x00\x00\x64\x08\x02\x00\x00\x00"
    return header + ihdr + b"\x00" * 30

@pytest.mark.asyncio
async def test_image_adapter_valid_png():
    """Tests ImageAdapter parsing PNG bytes and dimensions."""
    adapter = ImageAdapter()
    png_bytes = create_sample_png_bytes()

    req: UniversalAnalysisRequest = await adapter.adapt_to_request(raw_payload=png_bytes, source="WEB_APP")

    assert req.input_type == "IMAGE"
    assert req.metadata.mime_type == "image/png"
    assert req.metadata.extra_attributes["width"] == 100
    assert req.metadata.extra_attributes["height"] == 100
    assert "Pending OCR Engine" in req.raw_content

@pytest.mark.asyncio
async def test_image_adapter_with_ocr_text():
    """Tests ImageAdapter with pre-extracted OCR text."""
    adapter = ImageAdapter()
    png_bytes = create_sample_png_bytes()

    req = await adapter.adapt_to_request(
        raw_payload=png_bytes,
        ocr_extracted_text="URGENT: Verify your bank account at http://paypa1-check.top"
    )

    assert "paypa1-check.top" in req.raw_content

@pytest.mark.asyncio
async def test_image_adapter_errors():
    """Tests ImageAdapter error handling for None, empty, and invalid headers."""
    adapter = ImageAdapter()

    # None Rejection
    with pytest.raises(ImageAdapterError, match="cannot be None"):
        await adapter.adapt_to_request(None)

    # Empty Bytes Rejection
    with pytest.raises(ImageAdapterError, match="empty"):
        await adapter.adapt_to_request(b"")

    # Invalid Header Signature Rejection
    with pytest.raises(ImageAdapterError, match="Unsupported image format"):
        await adapter.adapt_to_request(b"NOT_AN_IMAGE_FILE")
