"""
GuardianAI ScamReport SQLAlchemy 2.0 ORM Models & Pydantic Schemas
Purpose: Complete production data model for crowdsourced Scam Reports, Attachments, and Weighted Votes.
         Includes Indexes, Check Constraints, JSONB Evidence Storage, and ORM Relationships.
"""

import uuid
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from sqlalchemy import String, Integer, Text, ForeignKey, DateTime, Boolean, Index, CheckConstraint, JSON, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pydantic import BaseModel, Field, ConfigDict

from app.db.base import Base, UUIDMixin, TimestampMixin

# ==========================================
# 1. SQLALCHEMY ORM MODELS
# ==========================================

class ScamReport(Base, UUIDMixin, TimestampMixin):
    """ScamReport Entity Model for crowdsourced cyber threat intelligence."""
    __tablename__ = "scam_reports"

    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="Reporting user ID"
    )
    category: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        index=True,
        comment="Category e.g. BANKING_FRAUD, DIGITAL_ARREST, PHISHING_URL, JOB_SCAM"
    )
    source: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="MANUAL_SUBMISSION",
        comment="Source channel e.g. SMS, EMAIL, PHONE, URL, WHATSAPP, TELEGRAM"
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Scam report title headline"
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="Full detailed narrative of scam encounter"
    )
    evidence_data: Mapped[Dict[str, Any]] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
        comment="JSONB container for extracted IOCs (phone numbers, URLs, UPI handles, BTC wallets)"
    )
    risk_level: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="HIGH",
        index=True,
        comment="Risk rating: SAFE, CAUTION, DANGEROUS, HIGH, CRITICAL"
    )
    verification_status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="PENDING",
        index=True,
        comment="Status: PENDING, UNDER_REVIEW, VERIFIED, REJECTED, MERGED"
    )
    upvote_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0", nullable=False)
    downvote_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0", nullable=False)
    weighted_score: Mapped[float] = mapped_column(Float, default=0.0, server_default="0.0", nullable=False)
    is_spam: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", nullable=False, index=True)

    # Relationships
    attachments: Mapped[List["ScamReportAttachment"]] = relationship(
        "ScamReportAttachment",
        back_populates="report",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    votes: Mapped[List["ScamReportVote"]] = relationship(
        "ScamReportVote",
        back_populates="report",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    __table_args__ = (
        Index("ix_scam_reports_status_created", "verification_status", "created_at"),
        Index("ix_scam_reports_category_status", "category", "verification_status"),
        CheckConstraint(
            "verification_status IN ('PENDING', 'UNDER_REVIEW', 'VERIFIED', 'REJECTED', 'MERGED')",
            name="check_valid_verification_status"
        ),
        CheckConstraint(
            "risk_level IN ('SAFE', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL', 'CAUTION', 'DANGEROUS')",
            name="check_valid_risk_level"
        )
    )

    def __init__(self, **kwargs):
        kwargs.setdefault("upvote_count", 0)
        kwargs.setdefault("downvote_count", 0)
        kwargs.setdefault("weighted_score", 0.0)
        kwargs.setdefault("is_spam", False)
        kwargs.setdefault("evidence_data", {})
        super().__init__(**kwargs)


class ScamReportAttachment(Base, UUIDMixin, TimestampMixin):
    """ScamReportAttachment Entity Model for multi-modal evidence files."""
    __tablename__ = "scam_report_attachments"

    report_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("scam_reports.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    file_type: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        comment="Type: SCREENSHOT, PDF_DOCUMENT, AUDIO_RECORDING"
    )
    file_url: Mapped[str] = mapped_column(String(512), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(64), nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)

    report: Mapped["ScamReport"] = relationship("ScamReport", back_populates="attachments")


class ScamReportVote(Base, UUIDMixin, TimestampMixin):
    """ScamReportVote Entity Model for weighted community trust votes."""
    __tablename__ = "scam_report_votes"

    report_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("scam_reports.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    vote_type: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        comment="UPVOTE, DOWNVOTE, CONFIRM_THREAT"
    )
    vote_weight: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)

    report: Mapped["ScamReport"] = relationship("ScamReport", back_populates="votes")

    __table_args__ = (
        Index("ix_unique_user_report_vote", "report_id", "user_id", unique=True),
    )


# ==========================================
# 2. PYDANTIC V2 SCHEMAS
# ==========================================

class AttachmentCreate(BaseModel):
    file_type: str = Field(description="SCREENSHOT, PDF_DOCUMENT, AUDIO_RECORDING")
    file_url: str = Field(description="Storage S3/vault URL")
    mime_type: str = Field(default="image/png")
    file_size_bytes: int = Field(gt=0)

class AttachmentResponse(AttachmentCreate):
    id: str
    report_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ScamReportCreateSchema(BaseModel):
    category: str = Field(description="BANKING_FRAUD, DIGITAL_ARREST, PHISHING_URL, JOB_SCAM")
    source: str = Field(default="MANUAL_SUBMISSION", description="SMS, EMAIL, PHONE, URL, WHATSAPP")
    title: str = Field(min_length=5, max_length=255)
    description: str = Field(min_length=10)
    evidence_data: Optional[Dict[str, Any]] = Field(default_factory=dict)
    attachments: Optional[List[AttachmentCreate]] = Field(default_factory=list)

class ScamReportResponseSchema(BaseModel):
    id: str
    user_id: Optional[str] = None
    category: str
    source: str
    title: str
    description: str
    evidence_data: Dict[str, Any]
    risk_level: str
    verification_status: str
    upvote_count: int
    downvote_count: int
    weighted_score: float
    is_spam: bool
    attachments: List[AttachmentResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
