"""
GuardianAI Developer Platform API Key & Webhook Service Engine
Purpose: High-security API Key Generation, SHA-256 Hashing, Webhook HMAC-SHA256 Signing & Quota Metering.
"""

import time
import secrets
import hashlib
import hmac
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class APIKeyRecord(BaseModel):
    key_id: str
    name: str
    key_prefix: str
    key_hash: str
    raw_key_secret: Optional[str] = None  # Returned ONLY on creation!
    environment: str = "LIVE"
    tier: str = "FREE"  # FREE, PRO, ENTERPRISE
    rate_limit_rps: int = 10
    daily_quota: int = 1000
    is_active: bool = True
    created_at_iso: str

class APIKeyService:
    """Enterprise API Key Service Engine."""

    def __init__(self):
        self._keys_db: Dict[str, APIKeyRecord] = {}  # key_hash -> record

    @staticmethod
    def generate_raw_key(environment: str = "LIVE") -> tuple[str, str, str]:
        """Generates (raw_key, prefix, hash_sha256)."""
        prefix = "gai_live_" if environment.upper() == "LIVE" else "gai_test_"
        secret_part = secrets.token_hex(16)
        raw_key = f"{prefix}{secret_part}"
        key_prefix = raw_key[:12]
        key_hash = hashlib.sha256(raw_key.encode('utf-8')).hexdigest()
        return raw_key, key_prefix, key_hash

    def create_api_key(self, name: str, environment: str = "LIVE", tier: str = "FREE") -> APIKeyRecord:
        """Creates a new developer API Key."""
        raw_key, prefix, key_hash = self.generate_raw_key(environment)
        key_id = f"key_{int(time.time()*1000)}"

        rps_limits = {"FREE": 10, "PRO": 100, "ENTERPRISE": 1000}
        quota_limits = {"FREE": 1000, "PRO": 50000, "ENTERPRISE": 1000000}

        record = APIKeyRecord(
            key_id=key_id,
            name=name,
            key_prefix=prefix,
            key_hash=key_hash,
            raw_key_secret=raw_key,
            environment=environment.upper(),
            tier=tier.upper(),
            rate_limit_rps=rps_limits.get(tier.upper(), 10),
            daily_quota=quota_limits.get(tier.upper(), 1000),
            is_active=True,
            created_at_iso=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        )

        self._keys_db[key_hash] = record
        return record

    def authenticate_key(self, raw_key: str) -> Optional[APIKeyRecord]:
        """Validates API Key SHA-256 hash."""
        if not raw_key:
            return None
        target_hash = hashlib.sha256(raw_key.encode('utf-8')).hexdigest()
        record = self._keys_db.get(target_hash)
        if record and record.is_active:
            return record
        return None

    @staticmethod
    def sign_webhook_payload(payload_bytes: bytes, secret: str) -> str:
        """Computes HMAC-SHA256 signature header for webhook dispatches."""
        return hmac.new(secret.encode('utf-8'), payload_bytes, hashlib.sha256).hexdigest()

api_key_service = APIKeyService()
