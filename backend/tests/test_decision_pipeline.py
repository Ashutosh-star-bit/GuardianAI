"""
GuardianAI Master Decision Engine Pipeline Integration Unit Test Suite
Purpose: Tests end-to-end 8-step decision evaluation pipeline execution across multi-modal intelligence inputs.
"""

import pytest
from app.decision_engine import DecisionPipeline, DecisionRequest, DecisionResult

@pytest.mark.asyncio
async def test_end_to_end_decision_pipeline_execution():
    """Tests 8-step decision evaluation pipeline for a smishing threat payload."""
    req = DecisionRequest(
        scan_id="scn_dec_pipe_100",
        raw_text="URGENT: Your PayPal account is suspended! Update at http://paypa1-check.top",
        channel_type="SMS",
        text_intelligence={"scam_category_hint": "BANK_SPOOF"},
        threat_intelligence={
            "scoring_result": {"technical_risk_score": 85, "confidence": 0.95},
            "evidence_report": {
                "evidence_list": [
                    {
                        "evidence_id": "ev_1",
                        "indicator": "paypa1-check.top",
                        "category": "DOMAIN",
                        "reason": "Typosquatting link mimicking PayPal",
                        "severity": "Critical",
                        "confidence": 0.98,
                        "source": "DOMAIN_INTELLIGENCE"
                    }
                ]
            }
        },
        gemini_analysis={
            "threat_score": 90,
            "confidence": 0.95,
            "psychological_factors": {"urgency": {"detected": True}, "impersonation": {"detected": True}}
        }
    )

    res: DecisionResult = await DecisionPipeline.evaluate_decision(req, target_persona="SENIOR_CITIZENS", locale="en")

    assert res.scan_id == "scn_dec_pipe_100"
    assert res.final_scam_probability == 90
    assert res.risk_level == "CRITICAL"
    assert res.confidence >= 0.90
    assert len(res.evidence) > 0
    assert len(res.action_plan) > 0
    assert "official banking app" in res.safe_reply
