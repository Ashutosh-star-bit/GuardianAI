"""
GuardianAI DecisionService Unit Test Suite
Purpose: Tests high-level DecisionService process_full_decision_scan execution across Text Intelligence, Threat Intelligence, and Decision Pipeline.
"""

import pytest
from app.decision_engine import DecisionService, DecisionServiceReport

@pytest.mark.asyncio
async def test_process_full_decision_scan():
    """Tests high-level DecisionService process_full_decision_scan execution for smishing message."""
    raw_payload = "URGENT: Your PayPal account is suspended. Verify at http://paypa1-check.top or send $500 to support.refund@okaxis"

    report: DecisionServiceReport = await DecisionService.process_full_decision_scan(
        scan_id="scn_srv_test_100",
        raw_text=raw_payload,
        channel_type="SMS",
        target_persona="SENIOR_CITIZENS",
        locale="en"
    )

    assert report.scan_id == "scn_srv_test_100"
    assert report.channel_type == "SMS"
    assert report.target_persona == "SENIOR_CITIZENS"
    assert report.decision.final_scam_probability >= 50
    assert report.decision.risk_level in ["HIGH", "CRITICAL"]
    assert report.text_intelligence_summary is not None
    assert report.threat_intelligence_summary is not None
