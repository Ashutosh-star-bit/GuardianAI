"""
GuardianAI LanguageDetector Pytest Suite
Purpose: Tests LanguageDetector for English (en), Hindi (hi), Mixed English-Hindi (hi-en),
         Unknown language detection, and confidence scoring.
"""

import pytest
from app.document_intel.language_detector import LanguageDetector, LanguageDetectionResult

def test_language_detector_english():
    """Tests English language identification, Latin script, and confidence score."""
    text = "URGENT NOTICE: Verify your bank account security details immediately."
    res: LanguageDetectionResult = LanguageDetector.detect_language_detailed(text)

    assert res.language_code == "en"
    assert res.script_type == "LATIN"
    assert res.confidence >= 0.85
    assert res.is_multilingual is False
    assert "en" in res.detected_languages

def test_language_detector_hindi():
    """Tests Hindi language identification, Devanagari script, and confidence score."""
    text = "यह एक अनधिकृत लॉगिन प्रयास है। कृपया अपना खाता सत्यापित करें।"
    res: LanguageDetectionResult = LanguageDetector.detect_language_detailed(text)

    assert res.language_code == "hi"
    assert res.script_type == "DEVANAGARI"
    assert res.confidence >= 0.85
    assert res.is_multilingual is False
    assert "hi" in res.detected_languages

def test_language_detector_mixed_english_hindi():
    """Tests mixed English-Hindi code-switched text detection."""
    text = "URGENT SECURITY ALERT: आपका खाता suspend कर दिया गया है। Click here to verify."
    res: LanguageDetectionResult = LanguageDetector.detect_language_detailed(text)

    assert res.language_code == "hi-en"
    assert res.script_type == "MIXED"
    assert res.confidence >= 0.90
    assert res.is_multilingual is True
    assert "hi" in res.detected_languages
    assert "en" in res.detected_languages

def test_language_detector_unknown():
    """Tests unknown language detection for empty/non-alphanumeric text."""
    res_empty = LanguageDetector.detect_language_detailed("")
    assert res_empty.language_code == "unknown"
    assert res_empty.confidence == 0.0

    res_symbols = LanguageDetector.detect_language_detailed("!!! ### $$$")
    assert res_symbols.language_code == "unknown"
    assert res_symbols.confidence <= 0.20
