"""
GuardianAI Universal AnalysisRequest DTO Schemas Unit Test Suite
Purpose: Tests validation, default factories, field validators, and serialization of UniversalAnalysisRequest, AdapterMetadata, and AttachmentMetadata DTOs.
"""

import pytest
from app.adapters.schemas import UniversalAnalysisRequest, AdapterMetadata, AttachmentMetadata

def test_universal_analysis_request_defaults_and_serialization():
    """Tests creating UniversalAnalysisRequest with default factories."""
    meta = AdapterMetadata(
        original_format="EMAIL",
        mime_type="message/rfc822",
        file_size_bytes=512,
        sender_info="support@paypa1-check.top",
        extracted_urls_count=1
    )

    req = UniversalAnalysisRequest(
        raw_content="Subject: URGENT Notice\nVerify at http://paypa1-check.top",
        metadata=meta,
        source="WEB_APP"
    )

    assert req.request_id.startswith("req_")
    assert req.scan_id.startswith("scn_")
    assert req.input_type == "TEXT"
    assert req.raw_content == "Subject: URGENT Notice\nVerify at http://paypa1-check.top"
    assert req.metadata.original_format == "EMAIL"
    assert req.source == "WEB_APP"

    # Verify JSON Serialization
    dump_dict = req.model_dump(mode="json")
    assert "request_id" in dump_dict
    assert dump_dict["metadata"]["sender_info"] == "support@paypa1-check.top"

def test_universal_analysis_request_validators():
    """Tests field validators for input_type, raw_content null bytes, and language."""
    meta = AdapterMetadata(original_format="TEXT")

    # Invalid input_type
    with pytest.raises(ValueError, match="Unsupported input_type"):
        UniversalAnalysisRequest(input_type="INVALID_TYPE", raw_content="Hello", metadata=meta)

    # Illegal null byte in raw_content
    with pytest.raises(ValueError, match="illegal null byte"):
        UniversalAnalysisRequest(raw_content="Hello\x00World", metadata=meta)

    # Invalid language
    with pytest.raises(ValueError, match="Unsupported language"):
        UniversalAnalysisRequest(raw_content="Hello", language="invalid_lang", metadata=meta)

def test_attachment_metadata_schema():
    """Tests AttachmentMetadata DTO defaults."""
    att = AttachmentMetadata(
        filename="invoice.pdf",
        mime_type="application/pdf",
        file_size_bytes=2048
    )

    assert att.attachment_id.startswith("att_")
    assert att.filename == "invoice.pdf"
    assert att.file_size_bytes == 2048
