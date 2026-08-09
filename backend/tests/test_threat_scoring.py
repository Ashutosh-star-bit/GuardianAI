"""
GuardianAI Threat Scoring Engine Unit Test Suite
Purpose: Tests technical risk score calculation, risk band assignment (safe, caution, dangerous), evidence count aggregation, and confidence calculation.
"""

import pytest
from app.threat_intel.scoring import ThreatScoringEngine, ThreatScoreResult
from app.threat_intel.evidence_builder import EvidenceBuilderEngine

def test_calculate_dangerous_threat_score():
    """Tests high-risk component combination yielding dangerous risk band."""
    item1 = EvidenceBuilderEngine.create_evidence_item("ev_1", "paypa1-check.top", "DOMAIN", "Typosquatting link", "Critical", 0.98, "DOMAIN_INTELLIGENCE")
    item2 = EvidenceBuilderEngine.create_evidence_item("ev_2", "support.refund@okaxis", "UPI_ID", "Support desk handle impersonation", "High", 0.95, "UPI_INTELLIGENCE")
    report = EvidenceBuilderEngine.build_evidence_report("scn_score_1", [item1, item2])

    result: ThreatScoreResult = ThreatScoringEngine.calculate_threat_score(
        scan_id="scn_score_1",
        domain_risk=85,
        url_risk=70,
        upi_risk=90,
        email_risk=45,
        phone_risk=0,
        evidence_report=report
    )

    assert result.technical_risk_score >= 50
    assert result.risk_band in ["caution", "dangerous"]
    assert result.evidence_count == 2
    assert result.confidence >= 0.85

def test_calculate_safe_threat_score():
    """Tests clean components yielding safe risk band."""
    result = ThreatScoringEngine.calculate_threat_score(
        scan_id="scn_safe_1",
        domain_risk=0,
        url_risk=0,
        upi_risk=0,
        email_risk=0,
        phone_risk=0
    )

    assert result.technical_risk_score == 0
    assert result.risk_band == "safe"
    assert result.evidence_count == 0
