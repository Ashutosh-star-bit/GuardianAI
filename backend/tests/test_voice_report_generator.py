"""
GuardianAI VoiceReportGenerator Pytest Suite
"""

import pytest
from app.voice_intel.report_generator import VoiceReportGenerator, VoiceScamReport
from app.voice_intel.schemas import VoiceAnalysisResult, STTResult, SpeakerMetadataResult

@pytest.fixture
def mock_voice_result():
    return VoiceAnalysisResult(
        scan_id="scn_test_100",
        audio_id="aud_test_100",
        duration_seconds=15.0,
        detected_language="en",
        stt_result=STTResult(
            raw_transcript="uh hello sir this is CBI officer calling. pay 50000 rupees.",
            cleaned_transcript="Hello sir this is CBI officer calling. Pay 50000 rupees.",
            detected_language="en",
            language_confidence=0.98,
            words=[],
            overall_confidence=0.95
        ),
        speaker_metadata=SpeakerMetadataResult(speaker_count=2, contains_urgency=True),
        preprocessed_duration_seconds=12.0,
        processing_time_ms=125.0
    )

def test_generate_voice_report(mock_voice_result):
    report = VoiceReportGenerator.generate_report(
        voice_result=mock_voice_result,
        pipeline_decision={"risk_level": "DANGEROUS", "final_scam_probability": 95, "confidence": 0.98},
        target_persona="SENIOR_CITIZENS"
    )

    assert isinstance(report, VoiceScamReport)
    assert report.scan_id == "scn_test_100"
    assert report.risk_level == "DANGEROUS"
    assert report.scam_probability == 95
    assert len(report.detected_indicators) > 0
    assert len(report.recommendations) > 0
    assert len(report.safe_reply_suggestions) > 0
    assert len(report.educational_notes) > 0

def test_voice_report_to_markdown(mock_voice_result):
    report = VoiceReportGenerator.generate_report(mock_voice_result)
    md = report.to_markdown()

    assert "# 🛡️ GuardianAI Voice Scam Analysis Report" in md
    assert "DANGEROUS" in md
    assert "Cleaned Speech Transcript" in md
    assert "Recommended Safety Actions" in md
