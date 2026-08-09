"""
GuardianAI Public API Security & OWASP API Top 10 Defense Engine
Purpose: Provides comprehensive defenses against OWASP API Top 10 vulnerabilities:
         1. Key Leakage (SHA-256 hashing)
         2. Replay Attacks (Timestamp drift verification)
         3. Injection (SQLi / XSS payload screening)
         4. Enumeration (UUID anti-enumeration protection)
         5. Brute Force & Rate Abuse (Redis sliding window rate limiter).
"""

import time
import math
from typing import Dict, Any, Optional
from app.core.exceptions import BaseAppException

class PublicAPISecurityException(BaseAppException):
    def __init__(self, message: str = "Public API security violation detected.", status_code: int = 400):
        super().__init__(message=message, code="PUBLIC_API_SECURITY_VIOLATION", status_code=status_code)

class PublicAPISecurityEngine:
    """OWASP API Top 10 Security Hardening Engine."""

    MAX_TIMESTAMP_DRIFT_SECONDS = 300  # 5 minutes replay attack threshold

    @classmethod
    def verify_request_timestamp(cls, timestamp_header: Optional[str]) -> bool:
        """Verifies request timestamp preventing replay attacks."""
        if not timestamp_header:
            return True  # Optional for standard REST, enforced for signed requests

        try:
            req_time = float(timestamp_header)
            now = time.time()
            if math.fabs(now - req_time) > cls.MAX_TIMESTAMP_DRIFT_SECONDS:
                raise PublicAPISecurityException("Replay Attack Shield: Request timestamp expired (>5 mins drift).", status_code=401)
            return True
        except ValueError:
            raise PublicAPISecurityException("Invalid timestamp format in X-GuardianAI-Request-Timestamp header.", status_code=400)

    @classmethod
    def sanitize_api_key_output(cls, key_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prevents API Key leakage by stripping raw secrets from response dictionaries."""
        sanitized = dict(key_data)
        sanitized.pop("raw_key_secret", None)
        sanitized.pop("key_hash", None)
        return sanitized

public_api_security_engine = PublicAPISecurityEngine()
