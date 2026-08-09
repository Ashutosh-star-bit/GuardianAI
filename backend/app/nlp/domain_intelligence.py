"""
GuardianAI Offline Domain Intelligence Engine
Purpose: Performs offline heuristic domain analysis extracting Domain, TLD, Subdomain, IP Addresses, Shortened URLs,
         Punycode/Unicode homoglyphs, and Typosquatting candidates WITHOUT making external network API calls.
"""

import re
import unicodedata
from typing import List, Dict, Optional, Set
from pydantic import BaseModel, Field

KNOWN_TARGET_BRANDS = [
    "paypal", "bankofamerica", "chase", "wellsfargo", "amazon", "apple", "google",
    "fedex", "dhl", "netflix", "microsoft", "facebook", "instagram", "whatsapp"
]

HIGH_RISK_TLDS = {".top", ".xyz", ".info", ".site", ".online", ".work", ".click", ".link", ".cc", ".icu"}
KNOWN_SHORTENERS = {"bit.ly", "t.co", "tinyurl.com", "is.gd", "buff.ly", "t.me", "wa.me"}

# Common Typosquatting Character Substitutions
TYPO_CHAR_MAP = {
    '1': 'l', 'l': 'i', '0': 'o', 'o': '0', '5': 's', '@': 'a', 'vv': 'w', 'rn': 'm'
}

class DomainIntelligenceReport(BaseModel):
    """Structured Domain Intelligence Analysis Report DTO."""
    domain: str
    tld: str
    subdomain: Optional[str] = None
    root_domain: str
    is_ip_address: bool = False
    is_shortened: bool = False
    is_unicode_punycode: bool = False
    high_risk_tld: bool = False
    impersonated_brand_candidate: Optional[str] = None
    typosquatting_detected: bool = False
    risk_score: int = Field(ge=0, le=100, description="Heuristic domain risk score 0 - 100")

class DomainIntelligenceEngine:
    """Enterprise Offline Domain Intelligence Analysis Engine."""

    @staticmethod
    def calculate_levenshtein_distance(s1: str, s2: str) -> int:
        """Calculates edit distance between two strings."""
        if len(s1) < len(s2):
            return DomainIntelligenceEngine.calculate_levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        return previous_row[-1]

    @classmethod
    def normalize_typo_string(cls, name: str) -> str:
        """Replaces common typosquatting substitutions (paypa1 -> paypal, amazon1 -> amazon)."""
        normalized = name.lower()
        for typo, val in TYPO_CHAR_MAP.items():
            normalized = normalized.replace(typo, val)
        return normalized

    @classmethod
    def detect_typosquatting(cls, domain_label: str) -> Optional[str]:
        """
        Analyzes domain label for typosquatting candidates mimicking known brands.
        Returns matching target brand name if detected.
        """
        label_clean = cls.normalize_typo_string(domain_label)

        for brand in KNOWN_TARGET_BRANDS:
            # 1. Exact match after typo normalization (paypa1 -> paypal)
            if brand in label_clean:
                return brand

            # 2. Levenshtein edit distance check (1 or 2 edits for brands >= 5 chars)
            if len(domain_label) >= 4 and abs(len(domain_label) - len(brand)) <= 2:
                dist = cls.calculate_levenshtein_distance(domain_label.lower(), brand)
                if 1 <= dist <= 2:
                    return brand

        return None

    @classmethod
    def analyze_domain(cls, raw_domain: str) -> DomainIntelligenceReport:
        """
        Performs offline heuristic analysis of domain hostname.
        """
        clean_domain = raw_domain.strip().lower().rstrip(".")

        # 1. Check IP Address
        is_ip = bool(re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', clean_domain))

        # 2. Check Unicode / Punycode (xn--...)
        is_punycode = clean_domain.startswith("xn--") or any(ord(c) > 127 for c in clean_domain)

        # 3. Check Shortener
        is_shortened = clean_domain in KNOWN_SHORTENERS

        # 4. TLD & Subdomain Decomposition
        parts = clean_domain.split(".")
        if is_ip:
            tld = ""
            subdomain = None
            root_domain = clean_domain
        elif len(parts) >= 2:
            tld = "." + parts[-1]
            if len(parts) > 2:
                subdomain = ".".join(parts[:-2])
                root_domain = ".".join(parts[-2:])
            else:
                subdomain = None
                root_domain = clean_domain
        else:
            tld = ""
            subdomain = None
            root_domain = clean_domain

        # 5. High-Risk TLD Check
        is_high_risk_tld = tld in HIGH_RISK_TLDS

        # 6. Typosquatting Analysis
        domain_label = parts[-2] if len(parts) >= 2 and not is_ip else clean_domain
        target_brand = cls.detect_typosquatting(domain_label)
        is_typosquatting = target_brand is not None and domain_label.lower() != target_brand

        # Calculate Heuristic Risk Score (0 - 100)
        risk_score = 0
        if is_ip:
            risk_score += 40
        if is_punycode:
            risk_score += 35
        if is_high_risk_tld:
            risk_score += 25
        if is_typosquatting:
            risk_score += 45

        risk_score = min(risk_score, 100)

        return DomainIntelligenceReport(
            domain=clean_domain,
            tld=tld,
            subdomain=subdomain,
            root_domain=root_domain,
            is_ip_address=is_ip,
            is_shortened=is_shortened,
            is_unicode_punycode=is_punycode,
            high_risk_tld=is_high_risk_tld,
            impersonated_brand_candidate=target_brand,
            typosquatting_detected=is_typosquatting,
            risk_score=risk_score
        )
