"""
GuardianAI Voice Pipeline Adapter
Purpose: Integrates Voice Intelligence into Master Scam Analysis Pipeline.
         Converts VoiceAnalysisResult into UniversalAnalysisRequest DTO.
"""

from typing import Dict, Any
from app.voice_intel.orchestrator import VoiceProcessor
from app.voice_intel.schemas import AudioPayload, VoiceAnalysisResult
from app.adapters.schemas import UniversalAnalysisRequest, AdapterMetadata

class VoicePipelineAdapter:
    """Production Adapter integrating Voice Intelligence into Scam Pipeline."""

    def __init__(self, voice_processor: VoiceProcessor = None):
        self.processor = voice_processor or VoiceProcessor()

    def process_and_adapt(
        self,
        raw_bytes: bytes,
        filename: str = "audio.wav",
        locale: str = "en"
    ) -> UniversalAnalysisRequest:
        payload = AudioPayload(
            raw_bytes=raw_bytes,
            filename=filename
        )

        res: VoiceAnalysisResult = self.processor.process_audio(payload)

        adapter_metadata = AdapterMetadata(
            original_format="VOICE",
            mime_type="audio/wav",
            file_size_bytes=len(raw_bytes),
            extra_attributes={
                "audio_id": res.audio_id,
                "duration_seconds": res.duration_seconds,
                "detected_language": res.detected_language,
                "speech_rate_wpm": res.speaker_metadata.speech_rate_wpm,
                "urgency_level": res.speaker_metadata.urgency_level,
                "speaker_turns": [turn.model_dump() for turn in res.speaker_metadata.speaker_turns]
            }
        )

        return UniversalAnalysisRequest(
            raw_content=res.stt_result.cleaned_transcript,
            input_type="VOICE",
            language=locale if locale in {"en", "hi"} else "en",
            metadata=adapter_metadata
        )
