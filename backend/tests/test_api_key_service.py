"""
GuardianAI APIKeyService Pytest Suite
"""

import pytest
from app.developer_platform.api_key_service import APIKeyService

@pytest.fixture
def key_service():
    return APIKeyService()

def test_create_and_authenticate_api_key(key_service):
    key_record = key_service.create_api_key("Production Mobile App", environment="LIVE", tier="PRO")
    assert key_record.raw_key_secret.startswith("gai_live_")
    assert key_record.tier == "PRO"
    assert key_record.rate_limit_rps == 100

    # Authenticate via raw secret key
    auth_result = key_service.authenticate_key(key_record.raw_key_secret)
    assert auth_result is not None
    assert auth_result.key_id == key_record.key_id

def test_invalid_api_key(key_service):
    assert key_service.authenticate_key("gai_live_invalid_fake_key") is None

def test_webhook_hmac_signing():
    payload = b'{"event": "SCAM_DETECTED", "risk_score": 98}'
    secret = "whsec_secret_123"
    sig = APIKeyService.sign_webhook_payload(payload, secret)
    assert len(sig) == 64
