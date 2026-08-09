"""
GuardianAI Text Intelligence Pipeline Integration Unit Test Suite
Purpose: Tests end-to-end 8-step pipeline execution (Preprocess -> Extract -> Render Prompt -> Gemini -> Auto-Repair -> Parse -> Telemetry).
"""

import pytest
from app.nlp.pipeline import TextIntelligencePipeline, TextIntelligencePipelineResult

@pytest.mark.asyncio
async def test_end_to_end_text_intelligence_pipeline():
    """Tests 8-step end-to-end text intelligence pipeline execution."""
    pipeline = TextIntelligencePipeline()
    raw_payload = "URGENT: Your PayPal account is suspended! Update now at http://paypa1-check.com"

    result: TextIntelligencePipelineResult = await pipeline.execute_pipeline(
        scan_id="scn_pipe_999",
        raw_text=raw_payload,
        channel_type="SMS"
    )

    assert result.scan_id == "scn_pipe_999"
    assert result.channel_type == "SMS"
    assert result.analysis.threat_score > 0
    assert result.analysis.risk_band in ["safe", "caution", "dangerous"]
    assert result.analysis.psychological_techniques.urgency.detected is True
    assert result.telemetry.total_tokens > 0
    assert result.telemetry.latency_ms > 0
