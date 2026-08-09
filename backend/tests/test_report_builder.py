"""
GuardianAI Executive Report Builder Unit Test Suite
Purpose: Tests synthesis of ExecutiveReportObject and rendering of Markdown reports.
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
from app.decision_engine.report_builder import ExecutiveReportBuilderEngine, ExecutiveReportObject

def test_build_executive_report_and_markdown_export():
    """Tests building an ExecutiveReportObject and exporting to Markdown."""
    dec_result = DecisionResult(
        scan_id="scn_rpt_test_100",
        final_scam_probability=94,
        confidence=0.98,
        risk_level="CRITICAL",
        risk_metrics=RiskMetricsSchema(final_scam_probability=94, risk_level="CRITICAL", technical_risk_score=85, psychological_risk_score=95),
        confidence_metrics=ConfidenceMetricsSchema(overall_confidence=0.98, cross_modal_agreement=0.95, certainty_band="VERY_HIGH"),
        reasons=["Spoofed domain paypa1-check.top mimicking PayPal"],
        evidence=[
            EvidenceItemSchema(
                evidence_id="ev_1",
                indicator="paypa1-check.top",
                category="DOMAIN",
                reason="Typosquatting domain link mimicking PayPal",
                severity="Critical",
                confidence=0.98,
                source="DOMAIN_INTELLIGENCE"
            )
        ],
        recommendations=["Do NOT click any web links."],
        safe_reply="I have logged and reported this unauthorized communication.",
        action_plan=[
            ActionPlanSchema(step_number=1, title="Block Sender", instruction="Block sender phone number immediately.", urgency="IMMEDIATE")
        ],
        explainability=DecisionXAISummary(summary="Critical danger smishing attempt.", detected_factors=["URGENCY"], key_threat_vectors=["TYPOSQUATTING"])
    )

    report: ExecutiveReportObject = ExecutiveReportBuilderEngine.build_executive_report(dec_result)

    assert report.report_id == "rpt_exec_rpt_test_100"
    assert report.risk_score == 94
    assert report.risk_level == "CRITICAL"
    assert "EXECUTIVE SUMMARY: High-risk threat attempt" in report.executive_summary
    assert len(report.next_steps) == 1

    # Test Markdown Export
    md_output = ExecutiveReportBuilderEngine.export_markdown_report(report)
    assert "# GuardianAI Executive Threat Analysis Report" in md_output
    assert "## 1. Executive Summary" in md_output
    assert "paypa1-check.top" in md_output
    assert "Block Sender" in md_output
