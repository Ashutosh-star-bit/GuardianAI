"""
GuardianAI Custom Application Domain Exceptions
Purpose: Defines domain exception hierarchy matching HTTP status codes and RFC 7807 problem detail response envelopes.
"""

from typing import Any, List, Optional

class BaseAppException(Exception):
    """Base class for all custom GuardianAI application domain exceptions."""
    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_SERVER_ERROR",
        status_code: int = 500,
        details: Optional[List[Any]] = None
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or []

class NotFoundError(BaseAppException):
    """Raised when a requested resource is not found (HTTP 404)."""
    def __init__(self, message: str = "The requested resource was not found.", details: Optional[List[Any]] = None):
        super().__init__(message=message, code="NOT_FOUND", status_code=404, details=details)

class AuthenticationError(BaseAppException):
    """Raised when authentication fails or credentials are invalid/missing (HTTP 401)."""
    def __init__(self, message: str = "Invalid or missing authentication credentials.", details: Optional[List[Any]] = None):
        super().__init__(message=message, code="UNAUTHORIZED", status_code=401, details=details)

class AuthorizationError(BaseAppException):
    """Raised when a user lacks required roles/permissions for an action (HTTP 403)."""
    def __init__(self, message: str = "Insufficient permissions to perform this action.", details: Optional[List[Any]] = None):
        super().__init__(message=message, code="FORBIDDEN", status_code=403, details=details)

class ValidationError(BaseAppException):
    """Raised when request payload fails domain business rules (HTTP 422)."""
    def __init__(self, message: str = "Input payload validation failed.", details: Optional[List[Any]] = None):
        super().__init__(message=message, code="UNPROCESSABLE_ENTITY", status_code=422, details=details)

class DatabaseError(BaseAppException):
    """Raised when a database query or constraint fails (HTTP 500)."""
    def __init__(self, message: str = "Database transaction error occurred.", details: Optional[List[Any]] = None):
        super().__init__(message=message, code="DATABASE_ERROR", status_code=500, details=details)

class RateLimitExceededError(BaseAppException):
    """Raised when request rate limits are exceeded (HTTP 429)."""
    def __init__(self, message: str = "Rate limit exceeded. Please try again later.", details: Optional[List[Any]] = None):
        super().__init__(message=message, code="RATE_LIMIT_EXCEEDED", status_code=429, details=details)

class InternalServerError(BaseAppException):
    """Raised when an unhandled server error occurs (HTTP 500)."""
    def __init__(self, message: str = "An unexpected server error occurred.", details: Optional[List[Any]] = None):
        super().__init__(message=message, code="INTERNAL_SERVER_ERROR", status_code=500, details=details)
