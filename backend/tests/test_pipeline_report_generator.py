"""
GuardianAI Pipeline ReportGenerator Unit Test Suite
Purpose: Tests synthesis of FullSecurityAnalysisReport and rendering of PDF-compatible Markdown text.
"""

import pytest
from app.decision_engine.schemas import (
    DecisionResult,
    RiskMetricsSchema,
    ConfidenceMetricsSchema,
    EvidenceItemSchema,
    ActionPlanSchema,
    DecisionXAISummary
)
from app.pipeline.report_generator import ReportGenerator, FullSecurityAnalysisReport

def test_generate_full_security_analysis_report():
    """Tests generating 8-section FullSecurityAnalysisReport and PDF Markdown export."""
    dec = DecisionResult(
        scan_id="scn_pdf_100",
        final_scam_probability=92,
        confidence=0.98,
        risk_level="CRITICAL",
        risk_metrics=RiskMetricsSchema(final_scam_probability=92, risk_level="CRITICAL", technical_risk_score=85, psychological_risk_score=90),
        confidence_metrics=ConfidenceMetricsSchema(overall_confidence=0.98, cross_modal_agreement=0.95, certainty_band="VERY_HIGH"),
        reasons=["Spoofed domain paypa1-check.top mimicking PayPal"],
        evidence=[
            EvidenceItemSchema(evidence_id="ev_1", indicator="paypa1-check.top", category="DOMAIN", reason="Typosquatting link", severity="Critical", confidence=0.98, source="DOMAIN_INTELLIGENCE")
        ],
        recommendations=["Do NOT click any web links."],
        safe_reply="I have logged and reported this unauthorized communication.",
        action_plan=[ActionPlanSchema(step_number=1, title="Block Sender", instruction="Block phone number immediately.", urgency="IMMEDIATE")],
        explainability=DecisionXAISummary(summary="Critical danger smishing attempt.", detected_factors=["URGENCY"], key_threat_vectors=["TYPOSQUATTING"])
    )

    report: FullSecurityAnalysisReport = ReportGenerator.generate_full_report(dec)

    assert report.report_id == "rpt_sec_pdf_100"
    assert report.risk_score == 92
    assert report.risk_level == "CRITICAL"
    assert len(report.educational_notes) >= 3

    # Test PDF Markdown Export
    md_output = ReportGenerator.export_pdf_markdown(report)
    assert "# GuardianAI Comprehensive Security Threat Report" in md_output
    assert "## 7. Educational Security Notes" in md_output
    assert "paypa1-check.top" in md_output
