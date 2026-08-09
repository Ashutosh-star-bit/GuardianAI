"""
GuardianAI End-to-End OCR & Scam Analysis Pipeline Integration Pytest Suite
Purpose: Verifies the complete 8-stage end-to-end flow:
         Upload -> OCR (Preprocess, OCR, Clean, Language) -> AnalysisRequest DTO ->
         Threat Intelligence & NLP -> Decision Engine -> Executive Report -> History Persistence -> Analytics Recording.
"""

import pytest
from app.pipeline import ScamAnalysisPipeline, ScamAnalysisPipelineResult
from app.pipeline.history_service import HistoryService
from app.pipeline.analytics_recorder import AnalyticsRecorder
from app.services.ocr_service import OCRService, OCRServiceResult

@pytest.fixture(autouse=True)
def clean_pipeline_environment():
    HistoryService.clear_all()
    AnalyticsRecorder.clear_all()
    yield
    HistoryService.clear_all()
    AnalyticsRecorder.clear_all()

@pytest.fixture
def sample_scam_screenshot_bytes():
    """PNG image header sample containing bank scam notice bytes."""
    return b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x04\x00\x00\x00\x03\x00"

@pytest.mark.asyncio
async def test_ocr_pipeline_e2e_full_flow(sample_scam_screenshot_bytes):
    """
    Tests complete 8-stage flow:
    Upload -> OCR -> AnalysisRequest -> Threat Intel -> Decision Engine -> Report -> History -> Analytics.
    """
    user_id = "usr_ocr_e2e_100"

    # 1 & 2. Run OCRService (Upload -> Preprocess -> OCR -> Clean -> Detect Language -> AnalysisRequest)
    ocr_service = OCRService()
    ocr_res: OCRServiceResult = await ocr_service.process_document_pipeline(
        raw_payload=sample_scam_screenshot_bytes,
        filename="bank_security_alert.png",
        user_id=user_id,
        language="en"
    )

    assert ocr_res.document_result.doc_id.startswith("doc_")
    assert ocr_res.analysis_request.user_id == user_id
    assert len(ocr_res.analysis_request.raw_content) > 0

    # 3 - 8. Execute ScamAnalysisPipeline (Threat Intel -> Decision -> Report -> History -> Analytics)
    pipeline_res: ScamAnalysisPipelineResult = await ScamAnalysisPipeline.execute_full_scam_analysis(
        raw_input=ocr_res.analysis_request,
        user_id=user_id,
        target_persona="SENIOR_CITIZENS",
        locale="en"
    )

    # 5. Verify Decision Engine Output
    assert pipeline_res.scan_id.startswith("scn_")
    assert pipeline_res.decision.risk_level in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "SAFE"]
    assert pipeline_res.decision.final_scam_probability >= 0.0
    assert len(pipeline_res.decision.action_plan) > 0

    # 6. Verify Executive Report Output
    assert pipeline_res.executive_report.executive_summary is not None
    assert len(pipeline_res.executive_report.recommendations) > 0

    # 7. Verify History Persistence
    history_record = HistoryService.get_scan_by_id(pipeline_res.scan_id)
    assert history_record is not None
    assert history_record.user_id == user_id
    assert history_record.input_format in ["PNG", "IMAGE", "DOCUMENT", "TEXT"]

    # 8. Verify Analytics Recording
    snapshot = AnalyticsRecorder.get_or_create_daily_snapshot()
    assert snapshot.total_scans >= 1
    assert snapshot.total_execution_ms > 0.0

@pytest.mark.asyncio
async def test_ocr_pipeline_direct_format_type(sample_scam_screenshot_bytes):
    """Tests executing pipeline directly with format_type='DOCUMENT'."""
    res = await ScamAnalysisPipeline.execute_full_scam_analysis(
        raw_input=sample_scam_screenshot_bytes,
        format_type="DOCUMENT",
        user_id="usr_ocr_e2e_200"
    )

    assert res.scan_id.startswith("scn_")
    assert res.decision.confidence >= 0.80
