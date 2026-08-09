"""
GuardianAI VoiceSecuritySanitizer Pytest Suite
"""

import pytest
from app.voice_intel.security import VoiceSecuritySanitizer, VoiceSecurityError

@pytest.fixture
def sample_wav_bytes():
    return b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x80\x3e\x00\x00\x00\x7d\x00\x00\x02\x00\x10\x00data\x00\x00\x00\x00"

def test_validate_audio_upload_success(sample_wav_bytes):
    fmt, mime = VoiceSecuritySanitizer.validate_audio_upload(sample_wav_bytes, filename="call.wav")
    assert fmt == "WAV"
    assert mime == "audio/wav"

def test_validate_audio_upload_oversized():
    large_bytes = b"RIFF" + (b"A" * (26 * 1024 * 1024))
    with pytest.raises(VoiceSecurityError):
        VoiceSecuritySanitizer.validate_audio_upload(large_bytes)

def test_validate_audio_upload_blocked_extension(sample_wav_bytes):
    with pytest.raises(VoiceSecurityError):
        VoiceSecuritySanitizer.validate_audio_upload(sample_wav_bytes, filename="malware.exe")

def test_validate_audio_upload_corrupted_header():
    with pytest.raises(VoiceSecurityError):
        VoiceSecuritySanitizer.validate_audio_upload(b"INVALID_HEADER_DATA_STREAM")

def test_sanitize_transcript_pii():
    raw_transcript = "My Aadhaar number is 2345 6789 0123 and my PAN card is ABCDE1234F. My OTP is 987654."
    cleaned = VoiceSecuritySanitizer.sanitize_transcript(raw_transcript)

    assert "2345 6789 0123" not in cleaned
    assert "[REDACTED_AADHAAR]" in cleaned
    assert "ABCDE1234F" not in cleaned
    assert "[REDACTED_PAN]" in cleaned
    assert "[REDACTED_OTP]" in cleaned

def test_shred_memory_buffer():
    buf = bytearray(b"SENSITIVE_AUDIO_STREAM")
    VoiceSecuritySanitizer.shred_memory_buffer(buf)
    assert all(b == 0 for b in buf)
