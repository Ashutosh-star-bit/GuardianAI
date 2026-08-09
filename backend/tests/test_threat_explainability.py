"""
GuardianAI Threat Explainability Engine Unit Test Suite
Purpose: Tests generation of 4-part XAI explanations (Why suspicious, How detected, False positive, Suggested action).
"""

import pytest
from app.threat_intel.explainability import ThreatExplainabilityEngine, ThreatIndicatorXAIRecord, ThreatIntelXAISummary

def test_explain_typosquatting_indicator():
    """Tests 4-part XAI explanation generation for TYPOSQUATTING indicator."""
    record: ThreatIndicatorXAIRecord = ThreatExplainabilityEngine.explain_indicator("TYPOSQUATTING_MISSPELLED_BRAND_PAYPAL")

    assert record.indicator_key == "TYPOSQUATTING_MISSPELLED_BRAND_PAYPAL"
    assert "mimics a well-known brand" in record.suspicious_reason
    assert "Levenshtein edit distance" in record.detection_method
    assert "false_positive" in str(record.false_positive_possibility).lower() or len(record.false_positive_possibility) > 5
    assert "Do NOT enter passwords" in record.suggested_action

def test_generate_complete_xai_summary():
    """Tests bundling multiple indicator XAI records into ThreatIntelXAISummary."""
    keys = ["UNENCRYPTED_HTTP_PROTOCOL", "DISPLAY_NAME_EXECUTIVE_SPOOFING_CEO"]
    summary: ThreatIntelXAISummary = ThreatExplainabilityEngine.generate_xai_summary("scn_xai_100", keys)

    assert summary.scan_id == "scn_xai_100"
    assert "Multiple high-risk indicators detected" in summary.overall_summary
    assert len(summary.explained_indicators) == 2
    assert summary.explained_indicators[0].indicator_key == "UNENCRYPTED_HTTP_PROTOCOL"
