"""
GuardianAI Custom Text Intelligence (NLP) Exceptions Unit Test Suite
Purpose: Tests status codes, error codes, and message formatting across the NLP exception hierarchy.
"""

from app.nlp.exceptions import (
    BaseNLPException,
    InvalidInputError,
    ParsingFailureError,
    GeminiTimeoutError,
    MalformedJSONError,
    UnsupportedEncodingError
)

def test_invalid_input_error():
    """Tests InvalidInputError status code 422."""
    err = InvalidInputError()
    assert err.status_code == 422
    assert err.code == "NLP_INVALID_INPUT"

def test_parsing_failure_error():
    """Tests ParsingFailureError status code 422."""
    err = ParsingFailureError("Failed to extract entities")
    assert err.status_code == 422
    assert err.code == "NLP_PARSING_FAILURE"
    assert "Failed to extract entities" in err.message

def test_gemini_timeout_error():
    """Tests GeminiTimeoutError status code 504."""
    err = GeminiTimeoutError()
    assert err.status_code == 504
    assert err.code == "GEMINI_TIMEOUT_EXCEEDED"

def test_malformed_json_error():
    """Tests MalformedJSONError status code 422."""
    err = MalformedJSONError()
    assert err.status_code == 422
    assert err.code == "NLP_MALFORMED_JSON"

def test_unsupported_encoding_error():
    """Tests UnsupportedEncodingError status code 400."""
    err = UnsupportedEncodingError()
    assert err.status_code == 400
    assert err.code == "UNSUPPORTED_ENCODING"
