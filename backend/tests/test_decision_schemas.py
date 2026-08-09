"""
GuardianAI Master Decision Engine Schemas Unit Test Suite
Purpose: Tests validation of DecisionRequest, DecisionResult, and nested DTO schemas with future scalability extra key ignoring.
"""

import pytest
from app.decision_engine.schemas import (
    DecisionRequest,
    DecisionResult,
    RiskMetricsSchema,
    ConfidenceMetricsSchema,
    EvidenceItemSchema,
    ActionPlanSchema,
    DecisionXAISummary
)

def test_decision_request_and_result_validation():
    """Tests parsing complete DecisionRequest and DecisionResult payloads."""
    req = DecisionRequest(
        scan_id="scn_dec_999",
        raw_text="URGENT: Verify at http://paypa1-check.top",
        channel_type="SMS"
    )
    assert req.scan_id == "scn_dec_999"

    res_data = {
        "scan_id": "scn_dec_999",
        "final_scam_probability": 92,
        "confidence": 0.95,
        "risk_level": "DANGEROUS",
        "risk_metrics": {
            "final_scam_probability": 92,
            "risk_level": "DANGEROUS",
            "technical_risk_score": 85,
            "psychological_risk_score": 90
        },
        "confidence_metrics": {
            "overall_confidence": 0.95,
            "cross_modal_agreement": 0.92,
            "certainty_band": "VERY_HIGH"
        },
        "reasons": ["Spoofed domain paypa1-check.top mimicking PayPal"],
        "evidence": [
            {
                "evidence_id": "ev_1",
                "indicator": "paypa1-check.top",
                "category": "DOMAIN",
                "reason": "Typosquatting link",
                "severity": "Critical",
                "confidence": 0.98,
                "source": "DOMAIN_INTELLIGENCE"
            }
        ],
        "recommendations": ["Do NOT click the link."],
        "safe_reply": "I have reported this unauthorized message.",
        "action_plan": [
            {
                "step_number": 1,
                "title": "Block Sender",
                "instruction": "Block phone number immediately.",
                "urgency": "IMMEDIATE"
            }
        ],
        "explainability": {
            "summary": "High risk smishing attempt.",
            "detected_factors": ["URGENCY", "IMPERSONATION"],
            "key_threat_vectors": ["TYPOSQUATTING"]
        }
    }

    res = DecisionResult.model_validate(res_data)
    assert res.final_scam_probability == 92
    assert res.risk_level == "DANGEROUS"
    assert res.confidence == 0.95
    assert len(res.evidence) == 1
    assert res.action_plan[0].title == "Block Sender"

def test_decision_schemas_future_scalability():
    """Tests future scalability where extra unexpected fields are safely ignored."""
    res_data = {
        "scan_id": "scn_dec_future",
        "final_scam_probability": 10,
        "confidence": 0.99,
        "risk_level": "SAFE",
        "risk_metrics": {"final_scam_probability": 10, "risk_level": "SAFE", "technical_risk_score": 0, "psychological_risk_score": 0},
        "confidence_metrics": {"overall_confidence": 0.99, "cross_modal_agreement": 1.0, "certainty_band": "VERY_HIGH"},
        "reasons": ["Safe conversation."],
        "explainability": {"summary": "Safe payload."},
        "future_v3_quantum_flag": "ENABLED_EXTRA_KEY" # Extra key from future version
    }

    res = DecisionResult.model_validate(res_data)
    assert res.scan_id == "scn_dec_future"
    assert not hasattr(res, "future_v3_quantum_flag") # Extra key safely ignored
