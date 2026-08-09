"""
GuardianAI Pipeline ReportGenerator Engine
Purpose: Synthesizes complete 8-section Security Analysis Reports (Executive Summary, Risk Level, Confidence,
         Evidence List, Threat Indicators, Recommendations, Safe Reply, Educational Notes) with PDF Markdown Export rendering.
"""

from datetime import datetime, timezone
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from app.decision_engine.schemas import DecisionResult, EvidenceItemSchema, ActionPlanSchema

class FullSecurityAnalysisReport(BaseModel):
    """Structured Full Security Analysis Report Object DTO."""
    report_id: str
    scan_id: str
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    executive_summary: str
    risk_score: int = Field(ge=0, le=100)
    risk_level: str
    confidence: float
    certainty_band: str
    threat_indicators: List[str]
    evidence_list: List[EvidenceItemSchema]
    recommendations: List[str]
    safe_reply: Optional[str] = None
    next_steps: List[ActionPlanSchema]
    educational_notes: List[str]

class ReportGenerator:
    """Enterprise Pipeline Security Report Generator Engine."""

    @classmethod
    def generate_full_report(cls, decision_result: DecisionResult) -> FullSecurityAnalysisReport:
        """
        Synthesizes a DecisionResult DTO into a complete 8-section FullSecurityAnalysisReport DTO.
        """
        report_id = f"rpt_sec_{decision_result.scan_id.replace('scn_', '')}"
        r_level = decision_result.risk_level.upper()
        prob = decision_result.final_scam_probability

        # 1. Executive Summary
        if r_level in ("CRITICAL", "HIGH"):
            exec_summary = (
                f"EXECUTIVE SUMMARY: Critical scam threat identified with a Scam Probability of {prob}/100 ({r_level} RISK). "
                f"The message uses fake urgency and spoofed brand links to trick users into revealing credentials or sending funds."
            )
        elif r_level == "MEDIUM":
            exec_summary = (
                f"EXECUTIVE SUMMARY: Moderate threat level evaluated with a Scam Probability of {prob}/100 ({r_level} RISK). "
                f"Unverified links or unusual formatting were detected requiring user caution."
            )
        else:
            exec_summary = (
                f"EXECUTIVE SUMMARY: Safe message verified with a Scam Probability of {prob}/100 ({r_level} RISK). "
                f"No malicious IOC indicators or fake urgency markers were found."
            )

        # 8. Educational Notes
        educational_notes = [
            "Scammers commonly use artificial urgency ('Account Suspended in 24 Hours') to induce panic.",
            "Legitimate organizations will NEVER ask for One-Time Passwords (OTP), PINs, or wire transfers via text message.",
            "Always inspect links character-by-character (e.g., paypa1-check.com is NOT paypal.com)."
        ]

        return FullSecurityAnalysisReport(
            report_id=report_id,
            scan_id=decision_result.scan_id,
            generated_at=datetime.now(timezone.utc).isoformat(),
            executive_summary=exec_summary,
            risk_score=prob,
            risk_level=decision_result.risk_level,
            confidence=decision_result.confidence,
            certainty_band=decision_result.confidence_metrics.certainty_band,
            threat_indicators=decision_result.reasons,
            evidence_list=decision_result.evidence,
            recommendations=decision_result.recommendations,
            safe_reply=decision_result.safe_reply,
            next_steps=decision_result.action_plan,
            educational_notes=educational_notes
        )

    @classmethod
    def export_pdf_markdown(cls, report: FullSecurityAnalysisReport) -> str:
        """
        Renders FullSecurityAnalysisReport into clean GitHub-flavored Markdown formatted text ready for PDF byte generation.
        """
        lines = [
            f"# GuardianAI Comprehensive Security Threat Report",
            f"**Report ID:** `{report.report_id}` | **Scan ID:** `{report.scan_id}`  ",
            f"**Date:** {report.generated_at}  ",
            f"**Threat Assessment:** `{report.risk_level}` ({report.risk_score}/100 Risk Score)  ",
            f"**Confidence Rating:** {report.confidence} ({report.certainty_band})  ",
            "---",
            "## 1. Executive Summary",
            report.executive_summary,
            "",
            "## 2. Technical Threat Indicators",
        ]
        for ind in report.threat_indicators:
            lines.append(f"- {ind}")

        lines.extend(["", "## 3. Evidence List"])
        for ev in report.evidence_list:
            lines.append(f"- **[{ev.severity.upper()}] {ev.category}:** `{ev.indicator}` — {ev.reason}")

        lines.extend(["", "## 4. Next Steps & Action Plan"])
        for step in report.next_steps:
            lines.append(f"1. **{step.title}** ({step.urgency}): {step.instruction}")

        lines.extend(["", "## 5. Security Recommendations"])
        for rec in report.recommendations:
            lines.append(f"- {rec}")

        if report.safe_reply:
            lines.extend(["", "## 6. Recommended Safe Decline Reply", f"> {report.safe_reply}"])

        lines.extend(["", "## 7. Educational Security Notes"])
        for note in report.educational_notes:
            lines.append(f"- {note}")

        return "\n".join(lines)
