"""
GuardianAI SQLAlchemy Models Package
Purpose: Exposes all ORM models to ensure proper mapper initialization.
"""

from app.models.user import User
from app.models.scan import Scan
from app.models.scam_report import ScamReport, ScamReportAttachment, ScamReportVote
from app.models.feedback import AIPredictionFeedback

__all__ = [
    "User",
    "Scan",
    "ScamReport",
    "ScamReportAttachment",
    "ScamReportVote",
    "AIPredictionFeedback"
]
