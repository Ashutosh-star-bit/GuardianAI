"""
GuardianAI Voice Intelligence Exception Hierarchy
"""

from typing import Optional, List, Any
from app.core.exceptions import BaseAppException

class VoiceIntelError(BaseAppException):
    """Base exception for all Voice Intelligence errors."""
    def __init__(self, message: str = "Voice intelligence error.", details: Optional[List[Any]] = None):
        super().__init__(message=message, code="VOICE_INTEL_ERROR", status_code=400, details=details)

class UnsupportedAudioFormatError(VoiceIntelError):
    """Raised when uploaded audio container format is unsupported."""
    def __init__(self, message: str = "Unsupported audio container format.", details: Optional[List[Any]] = None):
        super().__init__(message=message, details=details)
        self.code = "UNSUPPORTED_AUDIO_FORMAT"

class STTProviderError(VoiceIntelError):
    """Raised when Speech-to-Text provider fails transcription."""
    def __init__(self, message: str = "STT transcription provider error.", details: Optional[List[Any]] = None):
        super().__init__(message=message, details=details)
        self.code = "STT_PROVIDER_ERROR"
        self.status_code = 502

class AudioPreprocessingError(VoiceIntelError):
    """Raised when audio resampling or VAD processing fails."""
    def __init__(self, message: str = "Audio preprocessing failed.", details: Optional[List[Any]] = None):
        super().__init__(message=message, details=details)
        self.code = "AUDIO_PREPROCESSING_ERROR"
