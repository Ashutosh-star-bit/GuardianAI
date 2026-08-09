"""
GuardianAI Custom AI Domain Exception Hierarchy
Purpose: Provides structured domain exceptions for AI model execution matching HTTP status codes and RFC 7807 problem detail envelopes.
"""

from typing import Any, List, Optional
from app.core.exceptions import BaseAppException

class BaseAIException(BaseAppException):
    """Base class for all AI infrastructure domain exceptions."""
    def __init__(
        self,
        message: str = "AI Engine error occurred.",
        code: str = "AI_ENGINE_ERROR",
        status_code: int = 500,
        details: Optional[List[Any]] = None
    ):
        super().__init__(message=message, code=code, status_code=status_code, details=details)

class AINetworkError(BaseAIException):
    """Raised when underlying network connectivity to AI provider fails (HTTP 503)."""
    def __init__(self, message: str = "Network connectivity failure while reaching AI model provider.", details: Optional[List[Any]] = None):
        super().__init__(message=message, code="AI_NETWORK_ERROR", status_code=503, details=details)

class GeminiAPIError(BaseAIException):
    """Raised when upstream Gemini API returns an error response (HTTP 502)."""
    def __init__(self, message: str = "Upstream Gemini API returned an error.", details: Optional[List[Any]] = None):
        super().__init__(message=message, code="GEMINI_API_ERROR", status_code=502, details=details)

class AIRateLimitError(BaseAIException):
    """Raised when AI provider rate limits are exceeded (HTTP 429)."""
    def __init__(self, message: str = "AI model provider rate limit exceeded. Please try again later.", details: Optional[List[Any]] = None):
        super().__init__(message=message, code="AI_RATE_LIMIT_EXCEEDED", status_code=429, details=details)

class AIInvalidResponseError(BaseAIException):
    """Raised when AI model returns malformed JSON or unparseable text output (HTTP 422)."""
    def __init__(self, message: str = "AI model returned an unparseable or invalid response payload.", details: Optional[List[Any]] = None):
        super().__init__(message=message, code="AI_INVALID_RESPONSE", status_code=422, details=details)

class AITimeoutError(BaseAIException):
    """Raised when AI model execution breaches SLA timeout window (HTTP 504)."""
    def __init__(self, message: str = "AI model execution exceeded SLA timeout limit.", details: Optional[List[Any]] = None):
        super().__init__(message=message, code="AI_TIMEOUT_EXCEEDED", status_code=504, details=details)

class AIAuthenticationError(BaseAIException):
    """Raised when AI provider API key is missing or unauthorized (HTTP 401)."""
    def __init__(self, message: str = "Invalid or missing AI model provider API key.", details: Optional[List[Any]] = None):
        super().__init__(message=message, code="AI_AUTHENTICATION_FAILED", status_code=401, details=details)
