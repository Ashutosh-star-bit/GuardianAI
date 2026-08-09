"""
GuardianAI Reusable Email Intelligence Analysis Engine
Purpose: Performs offline email threat analysis evaluating Email Format, Display Name, Domain, Disposable Email Detection,
         Free Webmail Detection, Government/Educational/Corporate Domain Classification, and Display Name Spoofing Indicators.
"""

import re
from typing import List, Dict, Optional, Tuple
from pydantic import BaseModel, Field

# Pre-compiled RFC 5322 Email Header Matcher ("Display Name" <user@domain.com> or user@domain.com)
EMAIL_HEADER_REGEX = re.compile(r'(?:"?([^"<]+)"?\s*)?<?([a-zA-Z0-9._%+-]+@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,}))>?')

DISPOSABLE_DOMAINS = {
    "mailinator.com", "guerrillamail.com", "10minutemail.com", "tempmail.com", "trashmail.com",
    "yopmail.com", "dispostable.com", "sharklasers.com", "throwawaymail.com", "getairmail.com"
}

FREE_WEBMAIL_DOMAINS = {
    "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com", "icloud.com", "protonmail.com"
}

KNOWN_VIP_TITLES = ["ceo", "cfo", "president", "director", "manager", "support", "helpdesk", "customer service"]

class EmailIntelReport(BaseModel):
    """Structured Email Intelligence Analysis Output DTO."""
    raw_header: str
    display_name: Optional[str] = None
    email_address: str
    username: str
    domain: str
    is_valid_format: bool = True
    is_disposable: bool = False
    is_free_provider: bool = False
    is_government: bool = False
    is_educational: bool = False
    is_corporate: bool = False
    spoofing_detected: bool = False
    impersonated_title_or_brand: Optional[str] = None
    risk_indicators: List[str] = Field(default_factory=list)
    risk_score: int = Field(ge=0, le=100, description="Email Threat Risk Score 0 - 100")

class EmailIntelligenceEngine:
    """Enterprise Reusable Email Intelligence Analysis Engine."""

    @classmethod
    def parse_email_header(cls, raw_input: str) -> Optional[Tuple[Optional[str], str, str, str]]:
        """Parses display name, full email address, username, and domain from raw string."""
        match = EMAIL_HEADER_REGEX.search(raw_input.strip())
        if not match:
            return None

        display_name = match.group(1).strip() if match.group(1) else None
        email_addr = match.group(2).strip().lower()
        domain = match.group(3).strip().lower()
        username = email_addr.split("@")[0]

        return display_name, email_addr, username, domain

    @classmethod
    def analyze_email(cls, raw_email_input: str) -> EmailIntelReport:
        """
        Executes deep offline email threat analysis across 9 indicators.
        """
        parsed = cls.parse_email_header(raw_email_input)
        risk_indicators: List[str] = []
        risk_score = 0

        if not parsed:
            return EmailIntelReport(
                raw_header=raw_email_input,
                email_address="",
                username="",
                domain="",
                is_valid_format=False,
                risk_indicators=["INVALID_EMAIL_HEADER_FORMAT"],
                risk_score=50
            )

        display_name, email_addr, username, domain = parsed

        # 1. Disposable Email Detection
        is_disposable = domain in DISPOSABLE_DOMAINS
        if is_disposable:
            risk_indicators.append(f"DISPOSABLE_TEMPORARY_EMAIL_{domain.upper()}")
            risk_score += 45

        # 2. Free Webmail Provider Detection
        is_free_provider = domain in FREE_WEBMAIL_DOMAINS

        # 3. Government Domain Classification (.gov, .gov.in, .gov.uk, irs.gov, ftc.gov)
        is_gov = domain.endswith(".gov") or ".gov." in domain or domain in ("irs.gov", "ftc.gov")

        # 4. Educational Domain Classification (.edu, .ac.uk, .edu.in)
        is_edu = domain.endswith(".edu") or ".edu." in domain or ".ac." in domain

        # 5. Corporate Domain Classification
        is_corporate = not (is_free_provider or is_disposable or is_gov or is_edu)

        # 6. Display Name Spoofing & Executive Impersonation Analysis
        spoofing_detected = False
        impersonated_title_or_brand = None

        if display_name:
            name_lower = display_name.lower()

            # Check if display name claims executive title (CEO, CFO, Support) but uses free/disposable webmail
            title_found = next((t for t in KNOWN_VIP_TITLES if t in name_lower), None)
            if title_found and (is_free_provider or is_disposable):
                spoofing_detected = True
                impersonated_title_or_brand = title_found.upper()
                risk_indicators.append(f"DISPLAY_NAME_EXECUTIVE_SPOOFING_{title_found.upper()}")
                risk_score += 45

            # Check if display name claims brand (e.g. PayPal) but domain is not official
            if "paypal" in name_lower and "paypal.com" not in domain:
                spoofing_detected = True
                impersonated_title_or_brand = "PAYPAL"
                risk_indicators.append("DISPLAY_NAME_BRAND_SPOOFING_PAYPAL")
                risk_score += 50

        # Cap Risk Score at 100
        risk_score = min(risk_score, 100)

        return EmailIntelReport(
            raw_header=raw_email_input,
            display_name=display_name,
            email_address=email_addr,
            username=username,
            domain=domain,
            is_valid_format=True,
            is_disposable=is_disposable,
            is_free_provider=is_free_provider,
            is_government=is_gov,
            is_educational=is_edu,
            is_corporate=is_corporate,
            spoofing_detected=spoofing_detected,
            impersonated_title_or_brand=impersonated_title_or_brand,
            risk_indicators=risk_indicators,
            risk_score=risk_score
        )
