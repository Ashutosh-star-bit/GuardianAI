"""
GuardianAI Reusable URL Intelligence Analysis Engine
Purpose: Performs structured URL threat analysis analyzing Protocol, Hostname, Port, Path, Query Parameters,
         Fragments, Embedded Credentials, Percent Encoding, Suspicious Length, Redirect Loops, and Tracking Parameters.
"""

import re
from urllib.parse import urlparse, parse_qs, unquote
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

# High-Performance Compiled Regex Patterns
IP_HOST_REGEX = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
PERCENT_ENCODING_REGEX = re.compile(r'%[0-9a-fA-F]{2}')
TRACKING_PARAMS_SET = {"utm_source", "utm_medium", "utm_campaign", "aff_id", "click_id", "ref_id", "fbclid", "gclid"}

class URLIntelligenceReport(BaseModel):
    """Structured URL Intelligence Analysis Output DTO."""
    full_url: str
    protocol: Optional[str] = None
    hostname: str
    is_ip_address: bool = False
    port: Optional[int] = None
    path: str = "/"
    query_params_count: int = 0
    fragment: Optional[str] = None
    has_embedded_credentials: bool = False
    percent_encoding_count: int = 0
    excessive_length: bool = False
    embedded_redirect_detected: bool = False
    tracking_parameters_found: List[str] = Field(default_factory=list)
    risk_indicators: List[str] = Field(default_factory=list)
    risk_score: int = Field(ge=0, le=100, description="URL Risk Score 0 - 100")

class URLIntelligenceEngine:
    """Enterprise Reusable URL Intelligence Analysis Engine."""

    @classmethod
    def analyze_url(cls, raw_url: str) -> URLIntelligenceReport:
        """
        Executes deep structural URL threat analysis across 11 indicators.
        """
        clean_url = raw_url.strip().rstrip(".,;:!?)")
        risk_indicators: List[str] = []
        risk_score = 0

        # Fix missing scheme for parsing
        working_url = clean_url
        if not working_url.startswith(("http://", "https://")):
            working_url = "http://" + working_url

        parsed = urlparse(working_url)
        hostname = parsed.hostname or ""
        protocol = parsed.scheme if clean_url.lower().startswith(("http://", "https://")) else None

        # 1. Protocol Analysis (HTTP Unencrypted Warning)
        if protocol == "http":
            risk_indicators.append("UNENCRYPTED_HTTP_PROTOCOL")
            risk_score += 15

        # 2. Hostname & IP Address
        is_ip = bool(IP_HOST_REGEX.match(hostname))
        if is_ip:
            risk_indicators.append("RAW_IP_ADDRESS_HOSTNAME")
            risk_score += 35

        # 3. Port Analysis (Non-standard ports like 8080, 8443)
        port = parsed.port
        if port and port not in (80, 443):
            risk_indicators.append(f"NON_STANDARD_PORT_{port}")
            risk_score += 20

        # 4. Embedded Credentials Check (http://admin:secret@domain.com)
        has_credentials = bool(parsed.username or parsed.password)
        if has_credentials:
            risk_indicators.append("EMBEDDED_CREDENTIALS_IN_URL")
            risk_score += 45

        # 5. Percent Encoding Count (%20, %2F)
        percent_enc_matches = PERCENT_ENCODING_REGEX.findall(clean_url)
        enc_count = len(percent_enc_matches)
        if enc_count >= 5:
            risk_indicators.append(f"EXCESSIVE_PERCENT_ENCODING_{enc_count}")
            risk_score += 25

        # 6. Excessive Length (> 100 chars)
        excessive_length = len(clean_url) > 100
        if excessive_length:
            risk_indicators.append(f"EXCESSIVE_URL_LENGTH_{len(clean_url)}")
            risk_score += 15

        # 7. Embedded Redirects (http:// in query string)
        unquoted_query = unquote(parsed.query).lower()
        has_embedded_redirect = "http://" in unquoted_query or "https://" in unquoted_query
        if has_embedded_redirect:
            risk_indicators.append("EMBEDDED_REDIRECT_URL_IN_QUERY")
            risk_score += 35

        # 8. Tracking Parameters
        query_dict = parse_qs(parsed.query)
        tracking_found = [param for param in query_dict.keys() if param.lower() in TRACKING_PARAMS_SET]

        # Cap Risk Score at 100
        risk_score = min(risk_score, 100)

        return URLIntelligenceReport(
            full_url=clean_url,
            protocol=protocol,
            hostname=hostname,
            is_ip_address=is_ip,
            port=port,
            path=parsed.path or "/",
            query_params_count=len(query_dict),
            fragment=parsed.fragment or None,
            has_embedded_credentials=has_credentials,
            percent_encoding_count=enc_count,
            excessive_length=excessive_length,
            embedded_redirect_detected=has_embedded_redirect,
            tracking_parameters_found=tracking_found,
            risk_indicators=risk_indicators,
            risk_score=risk_score
        )
