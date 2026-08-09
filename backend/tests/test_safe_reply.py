"""
GuardianAI Safe Reply Generator Unit Test Suite
Purpose: Tests safe decline reply template generation across 9 scam categories and multilingual locales (EN, ES, HI, FR).
"""

import pytest
from app.decision_engine.safe_reply import SafeReplyGenerator, SafeReplyTemplate

def test_generate_english_bank_spoof_reply():
    """Tests generating English bank spoof safe decline reply."""
    template: SafeReplyTemplate = SafeReplyGenerator.generate_reply("BANK_SPOOF", locale="en")
    assert template.category_key == "BANK_SPOOF"
    assert template.locale == "en"
    assert "official banking app" in template.safe_reply_text

def test_generate_spanish_job_scam_reply():
    """Tests generating Spanish job scam safe decline reply."""
    template = SafeReplyGenerator.generate_reply("JOB_SCAM", locale="es")
    assert template.category_key == "JOB_SCAM"
    assert template.locale == "es"
    assert "ofertas de trabajo no solicitadas" in template.safe_reply_text

def test_generate_hindi_otp_request_reply():
    """Tests generating Hindi OTP refusal safe reply."""
    template = SafeReplyGenerator.generate_reply("OTP_REQUEST", locale="hi")
    assert template.category_key == "OTP_REQUEST"
    assert template.locale == "hi"
    assert "वन-टाइम पासवर्ड (OTP)" in template.safe_reply_text

def test_generate_french_lottery_reply():
    """Tests generating French lottery decline safe reply."""
    template = SafeReplyGenerator.generate_reply("LOTTERY_SCAM", locale="fr")
    assert template.category_key == "LOTTERY_SCAM"
    assert template.locale == "fr"
    assert "aucune loterie ni concours" in template.safe_reply_text
