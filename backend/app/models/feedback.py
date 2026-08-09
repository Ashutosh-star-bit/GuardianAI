"""
GuardianAI AI Prediction Feedback SQLAlchemy 2.0 ORM Model & Pydantic Schemas
Purpose: Records user feedback on AI scan predictions (True Positives, False Positives, Ratings, Comments)
         to fuel the Human-in-the-Loop (HITL) RLHF continuous model retraining pipeline.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from sqlalchemy import String, Integer, Text, ForeignKey, DateTime, Boolean, Index, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pydantic import BaseModel, Field, ConfigDict

from app.db.base import Base, UUIDMixin, TimestampMixin

# ==========================================
# 1. SQLALCHEMY ORM MODEL
# ==========================================

class AIPredictionFeedback(Base, UUIDMixin, TimestampMixin):
    """AIPredictionFeedback Entity Model storing HITL feedback loop records."""
    __tablename__ = "ai_prediction_feedback"

    scan_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("scans.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="Associated scan ID if feedback relates to an automated scan"
    )
    report_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("scam_reports.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="Associated community report ID if feedback relates to a report"
    )
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="User submitting the feedback"
    )
    feedback_type: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        index=True,
        comment="CORRECT_PREDICTION, INCORRECT_PREDICTION, FALSE_POSITIVE, FALSE_NEGATIVE"
    )
    predicted_risk_level: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        comment="Original AI predicted risk level e.g. SAFE, CAUTION, DANGEROUS"
    )
    actual_risk_level: Mapped[Optional[str]] = mapped_column(
        String(32),
        nullable=True,
        comment="User/Moderator corrected actual risk level"
    )
    suggested_category: Mapped[Optional[str]] = mapped_column(
        String(64),
        nullable=True,
        comment="User suggested scam category e.g. DIGITAL_ARREST, BANKING_FRAUD"
    )
    rating: Mapped[int] = mapped_column(
        Integer,
        default=5,
        nullable=False,
        comment="User satisfaction rating from 1 to 5 stars"
    )
    comment: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Optional qualitative user commentary or correction rationale"
    )
    is_verified_by_moderator: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
        comment="Flag indicating whether feedback has been verified by a moderator"
    )

    __table_args__ = (
        Index("ix_feedback_type_verified", "feedback_type", "is_verified_by_moderator"),
        CheckConstraint(
            "feedback_type IN ('CORRECT_PREDICTION', 'INCORRECT_PREDICTION', 'FALSE_POSITIVE', 'FALSE_NEGATIVE')",
            name="check_valid_feedback_type"
        ),
        CheckConstraint(
            "rating >= 1 AND rating <= 5",
            name="check_valid_rating_range"
        )
    )

    def __init__(self, **kwargs):
        kwargs.setdefault("rating", 5)
        kwargs.setdefault("is_verified_by_moderator", False)
        super().__init__(**kwargs)


# ==========================================
# 2. PYDANTIC V2 SCHEMAS
# ==========================================

class FeedbackCreateSchema(BaseModel):
    scan_id: Optional[str] = Field(default=None, description="Scan ID if feedback is for a scan")
    report_id: Optional[str] = Field(default=None, description="Report ID if feedback is for a report")
    feedback_type: str = Field(description="CORRECT_PREDICTION, INCORRECT_PREDICTION, FALSE_POSITIVE, FALSE_NEGATIVE")
    predicted_risk_level: str = Field(description="Original AI risk level prediction")
    actual_risk_level: Optional[str] = Field(default=None, description="User/Moderator corrected actual risk level")
    suggested_category: Optional[str] = Field(default=None, description="Suggested scam category")
    rating: int = Field(default=5, ge=1, le=5, description="Satisfaction rating (1 to 5)")
    comment: Optional[str] = Field(default=None, description="Qualitative feedback commentary")

class FeedbackResponseSchema(BaseModel):
    id: str
    scan_id: Optional[str] = None
    report_id: Optional[str] = None
    user_id: str
    feedback_type: str
    predicted_risk_level: str
    actual_risk_level: Optional[str] = None
    suggested_category: Optional[str] = None
    rating: int
    comment: Optional[str] = None
    is_verified_by_moderator: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
