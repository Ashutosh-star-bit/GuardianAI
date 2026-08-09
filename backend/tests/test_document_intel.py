"""
GuardianAI Document Intelligence Module Pytest Suite
Purpose: Tests DocumentProcessor, MetadataExtractor, ImagePreprocessor, LayoutAnalyzer, OCRProcessor, TextCleaner, LanguageDetector, and PipelineAdapter.
"""

import pytest
from app.document_intel import (
    DocumentProcessor,
    MetadataExtractor,
    ImagePreprocessor,
    LayoutAnalyzer,
    OCRProcessor,
    TextCleaner,
    LanguageDetector,
    DocumentPipelineAdapter
)
from app.document_intel.exceptions import DocumentMetadataExtractionError, ImagePreprocessingError

@pytest.mark.asyncio
async def test_document_processor_end_to_end():
    """Tests end-to-end DocumentProcessor execution on PNG image payload bytes."""
    png_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x04\x00\x00\x00\x03\x00\x08\x06\x00\x00\x00"
    processor = DocumentProcessor()

    result = await processor.process_document(png_bytes, filename="alert.png")

    assert result.doc_id.startswith("doc_")
    assert result.metadata.file_format == "PNG"
    assert result.metadata.width == 1024
    assert result.metadata.height == 768
    assert len(result.layout_blocks) >= 3
    assert result.ocr_result.confidence >= 0.90
    assert result.detected_language in ["en", "es", "hi"]
    assert result.script_type in ["LATIN", "DEVANAGARI", "CYRILLIC"]
    assert result.processing_time_ms > 0

def test_metadata_extractor_sniffing():
    """Tests MetadataExtractor header sniffing for PNG, JPEG, and PDF."""
    png_meta = MetadataExtractor.extract_metadata(b"\x89PNG\r\n\x1a\nHeaderData")
    assert png_meta.file_format == "PNG"
    assert png_meta.mime_type == "image/png"

    pdf_meta = MetadataExtractor.extract_metadata(b"%PDF-1.7\n/Type /Page\n/Type /Page")
    assert pdf_meta.file_format == "PDF"
    assert pdf_meta.page_count == 2

    with pytest.raises(DocumentMetadataExtractionError):
        MetadataExtractor.extract_metadata(b"")

def test_image_preprocessor():
    """Tests ImagePreprocessor computer vision heuristics."""
    pre = ImagePreprocessor()
    data, meta = pre.preprocess_image(b"\x89PNG\r\n\x1a\nTest")

    assert meta["grayscale_applied"] is True
    assert meta["contrast_stretched"] is True
    assert meta["deskew_angle_deg"] == 0.0

    with pytest.raises(ImagePreprocessingError):
        pre.preprocess_image(b"")

def test_layout_analyzer():
    """Tests LayoutAnalyzer spatial document block segmentation."""
    analyzer = LayoutAnalyzer()
    blocks = analyzer.analyze_layout(b"\x89PNG\r\n\x1a\nImageData", width=1000, height=800)

    assert len(blocks) >= 3
    types_found = {b.block_type for b in blocks}
    assert "TITLE" in types_found or "HEADER" in types_found
    assert "PARAGRAPH" in types_found

def test_ocr_processor():
    """Tests OCRProcessor text recognition dispatcher."""
    ocr = OCRProcessor(engine_name="TESSERACT_TEST")
    res = ocr.recognize_text(b"\x89PNG\r\n\x1a\nImageBytes")

    assert "TESSERACT_TEST" in res.engine_name
    assert res.confidence >= 0.90
    assert "PayPal" in res.cleaned_text or "PayPal" in res.raw_text

def test_text_cleaner():
    """Tests TextCleaner removing OCR artifacts and repairing broken line wraps."""
    raw_ocr = "URGENT:\nVerifi-\ncation needed\n\x00\x01\n\n\n\nPlease click link"
    cleaned = TextCleaner.clean_ocr_text(raw_ocr)

    assert "Verification needed" in cleaned
    assert "\x00" not in cleaned
    assert "\n\n\n" not in cleaned

def test_language_detector():
    """Tests LanguageDetector identifying Devanagari (Hindi) and Latin (English/Spanish/French)."""
    # Devanagari (Hindi)
    s_hi, l_hi = LanguageDetector.detect_script_and_language("यह एक अनधिकृत लॉगिन प्रयास है।")
    assert s_hi == "DEVANAGARI"
    assert l_hi == "hi"

    # Latin English
    s_en, l_en = LanguageDetector.detect_script_and_language("URGENT: Verify your account immediately")
    assert s_en == "LATIN"
    assert l_en == "en"

    # Latin Spanish
    s_es, l_es = LanguageDetector.detect_script_and_language("Verificar su cuenta por favor como respuesta")
    assert s_es == "LATIN"
    assert l_es == "es"

@pytest.mark.asyncio
async def test_document_pipeline_adapter():
    """Tests DocumentPipelineAdapter transforming DocumentAnalysisResult to UniversalAnalysisRequest DTO."""
    png_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
    processor = DocumentProcessor()
    doc_res = await processor.process_document(png_bytes)

    univ_req = DocumentPipelineAdapter.adapt_to_universal_request(doc_res)

    assert univ_req.input_type in ["PNG", "IMAGE"]
    assert len(univ_req.raw_content) > 0
    assert univ_req.language in ["en", "es", "hi"]
    assert univ_req.metadata.extra_attributes["ocr_confidence"] >= 0.90
