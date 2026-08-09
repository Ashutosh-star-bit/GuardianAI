"""
GuardianAI Multilingual Language Detector & Locale Resolver
Purpose: Detects message language (English, Spanish, Hindi, French) and provides locale-specific pattern dictionaries.
"""

from typing import Dict, Any

LANGUAGE_KEYWORDS: Dict[str, list] = {
    "es": ["urgente", "banco", "cuenta", "ganado", "premio", "bloqueada", "verificar"],
    "hi": ["बधाई", "बैंक", "खाता", "अकाउंट", "इनाम", "जीते", "तुरंत"],
    "fr": ["urgent", "banque", "compte", "gagné", "suspendu", "vérifier"],
    "en": ["urgent", "bank", "account", "won", "prize", "locked", "verify"]
}

class MultilingualDetector:
    """Detects input text language code."""

    @staticmethod
    def detect_language(text: str) -> str:
        """Simple keyword-based language detector (en, es, hi, fr). Defaults to 'en'."""
        text_lower = text.lower()
        scores: Dict[str, int] = {"en": 0, "es": 0, "hi": 0, "fr": 0}

        for lang, kws in LANGUAGE_KEYWORDS.items():
            for kw in kws:
                if kw in text_lower:
                    scores[lang] += 1

        best_lang = max(scores, key=scores.get)
        if scores[best_lang] > 0:
            return best_lang

        return "en"
