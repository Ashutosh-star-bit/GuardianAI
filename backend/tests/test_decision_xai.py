"""
GuardianAI Persona-Tailored Explainability (XAI) Engine Unit Test Suite
Purpose: Tests persona-tailored XAI explanations for Senior Citizens, Parents, Students, and Professionals.
"""

import pytest
from app.decision_engine.xai import DecisionXAIEngine, DecisionXAIExplanationReport

def test_generate_senior_citizens_xai_explanation():
    """Tests Senior Citizens non-jargon comforting XAI explanation."""
    report: DecisionXAIExplanationReport = DecisionXAIEngine.generate_full_xai_report(
        scan_id="scn_xai_senior",
        risk_level="CRITICAL",
        confidence=0.98,
        evidence_list=["paypa1-check.top typosquatting link"],
        target_persona="SENIOR_CITIZENS"
    )

    assert report.active_persona == "SENIOR_CITIZENS"
    primary = report.primary_explanation
    assert "CAUTION: This message looks like a scam attempt" in primary.risk_summary
    assert "PLEASE DO NOT CLICK ANY LINKS" in primary.recommended_action
    assert "98%" in primary.confidence_explanation

def test_generate_students_xai_explanation():
    """Tests Students concise modern terminology XAI explanation."""
    report = DecisionXAIEngine.generate_full_xai_report(
        scan_id="scn_xai_student",
        risk_level="HIGH",
        confidence=0.92,
        target_persona="STUDENTS"
    )

    primary = report.all_persona_explanations["STUDENTS"]
    assert "HEADS UP" in primary.risk_summary
    assert "Don't click the link or DM the sender" in primary.recommended_action

def test_generate_professionals_xai_explanation():
    """Tests Professionals formal BEC context XAI explanation."""
    report = DecisionXAIEngine.generate_full_xai_report(
        scan_id="scn_xai_prof",
        risk_level="HIGH",
        confidence=0.95,
        target_persona="PROFESSIONALS"
    )

    primary = report.all_persona_explanations["PROFESSIONALS"]
    assert "Business Email Compromise (BEC)" in primary.risk_summary
    assert "abuse@domain.com" in primary.recommended_action
