"""
GuardianAI Scan Database Model
Purpose: SQLAlchemy ORM schema definition for the scans table recording threat evaluation results and XAI summaries.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Scan(Base):
    __tablename__ = "scans"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=True)
    payload_type: Mapped[str] = mapped_column(String(32), nullable=False) # text, url, qr, email
    threat_score: Mapped[int] = mapped_column(Integer, nullable=False) # 0 to 100
    risk_band: Mapped[str] = mapped_column(String(16), nullable=False) # safe, caution, dangerous
    plain_rationale: Mapped[str] = mapped_column(Text, nullable=False)
    execution_ms: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="scans")
