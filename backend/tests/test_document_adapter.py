"""
GuardianAI DocumentAdapter Integration Pytest Suite
Purpose: Tests DocumentAdapter converting OCR & Document Intelligence output into UniversalAnalysisRequest DTO
         and integrating directly with the Scam Analysis Pipeline.
"""

import pytest
from app.adapters.document_adapter import DocumentAdapter, DocumentAdapterError
from app.adapters.factory import InputAdapterFactory
from app.adapters.schemas import UniversalAnalysisRequest
from app.document_intel.orchestrator import DocumentProcessor
from app.pipeline.orchestrator import ScamAnalysisPipeline

@pytest.fixture
def sample_screenshot_bytes():
    return b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x04\x00\x00\x00\x03\x00"

@pytest.mark.asyncio
async def test_document_adapter_adapt_raw_bytes(sample_screenshot_bytes):
    """Tests DocumentAdapter adapting raw screenshot bytes into UniversalAnalysisRequest DTO."""
    adapter = DocumentAdapter()
    req: UniversalAnalysisRequest = await adapter.adapt_to_request(
        sample_screenshot_bytes,
        user_id="usr_doc_100",
        filename="bank_scam_alert.png"
    )

    assert req.user_id == "usr_doc_100"
    assert req.input_type in ["PNG", "IMAGE"]
    assert len(req.raw_content) > 0
    assert req.metadata.extra_attributes["doc_id"].startswith("doc_")
    assert req.metadata.extra_attributes["ocr_confidence"] >= 0.90

@pytest.mark.asyncio
async def test_document_adapter_factory_resolution(sample_screenshot_bytes):
    """Tests InputAdapterFactory resolving DocumentAdapter for 'DOCUMENT' key and auto-sniffing."""
    adapter = InputAdapterFactory.get_adapter("DOCUMENT")
    assert isinstance(adapter, DocumentAdapter)

    sniffed_adapter = InputAdapterFactory.sniff_and_get_adapter(sample_screenshot_bytes)
    assert isinstance(sniffed_adapter, DocumentAdapter)

@pytest.mark.asyncio
async def test_document_adapter_pipeline_integration(sample_screenshot_bytes):
    """Tests end-to-end integration: DocumentAdapter -> UniversalAnalysisRequest -> ScamAnalysisPipeline."""
    req = await InputAdapterFactory.process_payload(
        raw_payload=sample_screenshot_bytes,
        format_type="DOCUMENT",
        user_id="usr_doc_200"
    )

    pipeline_result = await ScamAnalysisPipeline.execute_full_scam_analysis(req)

    assert pipeline_result.scan_id.startswith("scn_")
    assert pipeline_result.decision.risk_level in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "SAFE"]
    assert pipeline_result.decision.final_scam_probability >= 0.0

@pytest.mark.asyncio
async def test_document_adapter_error_handling():
    """Tests error validation for invalid or empty document payloads."""
    adapter = DocumentAdapter()

    with pytest.raises(DocumentAdapterError, match="cannot be None"):
        await adapter.adapt_to_request(None)

    with pytest.raises(DocumentAdapterError, match="cannot be empty"):
        await adapter.adapt_to_request(b"")

    with pytest.raises(DocumentAdapterError, match="Unsupported document payload"):
        await adapter.adapt_to_request(12345)
