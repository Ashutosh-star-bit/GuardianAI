"""
GuardianAI Open-Source OCRProcessor Pytest Suite
Purpose: Tests single image text extraction, spatial bounding boxes, confidence scoring, multi-page processing,
         multi-image batch processing, and ISO-639 multilingual script mappings.
"""

import pytest
from app.document_intel.ocr_processor import OCRProcessor, OCREngineConfig, OCRResult
from app.document_intel.schemas import LayoutBlock, BoundingBox
from app.document_intel.exceptions import OCREngineError

@pytest.fixture
def sample_image_bytes():
    return b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x01\x00\x00\x00\x01\x00"

def test_ocr_processor_single_image(sample_image_bytes):
    """Tests single image text extraction, confidence scoring, and spatial bounding boxes."""
    ocr = OCRProcessor()
    res: OCRResult = ocr.recognize_text(sample_image_bytes, language="en")

    assert res.engine_name == "OPEN_SOURCE_TESSERACT_ENG"
    assert len(res.raw_text) > 0
    assert res.confidence >= 0.90
    assert len(res.blocks) == 3
    assert res.blocks[0].bounding_box.xmin == 50.0
    assert res.word_count > 0

def test_ocr_processor_multilingual_script_mapping(sample_image_bytes):
    """Tests ISO-639 language code script pack resolution (Spanish, Hindi, French, German)."""
    ocr = OCRProcessor()

    # Spanish
    res_es = ocr.recognize_text(sample_image_bytes, language="es")
    assert "SPA" in res_es.engine_name

    # Hindi
    res_hi = ocr.recognize_text(sample_image_bytes, language="hi")
    assert "HIN" in res_hi.engine_name

    # French
    res_fr = ocr.recognize_text(sample_image_bytes, language="fr")
    assert "FRA" in res_fr.engine_name

def test_ocr_processor_multi_page(sample_image_bytes):
    """Tests multi-page document processing."""
    ocr = OCRProcessor()
    pages = [sample_image_bytes, sample_image_bytes, sample_image_bytes]

    results = ocr.recognize_multi_page(pages, language="en")

    assert len(results) == 3
    for res in results:
        assert res.confidence >= 0.90
        assert len(res.blocks) == 3

def test_ocr_processor_batch_images(sample_image_bytes):
    """Tests batch multi-image processing."""
    ocr = OCRProcessor()
    batch = [("img_1", sample_image_bytes), ("img_2", sample_image_bytes)]

    res_dict = ocr.recognize_batch_images(batch, language="en")

    assert len(res_dict) == 2
    assert "img_1" in res_dict
    assert "img_2" in res_dict
    assert res_dict["img_1"].word_count > 0

def test_ocr_processor_error_handling():
    """Tests error validation for empty image payloads."""
    ocr = OCRProcessor()

    with pytest.raises(OCREngineError, match="cannot be empty"):
        ocr.recognize_text(b"")

    with pytest.raises(OCREngineError, match="cannot be empty"):
        ocr.recognize_multi_page([])

    with pytest.raises(OCREngineError, match="cannot be empty"):
        ocr.recognize_batch_images([])
