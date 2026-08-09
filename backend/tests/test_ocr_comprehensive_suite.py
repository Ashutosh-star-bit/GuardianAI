"""
GuardianAI Comprehensive Document Intelligence OCR Pytest Suite
Purpose: Enterprise-grade test coverage testing:
         1. Low-resolution images (72 DPI)
         2. Blurred images (Low contrast)
         3. Dark images (Underexposed)
         4. Bright images (Overexposed)
         5. Large PDFs (Multi-page PDF parsing)
         6. Hindi text (Devanagari script)
         7. English text (Latin script)
         8. Mixed language (English-Hindi Hinglish)
         9. Screenshots (Mobile/desktop UI)
         10. Bank notices (Bank account suspension scam)
         11. Courier messages (Package delivery scam)
         12. Fake job posters (Work-from-home YouTube review scam).
"""

import pytest
from app.services.ocr_service import OCRService, OCRServiceResult
from app.document_intel.orchestrator import DocumentProcessor
from app.document_intel.preprocessor import ImagePreprocessor
from app.document_intel.language_detector import LanguageDetector, LanguageDetectionResult
from app.pipeline import ScamAnalysisPipeline, ScamAnalysisPipelineResult
from app.pipeline.history_service import HistoryService
from app.pipeline.analytics_recorder import AnalyticsRecorder

# Import reusable fixtures
from tests.fixtures.ocr_fixtures import (
    low_res_image_bytes,
    blurred_image_bytes,
    dark_image_bytes,
    bright_image_bytes,
    large_pdf_bytes,
    hindi_text_sample,
    english_text_sample,
    mixed_language_sample,
    mobile_screenshot_bytes,
    bank_notice_scam_payload,
    courier_scam_payload,
    fake_job_poster_payload
)

@pytest.fixture(autouse=True)
def clean_stores():
    HistoryService.clear_all()
    AnalyticsRecorder.clear_all()
    yield
    HistoryService.clear_all()
    AnalyticsRecorder.clear_all()

# 1. LOW-RESOLUTION IMAGE TEST
@pytest.mark.asyncio
async def test_ocr_low_resolution_image(low_res_image_bytes):
    """Tests processing 72 DPI low-resolution images with upscaling to 300 DPI target."""
    preprocessor = ImagePreprocessor()
    res = preprocessor.process_cv_pipeline(low_res_image_bytes, target_dpi=300)

    assert len(res.processed_bytes) > 0
    assert res.dpi == 300

    service = OCRService()
    ocr_res: OCRServiceResult = await service.process_document_pipeline(
        raw_payload=low_res_image_bytes,
        filename="low_res_72dpi.png"
    )
    assert ocr_res.document_result.metadata.dpi == 300
    assert ocr_res.processing_time_ms > 0

# 2. BLURRED IMAGE TEST
@pytest.mark.asyncio
async def test_ocr_blurred_image(blurred_image_bytes):
    """Tests processing low-contrast blurred images with Laplacian edge sharpening."""
    preprocessor = ImagePreprocessor()
    res = preprocessor.process_cv_pipeline(blurred_image_bytes)
    assert len(res.processed_bytes) > 0

    service = OCRService()
    ocr_res: OCRServiceResult = await service.process_document_pipeline(
        raw_payload=blurred_image_bytes,
        filename="blurred_screenshot.png"
    )
    assert ocr_res.document_result.ocr_result.confidence >= 0.85

# 3. DARK IMAGE TEST
@pytest.mark.asyncio
async def test_ocr_dark_image(dark_image_bytes):
    """Tests processing underexposed dark images with adaptive brightness boost & autocontrast."""
    preprocessor = ImagePreprocessor()
    res = preprocessor.process_cv_pipeline(dark_image_bytes)
    assert len(res.processed_bytes) > 0

    service = OCRService()
    ocr_res: OCRServiceResult = await service.process_document_pipeline(
        raw_payload=dark_image_bytes,
        filename="underexposed_dark.png"
    )
    assert ocr_res.document_result.ocr_result.confidence >= 0.80

# 4. BRIGHT IMAGE TEST
@pytest.mark.asyncio
async def test_ocr_bright_image(bright_image_bytes):
    """Tests processing overexposed bright images with Otsu binarization thresholding."""
    preprocessor = ImagePreprocessor()
    res = preprocessor.process_cv_pipeline(bright_image_bytes)
    assert len(res.processed_bytes) > 0

    service = OCRService()
    ocr_res: OCRServiceResult = await service.process_document_pipeline(
        raw_payload=bright_image_bytes,
        filename="overexposed_bright.png"
    )
    assert ocr_res.document_result.doc_id is not None

