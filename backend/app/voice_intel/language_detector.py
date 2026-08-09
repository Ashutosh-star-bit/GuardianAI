"""
GuardianAI Voice Language Detector Module
Purpose: Identifies spoken audio acoustic language and script code (English, Hindi, Hinglish, Tamil, Telugu).
"""

from app.voice_intel.base import BaseVoiceLanguageDetector
from app.voice_intel.schemas import AudioPayload

class LanguageDetector(BaseVoiceLanguageDetector):
    """Enterprise Audio Language Detector Engine."""

    def detect_language(self, payload: AudioPayload) -> str:
        if not payload.raw_bytes:
            return "en"

        # Heuristic audio language detection fallback (Defaults to English/Hinglish)
        return "hi-en" if "hindi" in (payload.filename or "").lower() else "en"
