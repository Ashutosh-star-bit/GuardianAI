"""
GuardianAI Custom AI Exceptions Unit Test Suite
Purpose: Tests status codes, error codes, and message formatting across the AI exception hierarchy.
"""

from app.ai.exceptions import (
    BaseAIException,
    AINetworkError,
    GeminiAPIError,
    AIRateLimitError,
    AIInvalidResponseError,
    AITimeoutError,
    AIAuthenticationError
)

def test_ai_network_error():
    """Tests AINetworkError status code 503."""
    err = AINetworkError()
    assert err.status_code == 503
    assert err.code == "AI_NETWORK_ERROR"

def test_gemini_api_error():
    """Tests GeminiAPIError status code 502."""
    err = GeminiAPIError("Upstream service unavailable")
    assert err.status_code == 502
    assert err.code == "GEMINI_API_ERROR"
    assert "Upstream service unavailable" in err.message

def test_ai_rate_limit_error():
    """Tests AIRateLimitError status code 429."""
    err = AIRateLimitError()
    assert err.status_code == 429
    assert err.code == "AI_RATE_LIMIT_EXCEEDED"

def test_ai_invalid_response_error():
    """Tests AIInvalidResponseError status code 422."""
    err = AIInvalidResponseError()
    assert err.status_code == 422
    assert err.code == "AI_INVALID_RESPONSE"

def test_ai_timeout_error():
    """Tests AITimeoutError status code 504."""
    err = AITimeoutError()
    assert err.status_code == 504
    assert err.code == "AI_TIMEOUT_EXCEEDED"

def test_ai_authentication_error():
    """Tests AIAuthenticationError status code 401."""
    err = AIAuthenticationError()
    assert err.status_code == 401
    assert err.code == "AI_AUTHENTICATION_FAILED"
