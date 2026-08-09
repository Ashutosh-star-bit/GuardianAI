"""
GuardianAI ScamAnalysisPipeline Master Orchestrator Unit Test Suite
Purpose: Tests complete 10-stage Master Pipeline execution (Validate -> Preprocess -> Extract -> Threat Intel -> Text Intel -> Decision -> XAI -> Report -> Latency -> Result).
"""

import pytest
from app.pipeline import ScamAnalysisPipeline, ScamAnalysisPipelineResult

@pytest.mark.asyncio
async def test_end_to_end_master_scam_analysis_pipeline():
    """Tests 10-stage end-to-end Master Scam Analysis Pipeline for a smishing threat message."""
    raw_payload = "URGENT: Your PayPal account is suspended. Verify at http://paypa1-check.top or send $500 to support.refund@okaxis"

    result: ScamAnalysisPipelineResult = await ScamAnalysisPipeline.execute_full_scam_analysis(
        raw_input=raw_payload,
        format_type="TEXT",
        target_persona="SENIOR_CITIZENS",
        locale="en"
    )

    assert result.request_id.startswith("req_")
    assert result.scan_id.startswith("scn_")
    assert result.input_format == "TEXT"
    assert result.target_persona == "SENIOR_CITIZENS"
    assert result.execution_time_ms > 0
    assert result.decision.final_scam_probability >= 50
    assert result.decision.risk_level in ["HIGH", "CRITICAL"]
    assert result.executive_report.risk_score >= 50
    assert len(result.decision.evidence) > 0
    assert len(result.decision.action_plan) > 0
