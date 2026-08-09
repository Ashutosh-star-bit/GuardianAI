"""
GuardianAI Reusable Risk Classification System
Purpose: Provides 5-tier Risk Level Classification (Safe, Low, Medium, High, Critical) with score thresholds,
         UI colors, SVG icons, user status messages, and recommended safety actions.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

class RiskLevelDefinition(BaseModel):
    """Structured Risk Level Classification Definition DTO."""
    level_key: str = Field(description="SAFE, LOW, MEDIUM, HIGH, CRITICAL")
    min_score: int = Field(ge=0, le=100)
    max_score: int = Field(ge=0, le=100)
    display_title: str
    description: str
    hex_color: str = Field(description="Hex color code for UI styling")
    badge_bg_color: str = Field(description="Background pill color")
    icon_svg_name: str
    user_header_message: str
    user_subtext_message: str
    recommended_actions: List[str]

# Master 5-Tier Risk Classification Registry Map
RISK_LEVEL_DEFINITIONS: Dict[str, RiskLevelDefinition] = {
    "SAFE": RiskLevelDefinition(
        level_key="SAFE",
        min_score=0,
        max_score=19,
        display_title="Safe Payload",
        description="No suspicious threat indicators or psychological manipulation tactics detected.",
        hex_color="#10B981", # Emerald Green
        badge_bg_color="rgba(16, 185, 129, 0.15)",
        icon_svg_name="shield-check",
        user_header_message="No Scam Threat Detected",
        user_subtext_message="This message appears safe. No suspicious links, fake urgent warnings, or spoofed credentials were found.",
        recommended_actions=[
            "Standard vigilance is recommended.",
            "Never share passwords or OTP codes with unverified senders."
        ]
    ),
    "LOW": RiskLevelDefinition(
        level_key="LOW",
        min_score=20,
        max_score=39,
        display_title="Low Risk Caution",
        description="Minor unusual indicators found, but no high-risk malicious markers detected.",
        hex_color="#3B82F6", # Sky Blue
        badge_bg_color="rgba(59, 130, 246, 0.15)",
        icon_svg_name="info-circle",
        user_header_message="Low Threat Activity",
        user_subtext_message="Message contains mild formatting or tracking parameters, but exhibits no confirmed phishing markers.",
        recommended_actions=[
            "Verify the sender identity if unexpected.",
            "Avoid clicking marketing tracking links."
        ]
    ),
    "MEDIUM": RiskLevelDefinition(
        level_key="MEDIUM",
        min_score=40,
        max_score=59,
        display_title="Medium Risk Warning",
        description="Suspicious urgency, unverified links, or personal UPI handles detected.",
        hex_color="#F59E0B", # Amber Yellow
        badge_bg_color="rgba(245, 158, 11, 0.15)",
        icon_svg_name="alert-triangle",
        user_header_message="Caution Advised",
        user_subtext_message="This message contains artificial time pressure or unverified web links requiring extra caution.",
        recommended_actions=[
            "Do NOT click embedded links directly.",
            "Navigate to the official website or mobile app independently."
        ]
    ),
    "HIGH": RiskLevelDefinition(
        level_key="HIGH",
        min_score=60,
        max_score=79,
        display_title="High Threat Danger",
        description="Strong signs of smishing, executive display name spoofing, or fake account lock claims.",
        hex_color="#F97316", # Orange
        badge_bg_color="rgba(249, 115, 22, 0.15)",
        icon_svg_name="alert-circle",
        user_header_message="High Risk Scam Threat",
        user_subtext_message="High probability of phishing or credential theft attempt. Fake account lock warning detected.",
        recommended_actions=[
            "Do NOT click any links or reply to the message.",
            "Block sender phone number or email address immediately.",
            "Log into your official banking portal independently to verify account safety."
        ]
    ),
    "CRITICAL": RiskLevelDefinition(
        level_key="CRITICAL",
        min_score=80,
        max_score=100,
        display_title="Critical Danger Scam",
        description="Confirmed malicious typosquatting, spoofed SPF/DKIM, or fraudulent UPI payment demand.",
        hex_color="#EF4444", # Crimson Red
        badge_bg_color="rgba(239, 68, 68, 0.15)",
        icon_svg_name="octagon-alert",
        user_header_message="CRITICAL SCAM WARNING",
        user_subtext_message="Confirmed fraudulent threat payload. Uses fake brand links and fake support handles to steal funds or credentials.",
        recommended_actions=[
            "STOP IMMEDIATELY: Do NOT click links or transfer any funds.",
            "Block sender and report message to national cybercrime authorities.",
            "If you entered credentials, change your passwords immediately."
        ]
    )
}

class RiskClassifierEngine:
    """Enterprise Reusable Risk Classification Engine."""

    @classmethod
    def classify_score(cls, scam_probability_score: int) -> RiskLevelDefinition:
        """
        Classifies a numerical scam probability score (0 to 100) into a 5-tier RiskLevelDefinition.
        """
        score = max(0, min(100, scam_probability_score))

        for level_def in RISK_LEVEL_DEFINITIONS.values():
            if level_def.min_score <= score <= level_def.max_score:
                return level_def

        # Default fallback to CRITICAL if >= 80
        return RISK_LEVEL_DEFINITIONS["CRITICAL"]
