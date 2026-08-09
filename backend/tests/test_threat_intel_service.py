"""
GuardianAI ThreatIntelligenceService Master Pipeline Unit Test Suite
Purpose: Tests end-to-end execution of ThreatIntelligenceService across URLs, Domains, Emails, Phones, UPI IDs, Evidence, Scoring, and XAI.
"""

import pytest
from app.threat_intel import ThreatIntelligenceService, ThreatIntelligencePipelineResult

@pytest.mark.asyncio
async def test_end_to_end_threat_intelligence_service():
    """Tests master pipeline execution for a composite smishing payload."""
    payload = (
        "URGENT: Your PayPal account is suspended. Update at http://paypa1-check.top "
        "or send $500 to support.refund@okaxis or call +1-800-555-0199 "
        "or email support@paypal.com"
    )

    result: ThreatIntelligencePipelineResult = await ThreatIntelligenceService.analyze_threat_payload(
        scan_id="scn_ti_master_100",
        raw_text=payload
    )

    assert result.scan_id == "scn_ti_master_100"
    assert len(result.url_reports) > 0
    assert len(result.domain_reports) > 0
    assert len(result.email_reports) > 0
    assert len(result.phone_reports) > 0
    assert len(result.upi_reports) > 0
    assert result.evidence_report.total_evidence_count > 0
    assert result.scoring_result.technical_risk_score >= 50
    assert len(result.xai_summary.explained_indicators) > 0
