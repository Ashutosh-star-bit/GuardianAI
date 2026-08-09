"""
GuardianAI Common API Envelopes & Response Models
Purpose: Defines global success response wrappers (ApiResponse[T]) and standard RFC 7807 error models.
"""

from typing import Generic, TypeVar, Optional, List, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field

T = TypeVar("T")

class MetaInfo(BaseModel):
    """Metadata included in global API responses."""
    requestId: str = Field(..., description="Unique UUIDv4 correlation ID for request tracing")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    version: str = Field(default="1.0.0")

class ApiResponse(BaseModel, Generic[T]):
    """Standard global success response envelope wrapper."""
    success: bool = Field(default=True)
    data: T
    meta: MetaInfo

class ErrorDetailItem(BaseModel):
    """Field-level validation error detail item."""
    field: str
    issue: str

class ErrorPayload(BaseModel):
    """Standard RFC 7807 error payload schema."""
    code: str = Field(..., description="Machine-readable error code (e.g. UNPROCESSABLE_ENTITY, NOT_FOUND)")
    message: str = Field(..., description="Human-readable error summary")
    status: int = Field(..., description="HTTP status code")
    requestId: str = Field(..., description="Correlation ID for logs & debugging")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    details: List[ErrorDetailItem] = Field(default_factory=list)

class ApiErrorEnvelope(BaseModel):
    """Standard global error response envelope wrapper."""
    success: bool = Field(default=False)
    error: ErrorPayload
