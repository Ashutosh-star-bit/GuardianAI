"""
GuardianAI Action Plan & Recommendation Engine Unit Test Suite
Purpose: Tests generation of Immediate Actions, Things NOT to Do, Reporting Suggestions, Safety Advice, and Safe Decline Replies.
"""

import pytest
from app.decision_engine.action_planner import RecommendationEngine, GeneratedRecommendationReport

def test_generate_critical_bank_scam_recommendations():
    """Tests critical bank scam recommendations generation."""
    report: GeneratedRecommendationReport = RecommendationEngine.generate_recommendations(
        scan_id="scn_rec_100",
        risk_level="CRITICAL",
        scam_category="BANK_SPOOF",
        detected_threat_keys=["TYPOSQUATTING", "UPI_SPOOFING"]
    )

    assert report.scan_id == "scn_rec_100"
    assert report.risk_level == "CRITICAL"
    assert len(report.immediate_actions) >= 2
    assert report.immediate_actions[0].title == "Block Sender Immediately"
    assert "Do NOT click any web links" in report.things_not_to_do[0]
    assert "Do NOT enter your UPI PIN" in str(report.things_not_to_do)
    assert "Report smishing" in report.reporting_suggestions[0]
    assert "I have logged and reported" in report.safe_decline_reply

def test_generate_safe_recommendations():
    """Tests safe level recommendations generation."""
    report = RecommendationEngine.generate_recommendations(
        scan_id="scn_rec_safe",
        risk_level="SAFE",
        scam_category="GENERIC"
    )

    assert report.risk_level == "SAFE"
    assert len(report.immediate_actions) == 1
    assert report.immediate_actions[0].title == "Standard Vigilance"
    assert "Thank you for the message" in report.safe_decline_reply
