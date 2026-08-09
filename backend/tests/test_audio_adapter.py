"""
GuardianAI AudioAdapter Master Pytest Suite
"""

import pytest
from app.adapters.audio_adapter import AudioAdapter, AudioAdapterError
from app.adapters.factory import InputAdapterFactory

@pytest.fixture
def sample_wav_bytes():
    return b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x80\x3e\x00\x00\x00\x7d\x00\x00\x02\x00\x10\x00data\x00\x00\x00\x00"

@pytest.fixture
def sample_mp3_bytes():
    return b"ID3\x04\x00\x00\x00\x00\x00\x00\xff\xfb\x90\x44\x00"

def test_audio_adapter_wav(sample_wav_bytes):
    adapter = AudioAdapter()
    req = adapter.adapt(sample_wav_bytes, filename="police_scam.wav")

    assert req.input_type == "VOICE"
    assert req.metadata.original_format == "VOICE"
    assert req.metadata.mime_type == "audio/wav"
    assert req.metadata.file_size_bytes == len(sample_wav_bytes)
    assert req.metadata.extra_attributes["duration_seconds"] > 0

def test_audio_adapter_mp3(sample_mp3_bytes):
    adapter = AudioAdapter()
    req = adapter.adapt(sample_mp3_bytes, filename="fraud_call.mp3")

    assert req.input_type == "VOICE"
    assert req.metadata.mime_type == "audio/mpeg"

def test_audio_adapter_empty_bytes():
    adapter = AudioAdapter()
    with pytest.raises(AudioAdapterError):
        adapter.adapt(b"")

def test_audio_adapter_oversized_file():
    adapter = AudioAdapter()
    large_bytes = b"RIFF" + b"A" * (26 * 1024 * 1024)

    with pytest.raises(AudioAdapterError):
        adapter.adapt(large_bytes)

def test_audio_adapter_unsupported_extension(sample_wav_bytes):
    adapter = AudioAdapter()
    with pytest.raises(AudioAdapterError):
        adapter.adapt(sample_wav_bytes, filename="virus.exe")

def test_input_adapter_factory_sniff_audio(sample_wav_bytes):
    adapter = InputAdapterFactory.sniff_and_get_adapter(sample_wav_bytes)
    assert isinstance(adapter, AudioAdapter)
