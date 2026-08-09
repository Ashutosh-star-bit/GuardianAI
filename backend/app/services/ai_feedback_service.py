"""
GuardianAI AI Feedback Service Engine
Purpose: Enterprise Service recording Human-in-the-Loop (HITL) feedback on AI predictions:
         Stores AI Prediction, Confidence, Decision Rationale, User Feedback, and Suggested Corrections.
         NOTE: Buffers records safely for offline RLHF batch exports; DOES NOT automatically trigger model retraining.
"""

from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.feedback import AIPredictionFeedback, FeedbackCreateSchema
from app.models.scan import Scan
from app.models.scam_report import ScamReport
from app.core.exceptions import BaseAppException

class AIFeedbackServiceError(BaseAppException):
    """Raised when recording AI feedback fails."""
    def __init__(self, message: str = "Recording AI feedback failed.", details: Optional[list] = None):
        super().__init__(message=message, code="AI_FEEDBACK_SERVICE_ERROR", status_code=400, details=details)

class AIFeedbackService:
    """Enterprise Reusable AI Prediction Feedback Service."""

    def record_feedback(
        self,
        db: Session,
        payload: FeedbackCreateSchema,
        user_id: str
    ) -> AIPredictionFeedback:
        """
        Records user feedback on an AI scan prediction without triggering automated model retraining.
        """
        # 1. Optional Scan or Report Integrity Check
        if payload.scan_id:
            scan = db.execute(select(Scan).where(Scan.id == payload.scan_id)).scalar_one_or_none()
            if not scan:
                # Log warning or proceed if scan record is transient
                pass

        if payload.report_id:
            report = db.execute(select(ScamReport).where(ScamReport.id == payload.report_id)).scalar_one_or_none()
            if not report:
                pass

        # 2. ORM Entity Construction
        feedback_record = AIPredictionFeedback(
            scan_id=payload.scan_id,
            report_id=payload.report_id,
            user_id=user_id,
            feedback_type=payload.feedback_type,
            predicted_risk_level=payload.predicted_risk_level,
            actual_risk_level=payload.actual_risk_level,
            suggested_category=payload.suggested_category,
            rating=payload.rating,
            comment=payload.comment,
            is_verified_by_moderator=False
        )

        db.add(feedback_record)
        db.commit()
        db.refresh(feedback_record)
        return feedback_record

    def get_unverified_feedback(self, db: Session, limit: int = 50) -> list[AIPredictionFeedback]:
        """Retrieves unverified AI feedback records for moderator review."""
        stmt = select(AIPredictionFeedback).where(
            AIPredictionFeedback.is_verified_by_moderator == False
        ).limit(limit)
        return list(db.execute(stmt).scalars().all())
