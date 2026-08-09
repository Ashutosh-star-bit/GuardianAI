"""
GuardianAI Text Preprocessor Unit Test Suite
Purpose: Tests Unicode normalization, emoji translation, whitespace collapse, repeated character reduction,
         and extraction of URLs, emails, phone numbers, currencies, and OTP codes.
"""

import pytest
from app.nlp.preprocessing import TextPreprocessor

def test_unicode_and_emoji_translation():
    """Tests Unicode normalization and emoji conversion."""
    raw = "🚨 URGENT: 💰 Transfer $500!"
    translated = TextPreprocessor.translate_emojis(raw)
    assert "[ALERT]" in translated
    assert "[MONEY]" in translated

def test_whitespace_and_repeated_characters():
    """Tests whitespace collapse and repeated character reduction."""
    raw = "URGENTTTTT      ACTION      REQUIRED!!!!"
    normalized = TextPreprocessor.normalize_whitespace(raw)
    reduced = TextPreprocessor.reduce_repeated_characters(normalized)
    assert "URGENT" in reduced
    assert "REQUIRED!" in reduced

def test_structured_artifact_extractions():
    """Tests extraction of URLs, emails, phones, currencies, and OTP codes."""
    payload = (
        "🚨 URGENT: OTP code is 987654. Send $500 to support@paypal.com "
        "or call +1-800-555-0199 or visit http://paypa1-check.com"
    )

    artifacts, cleaned = TextPreprocessor.extract_structured_artifacts(payload)

    assert "http://paypa1-check.com" in artifacts.urls
    assert "support@paypal.com" in artifacts.emails
    assert len(artifacts.phones) > 0
    assert "$500" in artifacts.currencies
    assert "987654" in artifacts.otps
