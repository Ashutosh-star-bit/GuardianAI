"""
GuardianAI Explainable Threat Intelligence (XAI) Engine
Purpose: Generates structured, transparent XAI explanations for every technical threat indicator detailing:
         1. Why it is suspicious, 2. How it was detected, 3. Possible false positives, and 4. Suggested user action.
"""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class ThreatIndicatorXAIRecord(BaseModel):
    """Structured XAI Explanation Record DTO for an individual threat indicator."""
    indicator_key: str
    suspicious_reason: str = Field(description="Non-technical explanation of why indicator is suspicious")
    detection_method: str = Field(description="Technical detection method e.g. Levenshtein edit distance")
    false_positive_possibility: str = Field(description="Scenarios where legitimate activity triggers this indicator")
    suggested_action: str = Field(description="Actionable safety guidance for end users")

class ThreatIntelXAISummary(BaseModel):
    """Container for complete Threat Intelligence XAI explanation."""
    scan_id: str
    overall_summary: str
    explained_indicators: List[ThreatIndicatorXAIRecord] = Field(default_factory=list)

# Master Threat Indicator XAI Knowledge Base Dictionary
XAI_KNOWLEDGE_BASE: Dict[str, Dict[str, str]] = {
    "TYPOSQUATTING": {
        "reason": "The domain name closely mimics a well-known brand (e.g. paypa1 instead of paypal) to trick users into revealing credentials.",
        "detection_method": "Character leetspeak normalization and Levenshtein edit distance analysis against target brand catalogs.",
        "false_positive": "Rare brand renames, regional subsidiaries, or intentional satirical domains.",
        "action": "Do NOT enter passwords or payment details. Verify the URL character-by-character or use official mobile apps."
    },
    "UNENCRYPTED_HTTP_PROTOCOL": {
        "reason": "The website link uses unencrypted HTTP instead of HTTPS, allowing network eavesdroppers to intercept passwords.",
        "detection_method": "URL scheme inspection verifying absence of TLS/SSL encryption.",
        "false_positive": "Legacy informational websites or local intranet development environments.",
        "action": "Never enter sensitive credentials or card numbers on unencrypted HTTP pages."
    },
    "RAW_IP_ADDRESS_HOSTNAME": {
        "reason": "The link uses a raw IP address (e.g. 192.168.1.1) instead of a registered domain name, bypassing DNS safety filters.",
        "detection_method": "IPv4 / IPv6 regex pattern matching against URL host header.",
        "false_positive": "Internal network router dashboards or corporate development servers.",
        "action": "Avoid clicking IP address links in unsolicited SMS or email messages."
    },
    "DISPOSABLE_TEMPORARY_EMAIL": {
        "reason": "The email was sent from a temporary 10-minute inbox service commonly used by scammers to avoid tracing.",
        "detection_method": "Domain lookup against a global disposable webmail provider database.",
        "false_positive": "Privacy-conscious users using anonymous relay addresses for one-time registrations.",
        "action": "Treat messages from temporary email addresses with extreme caution."
    },
    "DISPLAY_NAME_EXECUTIVE_SPOOFING": {
        "reason": "The email display name claims an executive title (e.g. CEO or Customer Support) but originates from a free webmail account.",
        "detection_method": "Header parsing matching executive titles against free webmail domains (Gmail, Yahoo).",
        "false_positive": "Small business owners using personal webmail accounts for business correspondence.",
        "action": "Verify executive wire transfer requests via a separate out-of-band phone call."
    },
    "SUSPICIOUS_UPI_NAME_PATTERN": {
        "reason": "The UPI payment handle claims to belong to a official support desk (e.g. support.refund) on a personal PSP handle.",
        "detection_method": "Pattern matching handle prefix against support and refund keywords on public PSP handles.",
        "false_positive": "Legitimate small merchant handle containing descriptive terms.",
        "action": "Never send money to claim a refund or prize. Genuine refunds are credited automatically without payment."
    }
}

class ThreatExplainabilityEngine:
    """Enterprise Explainable Threat Intelligence Engine."""

    @classmethod
    def explain_indicator(cls, indicator_key: str) -> ThreatIndicatorXAIRecord:
        """
        Generates structured 4-part XAI explanation for a specific threat indicator key.
        """
        key_upper = indicator_key.upper()

        # Match base indicator category if specific key not in KB
        matching_key = next((k for k in XAI_KNOWLEDGE_BASE.keys() if k in key_upper), None)
        info = XAI_KNOWLEDGE_BASE.get(matching_key) if matching_key else None

        if not info:
            info = {
                "reason": f"Indicator '{indicator_key}' exhibited abnormal behavioral patterns exceeding threat risk thresholds.",
                "detection_method": "Heuristic rule matching against threat indicator database.",
                "false_positive": "Non-standard corporate configurations or unusual user formatting.",
                "action": "Exercise caution and verify the source independently before interacting."
            }

        return ThreatIndicatorXAIRecord(
            indicator_key=indicator_key,
            suspicious_reason=info["reason"],
            detection_method=info["detection_method"],
            false_positive_possibility=info["false_positive"],
            suggested_action=info["action"]
        )

    @classmethod
    def generate_xai_summary(cls, scan_id: str, indicator_keys: List[str]) -> ThreatIntelXAISummary:
        """
        Generates complete XAI explanation summary for a list of detected threat indicator keys.
        """
        records = [cls.explain_indicator(k) for k in indicator_keys]

        if not records:
            summary_text = "No suspicious technical threat indicators detected. The payload appears clean."
        elif len(records) >= 2:
            summary_text = f"Multiple high-risk indicators detected ({len(records)} items). The message exhibits strong signs of impersonation or phishing."
        else:
            summary_text = "Suspicious technical threat indicators detected requiring user vigilance."

        return ThreatIntelXAISummary(
            scan_id=scan_id,
            overall_summary=summary_text,
            explained_indicators=records
        )
