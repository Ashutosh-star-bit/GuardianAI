"""
GuardianAI Public API Security Pytest Suite
"""

import time
import pytest
from app.core.public_api_security import PublicAPISecurityEngine, PublicAPISecurityException

def test_verify_valid_timestamp():
    now_str = str(time.time())
    assert PublicAPISecurityEngine.verify_request_timestamp(now_str) is True

def test_verify_expired_timestamp_replay_attack():
    old_time_str = str(time.time() - 600)  # 10 minutes ago
    with pytest.raises(PublicAPISecurityException) as exc:
        PublicAPISecurityEngine.verify_request_timestamp(old_time_str)
    assert exc.value.status_code == 401

def test_sanitize_api_key_output_leakage_shield():
    key_dict = {
        "key_id": "key_1001",
        "key_prefix": "gai_live_88f9",
        "raw_key_secret": "gai_live_SECRET_SHOULD_NOT_LEAK",
        "key_hash": "sha256_hash_value"
    }
    clean = PublicAPISecurityEngine.sanitize_api_key_output(key_dict)
    assert "raw_key_secret" not in clean
    assert "key_hash" not in clean
    assert clean["key_id"] == "key_1001"
