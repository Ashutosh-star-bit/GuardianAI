"""
GuardianAI Enterprise LanguageDetector Subsystem
Purpose: Detects document language and script type:
         English (en), Hindi (hi), Spanish (es), Mixed English-Hindi (hi-en), Unknown (unknown),
         with explicit confidence score output (0.0 to 1.0).
"""

import re
from typing import Tuple, List, Dict, Any
from pydantic import BaseModel, Field

class LanguageDetectionResult(BaseModel):
    """Result DTO for document language and script detection."""
    language_code: str = Field(description="en, hi, es, hi-en, unknown")
    script_type: str = Field(description="LATIN, DEVANAGARI, MIXED, UNKNOWN")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    is_multilingual: bool = Field(default=False)
    detected_languages: List[str] = Field(default_factory=list)

class LanguageDetector:
    """Enterprise Script & ISO-639 Language Code Identifier Engine."""

    # Unicode Script Regular Expressions
    DEVANAGARI_REGEX = re.compile(r'[\u0900-\u097F]')
    LATIN_REGEX = re.compile(r'[a-zA-Z]')
    CYRILLIC_REGEX = re.compile(r'[\u0400-\u04FF]')

    # Common Keyword Sets
    ENGLISH_KEYWORDS = {"urgent", "verify", "account", "paypal", "bank", "security", "notice", "suspended", "click", "user"}
    SPANISH_KEYWORDS = {"el", "la", "los", "las", "por", "para", "como", "cuenta", "verificar", "respuesta"}
    HINGLISH_KEYWORDS = {"aapka", "kare", "karo", "paisa", "khata", "bhejo", "turant", "padhe"}

    @classmethod
    def detect_script_and_language(cls, text: str) -> Tuple[str, str]:
        """
        Base contract implementation returning Tuple[script_type, iso_639_lang_code].
        """
        res = cls.detect_language_detailed(text)
        return res.script_type, res.language_code

    @classmethod
    def detect_language_detailed(cls, text: str) -> LanguageDetectionResult:
        """
        Detects document language code, script type, confidence score, and multilingual presence.
        """
        if not text or not text.strip():
            return LanguageDetectionResult(
                language_code="unknown",
                script_type="UNKNOWN",
                confidence=0.0,
                is_multilingual=False,
                detected_languages=["unknown"]
            )

        devanagari_count = len(cls.DEVANAGARI_REGEX.findall(text))
        latin_count = len(cls.LATIN_REGEX.findall(text))
        total_chars = devanagari_count + latin_count

        # 1. Unknown Language Check (Low alphanumeric density)
        if total_chars < 3:
            return LanguageDetectionResult(
                language_code="unknown",
                script_type="UNKNOWN",
                confidence=0.20,
                is_multilingual=False,
                detected_languages=["unknown"]
            )

        dev_ratio = devanagari_count / max(total_chars, 1)
        lat_ratio = latin_count / max(total_chars, 1)

        # 2. Mixed English-Hindi (Hinglish or Code-Switched text)
        if devanagari_count >= 3 and latin_count >= 5:
            return LanguageDetectionResult(
                language_code="hi-en",
                script_type="MIXED",
                confidence=0.95,
                is_multilingual=True,
                detected_languages=["hi", "en"]
            )

        # 3. Hindi (Devanagari script dominant)
        if dev_ratio > 0.60:
            return LanguageDetectionResult(
                language_code="hi",
                script_type="DEVANAGARI",
                confidence=round(min(0.85 + dev_ratio * 0.15, 0.99), 2),
                is_multilingual=False,
                detected_languages=["hi"]
            )

        # 4. Spanish & English Keyword Disambiguation
        words = set(re.findall(r'\b\w+\b', text.lower()))
        es_match = len(words.intersection(cls.SPANISH_KEYWORDS))
        eng_match = len(words.intersection(cls.ENGLISH_KEYWORDS))
        hinglish_match = len(words.intersection(cls.HINGLISH_KEYWORDS))

        if es_match >= 2 and es_match > eng_match:
            return LanguageDetectionResult(
                language_code="es",
                script_type="LATIN",
                confidence=0.90,
                is_multilingual=False,
                detected_languages=["es"]
            )

        if hinglish_match >= 2 and devanagari_count == 0:
            return LanguageDetectionResult(
                language_code="hi-en",
                script_type="LATIN",
                confidence=0.88,
                is_multilingual=True,
                detected_languages=["hi", "en"]
            )

        confidence_score = round(min(0.80 + (eng_match * 0.05) + (lat_ratio * 0.15), 0.99), 2)

        return LanguageDetectionResult(
            language_code="en",
            script_type="LATIN",
            confidence=confidence_score,
            is_multilingual=False,
            detected_languages=["en"]
        )
