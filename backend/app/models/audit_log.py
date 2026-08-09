"""
GuardianAI Immutable Compliance Audit Log ORM Model
Purpose: High-security immutable audit record storing administrative & system events with cryptographic SHA-256 hash chaining.
"""

import time
import hashlib
from typing import Optional, Dict, Any
from sqlalchemy import String, DateTime, Text, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.db.base import Base

class AuditLog(Base):
    """Immutable Audit Log Entity with SHA-256 Tamper-Evident Hash Chaining."""
    __tablename__ = "audit_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    actor_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False) # User ID or System Service
    action_type: Mapped[str] = mapped_column(String(64), index=True, nullable=False) # LOGIN, ROLE_CHANGE, REPORT_APPROVAL, etc.
    target_resource: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    payload_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    
    # Cryptographic Tamper-Evident Chain
    previous_hash: Mapped[str] = mapped_column(String(64), nullable=False, default="0"*64)
    record_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True,
        nullable=False
    )

    @classmethod
    def compute_record_hash(cls, actor_id: str, action_type: str, target: str, timestamp_str: str, prev_hash: str) -> str:
        """Calculates SHA-256 tamper-evident hash for audit record."""
        payload = f"{prev_hash}|{actor_id}|{action_type}|{target}|{timestamp_str}"
        return hashlib.sha256(payload.encode('utf-8')).hexdigest()
