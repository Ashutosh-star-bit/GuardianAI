"""
GuardianAI Reusable Keyword & Threat Trigger Detection Engine
Purpose: Provides rule-based keyword trigger detection for Urgency, Phishing CTA, Lottery, Banking, Financial Coercion, OTP, and Courier Fraud,
         supporting dynamic rule registration and extensible keyword catalogs.
"""

import re
from typing import Dict, List, Set, Optional
from pydantic import BaseModel, Field

class KeywordRule(BaseModel):
    """Structured Keyword Detection Rule DTO."""
    keyword_id: str = Field(description="Unique keyword identifier e.g. kw_urgent")
    trigger: str = Field(description="Exact phrase or word to match")
    category: str = Field(description="URGENCY, PHISHING_CTA, LOTTERY, BANKING, FINANCIAL, OTP, COURIER")
    severity: str = Field(default="High", description="Low, Medium, High, Critical")
    weight: float = Field(default=0.2, ge=0.0, le=1.0, description="Risk weight score contribution")
    is_regex: bool = Field(default=False)

class KeywordMatchResult(BaseModel):
    """Result container for a matched keyword trigger."""
    rule: KeywordRule
    matched_text: str
    position_start: int
    position_end: int

class KeywordDetectionEngine:
    """Enterprise Keyword & Threat Trigger Detection Engine."""

    # Default Extensible Keyword Catalog
    _rules: Dict[str, KeywordRule] = {}

    @classmethod
    def register_rule(cls, rule: KeywordRule) -> None:
        """Registers a new keyword detection rule dynamically."""
        cls._rules[rule.keyword_id] = rule

    @classmethod
    def register_rules(cls, rules: List[KeywordRule]) -> None:
        """Bulk registers a list of keyword detection rules."""
        for r in rules:
            cls.register_rule(r)

    @classmethod
    def detect_keywords(cls, text: str) -> List[KeywordMatchResult]:
        """
        Scans text payload against all registered keyword rules.
        Returns list of KeywordMatchResult objects.
        """
        results: List[KeywordMatchResult] = []
        if not text:
            return results

        text_lower = text.lower()

        for rule in cls._rules.values():
            trigger_pattern = rule.trigger.lower()
            if rule.is_regex:
                for match in re.finditer(trigger_pattern, text_lower):
                    results.append(
                        KeywordMatchResult(
                            rule=rule,
                            matched_text=match.group(0),
                            position_start=match.start(),
                            position_end=match.end()
                        )
                    )
            else:
                # Word boundary match
                pattern = r'\b' + re.escape(trigger_pattern) + r'\b'
                for match in re.finditer(pattern, text_lower):
                    results.append(
                        KeywordMatchResult(
                            rule=rule,
                            matched_text=match.group(0),
                            position_start=match.start(),
                            position_end=match.end()
                        )
                    )

        return results

# Register Required Standard Keywords Catalog
STANDARD_RULES = [
    # 1. Urgency Triggers
    KeywordRule(keyword_id="kw_urgent", trigger="urgent", category="URGENCY", severity="High", weight=0.25),
    KeywordRule(keyword_id="kw_immediately", trigger="immediately", category="URGENCY", severity="High", weight=0.25),
    KeywordRule(keyword_id="kw_limited_time", trigger="limited time", category="URGENCY", severity="High", weight=0.30),

    # 2. Phishing CTA Triggers
    KeywordRule(keyword_id="kw_verify", trigger="verify", category="PHISHING_CTA", severity="High", weight=0.20),
    KeywordRule(keyword_id="kw_click", trigger="click", category="PHISHING_CTA", severity="Medium", weight=0.15),

    # 3. Lottery & Prize Triggers
    KeywordRule(keyword_id="kw_winner", trigger="winner", category="LOTTERY", severity="Critical", weight=0.35),
    KeywordRule(keyword_id="kw_prize", trigger="prize", category="LOTTERY", severity="Critical", weight=0.35),
    KeywordRule(keyword_id="kw_lottery", trigger="lottery", category="LOTTERY", severity="Critical", weight=0.40),

    # 4. Banking & Impersonation Triggers
    KeywordRule(keyword_id="kw_kyc", trigger="kyc", category="BANKING", severity="Critical", weight=0.35),
    KeywordRule(keyword_id="kw_account_blocked", trigger="account blocked", category="BANKING", severity="Critical", weight=0.40),
    KeywordRule(keyword_id="kw_bank_alert", trigger="bank alert", category="BANKING", severity="Critical", weight=0.35),

    # 5. Financial Coercion Triggers
    KeywordRule(keyword_id="kw_refund", trigger="refund", category="FINANCIAL", severity="Medium", weight=0.20),
    KeywordRule(keyword_id="kw_investment", trigger="investment", category="FINANCIAL", severity="High", weight=0.25),
    KeywordRule(keyword_id="kw_crypto", trigger="crypto", category="FINANCIAL", severity="High", weight=0.25),

    # 6. Credential Theft Triggers
    KeywordRule(keyword_id="kw_otp", trigger="otp", category="OTP", severity="Critical", weight=0.30),

    # 7. Delivery & Courier Triggers
    KeywordRule(keyword_id="kw_courier", trigger="courier", category="COURIER", severity="High", weight=0.25),
]

# Initialize Registry with Standard Catalog
KeywordDetectionEngine.register_rules(STANDARD_RULES)
