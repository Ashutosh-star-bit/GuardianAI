"""
GuardianAI Community Intelligence Custom Domain Exceptions
"""

from typing import Optional
from app.core.exceptions import BaseAppException

class CommunityIntelError(BaseAppException):
    """Base exception for Community Intelligence operations."""
    def __init__(self, message: str = "Community Intelligence operation failed.", code: str = "COMMUNITY_INTEL_ERROR", status_code: int = 400, details: Optional[list] = None):
        super().__init__(message=message, code=code, status_code=status_code, details=details)

class DuplicateReportError(CommunityIntelError):
    """Raised when a duplicate scam report is detected."""
    def __init__(self, message: str = "Duplicate scam report detected.", existing_report_id: Optional[str] = None):
        super().__init__(message=message, code="DUPLICATE_REPORT_ERROR", status_code=409, details=[{"existing_report_id": existing_report_id}] if existing_report_id else None)

class InvalidVoteError(CommunityIntelError):
    """Raised when a vote operation is invalid or duplicate."""
    def __init__(self, message: str = "Invalid or duplicate vote cast."):
        super().__init__(message=message, code="INVALID_VOTE_ERROR", status_code=400)
