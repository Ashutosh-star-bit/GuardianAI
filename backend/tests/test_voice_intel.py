"""
GuardianAI Voice Intelligence Master Pytest Test Suite
"""

import pytest
from app.voice_intel.schemas import AudioPayload
from app.voice_intel.orchestrator import VoiceProcessor
from app.voice_intel.pipeline_adapter import VoicePipelineAdapter
from app.voice_intel.exceptions import AudioPreprocessingError

@pytest.fixture
def sample_wav_bytes():
    return b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x80\x3e\x00\x00\x00\x7d\x00\x00\x02\x00\x10\x00data\x00\x00\x00\x00"

def test_voice_processor_pipeline(sample_wav_bytes):
    processor = VoiceProcessor()
    payload = AudioPayload(raw_bytes=sample_wav_bytes, filename="test_fraud_call.wav")

    result = processor.process_audio(payload)

    assert result.audio_id.startswith("aud_")
    assert result.stt_result.cleaned_transcript != ""
    assert "CBI" in result.stt_result.cleaned_transcript or "Aadhaar" in result.stt_result.cleaned_transcript
    assert result.speaker_metadata.total_speakers == 2
    assert result.speaker_metadata.urgency_level in ["HIGH_URGENCY", "ELEVATED", "NORMAL"]
    assert result.processing_time_ms >= 0.0

def test_voice_pipeline_adapter(sample_wav_bytes):
    adapter = VoicePipelineAdapter()
    req = adapter.process_and_adapt(
        raw_bytes=sample_wav_bytes,
        filename="scam_recording.wav"
    )

    assert req.input_type == "VOICE"
    assert req.raw_content != ""
    assert req.metadata.extra_attributes["duration_seconds"] > 0
    assert "urgency_level" in req.metadata.extra_attributes

def test_voice_processor_empty_bytes():
    processor = VoiceProcessor()
    payload = AudioPayload(raw_bytes=b"")

    with pytest.raises(AudioPreprocessingError):
        processor.process_audio(payload)
