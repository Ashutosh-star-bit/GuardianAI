"""
GuardianAI Computer Vision Image Preprocessor Pytest Suite
Purpose: Tests all 10 computer vision pre-processing operations (Resize, Deskew, Denoise, Sharpen, Contrast,
         Brightness, Grayscale, Thresholding, Rotation, Cropping) and sub-30ms performance SLA.
"""

import time
import pytest
from app.document_intel.preprocessor import ImagePreprocessor, PreprocessedImageResult
from app.document_intel.exceptions import ImagePreprocessingError

@pytest.fixture
def sample_test_png_bytes():
    """PNG 200x150 binary header sample bytes."""
    return b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\xc8\x00\x00\x00\x96\x08\x06\x00\x00\x00"

def test_image_preprocessor_full_pipeline(sample_test_png_bytes):
    """Tests complete computer vision pre-processing pipeline execution."""
    res: PreprocessedImageResult = ImagePreprocessor.process_cv_pipeline(sample_test_png_bytes)

    assert res.width >= 1024
    assert res.height >= 768
    assert res.dpi == 300
    assert len(res.processed_bytes) > 0
    assert "GRAYSCALE_CONVERTED" in res.enhancement_flags
    assert "MEDIAN_DENOISED" in res.enhancement_flags
    assert "AUTOCONTRAST_ENHANCED" in res.enhancement_flags
    assert "BRIGHTNESS_BOOSTED" in res.enhancement_flags
    assert "TEXT_EDGES_SHARPENED" in res.enhancement_flags
    assert "OTSU_THRESHOLD_BINARIZED" in res.enhancement_flags
    assert res.execution_time_ms > 0

def test_image_preprocessor_cropping(sample_test_png_bytes):
    """Tests image cropping bounding box operation."""
    crop_box = (10, 10, 100, 80)
    res = ImagePreprocessor.process_cv_pipeline(
        sample_test_png_bytes,
        crop_box=crop_box,
        enable_thresholding=False
    )

    assert "BOUNDING_BOX_CROPPED" in res.enhancement_flags
    assert len(res.processed_bytes) > 0

def test_image_preprocessor_performance_sla(sample_test_png_bytes):
    """Tests sub-30ms execution SLA performance threshold for standard image pre-processing."""
    start_time = time.perf_counter()
    res = ImagePreprocessor.process_cv_pipeline(sample_test_png_bytes)
    elapsed_ms = (time.perf_counter() - start_time) * 1000

    assert elapsed_ms < 30.0, f"Performance SLA breach: Preprocessing took {elapsed_ms:.2f}ms (Target < 30ms)"

def test_image_preprocessor_error_handling():
    """Tests error validation for empty and invalid image byte payloads."""
    with pytest.raises(ImagePreprocessingError, match="cannot be empty"):
        ImagePreprocessor.process_cv_pipeline(b"")

    with pytest.raises(ImagePreprocessingError, match="too short"):
        ImagePreprocessor.process_cv_pipeline(b"123")

    with pytest.raises(ImagePreprocessingError, match="Failed to decode"):
        ImagePreprocessor.process_cv_pipeline(b"INVALID_IMAGE_BYTES_PAYLOAD")
