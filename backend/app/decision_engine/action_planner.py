"""
GuardianAI Action Plan & Recommendation Engine
Purpose: Generates structured user recommendations, 4-tier security action plans (Immediate Actions, Things NOT to Do,
         Reporting Suggestions, General Safety Advice), and AI-generated Safe Decline Reply Templates.
"""

from typing import List, Dict, Optional, Any
from app.decision_engine.schemas import ActionPlanSchema
from pydantic import BaseModel, Field

class GeneratedRecommendationReport(BaseModel):
    """Structured Recommendation & Action Plan Output DTO."""
    scan_id: str
    risk_level: str
    scam_category: str
    immediate_actions: List[ActionPlanSchema] = Field(default_factory=list)
    things_not_to_do: List[str] = Field(default_factory=list)
    reporting_suggestions: List[str] = Field(default_factory=list)
    general_safety_advice: List[str] = Field(default_factory=list)
    safe_decline_reply: str

class RecommendationEngine:
    """Enterprise Action Plan & Recommendation Engine."""

    @classmethod
    def generate_recommendations(
        cls,
        scan_id: str,
        risk_level: str = "HIGH",
        scam_category: str = "GENERIC_FRAUD",
        detected_threat_keys: Optional[List[str]] = None
    ) -> GeneratedRecommendationReport:
        """
        Generates tailored recommendations, step-by-step action plans, prohibitions, reporting links, and safe reply template.
        """
        threat_keys = [k.upper() for k in (detected_threat_keys or [])]
        risk_upper = risk_level.upper()
        scam_upper = scam_category.upper()

        # 1. Immediate Actions Steps (ActionPlanSchema)
        immediate_actions: List[ActionPlanSchema] = []

        if risk_upper in ("CRITICAL", "HIGH"):
            immediate_actions.append(
                ActionPlanSchema(
                    step_number=1,
                    title="Block Sender Immediately",
                    instruction="Block sender phone number or email address to prevent follow-up coercion attempts.",
                    urgency="IMMEDIATE"
                )
            )
            immediate_actions.append(
                ActionPlanSchema(
                    step_number=2,
                    title="Verify Independently via Official App",
                    instruction="Log into your official banking app or corporate portal independently. Never use links provided in unsolicited messages.",
                    urgency="IMMEDIATE"
                )
            )
            if "BANK" in scam_upper or "BANK_SPOOF" in threat_keys:
                immediate_actions.append(
                    ActionPlanSchema(
                        step_number=3,
                        title="Contact Bank Fraud Department",
                        instruction="Call your bank's official customer support hotline listed on the back of your debit/credit card.",
                        urgency="RECOMMENDED"
                    )
                )
        elif risk_upper == "MEDIUM":
            immediate_actions.append(
                ActionPlanSchema(
                    step_number=1,
                    title="Exercise Heightened Caution",
                    instruction="Inspect URLs carefully character-by-character before clicking.",
                    urgency="RECOMMENDED"
                )
            )
        else:
            immediate_actions.append(
                ActionPlanSchema(
                    step_number=1,
                    title="Standard Vigilance",
                    instruction="No immediate action required. Maintain standard security awareness.",
                    urgency="OPTIONAL"
                )
            )

        # 2. Things NOT to Do (Prohibitions)
        things_not_to_do: List[str] = [
            "Do NOT click any web links embedded inside unsolicited SMS or email messages.",
            "Do NOT share One-Time Passwords (OTP), PINs, or account passwords with anyone.",
            "Do NOT transfer money or buy gift cards to claim prizes, refunds, or job offers."
        ]

        if "UPI" in scam_upper or any("UPI" in k for k in threat_keys):
            things_not_to_do.append("Do NOT enter your UPI PIN to receive money. Genuine refunds are credited automatically without PIN entry.")

        # 3. Reporting Suggestions
        reporting_suggestions: List[str] = [
            "Report smishing / phishing attempts to your mobile carrier or national cybercrime portal.",
            "Forward suspicious emails to official corporate IT security (abuse@domain.com)."
        ]

        # 4. General Safety Advice
        general_safety_advice: List[str] = [
            "Enable Multi-Factor Authentication (MFA) on all financial and digital accounts.",
            "Keep your mobile operating system and banking apps updated to the latest security patch."
        ]

        # 5. AI Safe Decline Reply Template
        if risk_upper in ("CRITICAL", "HIGH", "MEDIUM"):
            safe_reply = "I have logged and reported this unauthorized communication to official security channels. Do not contact me again."
        else:
            safe_reply = "Thank you for the message. I will review and follow up through official channels if necessary."

        return GeneratedRecommendationReport(
            scan_id=scan_id,
            risk_level=risk_upper,
            scam_category=scam_upper,
            immediate_actions=immediate_actions,
            things_not_to_do=things_not_to_do,
            reporting_suggestions=reporting_suggestions,
            general_safety_advice=general_safety_advice,
            safe_decline_reply=safe_reply
        )
