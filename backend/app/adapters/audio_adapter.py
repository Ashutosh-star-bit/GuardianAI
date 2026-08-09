"""
GuardianAI Production Audio Adapter Engine
Purpose: Validates, inspects binary magic headers, checks size/duration bounds,
         prevents corrupted/spoofed audio files, and converts raw audio payloads into
         UniversalAnalysisRequest DTO for ScamAnalysisPipeline consumption.
"""

import pathlib
from typing import Dict, Any, Tuple, Optional
from app.adapters.schemas import UniversalAnalysisRequest, AdapterMetadata
from app.voice_intel.orchestrator import VoiceProcessor
from app.voice_intel.schemas import AudioPayload, VoiceAnalysisResult
from app.core.exceptions import BaseAppException

class AudioAdapterError(BaseAppException):
    """Raised when audio validation or adaptation fails."""
    def __init__(self, message: str = "Audio payload validation failed.", details: Optional[list] = None):
        super().__init__(message=message, code="AUDIO_ADAPTER_ERROR", status_code=400, details=details)

class AudioAdapter:
    """Production Audio Input Adapter Engine."""

    MAX_FILE_SIZE_BYTES = 25 * 1024 * 1024  # 25 MB
    MAX_DURATION_SECONDS = 900.0             # 15 minutes

    # Whitelisted Audio Magic Signatures
    MAGIC_SIGNATURES = {
        "WAV": b"RIFF",
        "MP3_ID3": b"ID3",
        "MP3_SYNC": b"\xff\xfb",
        "FLAC": b"fLaC",
        "OGG": b"OggS",
        "M4A": b"ftyp"
    }

    ALLOWED_EXTENSIONS = {"wav", "mp3", "m4a", "aac", "flac", "ogg"}

    def __init__(self, voice_processor: Optional[VoiceProcessor] = None):
        self.voice_processor = voice_processor or VoiceProcessor()

    @classmethod
    def validate_audio_payload(cls, raw_bytes: bytes, filename: Optional[str] = None) -> Tuple[str, str]:
        """
        Validates audio binary payload for magic signatures, size bounds, and extension safety.
        Returns Tuple[detected_format, mime_type].
        """
        if not raw_bytes or len(raw_bytes) == 0:
            raise AudioAdapterError("Audio payload is empty (0 bytes).")

        if len(raw_bytes) > cls.MAX_FILE_SIZE_BYTES:
            raise AudioAdapterError(
                f"Audio file size ({len(raw_bytes)} bytes) exceeds maximum allowed limit of {cls.MAX_FILE_SIZE_BYTES} bytes."
            )

        # File Extension Check
        if filename:
            clean_name = pathlib.Path(filename).name
            ext = clean_name.split(".")[-1].lower() if "." in clean_name else ""
            if ext and ext not in cls.ALLOWED_EXTENSIONS:
                raise AudioAdapterError(f"Audio file extension '.{ext}' is not supported.")

        # Magic Header Inspection
        detected_format = None
        mime_type = "audio/wav"

        if raw_bytes.startswith(cls.MAGIC_SIGNATURES["WAV"]) and b"WAVE" in raw_bytes[:16]:
            detected_format = "WAV"
            mime_type = "audio/wav"
        elif raw_bytes.startswith(cls.MAGIC_SIGNATURES["MP3_ID3"]) or raw_bytes.startswith(cls.MAGIC_SIGNATURES["MP3_SYNC"]):
            detected_format = "MP3"
            mime_type = "audio/mpeg"
        elif raw_bytes.startswith(cls.MAGIC_SIGNATURES["FLAC"]):
            detected_format = "FLAC"
            mime_type = "audio/flac"
        elif raw_bytes.startswith(cls.MAGIC_SIGNATURES["OGG"]):
            detected_format = "OGG"
            mime_type = "audio/ogg"
        elif b"ftyp" in raw_bytes[:12]:
            detected_format = "M4A"
            mime_type = "audio/mp4"

        if not detected_format:
            raise AudioAdapterError("Unrecognized or corrupted audio header magic signature.")

        return detected_format, mime_type

    def adapt(
        self,
        raw_bytes: bytes,
        filename: Optional[str] = None,
        language: str = "en",
        locale: str = "en",
        **kwargs: Any
    ) -> UniversalAnalysisRequest:
        """
        Converts raw audio binary payload into UniversalAnalysisRequest DTO.
        """
        lang = language or locale or "en"
        detected_format, mime_type = self.validate_audio_payload(raw_bytes, filename)

        payload = AudioPayload(
            raw_bytes=raw_bytes,
            filename=filename or f"audio.{detected_format.lower()}",
            format_type=detected_format
        )

        voice_result: VoiceAnalysisResult = self.voice_processor.process_audio(payload)

        if voice_result.duration_seconds > self.MAX_DURATION_SECONDS:
            raise AudioAdapterError(
                f"Audio duration ({voice_result.duration_seconds:.1f}s) exceeds maximum allowed limit of {self.MAX_DURATION_SECONDS}s."
            )

        metadata = AdapterMetadata(
            original_format="VOICE",
            mime_type=mime_type,
            file_size_bytes=len(raw_bytes),
            language=lang,
            extra_attributes={
                "audio_id": voice_result.audio_id,
                "detected_format": detected_format,
                "duration_seconds": voice_result.duration_seconds,
                "speaker_count": voice_result.speaker_metadata.total_speakers,
                "urgency_level": voice_result.speaker_metadata.urgency_level,
                "detected_language": voice_result.detected_language,
                "stt_confidence": voice_result.stt_result.overall_confidence
            }
        )

        return UniversalAnalysisRequest(
            raw_content=voice_result.stt_result.cleaned_transcript,
            input_type="VOICE",
            metadata=metadata,
            language=lang
        )
