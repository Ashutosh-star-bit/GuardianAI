"""
GuardianAI Enterprise Reusable Pattern Detection Engine
Purpose: Provides extensible regex pattern detection across 10 core fraud threat categories:
         OTP Requests, Money Requests, Gift Card Requests, Investment Promises, High Returns,
         Threats, Warnings, Account Suspension, Prize Claims, and Refund Claims.
"""

import re
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class PatternDefinition(BaseModel):
    """Structured Pattern Rule Definition DTO."""
    pattern_id: str = Field(description="Unique pattern identifier e.g. pat_otp_solicitation")
    category: str = Field(description="OTP_REQUEST, MONEY_REQUEST, GIFT_CARD, INVESTMENT, HIGH_RETURNS, THREATS, WARNINGS, ACCOUNT_SUSPENSION, PRIZE_CLAIM, REFUND_CLAIM")
    pattern_name: str = Field(description="Human-readable pattern title")
    regex: str = Field(description="Compiled Python regular expression string")
    severity: str = Field(default="High", description="Low, Medium, High, Critical")
    description: str

class ExtractedPatternMatch(BaseModel):
    """Container for a detected pattern match."""
    pattern: PatternDefinition
    matched_text: str
    position_start: int
    position_end: int

    @property
    def category(self) -> str:
        return self.pattern.category

    @property
    def pattern_name(self) -> str:
        return self.pattern.pattern_name

    @property
    def severity(self) -> str:
        return self.pattern.severity

class PatternEngine:
    """Enterprise Reusable Pattern Detection Engine."""

    # Storage layout: _patterns[pattern_id] = PatternDefinition
    _patterns: Dict[str, PatternDefinition] = {}

    @classmethod
    def register_pattern(cls, pattern: PatternDefinition) -> None:
        """Registers a new pattern definition dynamically."""
        cls._patterns[pattern.pattern_id] = pattern

    @classmethod
    def register_patterns(cls, patterns: List[PatternDefinition]) -> None:
        """Bulk registers a list of pattern definitions."""
        for p in patterns:
            cls.register_pattern(p)

    @classmethod
    def detect_patterns(cls, text: str) -> List[ExtractedPatternMatch]:
        """
        Scans text payload against all registered pattern definitions.
        Returns list of ExtractedPatternMatch objects.
        """
        results: List[ExtractedPatternMatch] = []
        if not text:
            return results

        for pattern_def in cls._patterns.values():
            try:
                for match in re.finditer(pattern_def.regex, text, re.IGNORECASE):
                    results.append(
                        ExtractedPatternMatch(
                            pattern=pattern_def,
                            matched_text=match.group(0),
                            position_start=match.start(),
                            position_end=match.end()
                        )
                    )
            except re.error:
                continue

        return results

# Alias for backwards compatibility
PatternDetector = PatternEngine

# Register Required 10 Threat Pattern Categories Catalog
STANDARD_PATTERNS = [
    # 1. OTP Requests
    PatternDefinition(
        pattern_id="pat_otp_request",
        category="OTP_REQUEST",
        pattern_name="OTP Solicitation Request",
        regex=r"(?:share your otp|send me (?:the|your) (?:code|passcode)|verify (?:the|your) 6-digit code|provide your otp)",
        severity="Critical",
        description="Solicits one-time authentication passcodes"
    ),
    # 2. Money Requests
    PatternDefinition(
        pattern_id="pat_money_request",
        category="MONEY_REQUEST",
        pattern_name="Wire / Transfer Payment Demand",
        regex=r"(?:transfer \$\d+|send money|wire transfer|pay to upi|deposit cash|send payment|send \$\d+)",
        severity="Critical",
        description="Demands direct wire transfer or electronic payment"
    ),
    # 3. Gift Card Requests
    PatternDefinition(
        pattern_id="pat_gift_card",
        category="GIFT_CARD",
        pattern_name="Gift Card Purchase Request",
        regex=r"(?:buy (?:apple|itunes|amazon|steam|google play) gift cards|send gift card (?:code|pin)|purchase gift cards)",
        severity="Critical",
        description="Solicits untraceable retail gift card codes"
    ),
    # 4. Investment Promises
    PatternDefinition(
        pattern_id="pat_investment",
        category="INVESTMENT",
        pattern_name="Guaranteed Investment Returns",
        regex=r"(?:guaranteed (?:investment|return|profit)|double your crypto|high yield investment|risk-free profit)",
        severity="High",
        description="Promises unrealistic risk-free investment returns"
    ),
    # 5. High Returns
    PatternDefinition(
        pattern_id="pat_high_returns",
        category="HIGH_RETURNS",
        pattern_name="100% Daily ROI Yield Promise",
        regex=r"(?:100% return|daily \d+% (?:profit|return)|earn \$\d+ daily|weekly return)",
        severity="High",
        description="Promises fixed daily/weekly high return percentages"
    ),
    # 6. Threats
    PatternDefinition(
        pattern_id="pat_threats",
        category="THREATS",
        pattern_name="Legal Action / Arrest Warrant Threat",
        regex=r"(?:arrest warrant|legal action|police will|customs seizure|court order)",
        severity="Critical",
        description="Threatens law enforcement or legal arrest"
    ),
    # 7. Warnings
    PatternDefinition(
        pattern_id="pat_warnings",
        category="WARNINGS",
        pattern_name="Urgent Security Breach Warning",
        regex=r"(?:final warning|security alert|unauthorized login|action required|immediate attention|urgent)",
        severity="High",
        description="Warns of security breach requiring immediate user action"
    ),
    # 8. Account Suspension
    PatternDefinition(
        pattern_id="pat_account_suspension",
        category="ACCOUNT_SUSPENSION",
        pattern_name="Account Lock & Suspension Claim",
        regex=r"(?:account.*(?:suspended|locked|blocked|revoked)|access terminated)",
        severity="Critical",
        description="Claims user digital or bank account is locked"
    ),
    # 9. Prize Claims
    PatternDefinition(
        pattern_id="pat_prize_claim",
        category="PRIZE_CLAIM",
        pattern_name="Jackpot & Lottery Prize Claim",
        regex=r"(?:claim your (?:prize|reward|jackpot)|won \$\d+|congratulations.*winner)",
        severity="Critical",
        description="Instructs user to claim lottery or contest winnings"
    ),
    # 10. Refund Claims
    PatternDefinition(
        pattern_id="pat_refund_claim",
        category="REFUND_CLAIM",
        pattern_name="Tax / Overcharge Refund Claim",
        regex=r"(?:claim your (?:tax |overcharge )?refund|refund of \$\d+|eligible for a refund)",
        severity="High",
        description="Offers fake tax or overcharge reimbursement"
    )
]

# Initialize Registry with Standard Patterns Catalog
PatternEngine.register_patterns(STANDARD_PATTERNS)
