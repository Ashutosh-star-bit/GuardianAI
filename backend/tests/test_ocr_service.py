"""
GuardianAI Enterprise OCRService Pytest Suite
Purpose: Tests OCRService pipeline execution: Receive document -> Preprocess -> OCR -> Clean text ->
         Detect language -> Generate AnalysisRequest -> Return result.
"""

import pytest
from app.services.ocr_service import OCRService, OCRServiceResult, OCRServiceError

@pytest.fixture
def sample_document_bytes():
    return b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x04\x00\x00\x00\x03\x00"

@pytest.mark.asyncio
async def test_ocr_service_full_pipeline(sample_document_bytes):
    """Tests complete OCRService execution returning DocumentAnalysisResult and UniversalAnalysisRequest DTOs."""
    service = OCRService()
    res: OCRServiceResult = await service.process_document_pipeline(
        raw_payload=sample_document_bytes,
        filename="bank_scam.png",
        user_id="usr_ocr_100",
        language="en"
    )

    assert res.document_result.doc_id.startswith("doc_")
    assert res.document_result.metadata.file_format == "PNG"
    assert res.analysis_request.user_id == "usr_ocr_100"
    assert res.analysis_request.input_type in ["PNG", "IMAGE"]
    assert len(res.analysis_request.raw_content) > 0
    assert res.document_result.ocr_result.confidence >= 0.90
    assert res.processing_time_ms > 0

@pytest.mark.asyncio
async def test_ocr_service_error_handling():
    """Tests error validation for empty or None document payloads."""
    service = OCRService()

    with pytest.raises(OCRServiceError, match="cannot be None"):
        await service.process_document_pipeline(None)

    with pytest.raises(OCRServiceError, match="processing failed"):
        await service.process_document_pipeline(b"")
