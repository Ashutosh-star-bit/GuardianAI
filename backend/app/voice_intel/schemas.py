"""
GuardianAI Voice Intelligence DTO Schemas
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class AudioPayload(BaseModel):
    raw_bytes: bytes
    filename: Optional[str] = None
    sample_rate: int = 16000
    channels: int = 1
    duration_seconds: float = 0.0
    format_type: str = "WAV" # WAV, MP3, M4A, OGG, FLAC

class PreprocessedAudio(BaseModel):
    clean_pcm_bytes: bytes
    sample_rate: int = 16000
    channels: int = 1
    duration_seconds: float
    speech_segments_count: int
    noise_reduction_applied: bool = True

class WordTimestamp(BaseModel):
    word: str
    start_time: float
    end_time: float
    confidence: float

class SpeakerTurn(BaseModel):
    speaker_id: str # e.g. SPEAKER_00 (Caller/Fraudster), SPEAKER_01 (Victim)
    start_time: float
    end_time: float
    transcript_segment: str
    urgency_score: float = 0.0

class STTResult(BaseModel):
    raw_transcript: str
    cleaned_transcript: str
    detected_language: str = "en"
    language_confidence: float = 0.95
    words: List[WordTimestamp] = Field(default_factory=list)
    overall_confidence: float = 0.90

class SpeakerMetadataResult(BaseModel):
    total_speakers: int = 2
    speaker_turns: List[SpeakerTurn] = Field(default_factory=list)
    speech_rate_wpm: float = 140.0
    urgency_level: str = "NORMAL" # NORMAL, ELEVATED, HIGH_URGENCY

class VoiceAnalysisResult(BaseModel):
    audio_id: str
    scan_id: Optional[str] = None
    duration_seconds: float
    stt_result: STTResult
    speaker_metadata: SpeakerMetadataResult
    detected_language: str
    is_streaming: bool = False
    processing_time_ms: float
