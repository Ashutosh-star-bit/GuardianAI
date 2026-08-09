"""
GuardianAI Advanced URL & Domain Component Extractor
Purpose: Extracts and parses Full URLs, Short URLs, Root Domains, Subdomains, Protocols, Paths, and Query Parameters.
"""

import re
from urllib.parse import urlparse, parse_qs
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

# High-Performance Compiled URL Extraction Regex
URL_FULL_REGEX = re.compile(
    r'(?:https?://|www\.|t\.me/|wa\.me/|bit\.ly/|tinyurl\.com/)[^\s<>"\'()]+|(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?:/[^\s<>"\'()]*)?',
    re.IGNORECASE
)

KNOWN_SHORTENERS = {
    "bit.ly", "t.co", "tinyurl.com", "is.gd", "buff.ly", "ow.ly", "t.me", "wa.me", "goo.gl", "rb.gy"
}

class ParsedURLComponents(BaseModel):
    """Structured URL Breakdown DTO."""
    full_url: str
    is_shortened: bool = False
    protocol: Optional[str] = None
    domain: str
    subdomain: Optional[str] = None
    root_domain: str
    port: Optional[int] = None
    path: str = "/"
    query_params: Dict[str, List[str]] = Field(default_factory=dict)
    fragment: Optional[str] = None

class URLExtractorEngine:
    """Enterprise URL & Domain Component Parsing Engine."""

    @classmethod
    def parse_url_components(cls, raw_url: str) -> Optional[ParsedURLComponents]:
        """
        Parses raw URL string into protocol, subdomain, root domain, path, and query params.
        Handles edge cases such as missing http:// prefixes and IP addresses.
        """
        clean_url = raw_url.strip().rstrip(".,;:!?)")
        if not clean_url:
            return None

        # Fix missing scheme
        working_url = clean_url
        if not working_url.startswith(("http://", "https://")):
            working_url = "http://" + working_url

        try:
            parsed = urlparse(working_url)
            hostname = parsed.hostname or ""
            if not hostname:
                return None

            protocol = parsed.scheme if raw_url.lower().startswith(("http://", "https://")) else None
            port = parsed.port

            # Parse Subdomain vs Root Domain
            domain_parts = hostname.split(".")
            if len(domain_parts) > 2 and not re.match(r'^\d+\.\d+\.\d+\.\d+$', hostname):
                subdomain = ".".join(domain_parts[:-2])
                root_domain = ".".join(domain_parts[-2:])
            else:
                subdomain = None
                root_domain = hostname

            # Check if Shortener
            is_shortened = hostname.lower() in KNOWN_SHORTENERS

            # Query Params
            query_dict = parse_qs(parsed.query)

            return ParsedURLComponents(
                full_url=clean_url,
                is_shortened=is_shortened,
                protocol=protocol,
                domain=hostname,
                subdomain=subdomain,
                root_domain=root_domain,
                port=port,
                path=parsed.path or "/",
                query_params=query_dict,
                fragment=parsed.fragment or None
            )
        except Exception:
            return None

    @classmethod
    def extract_urls(cls, text: str) -> List[ParsedURLComponents]:
        """
        Extracts all embedded URLs from text payload and returns list of ParsedURLComponents.
        """
        if not text:
            return []

        matches = URL_FULL_REGEX.findall(text)
        results: List[ParsedURLComponents] = []
        seen: set = set()

        for raw_u in matches:
            cleaned = raw_u.strip().rstrip(".,;:!?)")
            if cleaned not in seen and len(cleaned) >= 4:
                seen.add(cleaned)
                parsed = cls.parse_url_components(cleaned)
                if parsed:
                    results.append(parsed)

        return results
