"""
GuardianAI Unified API Response Envelope Schemas
Purpose: Defines standardized Pydantic v2 response schemas enforcing uniform API payload structures.
"""

from typing import Generic, TypeVar, Optional, List, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict

T = TypeVar("T")

class APIResponse(BaseModel, Generic[T]):
    """Unified API Response Envelope DTO."""
    success: bool = Field(description="Indicates operation success (True) or failure (False)")
    message: str = Field(description="Human-readable response message summary")
    data: Optional[T] = Field(default=None, description="Response payload data object or list")
    errors: Optional[List[Any]] = Field(default_factory=list, description="List of error details if applicable")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat(), description="ISO 8601 UTC timestamp")
    request_id: Optional[str] = Field(default="req_unknown", description="Correlation Request ID")

    model_config = ConfigDict(from_attributes=True)

class PaginatedData(BaseModel, Generic[T]):
    """Paginated data container object."""
    items: List[T] = Field(description="Page payload items list")
    total: int = Field(description="Total count of matching records")
    page: int = Field(description="Current page number")
    size: int = Field(description="Page items limit size")
    pages: int = Field(description="Total count of pages")

class PaginatedAPIResponse(APIResponse[PaginatedData[T]], Generic[T]):
    """Unified API Response Envelope for Paginated List endpoints."""
    pass
