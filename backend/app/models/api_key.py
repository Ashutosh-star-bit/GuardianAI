"""
GuardianAI Developer API Key SQLAlchemy Model
Purpose: Stores SHA-256 hashed API key metadata, environment isolation, scopes, expiration, and usage telemetry.
"""

import time
import hashlib
from sqlalchemy import Column, String, Boolean, Integer, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base

class APIKeyModel(Base):
    __tablename__ = "api_keys"

    id = Column(String(36), primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(128), nullable=False)
    key_prefix = Column(String(12), nullable=False)  # e.g., "gai_live_88f9"
    key_hash = Column(String(64), nullable=False, unique=True, index=True)  # SHA-256
    environment = Column(String(16), nullable=False, default="LIVE")  # LIVE, TEST
    tier = Column(String(16), nullable=False, default="FREE")  # FREE, PRO, ENTERPRISE
    scopes = Column(JSON, nullable=False, default=list)  # ["scan:read", "scan:write"]
    rate_limit_rps = Column(Integer, nullable=False, default=10)
    daily_quota = Column(Integer, nullable=False, default=1000)
    requests_today = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    last_used_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    @staticmethod
    def hash_key(raw_key: str) -> str:
        """Computes SHA-256 hash of raw API Key secret."""
        return hashlib.sha256(raw_key.encode('utf-8')).hexdigest()
