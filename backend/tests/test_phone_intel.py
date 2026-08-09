"""
GuardianAI Phone Intelligence Engine Unit Test Suite
Purpose: Tests country code parsing, E.164 formatting, premium rate number detection, repeated digit checking, and hidden digit detection.
"""

import pytest
from app.threat_intel.phone_intel import PhoneIntelligenceEngine, PhoneIntelReport

def test_parse_international_phone_number():
    """Tests international US (+1) phone number parsing."""
    raw = "+1 (800) 555-0199"
    report: PhoneIntelReport = PhoneIntelligenceEngine.parse_phone_number(raw)

    assert report.country_code == "+1"
    assert "US/Canada" in report.country_name
    assert report.local_number == "8005550199"
    assert report.is_valid_length is True
    assert report.risk_score == 0

def test_detect_premium_rate_number():
    """Tests premium rate (1-900) number detection."""
    raw = "+1 (900) 555-9999"
    report = PhoneIntelligenceEngine.parse_phone_number(raw)

    assert report.is_premium_rate is True
    assert "POSSIBLE_PREMIUM_RATE_NUMBER" in report.risk_indicators
    assert report.risk_score >= 40

def test_detect_repeated_digits_and_obfuscation():
    """Tests repeated digits (9999999999) and hidden digits (* or X) detection."""
    raw = "+91-9999999999-XXX"
    report = PhoneIntelligenceEngine.parse_phone_number(raw)

    assert report.has_repeated_digits is True
    assert report.has_hidden_obfuscated_digits is True
    assert report.risk_score >= 65
