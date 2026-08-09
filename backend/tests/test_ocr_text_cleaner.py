"""
GuardianAI Enterprise OCRTextCleaner Pytest Suite
Purpose: Tests broken line rejoins, hyphenation repairs, repeated space/newline collapse,
         OCR character mistake corrections, invisible character stripping, and Unicode homoglyph normalization.
"""

import pytest
from app.document_intel.text_cleaner import TextCleaner

def test_text_cleaner_invisible_chars_and_null_bytes():
    """Tests stripping null bytes, zero-width spaces, and control characters."""
    raw = "URGENT:\x00 Message\u200b with\x07 control\x1f chars"
    cleaned = TextCleaner.clean_ocr_text(raw)

    assert "\x00" not in cleaned
    assert "\u200b" not in cleaned
    assert "\x07" not in cleaned
    assert cleaned == "URGENT: Message with control chars"

def test_text_cleaner_hyphenation_repair():
    """Tests repairing hyphenated line breaks across words."""
    raw = "Your account requires verifi-\n cation to continue."
    cleaned = TextCleaner.clean_ocr_text(raw)

    assert "verification" in cleaned
    assert "verifi-" not in cleaned

def test_text_cleaner_broken_line_rejoin():
    """Tests rejoining broken sentences split across newline boundaries."""
    raw = "This is a broken sentence line\nthat continues on next line."
    cleaned = TextCleaner.clean_ocr_text(raw)

    assert "broken sentence line that continues" in cleaned

def test_text_cleaner_ocr_mistakes_and_leetspeak():
    """Tests fixing common OCR character confusions (e.g. paypa1 -> paypal, v3r1fy -> verify)."""
    raw = "URGENT: Paypa1 acc0unt security notification. V3r1fy immediately."
    cleaned = TextCleaner.clean_ocr_text(raw)

    assert "paypal" in cleaned.lower()
    assert "account" in cleaned.lower()
    assert "verify" in cleaned.lower()

def test_text_cleaner_unicode_homoglyphs():
    """Tests Cyrillic homoglyph replacement (Cyrillic 'а', 'е', 'і')."""
    raw = "Pаypаl sеcurіty alert"  # Cyrillic homoglyphs
    cleaned = TextCleaner.clean_ocr_text(raw, fix_homoglyphs=True)

    assert "Paypal security alert" == cleaned

def test_text_cleaner_repeated_spaces_and_newlines():
    """Tests collapsing multiple spaces and 3+ line breaks."""
    raw = "URGENT:   Multiple    spaces\n\n\n\n\nNew paragraph"
    cleaned = TextCleaner.clean_ocr_text(raw)

    assert "URGENT: Multiple spaces" in cleaned
    assert "\n\n\n" not in cleaned
    assert "spaces\n\nNew paragraph" in cleaned
