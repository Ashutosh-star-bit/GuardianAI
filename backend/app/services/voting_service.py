"""
GuardianAI Voting Service Engine
Purpose: Enterprise Service processing weighted community votes (Upvote, Downvote, Confirm Threat)
         with DB-level duplicate vote prevention and user reputation impact.
"""

from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from app.models.scam_report import ScamReport, ScamReportVote
from app.models.user import User
from app.community_intel.schemas import CommunityVoteCreate, VoteType
from app.community_intel.trust_engine import UserTrustEngine
from app.core.exceptions import BaseAppException

class VotingServiceError(BaseAppException):
    """Raised when a vote operation fails or is duplicated."""
    def __init__(self, message: str = "Voting operation failed.", details: Optional[list] = None):
        super().__init__(message=message, code="VOTING_SERVICE_ERROR", status_code=400, details=details)

class VotingService:
    """Enterprise Reusable Community Voting Service."""

    def cast_vote(
        self,
        db: Session,
        report_id: str,
        user_id: str,
        vote_type: VoteType,
        user_trust_score: int = 50
    ) -> ScamReport:
        """
        Casts a weighted vote on a scam report with duplicate vote prevention.
        """
        # 1. Check if report exists
        report = db.execute(select(ScamReport).where(ScamReport.id == report_id)).scalar_one_or_none()
        if not report:
            raise VotingServiceError(f"Scam report '{report_id}' not found.", status_code=404)

        # 2. Check for duplicate vote by same user on same report
        existing_vote = db.execute(
            select(ScamReportVote).where(
                and_(
                    ScamReportVote.report_id == report_id,
                    ScamReportVote.user_id == user_id
                )
            )
        ).scalar_one_or_none()

        if existing_vote:
            raise VotingServiceError(
                f"User '{user_id}' has already voted on report '{report_id}'. Duplicate voting is prohibited."
            )

        # 3. Calculate trust-weighted vote impact
        weight = UserTrustEngine.calculate_vote_weight(user_trust_score)

        # 4. Update ScamReport counts and weighted score
        if vote_type == VoteType.UPVOTE:
            report.upvote_count += 1
            report.weighted_score += weight
        elif vote_type == VoteType.DOWNVOTE:
            report.downvote_count += 1
            report.weighted_score -= weight
        elif vote_type == VoteType.CONFIRM_THREAT:
            report.upvote_count += 1
            report.weighted_score += (weight * 1.5)

        # 5. Persist Vote Record
        vote_record = ScamReportVote(
            report_id=report_id,
            user_id=user_id,
            vote_type=vote_type.value,
            vote_weight=weight
        )

        db.add(vote_record)
        db.commit()
        db.refresh(report)
        return report
