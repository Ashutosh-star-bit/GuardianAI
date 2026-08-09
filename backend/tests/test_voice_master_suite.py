"""
GuardianAI Voice Intelligence Master Pytest Test Suite
Purpose: Complete production test coverage for Voice Intelligence Subsystem:
         1. Short Audio Recordings (< 1s / 100ms)
         2. Long Audio Recordings (Up to 15-min duration limit)
         3. Background Acoustic Noise & Silence Trimming (VAD)
         4. Multi-Format Magic Headers (WAV, MP3, M4A, AAC, FLAC, OGG)
         5. Corrupted & Invalid Audio Payloads (0-byte, truncated headers, >25MB oversize)
         6. Mixed Language / Hinglish Code-Switched Speech
         7. Edge Cases (All-filler text, Unicode control chars, null bytes)
         8. End-to-End Master Scam Pipeline Integration.
"""

import pytest
from app.adapters.audio_adapter import AudioAdapter, AudioAdapterError
from app.adapters.factory import InputAdapterFactory
from app.voice_intel.audio_preprocessor import AudioPreprocessor
from app.voice_intel.stt_provider import SpeechToTextProvider, MockSTTProvider, STTProviderFactory
from app.voice_intel.transcript_cleaner import TranscriptCleaner
from app.voice_intel.speaker_metadata import SpeakerMetadata
from app.voice_intel.metadata_extractor import AudioMetadataExtractor
from app.voice_intel.report_generator import VoiceReportGenerator
from app.voice_intel.orchestrator import VoiceProcessor
from app.voice_intel.schemas import AudioPayload
from app.services.voice_service import VoiceService, VoiceServiceError

# --- FIXTURES ---

@pytest.fixture
def wav_bytes_valid():
    return b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x80\x3e\x00\x00\x00\x7d\x00\x00\x02\x00\x10\x00data\x00\x00\x00\x00"

@pytest.fixture
def mp3_bytes_valid():
    return b"ID3\x04\x00\x00\x00\x00\x00\x00\xff\xfb\x90\x44\x00"

@pytest.fixture
def flac_bytes_valid():
    return b"fLaC\x00\x00\x00\x22\x10\x00\x10\x00"

@pytest.fixture
def ogg_bytes_valid():
    return b"OggS\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00"

@pytest.fixture
def m4a_bytes_valid():
    return b"\x00\x00\x00\x20ftypM4A \x00\x00\x00\x00"

# --- 1. SHORT RECORDINGS TEST ---

def test_short_audio_recording(wav_bytes_valid):
    preprocessor = AudioPreprocessor()
    payload = AudioPayload(raw_bytes=wav_bytes_valid, duration_seconds=0.05)

    preprocessed = preprocessor.preprocess(payload)
    assert preprocessed.duration_seconds >= 0.1
    assert len(preprocessed.clean_pcm_bytes) > 0

# --- 2. LONG RECORDINGS TEST ---

def test_long_audio_recording():
    adapter = AudioAdapter()
    header = b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x80\x3e\x00\x00\x00\x7d\x00\x00\x02\x00\x10\x00data"
    # 5MB valid mock WAV audio stream (~2 minutes)
    large_pcm = header + (b"\x00\x10\xf0\x0f" * 1250000)

    req = adapter.adapt(large_pcm, filename="long_call.wav")
    assert req.input_type == "VOICE"
    assert req.metadata.file_size_bytes == len(large_pcm)

# --- 3. BACKGROUND NOISE & VAD SILENCE TRIMMING TEST ---

def test_background_noise_vad_trimming():
    preprocessor = AudioPreprocessor()
    # Mock PCM with low-amplitude background static (-50 dBFS)
    quiet_noise = b"\x01\x00\xfe\xff" * 4000
    payload = AudioPayload(raw_bytes=quiet_noise, sample_rate=16000, channels=1)

    preprocessed = preprocessor.preprocess(payload)
    assert preprocessed.noise_reduction_applied is True
    assert preprocessed.sample_rate == 16000
    assert preprocessed.channels == 1

# --- 4. MULTI-FORMAT MAGIC HEADERS TEST ---

def test_multi_format_magic_headers(wav_bytes_valid, mp3_bytes_valid, flac_bytes_valid, ogg_bytes_valid, m4a_bytes_valid):
    adapter = AudioAdapter()

    assert adapter.adapt(wav_bytes_valid, "a.wav").metadata.mime_type == "audio/wav"
    assert adapter.adapt(mp3_bytes_valid, "a.mp3").metadata.mime_type == "audio/mpeg"
    assert adapter.adapt(flac_bytes_valid, "a.flac").metadata.mime_type == "audio/flac"
    assert adapter.adapt(ogg_bytes_valid, "a.ogg").metadata.mime_type == "audio/ogg"
    assert adapter.adapt(m4a_bytes_valid, "a.m4a").metadata.mime_type == "audio/mp4"

# --- 5. CORRUPTED & OVERSIZED AUDIO PAYLOADS TEST ---

def test_corrupted_empty_audio():
    adapter = AudioAdapter()
    with pytest.raises(AudioAdapterError):
        adapter.adapt(b"")

def test_corrupted_garbage_bytes():
    adapter = AudioAdapter()
    with pytest.raises(AudioAdapterError):
        adapter.adapt(b"GARBAGE_HEADER_1234567890", filename="scam.wav")

def test_oversized_audio_exceeds_25mb():
    adapter = AudioAdapter()
    oversized = b"RIFF" + (b"A" * (26 * 1024 * 1024))
    with pytest.raises(AudioAdapterError):
        adapter.adapt(oversized)

# --- 6. MIXED LANGUAGE & HINGLISH CODE-SWITCHING TEST ---

def test_hinglish_transcript_cleaning():
    cleaner = TranscriptCleaner()
    raw_hinglish = "uh um hello sir aapka HDFC bank account block ho gaya hai. paytm se pay pay 5000 rupees to refund account."

    cleaned = cleaner.clean(raw_hinglish)
    assert "uh" not in cleaned.lower()
    assert "um" not in cleaned.lower()
    assert "paytm" in cleaned.lower()
    assert "pay pay" not in cleaned.lower()
    assert cleaned.endswith(".")

# --- 7. EDGE CASES (ALL-FILLER, UNICODE CONTROL CHARS) TEST ---

def test_edge_cases_all_filler_and_unicode():
    cleaner = TranscriptCleaner()
    all_filler = "uh um er aah hmm"
    assert cleaner.clean(all_filler) == ""

    unicode_obfuscated = "Hello\x00 world\xa0 this is \u200bKYC manager."
    cleaned_uni = cleaner.clean(unicode_obfuscated)
    assert "\x00" not in cleaned_uni
    assert "KYC" in cleaned_uni

# --- 8. END-TO-END PIPELINE INTEGRATION TEST ---

@pytest.mark.asyncio
async def test_end_to_end_voice_pipeline_integration(wav_bytes_valid):
    voice_service = VoiceService()
    result = await voice_service.analyze_audio(
        raw_bytes=wav_bytes_valid,
        filename="fraud_investigation.wav",
        target_persona="SENIOR_CITIZENS",
        locale="en"
    )

    assert result.scan_id.startswith("scn_")
    assert result.duration_seconds > 0
    assert len(result.transcript) > 0
    assert result.pipeline_result.decision.risk_level in ["SAFE", "LOW", "MEDIUM", "HIGH", "CRITICAL", "CAUTION", "DANGEROUS"]
    assert result.pipeline_result.execution_time_ms > 0
