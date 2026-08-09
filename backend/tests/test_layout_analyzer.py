"""
GuardianAI Spatial Layout Analyzer Pytest Suite
Purpose: Tests LayoutAnalyzer block identification for Titles, Paragraphs, Tables, Buttons, Highlighted Text,
         QR Codes, spatial bounding box coordinates, and structured layout document containers.
"""

import pytest
from app.document_intel.layout_analyzer import LayoutAnalyzer, StructuredLayoutDocument
from app.document_intel.exceptions import LayoutAnalysisError

@pytest.fixture
def sample_document_bytes():
    return b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x04\x00\x00\x00\x03\x00"

def test_layout_analyzer_blocks_segmentation(sample_document_bytes):
    """Tests layout block segmentation across all 6 target block types."""
    analyzer = LayoutAnalyzer()
    blocks = analyzer.analyze_layout(sample_document_bytes, width=1024, height=768)

    assert len(blocks) == 6
    types_found = {b.block_type for b in blocks}

    assert "TITLE" in types_found
    assert "PARAGRAPH" in types_found
    assert "HIGHLIGHTED_TEXT" in types_found
    assert "BUTTON" in types_found
    assert "TABLE" in types_found
    assert "QR_CODE" in types_found

def test_layout_analyzer_structured_document(sample_document_bytes):
    """Tests StructuredLayoutDocument container model."""
    doc_struct: StructuredLayoutDocument = LayoutAnalyzer.analyze_structured_document(
        sample_document_bytes,
        width=1200,
        height=900
    )

    assert doc_struct.doc_width == 1200
    assert doc_struct.doc_height == 900
    assert doc_struct.total_blocks_count == 6

    assert len(doc_struct.titles) == 1
    assert len(doc_struct.paragraphs) == 1
    assert len(doc_struct.tables) == 1
    assert len(doc_struct.buttons) == 1
    assert len(doc_struct.highlighted_texts) == 1
    assert len(doc_struct.qr_codes) == 1

    # Verify Bounding Box values
    qr_blk = doc_struct.qr_codes[0]
    assert qr_blk.bounding_box.xmin == 0.70 * 1200
    assert qr_blk.bounding_box.ymin == 0.84 * 900
    assert qr_blk.confidence == 0.99

def test_layout_analyzer_error_handling():
    """Tests error handling for empty document bytes."""
    analyzer = LayoutAnalyzer()

    with pytest.raises(LayoutAnalysisError, match="cannot be empty"):
        analyzer.analyze_layout(b"", width=1024, height=768)
