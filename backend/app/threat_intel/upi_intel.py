"""
GuardianAI Reusable UPI Intelligence Analysis Engine
Purpose: Performs structured UPI payment handle threat analysis analyzing UPI ID, Handle Username, PSP Provider,
         Underlying Sponsor Bank, Formatting Mistakes, Unknown Providers, and Suspicious Naming Patterns.
"""

import re
from typing import List, Dict, Optional, Tuple
from pydantic import BaseModel, Field

# High-Performance Compiled Regex Matcher for UPI VPA (handle_name@psp_code)
UPI_VPA_REGEX = re.compile(r'^[a-zA-Z0-9._-]+@([a-zA-Z0-9.-]+)$')

# Master Catalog of Recognized Indian PSP Payment Handles & Sponsor Banks
KNOWN_UPI_PSP_MAP = {
    "okaxis": ("Google Pay", "Axis Bank"),
    "okicici": ("Google Pay", "ICICI Bank"),
    "oksbi": ("Google Pay", "State Bank of India"),
    "okbizaxis": ("Google Pay Business", "Axis Bank"),
    "ybl": ("PhonePe", "Yes Bank"),
    "ibl": ("PhonePe", "ICICI Bank"),
    "axl": ("PhonePe", "Axis Bank"),
    "paytm": ("Paytm", "Paytm Payments Bank"),
    "upi": ("BHIM UPI", "National Payments Corporation of India"),
    "sbi": ("BHIM SBI", "State Bank of India"),
    "icici": ("iMobile", "ICICI Bank"),
    "barodampay": ("Baroda Pay", "Bank of Baroda"),
    "hdfcbank": ("PageApp", "HDFC Bank")
}

SUSPICIOUS_NAME_KEYWORDS = ["support", "helpdesk", "customercare", "refund", "kyc", "verify", "official", "reward"]

class UPIIntelReport(BaseModel):
    """Structured UPI Intelligence Analysis Output DTO."""
    upi_id: str
    username_handle: str
    psp_handle: str
    psp_provider_name: Optional[str] = None
    sponsor_bank_name: Optional[str] = None
    is_valid_format: bool = True
    is_recognized_psp: bool = False
    has_suspicious_naming: bool = False
    impersonated_keyword: Optional[str] = None
    risk_indicators: List[str] = Field(default_factory=list)
    risk_score: int = Field(ge=0, le=100, description="UPI Threat Risk Score 0 - 100")

class UPIIntelligenceEngine:
    """Enterprise Reusable UPI Intelligence Analysis Engine."""

    @classmethod
    def analyze_upi(cls, raw_upi_id: str) -> UPIIntelReport:
        """
        Executes structural UPI VPA handle threat analysis across 7 indicators.
        """
        clean_upi = raw_upi_id.strip().lower()
        risk_indicators: List[str] = []
        risk_score = 0

        # 1. Format Check (must contain @ and valid handle syntax)
        match = UPI_VPA_REGEX.match(clean_upi)
        if not match:
            return UPIIntelReport(
                upi_id=clean_upi,
                username_handle=clean_upi,
                psp_handle="",
                is_valid_format=False,
                risk_indicators=["INVALID_UPI_VPA_FORMAT"],
                risk_score=40
            )

        parts = clean_upi.split("@")
        username_handle = parts[0]
        psp_handle = parts[1]

        # 2. Recognized PSP Provider & Sponsor Bank Check
        psp_info = KNOWN_UPI_PSP_MAP.get(psp_handle)
        is_recognized = psp_info is not None
        provider_name = psp_info[0] if psp_info else None
        bank_name = psp_info[1] if psp_info else None

        if not is_recognized:
            risk_indicators.append(f"UNKNOWN_UNRECOGNIZED_UPI_PSP_{psp_handle.upper()}")
            risk_score += 35

        # 3. Suspicious Naming Pattern Analysis (Impersonating Support / Refund Desks)
        has_suspicious = False
        keyword_found = None

        for kw in SUSPICIOUS_NAME_KEYWORDS:
            if kw in username_handle:
                has_suspicious = True
                keyword_found = kw.upper()
                risk_indicators.append(f"SUSPICIOUS_UPI_NAME_PATTERN_{keyword_found}")
                risk_score += 45
                break

        # Cap Risk Score at 100
        risk_score = min(risk_score, 100)

        return UPIIntelReport(
            upi_id=clean_upi,
            username_handle=username_handle,
            psp_handle=psp_handle,
            psp_provider_name=provider_name,
            sponsor_bank_name=bank_name,
            is_valid_format=True,
            is_recognized_psp=is_recognized,
            has_suspicious_naming=has_suspicious,
            impersonated_keyword=keyword_found,
            risk_indicators=risk_indicators,
            risk_score=risk_score
        )
