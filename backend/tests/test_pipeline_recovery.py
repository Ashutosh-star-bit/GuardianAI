"""
GuardianAI Pipeline Recovery Unit Test Suite
Purpose: Tests AI failure fallback, Threat Engine failure fallback, Database failure handling, and emergency decision creation.
"""

import pytest
from app.pipeline.recovery import PipelineErrorRecovery
from app.decision_engine.schemas import DecisionResult

def test_ai_failure_recovery_fallback():
    """Tests Gemini AI failure recovery fallback dictionary."""
    res = PipelineErrorRecovery.handle_ai_failure("URGENT: Verify account", Exception("Model Timeout 504"))
    assert res["fallback_active"] is True
    assert res["threat_score"] == 50
    assert "Gemini AI model execution unavailable" in res["fallback_reason"]

def test_threat_engine_failure_recovery_fallback():
    """Tests Threat Engine failure recovery fallback dictionary."""
    res = PipelineErrorRecovery.handle_threat_engine_failure("URGENT: Verify account", Exception("Database Connection Refused"))
    assert res["fallback_active"] is True
    assert res["scoring_result"]["technical_risk_score"] == 50
    assert "Threat Intelligence service unavailable" in res["fallback_reason"]

def test_emergency_fallback_decision_creation():
    """Tests emergency DecisionResult creation during critical failures."""
    dec: DecisionResult = PipelineErrorRecovery.create_emergency_fallback_decision("scn_rec_test")
    assert dec.scan_id == "scn_rec_test"
    assert dec.risk_level == "MEDIUM"
    assert dec.confidence == 0.50
    assert "Emergency Fallback" in dec.explainability.summary
