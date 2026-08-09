"""
GuardianAI Reusable Domain Intelligence Analysis Engine
Purpose: Performs deep offline domain threat analysis detecting TLDs, Subdomain Depth, Unicode, Punycode,
         Typosquatting Candidates, Suspicious TLDs, Misspelled Brands, Long Domains, DGA Random Strings, and IP Hostnames.
"""

import re
import math
from typing import List, Dict, Optional, Set
from pydantic import BaseModel, Field

KNOWN_TARGET_BRANDS = [
    "paypal", "bankofamerica", "chase", "wellsfargo", "amazon", "apple", "google",
    "fedex", "dhl", "netflix", "microsoft", "facebook", "instagram", "whatsapp"
]

HIGH_RISK_TLDS = {".top", ".xyz", ".info", ".site", ".online", ".work", ".click", ".link", ".cc", ".icu", ".top"}

class DomainIntelReport(BaseModel):
    """Structured Domain Intelligence Analysis Output DTO."""
    domain: str
    tld: str
    subdomain_depth: int = 0
    subdomain: Optional[str] = None
    root_domain: str
    is_ip_address: bool = False
    is_unicode: bool = False
    is_punycode: bool = False
    is_suspicious_tld: bool = False
    is_long_domain: bool = False
    is_dga_random_domain: bool = False
    impersonated_brand: Optional[str] = None
    typosquatting_detected: bool = False
    domain_length: int
    shannon_entropy: float
    risk_indicators: List[str] = Field(default_factory=list)
    risk_score: int = Field(ge=0, le=100, description="Domain Risk Score 0 - 100")

class DomainIntelligenceEngine:
    """Enterprise Reusable Domain Intelligence Analysis Engine."""

    @staticmethod
    def calculate_shannon_entropy(text: str) -> float:
        """Calculates Shannon Entropy score measuring randomness of domain label."""
        if not text:
            return 0.0
        prob = [float(text.count(c)) / len(text) for c in set(text)]
        entropy = -sum(p * math.log2(p) for p in prob)
        return round(entropy, 3)

    @staticmethod
    def calculate_levenshtein(s1: str, s2: str) -> int:
        """Calculates edit distance between two strings."""
        if len(s1) < len(s2):
            return DomainIntelligenceEngine.calculate_levenshtein(s2, s1)
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
    def detect_brand_misspelling(cls, domain_label: str) -> Optional[str]:
        """Detects typosquatting or misspelled brand candidates in domain label."""
        clean_label = domain_label.lower().replace("1", "l").replace("0", "o").replace("v", "u")

        for brand in KNOWN_TARGET_BRANDS:
            if brand in clean_label and clean_label != brand:
                return brand
            if len(domain_label) >= 4 and abs(len(domain_label) - len(brand)) <= 2:
                dist = cls.calculate_levenshtein(domain_label.lower(), brand)
                if 1 <= dist <= 2:
                    return brand
        return None

    @classmethod
    def analyze_domain_intel(cls, raw_domain: str) -> DomainIntelReport:
        """
        Executes deep domain analysis across 10 threat indicators.
        """
        clean_domain = raw_domain.strip().lower().rstrip(".")
        risk_indicators: List[str] = []
        risk_score = 0

        # 1. IP Address Check
        is_ip = bool(re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', clean_domain))
        if is_ip:
            risk_indicators.append("RAW_IP_ADDRESS_HOSTNAME")
            risk_score += 40

        # 2. Unicode & Punycode Check
        is_punycode = clean_domain.startswith("xn--") or "xn--" in clean_domain
        is_unicode = any(ord(c) > 127 for c in clean_domain)
        if is_punycode or is_unicode:
            risk_indicators.append("UNICODE_PUNYCODE_HOMOGLYPH_DOMAIN")
            risk_score += 35

        # 3. Subdomain Depth & TLD Decomposition
        parts = clean_domain.split(".")
        subdomain_depth = max(0, len(parts) - 2) if not is_ip else 0

        if is_ip:
            tld = ""
            subdomain = None
            root_domain = clean_domain
        elif len(parts) >= 2:
            tld = "." + parts[-1]
            root_domain = ".".join(parts[-2:])
            subdomain = ".".join(parts[:-2]) if len(parts) > 2 else None
        else:
            tld = ""
            subdomain = None
            root_domain = clean_domain

        if subdomain_depth >= 2:
            risk_indicators.append(f"EXCESSIVE_SUBDOMAIN_DEPTH_{subdomain_depth}")
            risk_score += 15

        # 4. Suspicious TLD Check
        is_suspicious_tld = tld in HIGH_RISK_TLDS
        if is_suspicious_tld:
            risk_indicators.append(f"HIGH_RISK_ABUSE_TLD_{tld}")
            risk_score += 25

        # 5. Long Domain Check (> 30 chars)
        domain_length = len(clean_domain)
        is_long_domain = domain_length > 30
        if is_long_domain:
            risk_indicators.append(f"LONG_DOMAIN_NAME_{domain_length}_CHARS")
            risk_score += 15

        # 6. Random Domain DGA Entropy Check (> 4.1 entropy)
        domain_label = parts[-2] if len(parts) >= 2 and not is_ip else clean_domain
        entropy = cls.calculate_shannon_entropy(domain_label)
        is_dga = entropy > 4.1 and len(domain_label) > 12
        if is_dga:
            risk_indicators.append(f"DGA_RANDOM_DOMAIN_ENTROPY_{entropy}")
            risk_score += 30

        # 7. Typosquatting & Misspelled Brand Check
        brand_match = cls.detect_brand_misspelling(domain_label)
        is_typosquatting = brand_match is not None and domain_label != brand_match
        if is_typosquatting:
            risk_indicators.append(f"TYPOSQUATTING_MISSPELLED_BRAND_{brand_match.upper()}")
            risk_score += 45

        # Cap Risk Score at 100
        risk_score = min(risk_score, 100)

        return DomainIntelReport(
            domain=clean_domain,
            tld=tld,
            subdomain_depth=subdomain_depth,
            subdomain=subdomain,
            root_domain=root_domain,
            is_ip_address=is_ip,
            is_unicode=is_unicode,
            is_punycode=is_punycode,
            is_suspicious_tld=is_suspicious_tld,
            is_long_domain=is_long_domain,
            is_dga_random_domain=is_dga,
            impersonated_brand=brand_match,
            typosquatting_detected=is_typosquatting,
            domain_length=domain_length,
            shannon_entropy=entropy,
            risk_indicators=risk_indicators,
            risk_score=risk_score
        )
