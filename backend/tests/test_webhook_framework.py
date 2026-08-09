"""
GuardianAI Webhook Framework Pytest Suite
"""

import pytest
from app.developer_platform.webhook_framework import WebhookFrameworkEngine, WebhookEventType, webhook_engine

def test_webhook_hmac_signing_and_verification():
    secret = "whsec_test_secret_9988"
    payload = b'{"event_id": "evt_1001", "event_type": "THREAT_DETECTED"}'

    signature = WebhookFrameworkEngine.compute_hmac_signature(payload, secret)
    assert len(signature) == 64

    # Valid verification
    assert WebhookFrameworkEngine.verify_webhook_signature(payload, secret, signature) is True

    # Invalid signature verification
    assert WebhookFrameworkEngine.verify_webhook_signature(payload, secret, "invalid_forged_sig") is False

def test_webhook_dispatch_event():
    result = webhook_engine.dispatch_event(
        event_type=WebhookEventType.THREAT_DETECTED,
        target_url="https://api.partner.com/webhook",
        secret="whsec_partner_secret",
        data={"scam_type": "DIGITAL_ARREST", "risk_score": 98}
    )
    assert result.is_success is True
    assert result.http_status == 200
    assert len(result.signature_header) == 64
