"""
GuardianAI Enterprise Structured Entity Extractor
Purpose: Extracts 12 entity types (URLs, Domains, Emails, Phone Numbers, UPI IDs, Bank Names,
         Government Orgs, Currency Values, Dates, Times, People, Companies) into structured Pydantic DTOs.
"""

import re
from typing import List, Optional
from urllib.parse import urlparse
from pydantic import BaseModel, Field
from app.nlp.schemas import DetectedEntity

class ExtractedEntitiesReport(BaseModel):
    """Structured entity extraction container for 12 entity types."""
    urls: List[str] = Field(default_factory=list)
    domains: List[str] = Field(default_factory=list)
    emails: List[str] = Field(default_factory=list)
    phones: List[str] = Field(default_factory=list)
    upi_ids: List[str] = Field(default_factory=list)
    banks: List[str] = Field(default_factory=list)
    gov_orgs: List[str] = Field(default_factory=list)
    currencies: List[str] = Field(default_factory=list)
    dates: List[str] = Field(default_factory=list)
    times: List[str] = Field(default_factory=list)
    people: List[str] = Field(default_factory=list)
    companies: List[str] = Field(default_factory=list)
    all_entities: List[DetectedEntity] = Field(default_factory=list)

KNOWN_BANKS = ["PayPal", "Bank of America", "Chase", "Wells Fargo", "HDFC", "ICICI", "SBI", "Citibank", "Barclays"]
GOV_ORGS = ["IRS", "FTC", "FBI", "Police", "Income Tax Department", "Customs", "SEBI", "Social Security Administration"]
KNOWN_COMPANIES = ["Amazon", "Apple", "Google", "FedEx", "DHL", "Netflix", "WhatsApp", "Telegram", "Binance"]

class EntityExtractor:
    """Enterprise Named Entity Extractor across 12 fraud categories."""

    @classmethod
    def extract_domain_from_url(cls, url: str) -> Optional[str]:
        """Extracts domain hostname from URL string."""
        try:
            if not url.startswith(("http://", "https://")):
                url = "http://" + url
            parsed = urlparse(url)
            return parsed.netloc or None
        except Exception:
            return None

    @classmethod
    def extract_all_entities(cls, text: str) -> ExtractedEntitiesReport:
        """
        Scans text payload and extracts 12 entity types into ExtractedEntitiesReport.
        """
        all_detected: List[DetectedEntity] = []
        text_lower = text.lower()

        # 1. URLs
        url_matches = re.findall(r'https?://[^\s]+|www\.[^\s]+|paypa1-[^\s]+', text, re.IGNORECASE)
        urls = list(set(url_matches))
        for u in urls:
            all_detected.append(DetectedEntity(entity_type="URL", text=u, confidence=0.98, context=f"URL: {u}"))

        # 2. Domains
        domains = list(set([cls.extract_domain_from_url(u) for u in urls if cls.extract_domain_from_url(u)]))
        for d in domains:
            all_detected.append(DetectedEntity(entity_type="DOMAIN", text=d, confidence=0.95, context=f"Domain: {d}"))

        # 3. Emails
        emails = list(set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text, re.IGNORECASE)))
        for e in emails:
            all_detected.append(DetectedEntity(entity_type="EMAIL", text=e, confidence=0.98, context=f"Email: {e}"))

        # 4. Phones
        raw_phones = re.findall(r'\+?\d{1,3}[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}', text)
        phones = list(set([p for p in raw_phones if len(re.sub(r'\D', '', p)) >= 10]))
        for p in phones:
            all_detected.append(DetectedEntity(entity_type="PHONE", text=p, confidence=0.90, context=f"Phone: {p}"))

        # 5. UPI IDs (e.g. merchant@okaxis, payee@ybl)
        upi_matches = list(set(re.findall(r'\b[a-zA-Z0-9._-]+@(?:okaxis|ybl|paytm|upi|ibl|sbi|icici)\b', text, re.IGNORECASE)))
        for upi in upi_matches:
            all_detected.append(DetectedEntity(entity_type="UPI_ID", text=upi, confidence=0.95, context=f"UPI Handle: {upi}"))

        # 6. Banks
        banks = [b for b in KNOWN_BANKS if b.lower() in text_lower]
        for b in banks:
            all_detected.append(DetectedEntity(entity_type="BANK", text=b, confidence=0.95, context=f"Bank Entity: {b}"))

        # 7. Government Organisations
        govs = [g for g in GOV_ORGS if g.lower() in text_lower]
        for g in govs:
            all_detected.append(DetectedEntity(entity_type="GOV_ORG", text=g, confidence=0.95, context=f"Government Org: {g}"))

        # 8. Currencies
        currencies = list(set(re.findall(r'[\$\€\£\₹]\s*\d+(?:,\d+)*(?:\.\d+)?|\b\d+\s*(?:USD|EUR|INR|GBP|BTC)\b', text, re.IGNORECASE)))
        for c in currencies:
            all_detected.append(DetectedEntity(entity_type="CURRENCY", text=c, confidence=0.92, context=f"Currency: {c}"))

        # 9. Dates
        dates = list(set(re.findall(r'\b(?:\d{1,2}/\d{1,2}/\d{2,4}|\d{4}-\d{2}-\d{2}|today|tomorrow|yesterday)\b', text, re.IGNORECASE)))
        for d in dates:
            all_detected.append(DetectedEntity(entity_type="DATE", text=d, confidence=0.88, context=f"Date: {d}"))

        # 10. Times
        times = list(set(re.findall(r'\b(?:\d{1,2}:\d{2}\s*(?:AM|PM)?|\d{1,2}\s*hours?)\b', text, re.IGNORECASE)))
        for t in times:
            all_detected.append(DetectedEntity(entity_type="TIME", text=t, confidence=0.85, context=f"Time: {t}"))

        # 11. People (Titles / Names)
        people_matches = list(set(re.findall(r'\b(?:CEO|Manager|Officer|Director|Agent)\s+[A-Z][a-z]+\b', text)))
        for p in people_matches:
            all_detected.append(DetectedEntity(entity_type="PEOPLE", text=p, confidence=0.85, context=f"Impersonated Person: {p}"))

        # 12. Companies
        companies = [c for c in KNOWN_COMPANIES if c.lower() in text_lower]
        for c in companies:
            all_detected.append(DetectedEntity(entity_type="COMPANY", text=c, confidence=0.95, context=f"Company: {c}"))

        return ExtractedEntitiesReport(
            urls=urls,
            domains=domains,
            emails=emails,
            phones=phones,
            upi_ids=upi_matches,
            banks=banks,
            gov_orgs=govs,
            currencies=currencies,
            dates=dates,
            times=times,
            people=people_matches,
            companies=companies,
            all_entities=all_detected
        )

    @classmethod
    def extract_entities(cls, text: str) -> List[DetectedEntity]:
        """Scans text payload and returns list of DetectedEntity objects."""
        report = cls.extract_all_entities(text)
        return report.all_entities
