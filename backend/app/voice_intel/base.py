"""
GuardianAI Voice Intelligence Abstract Base Classes
Purpose: Strict dependency injection contracts for Speech AI providers & audio processing engines.
"""

from abc import ABC, abstractmethod
from app.voice_intel.schemas import AudioPayload, PreprocessedAudio, STTResult, SpeakerMetadataResult

class BaseAudioPreprocessor(ABC):
    @abstractmethod
    def preprocess(self, payload: AudioPayload) -> PreprocessedAudio:
        """Resamples raw audio payload to 16kHz mono WAV, trims silence via VAD, and normalizes volume."""
        pass

class BaseSTTProvider(ABC):
    @abstractmethod
    def transcribe(self, preprocessed: PreprocessedAudio, language_hint: str = None) -> STTResult:
        """Transcribes PCM audio stream into raw text with word-level timestamps and confidence scores."""
        pass

class BaseTranscriptCleaner(ABC):
    @abstractmethod
    def clean(self, raw_transcript: str) -> str:
        """Cleans STT hesitation markers, filler words ('uh', 'um'), and homoglyph errors."""
        pass

class BaseSpeakerMetadataEngine(ABC):
    @abstractmethod
    def extract_metadata(self, preprocessed: PreprocessedAudio, transcript: str) -> SpeakerMetadataResult:
        """Extracts speaker turns (diarization), words-per-minute rate, and acoustic urgency markers."""
        pass

class BaseVoiceLanguageDetector(ABC):
    @abstractmethod
    def detect_language(self, payload: AudioPayload) -> str:
        """Identifies audio acoustic spoken language (English, Hindi, Hinglish, Tamil, Telugu)."""
        pass