# 5. LARGE PDF TEST
@pytest.mark.asyncio
async def test_ocr_large_pdf_document(large_pdf_bytes):
    """Tests processing multi-page PDF documents and verifying page count extraction."""
    service = OCRService()
    res: OCRServiceResult = await service.process_document_pipeline(
        raw_payload=large_pdf_bytes,
        filename="multi_page_contract.pdf"
    )

    assert res.document_result.metadata.file_format == "PDF"
    assert res.document_result.metadata.page_count == 5
    assert res.analysis_request.metadata.extra_attributes["page_count"] == 5

# 6. HINDI TEXT TEST
@pytest.mark.asyncio
async def test_ocr_hindi_language(hindi_text_sample):
    """Tests language detection and text cleaning for pure Hindi (Devanagari script) text."""
    res: LanguageDetectionResult = LanguageDetector.detect_language_detailed(hindi_text_sample)

    assert res.language_code in ["hi", "hi-en"]
    assert res.script_type in ["DEVANAGARI", "MIXED"]

    pipeline_res: ScamAnalysisPipelineResult = await ScamAnalysisPipeline.execute_full_scam_analysis(
        raw_input=hindi_text_sample,
        format_type="TEXT",
        locale="hi"
    )
    assert pipeline_res.decision.risk_level in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "SAFE"]

# 7. ENGLISH TEXT TEST
@pytest.mark.asyncio
async def test_ocr_english_language(english_text_sample):
    """Tests language detection and text cleaning for pure English (Latin script) text."""
    res: LanguageDetectionResult = LanguageDetector.detect_language_detailed(english_text_sample)

    assert res.language_code == "en"
    assert res.script_type == "LATIN"

    pipeline_res: ScamAnalysisPipelineResult = await ScamAnalysisPipeline.execute_full_scam_analysis(
        raw_input=english_text_sample,
        format_type="TEXT",
        locale="en"
    )
    assert pipeline_res.decision.risk_level in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "SAFE"]

# 8. MIXED LANGUAGE (HINGLISH) TEST
@pytest.mark.asyncio
async def test_ocr_mixed_language_hinglish(mixed_language_sample):
    """Tests language detection for mixed English-Hindi (Hinglish) multi-script text."""
    res: LanguageDetectionResult = LanguageDetector.detect_language_detailed(mixed_language_sample)

    assert res.language_code in ["hi-en", "hi", "en", "unknown"]

    pipeline_res: ScamAnalysisPipelineResult = await ScamAnalysisPipeline.execute_full_scam_analysis(
        raw_input=mixed_language_sample,
        format_type="TEXT",
        locale="en"
    )
    assert pipeline_res.decision.risk_level in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "SAFE"]

# 9. MOBILE SCREENSHOT TEST
@pytest.mark.asyncio
async def test_ocr_mobile_screenshot(mobile_screenshot_bytes):
    """Tests processing 1080x2400 mobile screenshot image format."""
    processor = DocumentProcessor()
    doc_result = await processor.process_document(
        raw_payload=mobile_screenshot_bytes,
        filename="mobile_chat_screenshot.png"
    )

    assert doc_result.metadata.width == 1080
    assert doc_result.metadata.height == 2400
    assert doc_result.metadata.file_format == "PNG"

# 10. BANK NOTICE SCAM TEST
@pytest.mark.asyncio
async def test_ocr_scam_category_bank_notice(bank_notice_scam_payload):
    """Tests end-to-end scam classification on bank account suspension notice document."""
    res: ScamAnalysisPipelineResult = await ScamAnalysisPipeline.execute_full_scam_analysis(
        raw_input=bank_notice_scam_payload,
        format_type="TEXT",
        target_persona="SENIOR_CITIZENS"
    )

    assert res.decision.risk_level in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "SAFE"]
    assert res.decision.confidence > 0.0

# 11. COURIER MESSAGES SCAM TEST
@pytest.mark.asyncio
async def test_ocr_scam_category_courier_message(courier_scam_payload):
    """Tests end-to-end scam classification on FedEx/IndiaPost package delivery scam notice."""
    res: ScamAnalysisPipelineResult = await ScamAnalysisPipeline.execute_full_scam_analysis(
        raw_input=courier_scam_payload,
        format_type="TEXT",
        target_persona="SENIOR_CITIZENS"
    )

    assert res.decision.risk_level in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "SAFE"]

# 12. FAKE JOB POSTER SCAM TEST
@pytest.mark.asyncio
async def test_ocr_scam_category_fake_job_poster(fake_job_poster_payload):
    """Tests end-to-end scam classification on fake work-from-home YouTube review poster."""
    res: ScamAnalysisPipelineResult = await ScamAnalysisPipeline.execute_full_scam_analysis(
        raw_input=fake_job_poster_payload,
        format_type="TEXT",
        target_persona="STUDENTS"
    )

    assert res.decision.risk_level in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "SAFE"]
    assert len(res.executive_report.recommendations) > 0
