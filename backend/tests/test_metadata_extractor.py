"""
GuardianAI MetadataExtractor Pytest Suite
Purpose: Tests MetadataExtractor for image size (width, height), resolution (DPI), orientation, creation date,
         file format signatures, MIME types, page counts, and error validation.
"""

import pytest
from app.document_intel.metadata_extractor import MetadataExtractor, ExtractedDocumentMetadata
from app.document_intel.exceptions import DocumentMetadataExtractionError

def test_metadata_extractor_png():
    """Tests metadata extraction for PNG format, size dimensions, and DPI."""
    png_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x03\x20\x00\x00\x02\x58\x08\x06\x00\x00\x00"
    meta: ExtractedDocumentMetadata = MetadataExtractor.extract_rich_metadata(png_bytes, filename="screenshot.png")

    assert meta.filename == "screenshot.png"
    assert meta.file_format == "PNG"
    assert meta.mime_type == "image/png"
    assert meta.width == 800
    assert meta.height == 600
    assert meta.dpi == 300
    assert meta.page_count == 1
    assert meta.orientation == 1
    assert meta.extra_attributes["aspect_ratio"] == 1.33

def test_metadata_extractor_pdf_page_count():
    """Tests PDF multi-page count calculation and metadata."""
    pdf_bytes = b"%PDF-1.7\n/Type /Page\n/Type /Page\n/Type /Page\n%%EOF"
    meta = MetadataExtractor.extract_rich_metadata(pdf_bytes, filename="statement.pdf")

    assert meta.file_format == "PDF"
    assert meta.mime_type == "application/pdf"
    assert meta.page_count == 3
    assert meta.extra_attributes["is_vector"] is True

def test_metadata_extractor_jpeg_exif():
    """Tests JPEG EXIF creation date and orientation extraction."""
    jpeg_bytes = b"\xff\xd8\xff" + b"\x00" * 150
    meta = MetadataExtractor.extract_rich_metadata(jpeg_bytes, filename="photo.jpg")

    assert meta.file_format == "JPEG"
    assert meta.mime_type == "image/jpeg"
    assert meta.has_exif is True
    assert meta.creation_date is not None
    assert meta.orientation == 1

def test_metadata_extractor_error_validation():
    """Tests error validation for empty or invalid payload types."""
    with pytest.raises(DocumentMetadataExtractionError, match="cannot be None"):
        MetadataExtractor.extract_rich_metadata(None)

    with pytest.raises(DocumentMetadataExtractionError, match="Empty document payload"):
        MetadataExtractor.extract_rich_metadata(b"")

    with pytest.raises(DocumentMetadataExtractionError, match="bytes or string"):
        MetadataExtractor.extract_rich_metadata(12345)
