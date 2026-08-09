"""
GuardianAI TranscriptCleaner Pytest Test Suite
"""

import pytest
from app.voice_intel.transcript_cleaner import TranscriptCleaner

def test_transcript_cleaner_fillers_and_repeated_words():
    cleaner = TranscriptCleaner()
    raw = "uh um hello hello sir this is uh CBI police department. pay pay 50000 rupees to pay pal immediately."

    cleaned = cleaner.clean(raw)

    assert "uh" not in cleaned.lower()
    assert "um" not in cleaned.lower()
    assert "hello hello" not in cleaned.lower()
    assert "pay pay" not in cleaned.lower()
    assert "paypal" in cleaned.lower()
    assert cleaned.startswith("Hello")
    assert cleaned.endswith(".")

def test_transcript_cleaner_unicode_normalization():
    cleaner = TranscriptCleaner()
    raw = "Hello\xa0world\x00 this is \u200bKYC verification."

    cleaned = cleaner.clean(raw)

    assert "\x00" not in cleaned
    assert "\xa0" not in cleaned
    assert "KYC" in cleaned

def test_transcript_cleaner_empty_string():
    cleaner = TranscriptCleaner()
    assert cleaner.clean("") == ""
    assert cleaner.clean("   \n\t  ") == ""
