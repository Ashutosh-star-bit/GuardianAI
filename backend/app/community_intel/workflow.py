"""
GuardianAI Moderation State Machine Workflow Engine
Purpose: Enforces state transitions for Scam Reports:
         PENDING -> UNDER_REVIEW -> VERIFIED / REJECTED / MERGED
"""

from typing import Dict, Any, Optional
from app.community_intel.schemas import ReportStatus
from app.community_intel.exceptions import CommunityIntelError

class ModerationWorkflowEngine:
    """State Machine Engine for Scam Report Moderation Flow."""

    # Allowed State Transitions Matrix
    VALID_TRANSITIONS = {
        ReportStatus.PENDING: {ReportStatus.UNDER_REVIEW, ReportStatus.VERIFIED, ReportStatus.REJECTED},
        ReportStatus.UNDER_REVIEW: {ReportStatus.VERIFIED, ReportStatus.REJECTED, ReportStatus.MERGED},
        ReportStatus.VERIFIED: {ReportStatus.MERGED, ReportStatus.REJECTED},
        ReportStatus.REJECTED: set(),
        ReportStatus.MERGED: set()
    }

    @classmethod
    def transition(cls, current_status: ReportStatus, target_status: ReportStatus) -> ReportStatus:
        """
        Validates and executes state transition from current_status to target_status.
        """
        allowed = cls.VALID_TRANSITIONS.get(current_status, set())
        if target_status not in allowed:
            raise CommunityIntelError(
                f"Invalid moderation state transition from '{current_status.value}' to '{target_status.value}'.",
                code="INVALID_STATE_TRANSITION",
                status_code=400
            )
        return target_status
