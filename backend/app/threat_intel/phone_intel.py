"""
GuardianAI Reusable Phone Intelligence Analysis Engine
Purpose: Performs structured phone threat analysis extracting Country Code, Local Number, E.164 Formatting,
         Possible Premium Rate Numbers, Repeated Digits, and Obfuscated/Hidden Numbers.
"""

import re
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

# Common International Calling Codes Map
COUNTRY_CODES_MAP = {
    "1": "US/Canada (+1)",
    "44": "United Kingdom (+44)",
    "91": "India (+91)",
    "61": "Australia (+61)",
    "49": "Germany (+49)",
    "33": "France (+33)",
    "81": "Japan (+81)",
    "86": "China (+86)",
}

PREMIUM_RATE_PREFIXES = {"900", "976", "0900", "0908", "0909"}

class PhoneIntelReport(BaseModel):
    """Structured Phone Intelligence Analysis Output DTO."""
    raw_input: str
    country_code: Optional[str] = None
    country_name: Optional[str] = None
    local_number: str
    e164_format: str
    is_valid_length: bool = True
    is_premium_rate: bool = False
    has_repeated_digits: bool = False
    has_hidden_obfuscated_digits: bool = False
    risk_indicators: List[str] = Field(default_factory=list)
    risk_score: int = Field(ge=0, le=100, description="Phone Threat Risk Score 0 - 100")

class PhoneIntelligenceEngine:
    """Enterprise Reusable Phone Intelligence Analysis Engine."""

    @classmethod
    def parse_phone_number(cls, raw_input: str) -> PhoneIntelReport:
        """
        Executes structural phone threat analysis across 6 indicators.
        """
        clean_input = raw_input.strip()
        risk_indicators: List[str] = []
        risk_score = 0

        # 1. Check Hidden / Obfuscated Digits (* or X)
        has_hidden = bool(re.search(r'[*X#]', clean_input, re.IGNORECASE))
        if has_hidden:
            risk_indicators.append("OBFUSCATED_HIDDEN_PHONE_DIGITS")
            risk_score += 30

        # Strip non-numeric except leading +
        digits_only = re.sub(r'[^\d+]', '', clean_input)
        numeric_digits = re.sub(r'\D', '', clean_input)

        # 2. Length Validation (7 to 15 digits)
        is_valid_len = 7 <= len(numeric_digits) <= 15
        if not is_valid_len:
            risk_indicators.append("INVALID_PHONE_NUMBER_LENGTH")
            risk_score += 25

        # 3. Repeated Digits (e.g. 9999999999, 0000000000)
        has_repeated = bool(re.search(r'(\d)\1{5,}', numeric_digits))
        if has_repeated:
            risk_indicators.append("SUSPICIOUS_REPEATED_DIGITS")
            risk_score += 35

        # 4. Country Code & Local Number Parsing
        country_code = None
        country_name = None
        local_number = numeric_digits

        if digits_only.startswith("+"):
            for cc, cname in COUNTRY_CODES_MAP.items():
                if numeric_digits.startswith(cc):
                    country_code = f"+{cc}"
                    country_name = cname
                    local_number = numeric_digits[len(cc):]
                    break
            if not country_code and len(numeric_digits) > 10:
                country_code = f"+{numeric_digits[:2]}"
                country_name = f"International ({country_code})"
                local_number = numeric_digits[2:]

        e164_format = f"{country_code or ''}{local_number}"

        # 5. Premium Rate Number Check (e.g. 900 prefix)
        is_premium = any(local_number.startswith(prefix) for prefix in PREMIUM_RATE_PREFIXES)
        if is_premium:
            risk_indicators.append("POSSIBLE_PREMIUM_RATE_NUMBER")
            risk_score += 40

        # Cap Risk Score at 100
        risk_score = min(risk_score, 100)

        return PhoneIntelReport(
            raw_input=clean_input,
            country_code=country_code,
            country_name=country_name,
            local_number=local_number,
            e164_format=e164_format,
            is_valid_length=is_valid_len,
            is_premium_rate=is_premium,
            has_repeated_digits=has_repeated,
            has_hidden_obfuscated_digits=has_hidden,
            risk_indicators=risk_indicators,
            risk_score=risk_score
        )
