"""
GuardianAI Text Input Payload Validator Unit Test Suite
Purpose: Tests empty input rejection, length boundary enforcement, null byte rejection, and language validation.
"""

import pytest
from app.nlp.validators import TextPayloadValidator, PayloadValidationError

def test_validate_clean_payload():
    """Tests successful validation of valid text payload."""
    clean = TextPayloadValidator.validate_full_payload("URGENT: Your account is suspended!", channel_type="SMS", language="en")
    assert clean == "URGENT: Your account is suspended!"

def test_reject_empty_and_whitespace():
    """Tests PayloadValidationError is raised for empty or whitespace-only input."""
    with pytest.raises(PayloadValidationError) as exc_info:
        TextPayloadValidator.validate_full_payload("    ")
    assert "whitespace-only" in exc_info.value.message

def test_reject_short_length():
    """Tests PayloadValidationError is raised for text below min 5 characters."""
    with pytest.raises(PayloadValidationError) as exc_info:
        TextPayloadValidator.validate_full_payload("Hey")
    assert "below minimum threshold" in exc_info.value.message

def test_reject_excessive_length():
    """Tests PayloadValidationError is raised for text over max 10,000 characters."""
    huge_text = "A" * 10_001
    with pytest.raises(PayloadValidationError) as exc_info:
        TextPayloadValidator.validate_full_payload(huge_text)
    assert "exceeds maximum limit" in exc_info.value.message

def test_reject_null_bytes():
    """Tests PayloadValidationError is raised for malformed inputs containing null bytes."""
    with pytest.raises(PayloadValidationError) as exc_info:
        TextPayloadValidator.validate_full_payload("URGENT\x00Message")
    assert "illegal null bytes" in exc_info.value.message

def test_reject_unsupported_language():
    """Tests PayloadValidationError is raised for unsupported language locales."""
    with pytest.raises(PayloadValidationError) as exc_info:
        TextPayloadValidator.validate_full_payload("URGENT: Verify now!", language="invalid_lang")
    assert "Unsupported language code" in exc_info.value.message
