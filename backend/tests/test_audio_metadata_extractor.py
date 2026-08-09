"""
GuardianAI AudioMetadataExtractor Pytest Suite
"""

import pytest
from app.voice_intel.metadata_extractor import AudioMetadataExtractor, AudioMetadataInfo

@pytest.fixture
def sample_wav_bytes():
    return b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x80\x3e\x00\x00\x00\x7d\x00\x00\x02\x00\x10\x00data\x00\x00\x00\x00"

@pytest.fixture
def sample_mp3_bytes():
    return b"ID3\x04\x00\x00\x00\x00\x00\x00\xff\xfb\x90\x44\x00"

def test_extract_wav_metadata(sample_wav_bytes):
    meta = AudioMetadataExtractor.extract_metadata(sample_wav_bytes, filename="recording.wav")

    assert isinstance(meta, AudioMetadataInfo)
    assert meta.format_type == "WAV"
    assert meta.codec == "PCM_16"
    assert meta.sample_rate_hz == 16000
    assert meta.channels == 1
    assert meta.file_size_bytes == len(sample_wav_bytes)

def test_extract_mp3_metadata(sample_mp3_bytes):
    meta = AudioMetadataExtractor.extract_metadata(sample_mp3_bytes, filename="speech.mp3")

    assert meta.format_type == "MP3"
    assert meta.codec == "MPEG_LAYER_3"
    assert meta.bitrate_kbps == 192

def test_extract_empty_bytes():
    meta = AudioMetadataExtractor.extract_metadata(b"")
    assert meta.file_size_bytes == 0
    assert meta.duration_seconds == 0.0
