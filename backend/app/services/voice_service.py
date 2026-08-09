"""
GuardianAI Voice Intelligence Production Service
Purpose: Connects Voice Intelligence Subsystem to the Master Scam Analysis Pipeline:
         1. Upload Audio -> 2. Audio Preprocessing -> 3. STT Transcription ->
         4. Transcript Cleaning -> 5. Generate UniversalAnalysisRequest ->
         6. Threat Intelligence Scan -> 7. Decision Engine Scam Scoring ->
         8. Generate Structured Report -> 9. Persist History & Analytics Record.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from app.voice_intel.orchestrator import VoiceProcessor
from app.voice_intel.pipeline_adapter import VoicePipelineAdapter
from app.voice_intel.schemas import AudioPayload, VoiceAnalysisResult
from app.adapters.schemas import UniversalAnalysisRequest
from app.pipeline.orchestrator import ScamAnalysisPipeline, ScamAnalysisPipelineResult
from app.core.exceptions import BaseAppException

class VoiceServiceError(BaseAppException):
    """Raised when voice pipeline processing fails."""
    def __init__(self, message: str = "Voice pipeline execution failed.", details: Optional[list] = None):
        super().__init__(message=message, code="VOICE_SERVICE_ERROR", status_code=400, details=details)

class VoiceServiceResult(BaseModel):
    """Response DTO for Voice Intelligence Scam Analysis."""
    scan_id: str
    audio_id: str
    duration_seconds: float
    detected_language: str
    transcript: str
    pipeline_result: ScamAnalysisPipelineResult
    processing_time_ms: float

class VoiceService:
    """Enterprise Production Voice Intelligence Service."""

    def __init__(
        self,
        voice_processor: Optional[VoiceProcessor] = None,
        pipeline: Optional[ScamAnalysisPipeline] = None
    ):
        self.voice_processor = voice_processor or VoiceProcessor()
        self.pipeline = pipeline or ScamAnalysisPipeline()
        self.pipeline_adapter = VoicePipelineAdapter(self.voice_processor)

    async def analyze_audio(
        self,
        raw_bytes: bytes,
        filename: str = "recording.wav",
        target_persona: str = "SENIOR_CITIZENS",
        locale: str = "en",
        user_id: Optional[str] = None
    ) -> VoiceServiceResult:
        """
        Executes complete 9-stage voice scam analysis pipeline.
        """
        if not raw_bytes or len(raw_bytes) == 0:
            raise VoiceServiceError("Uploaded audio payload is empty (0 bytes).")

        # 1. Process Voice Intelligence Subsystem outputs
        audio_payload = AudioPayload(raw_bytes=raw_bytes, filename=filename)
        voice_res: VoiceAnalysisResult = self.voice_processor.process_audio(audio_payload)

        # 2. Execute Master Scam Analysis Pipeline via InputAdapterFactory
        pipeline_result: ScamAnalysisPipelineResult = await self.pipeline.execute_full_scam_analysis(
            raw_input=raw_bytes,
            format_type="AUDIO",
            user_id=user_id,
            target_persona=target_persona,
            locale=locale
        )

        return VoiceServiceResult(
            scan_id=pipeline_result.scan_id,
            audio_id=voice_res.audio_id,
            duration_seconds=voice_res.duration_seconds,
            detected_language=voice_res.detected_language,
            transcript=voice_res.stt_result.cleaned_transcript,
            pipeline_result=pipeline_result,
            processing_time_ms=pipeline_result.execution_time_ms
        )
