"""
GuardianAI Feature Extraction Pipeline
Purpose: Extracts quantitative text feature metrics including urgency score, financial coercion score, caps ratio, and link counts.
"""

import re
from app.nlp.schemas import FeatureVector

URGENCY_KEYWORDS = [
    "urgent", "immediately", "action required", "account locked", "suspended",
    "expires in", "24 hours", "final warning", "verify now", "act fast"
]

FINANCIAL_KEYWORDS = [
    "bank", "wire transfer", "payment", "crypto", "bitcoin", "upi", "credit card",
    "refund", "lottery", "prize", "loan", "investment", "salary", "bonus"
]

class FeatureExtractor:
    """Quantitative feature extractor for text payloads."""

    @staticmethod
    def calculate_caps_ratio(text: str) -> float:
        """Calculates ratio of uppercase letters to total alphabetic characters."""
        alpha_chars = [c for c in text if c.isalpha()]
        if not alpha_chars:
            return 0.0
        caps_chars = [c for c in alpha_chars if c.isupper()]
        return round(len(caps_chars) / len(alpha_chars), 3)

    @staticmethod
    def count_links(text: str) -> int:
        """Counts occurrences of http/https/www/t.me/wa.me links in text."""
        link_pattern = r'https?://[^\s]+|www\.[^\s]+|t\.me/[^\s]+|wa\.me/[^\s]+'
        matches = re.findall(link_pattern, text, re.IGNORECASE)
        return len(matches)

    @classmethod
    def calculate_urgency_score(cls, text: str) -> float:
        """Calculates urgency intensity score (0.0 to 1.0) based on keyword frequency and exclamation marks."""
        text_lower = text.lower()
        matches = sum(1 for kw in URGENCY_KEYWORDS if kw in text_lower)
        exclamations = text.count("!")

        score = (matches * 0.25) + (min(exclamations, 5) * 0.05)
        return round(min(score, 1.0), 2)

    @classmethod
    def calculate_financial_coercion_score(cls, text: str) -> float:
        """Calculates financial demand intensity score (0.0 to 1.0)."""
        text_lower = text.lower()
        matches = sum(1 for kw in FINANCIAL_KEYWORDS if kw in text_lower)
        has_currency = bool(re.search(r'[\$\€\£\₹]\d+', text))

        score = (matches * 0.2) + (0.3 if has_currency else 0.0)
        return round(min(score, 1.0), 2)

    @classmethod
    def extract_features(cls, text: str) -> FeatureVector:
        """Extracts complete FeatureVector for a text payload."""
        caps_ratio = cls.calculate_caps_ratio(text)
        link_count = cls.count_links(text)
        urgency_score = cls.calculate_urgency_score(text)
        financial_score = cls.calculate_financial_coercion_score(text)

        return FeatureVector(
            urgency_score=urgency_score,
            financial_coercion_score=financial_score,
            caps_ratio=caps_ratio,
            link_count=link_count,
            homoglyph_detected=("@" in text or "$" in text)
        )
