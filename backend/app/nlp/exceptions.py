"""
GuardianAI Custom Text Intelligence (NLP) Exception Hierarchy
Purpose: Provides domain exceptions for Text Intelligence analysis matching HTTP status codes and RFC 7807 problem detail envelopes.
"""

from typing import Any, List, Optional
from app.core.exceptions import BaseAppException

class BaseNLPException(BaseAppException):
    """Base class for all Text Intelligence NLP domain exceptions."""
    def __init__(
        self,
        message: str = "Text Intelligence processing error.",
        code: str = "NLP_PROCESSING_ERROR",
        status_code: int = 500,
        details: Optional[List[Any]] = None
    ):
        super().__init__(message=message, code=code, status_code=status_code, details=details)

class InvalidInputError(BaseNLPException):
    """Raised when input text is empty, whitespace-only, or out of length bounds (HTTP 422)."""
    def __init__(self, message: str = "Invalid input payload provided for Text Intelligence analysis.", details: Optional[List[Any]] = None):
        super().__init__(message=message, code="NLP_INVALID_INPUT", status_code=422, details=details)

class ParsingFailureError(BaseNLPException):
    """Raised when text preprocessing, entity extraction, or pattern parsing fails (HTTP 422)."""
    def __init__(self, message: str = "Failed to parse text features or entity structures.", details: Optional[List[Any]] = None):
        super().__init__(message=message, code="NLP_PARSING_FAILURE", status_code=422, details=details)

class GeminiTimeoutError(BaseNLPException):
    """Raised when Gemini 3.6 Flash High model execution breaches SLA timeout (HTTP 504)."""
    def __init__(self, message: str = "Gemini AI model execution exceeded SLA timeout limit.", details: Optional[List[Any]] = None):
        super().__init__(message=message, code="GEMINI_TIMEOUT_EXCEEDED", status_code=504, details=details)

class MalformedJSONError(BaseNLPException):
    """Raised when LLM text output cannot be repaired into valid JSON syntax (HTTP 422)."""
    def __init__(self, message: str = "LLM model returned malformed JSON syntax that could not be auto-repaired.", details: Optional[List[Any]] = None):
        super().__init__(message=message, code="NLP_MALFORMED_JSON", status_code=422, details=details)

class UnsupportedEncodingError(BaseNLPException):
    """Raised when input text payload contains invalid UTF-8 byte sequences (HTTP 400)."""
    def __init__(self, message: str = "Input text payload contains unsupported or invalid byte encoding.", details: Optional[List[Any]] = None):
        super().__init__(message=message, code="UNSUPPORTED_ENCODING", status_code=400, details=details)
