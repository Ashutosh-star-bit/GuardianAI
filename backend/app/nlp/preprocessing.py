"""
GuardianAI High-Performance Reusable Text Preprocessing Engine
Purpose: Provides Unicode normalization, emoji handling, whitespace collapse, repeated character reduction,
         homoglyph deobfuscation, and regex extraction for URLs, emails, phone numbers, currencies, and OTP codes.
"""

import re
import unicodedata
from typing import Dict, List, Tuple, Any
from pydantic import BaseModel, Field

# Pre-compiled High-Performance Regular Expressions
URL_REGEX = re.compile(r'https?://[^\s]+|www\.[^\s]+|t\.me/[^\s]+|wa\.me/[^\s]+', re.IGNORECASE)
EMAIL_REGEX = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', re.IGNORECASE)
PHONE_REGEX = re.compile(r'\+?\d{1,3}[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}')
CURRENCY_REGEX = re.compile(r'[\$\€\£\₹]\s*\d+(?:,\d+)*(?:\.\d+)?|\b\d+\s*(?:USD|EUR|INR|GBP|BTC)\b', re.IGNORECASE)
OTP_REGEX = re.compile(r'\b(?:OTP|code|passcode)?\s*[:=-]?\s*(\d{4,8})\b', re.IGNORECASE)
REPEATED_CHARS_REGEX = re.compile(r'(.)\1{3,}')
WHITESPACE_REGEX = re.compile(r'\s+')

# Common Emoji Representation Dictionary
EMOJI_TRANSLATION_MAP = {
    "🚨": "[ALERT]",
    "⚠️": "[WARNING]",
    "💰": "[MONEY]",
    "💵": "[MONEY]",
    "🔒": "[LOCK]",
    "🔑": "[KEY]",
    "❗": "[EXCLAMATION]",
    "❌": "[CANCEL]",
    "✅": "[CHECKMARK]",
}

# Cyrillic to Latin homoglyph translation map
HOMOGLYPH_MAP = {
    'а': 'a', 'е': 'e', 'о': 'o', 'р': 'p', 'с': 'c', 'у': 'y', 'х': 'x',
    'А': 'A', 'В': 'B', 'Е': 'E', 'К': 'K', 'М': 'M', 'Н': 'H', 'О': 'O',
    'Р': 'P', 'С': 'C', 'Т': 'T', 'Х': 'X'
}

class ExtractedEntitiesContainer(BaseModel):
    """Container for extracted structured entity artifacts."""
    urls: List[str] = Field(default_factory=list)
    emails: List[str] = Field(default_factory=list)
    phones: List[str] = Field(default_factory=list)
    currencies: List[str] = Field(default_factory=list)
    otps: List[str] = Field(default_factory=list)

class TextPreprocessor:
    """High-performance reusable text preprocessor."""

    @staticmethod
    def normalize_unicode(text: str) -> str:
        """Applies NFKC Unicode normalization."""
        if not text:
            return ""
        return unicodedata.normalize("NFKC", text)

    @classmethod
    def translate_emojis(cls, text: str) -> str:
        """Translates security-relevant emojis into text tokens or removes obscure emojis."""
        normalized = cls.normalize_unicode(text)
        translated = "".join(EMOJI_TRANSLATION_MAP.get(char, char) for char in normalized)
        return translated

    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """Collapses consecutive spaces, tabs, and newlines into single spaces."""
        return WHITESPACE_REGEX.sub(" ", text).strip()

    @staticmethod
    def reduce_repeated_characters(text: str) -> str:
        """Reduces 4+ repeated characters to a single character (e.g. URGENTTTTT -> URGENT)."""
        return REPEATED_CHARS_REGEX.sub(r'\1', text)

    @classmethod
    def deobfuscate_homoglyphs(cls, text: str) -> str:
        """Deobfuscates Cyrillic/Latin homoglyphs."""
        if not text:
            return ""
        return "".join(HOMOGLYPH_MAP.get(char, char) for char in text)

    @classmethod
    def clean_text(cls, text: str) -> str:
        """Applies full preprocessing pipeline: NFKC normalization, emoji translation, whitespace collapse, repeated character reduction."""
        if not text:
            return ""
        step1 = cls.normalize_unicode(text)
        step2 = cls.translate_emojis(step1)
        step3 = cls.normalize_whitespace(step2)
        return cls.reduce_repeated_characters(step3)

    @classmethod
    def extract_structured_artifacts(cls, text: str) -> Tuple[ExtractedEntitiesContainer, str]:
        """
        Extracts URLs, emails, phone numbers, currencies, and OTP codes using compiled regex.
        Returns tuple of (ExtractedEntitiesContainer, cleaned_text).
        """
        normalized_text = cls.normalize_whitespace(cls.translate_emojis(text))

        # Extract artifacts
        urls = URL_REGEX.findall(normalized_text)
        emails = EMAIL_REGEX.findall(normalized_text)

        # Phone extraction with length validation (min 10 digits)
        raw_phones = PHONE_REGEX.findall(normalized_text)
        phones = [p for p in raw_phones if len(re.sub(r'\D', '', p)) >= 10]

        currencies = CURRENCY_REGEX.findall(normalized_text)

        # OTP Extraction
        otp_matches = OTP_REGEX.findall(normalized_text)
        otps = [m for m in otp_matches if m]

        container = ExtractedEntitiesContainer(
            urls=urls,
            emails=emails,
            phones=phones,
            currencies=currencies,
            otps=otps
        )

        cleaned = cls.reduce_repeated_characters(normalized_text)
        return container, cleaned
