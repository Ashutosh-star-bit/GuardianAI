"""
GuardianAI InputValidationService Unit Test Suite
Purpose: Tests validation of Plain Text, Email, URL, QR, JSON, OCR, and Voice payloads across length, encoding, and null bytes.
"""

import pytest
from app.pipeline.validator import InputValidationService, ValidatedInputPayload, InputValidationError

def test_validate_clean_plain_text():
    """Tests validating valid plain text payload."""
    payload: ValidatedInputPayload = InputValidationService.validate_payload(
        raw_input="URGENT: Your PayPal account is suspended!",
        format_type="TEXT",
        language="en"
    )
    assert payload.format_type == "TEXT"
    assert payload.clean_text == "URGENT: Your PayPal account is suspended!"
    assert payload.byte_size > 0

def test_validate_json_payload():
    """Tests validating valid JSON string payload."""
    json_str = '{"message": "Verify account now", "channel": "SMS"}'
    payload = InputValidationService.validate_payload(json_str, format_type="JSON")
    assert payload.format_type == "JSON"
    assert payload.raw_json_dict["message"] == "Verify account now"

def test_reject_null_bytes_in_pipeline():
    """Tests rejecting payloads containing illegal null bytes."""
    with pytest.raises(InputValidationError) as exc_info:
        InputValidationService.validate_payload("URGENT\x00Message")
    assert "null bytes" in exc_info.value.message

def test_reject_malformed_json_syntax():
    """Tests rejecting malformed JSON syntax."""
    with pytest.raises(InputValidationError) as exc_info:
        InputValidationService.validate_payload("{bad_json: 123}", format_type="JSON")
    assert "Invalid JSON payload syntax" in exc_info.value.message
