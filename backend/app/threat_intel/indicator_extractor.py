"""
GuardianAI Reusable Indicator Extraction Engine (IOC Extractor)
Purpose: Extracts 8 Indicators of Compromise (IOCs): URLs, Domains, Email Addresses, Phone Numbers,
         UPI IDs, Bank Names, Courier Tracking IDs, and Reference Numbers into structured Pydantic DTO containers.
"""

import re
from typing import List, Dict, Optional, Set, Any
from urllib.parse import urlparse
from pydantic import BaseModel, Field

# Pre-Compiled High-Performance Regex Catalog for 8 IOC Types
URL_IOC_REGEX = re.compile(r'https?://[^\s<>"\'()]+|www\.[^\s<>"\'()]+|paypa1-[^\s<>"\'()]+', re.IGNORECASE)
EMAIL_IOC_REGEX = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', re.IGNORECASE)
PHONE_IOC_REGEX = re.compile(r'\+?\d{1,3}[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}')
UPI_IOC_REGEX = re.compile(r'\b[a-zA-Z0-9._-]+@(?:okaxis|ybl|paytm|upi|ibl|sbi|icici)\b', re.IGNORECASE)
TRACKING_IOC_REGEX = re.compile(r'\b(?:AWB|TRACK|TRK|SHIP|WAYBILL)[-:]?\s*([a-zA-Z0-9]{8,16})\b', re.IGNORECASE)
REF_NUM_IOC_REGEX = re.compile(r'\b(?:REF|TXN|CASE|TICKET|ORDER)[-:#]?\s*([a-zA-Z0-9]{6,16})\b', re.IGNORECASE)

KNOWN_BANKS = ["PayPal", "Bank of America", "Chase", "Wells Fargo", "HDFC", "ICICI", "SBI", "Citibank", "Barclays"]

class ExtractedIOC(BaseModel):
    """Individual extracted Indicator of Compromise DTO."""
    ioc_type: str = Field(description="URL, DOMAIN, EMAIL, PHONE, UPI_ID, BANK, TRACKING_ID, REF_NUMBER")
    value: str
    confidence: float = Field(default=0.95, ge=0.0, le=1.0)
    context_snippet: Optional[str] = None

class StructuredIOCContainer(BaseModel):
    """Structured IOC extraction report container for 8 indicator types."""
    urls: List[str] = Field(default_factory=list)
    domains: List[str] = Field(default_factory=list)
    emails: List[str] = Field(default_factory=list)
    phones: List[str] = Field(default_factory=list)
    upi_ids: List[str] = Field(default_factory=list)
    banks: List[str] = Field(default_factory=list)
    tracking_ids: List[str] = Field(default_factory=list)
    ref_numbers: List[str] = Field(default_factory=list)
    all_indicators: List[ExtractedIOC] = Field(default_factory=list)

class IndicatorExtractorEngine:
    """Enterprise Reusable Indicator Extraction Engine."""

    @staticmethod
    def extract_domain_from_url(url: str) -> Optional[str]:
        """Extracts domain hostname from URL string."""
        try:
            if not url.startswith(("http://", "https://")):
                url = "http://" + url
            parsed = urlparse(url)
            return parsed.netloc or None
        except Exception:
            return None

    @classmethod
    def extract_all_indicators(cls, text: str) -> StructuredIOCContainer:
        """
        Scans input text payload and extracts 8 IOC types into a StructuredIOCContainer.
        """
        all_iocs: List[ExtractedIOC] = []
        if not text:
            return StructuredIOCContainer()

        text_lower = text.lower()

        # 1. URLs
        raw_urls = list(set(URL_IOC_REGEX.findall(text)))
        for u in raw_urls:
            all_iocs.append(ExtractedIOC(ioc_type="URL", value=u, confidence=0.98, context_snippet=f"URL: {u}"))

        # 2. Domains
        domains = list(set([cls.extract_domain_from_url(u) for u in raw_urls if cls.extract_domain_from_url(u)]))
        for d in domains:
            all_iocs.append(ExtractedIOC(ioc_type="DOMAIN", value=d, confidence=0.95, context_snippet=f"Domain: {d}"))

        # 3. Emails
        emails = list(set(EMAIL_IOC_REGEX.findall(text)))
        for e in emails:
            all_iocs.append(ExtractedIOC(ioc_type="EMAIL", value=e, confidence=0.98, context_snippet=f"Email: {e}"))

        # 4. Phones
        raw_phones = PHONE_IOC_REGEX.findall(text)
        phones = list(set([p for p in raw_phones if len(re.sub(r'\D', '', p)) >= 10]))
        for p in phones:
            all_iocs.append(ExtractedIOC(ioc_type="PHONE", value=p, confidence=0.90, context_snippet=f"Phone: {p}"))

        # 5. UPI IDs
        upi_ids = list(set(UPI_IOC_REGEX.findall(text)))
        for upi in upi_ids:
            all_iocs.append(ExtractedIOC(ioc_type="UPI_ID", value=upi, confidence=0.95, context_snippet=f"UPI Handle: {upi}"))

        # 6. Banks
        banks = [b for b in KNOWN_BANKS if b.lower() in text_lower]
        for b in banks:
            all_iocs.append(ExtractedIOC(ioc_type="BANK", value=b, confidence=0.95, context_snippet=f"Bank: {b}"))

        # 7. Tracking IDs (e.g. AWB123456789, TRACK-98765432)
        raw_tracking = TRACKING_IOC_REGEX.findall(text)
        tracking_ids = list(set(raw_tracking))
        for trk in tracking_ids:
            all_iocs.append(ExtractedIOC(ioc_type="TRACKING_ID", value=trk, confidence=0.92, context_snippet=f"Tracking ID: {trk}"))

        # 8. Reference Numbers (e.g. REF-889900, TXN987654321)
        raw_refs = REF_NUM_IOC_REGEX.findall(text)
        ref_numbers = list(set(raw_refs))
        for ref in ref_numbers:
            all_iocs.append(ExtractedIOC(ioc_type="REF_NUMBER", value=ref, confidence=0.90, context_snippet=f"Reference Num: {ref}"))

        return StructuredIOCContainer(
            urls=raw_urls,
            domains=domains,
            emails=emails,
            phones=phones,
            upi_ids=upi_ids,
            banks=banks,
            tracking_ids=tracking_ids,
            ref_numbers=ref_numbers,
            all_indicators=all_iocs
        )
