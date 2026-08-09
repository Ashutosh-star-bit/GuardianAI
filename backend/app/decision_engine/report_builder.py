"""
GuardianAI Executive Decision Report Builder Engine
Purpose: Synthesizes complete Executive Threat Reports containing Executive Summary, Risk Score, Confidence,
         Reasons, Evidence List, Recommendations, Safe Reply, Next Steps, and Future PDF Export Support.
"""

from datetime import datetime, timezone
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from app.decision_engine.schemas import DecisionResult, EvidenceItemSchema, ActionPlanSchema

class ExecutiveReportObject(BaseModel):
    """Structured Executive Decision Report Object DTO."""
    report_id: str
    scan_id: str
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    executive_summary: str
    risk_score: int = Field(ge=0, le=100)
    risk_level: str
    confidence: float
    certainty_band: str
    reasons: List[str]
    evidence: List[EvidenceItemSchema]
    recommendations: List[str]
    safe_reply: Optional[str] = None
    next_steps: List[ActionPlanSchema]

class ExecutiveReportBuilderEngine:
    """Enterprise Executive Decision Report Builder Engine."""

    @classmethod
    def build_executive_report(cls, decision_result: DecisionResult) -> ExecutiveReportObject:
        """
        Synthesizes a DecisionResult DTO into a structured ExecutiveReportObject.
        """
        report_id = f"rpt_exec_{decision_result.scan_id.replace('scn_', '')}"

        # Generate Executive Summary
        r_level = decision_result.risk_level.upper()
        prob = decision_result.final_scam_probability

        if r_level in ("CRITICAL", "HIGH"):
            exec_summary = (
                f"EXECUTIVE SUMMARY: High-risk threat attempt identified with a Scam Probability of {prob}/100 ({r_level} RISK). "
                f"The payload exhibits multiple severe phishing or smishing markers, including spoofed domain identities or coercive urgency."
            )
        elif r_level == "MEDIUM":
            exec_summary = (
                f"EXECUTIVE SUMMARY: Moderate risk detected with a Scam Probability of {prob}/100 ({r_level} RISK). "
                f"Caution is advised due to suspicious links or artificial time pressure."
            )
        else:
            exec_summary = (
                f"EXECUTIVE SUMMARY: Low/Safe threat level evaluated with a Scam Probability of {prob}/100 ({r_level} RISK). "
                f"No confirmed malicious IOCs or severe psychological coercion markers were detected."
            )

        return ExecutiveReportObject(
            report_id=report_id,
            scan_id=decision_result.scan_id,
            generated_at=datetime.now(timezone.utc).isoformat(),
            executive_summary=exec_summary,
            risk_score=decision_result.final_scam_probability,
            risk_level=decision_result.risk_level,
            confidence=decision_result.confidence,
            certainty_band=decision_result.confidence_metrics.certainty_band,
            reasons=decision_result.reasons,
            evidence=decision_result.evidence,
            recommendations=decision_result.recommendations,
            safe_reply=decision_result.safe_reply,
            next_steps=decision_result.action_plan
        )

    @classmethod
    def export_markdown_report(cls, report: ExecutiveReportObject) -> str:
        """
        Renders ExecutiveReportObject into clean GitHub-flavored Markdown text format suitable for rendering or PDF export.
        """
        md_lines = [
            f"# GuardianAI Executive Threat Analysis Report",
            f"**Report ID:** `{report.report_id}`  ",
            f"**Scan ID:** `{report.scan_id}`  ",
            f"**Generated Date:** {report.generated_at}  ",
            f"**Overall Risk Level:** `{report.risk_level}` ({report.risk_score}/100)  ",
            f"**Model Confidence:** {report.confidence} ({report.certainty_band})  ",
            "---",
            "## 1. Executive Summary",
            report.executive_summary,
            "",
            "## 2. Key Threat Reasons",
        ]
        for r in report.reasons:
            md_lines.append(f"- {r}")

        md_lines.extend(["", "## 3. Threat Evidence List"])
        for ev in report.evidence:
            md_lines.append(f"- **[{ev.severity.upper()}] {ev.category}:** `{ev.indicator}` — {ev.reason} (Source: {ev.source})")

        md_lines.extend(["", "## 4. Next Steps & Security Action Plan"])
        for step in report.next_steps:
            md_lines.append(f"1. **{step.title}** ({step.urgency}): {step.instruction}")

        if report.safe_reply:
            md_lines.extend(["", "## 5. Recommended Safe Reply", f"> {report.safe_reply}"])

        return "\n".join(md_lines)
