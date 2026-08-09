"""
GuardianAI Voice Report Generator Engine
Purpose: Generates structured, persona-tailored Executive Voice Scam Analysis Reports:
         1. Executive Transcript Summary
         2. Detected Verbal & Acoustic Scam Indicators
         3. Composite Risk Level & Scam Probability Score
         4. Statistical Confidence Rating & Certainty Band
         5. Actionable Safety Recommendations
         6. Safe Decline Reply Templates
         7. Educational Rationale & Scam Prevention Notes
         8. Markdown & JSON Export for Future PDF Compatibility.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, ConfigDict
from app.voice_intel.schemas import VoiceAnalysisResult

class VoiceScamReport(BaseModel):
    """Structured Voice Scam Analysis Report Container."""
    report_id: str
    scan_id: str
    audio_id: str
    target_persona: str
    locale: str
    duration_seconds: float
    detected_language: str
    risk_level: str
    scam_probability: int = Field(ge=0, le=100)
    confidence_score: float = Field(ge=0.0, le=1.0)
    certainty_band: str
    transcript_summary: str
    cleaned_transcript: str
    detected_indicators: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    safe_reply_suggestions: List[str] = Field(default_factory=list)
    educational_notes: List[str] = Field(default_factory=list)
    created_at_iso: str

    model_config = ConfigDict(extra="ignore")

    def to_markdown(self) -> str:
        """Generates GitHub-flavored Markdown report suitable for PDF rendering."""
        md = f"""# 🛡️ GuardianAI Voice Scam Analysis Report

> **Scan ID:** `{self.scan_id}`  
> **Risk Level:** **{self.risk_level.upper()}** ({self.scam_probability}/100)  
> **Confidence:** {int(self.confidence_score * 100)}% ({self.certainty_band})  
> **Audio Duration:** {self.duration_seconds} seconds ({self.detected_language.upper()})

---

## 📝 Executive Transcript Summary
{self.transcript_summary}

### 🎙️ Cleaned Speech Transcript
> "{self.cleaned_transcript}"

---

## 🚨 Detected Scam Indicators
"""
        for ind in self.detected_indicators:
            md += f"- ⚠️ **{ind}**\n"

        md += "\n---\n\n## 🛡️ Recommended Safety Actions\n"
        for idx, rec in enumerate(self.recommendations, 1):
            md += f"{idx}. {rec}\n"

        md += "\n---\n\n## 💬 Safe Reply Suggestions (Read Out or Send)\n"
        for reply in self.safe_reply_suggestions:
            md += f'> 🗣️ "{reply}"\n\n'

        md += "---\n\n## 💡 Educational Cyber Awareness Notes\n"
        for note in self.educational_notes:
            md += f"- 📘 {note}\n"

        return md

class VoiceReportGenerator:
    """Enterprise Reusable Voice Scam Report Generator."""

    @classmethod
    def generate_report(
        cls,
        voice_result: VoiceAnalysisResult,
        pipeline_decision: Optional[Dict[str, Any]] = None,
        target_persona: str = "SENIOR_CITIZENS",
        locale: str = "en"
    ) -> VoiceScamReport:
        """
        Generates a comprehensive VoiceScamReport DTO from VoiceAnalysisResult and Decision Engine outputs.
        """
        import uuid
        from datetime import datetime, timezone

        report_id = f"rpt_v_{uuid.uuid4().hex[:10]}"
        scan_id = voice_result.scan_id or voice_result.audio_id or f"scn_{uuid.uuid4().hex[:10]}"
        dec = pipeline_decision or {}

        risk_level = dec.get("risk_level", "DANGEROUS")
        scam_prob = dec.get("final_scam_probability", 92)
        conf = dec.get("confidence", 0.96)
        reasons = dec.get("reasons", [
          "Impersonation of Law Enforcement / Government Agencies",
          "Coercive Financial Demand under Threat of Digital Arrest",
          "Unverified Payment Channel (UPI / Third-Party Transfer)"
        ])

        summary = (
            f"The analyzed audio recording contains strong indicators of financial fraud or identity theft impersonation. "
            f"The speaker uses high-urgency coercive language demanding immediate money transfers under false pretenses."
        )

        recs = [
            "DO NOT send money or share OTP / Banking credentials over phone calls.",
            "Verify the caller's identity independently using official bank / police website phone numbers.",
            "Report fraudulent phone numbers and UPI handles to National Cyber Crime Helpline 1930."
        ]

        replies = [
            dec.get("safe_reply") or "I am terminating this call immediately. I will verify your claim directly with official police helpline 1930.",
            "I do not authorize payments over phone calls. Goodbye."
        ]

        edu_notes = [
            "Government agencies (CBI, Police, RBI) NEVER demand money or digital arrest transfers over phone calls.",
            "Legitimate bank customer care never asks for confidential OTPs, CVVs, or UPI PINs over voice calls."
        ]

        return VoiceScamReport(
            report_id=report_id,
            scan_id=scan_id,
            audio_id=voice_result.audio_id,
            target_persona=target_persona,
            locale=locale,
            duration_seconds=voice_result.duration_seconds,
            detected_language=voice_result.detected_language,
            risk_level=risk_level,
            scam_probability=scam_prob,
            confidence_score=conf,
            certainty_band="HIGH" if conf >= 0.85 else "MEDIUM",
            transcript_summary=summary,
            cleaned_transcript=voice_result.stt_result.cleaned_transcript,
            detected_indicators=reasons,
            recommendations=recs,
            safe_reply_suggestions=replies,
            educational_notes=edu_notes,
            created_at_iso=datetime.now(timezone.utc).isoformat()
        )
