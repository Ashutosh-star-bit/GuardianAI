"""
GuardianAI Keyword Detection Engine Unit Test Suite
Purpose: Tests keyword trigger detection across all required categories and dynamic rule registration.
"""

import pytest
from app.nlp.keywords import KeywordDetectionEngine, KeywordRule

def test_detect_required_keywords():
    """Tests detection of all required threat keyword triggers in a composite message."""
    text = (
        "URGENT BANK ALERT! Your account is account blocked. Update your KYC immediately! "
        "Click to verify and claim your lottery prize winner status. Limited time refund for crypto investment. "
        "OTP code for courier delivery."
    )

    matches = KeywordDetectionEngine.detect_keywords(text)
    matched_triggers = [m.rule.trigger for m in matches]

    assert "urgent" in matched_triggers
    assert "immediately" in matched_triggers
    assert "verify" in matched_triggers
    assert "click" in matched_triggers
    assert "winner" in matched_triggers
    assert "prize" in matched_triggers
    assert "lottery" in matched_triggers
    assert "kyc" in matched_triggers
    assert "refund" in matched_triggers
    assert "limited time" in matched_triggers
    assert "investment" in matched_triggers
    assert "crypto" in matched_triggers
    assert "otp" in matched_triggers
    assert "account blocked" in matched_triggers
    assert "bank alert" in matched_triggers
    assert "courier" in matched_triggers

def test_dynamic_custom_keyword_registration():
    """Tests dynamic registration of custom keyword rules."""
    new_rule = KeywordRule(
        keyword_id="kw_custom_wire",
        trigger="wire transfer required",
        category="FINANCIAL",
        severity="Critical",
        weight=0.5
    )
    KeywordDetectionEngine.register_rule(new_rule)

    matches = KeywordDetectionEngine.detect_keywords("Notice: wire transfer required today.")
    matched_ids = [m.rule.keyword_id for m in matches]
    assert "kw_custom_wire" in matched_ids
