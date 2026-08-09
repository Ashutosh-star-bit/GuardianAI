"""
GuardianAI Enterprise Evidence Builder System
Purpose: Converts extracted technical indicators, domain analysis, pattern matches, and email spoofing signals
         into standardized ThreatEvidence records containing Indicator, Category, Reason, Severity, Confidence, Source, and Timestamp.
"""

from datetime import datetime, timezone
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class ThreatEvidenceItem(BaseModel):
    """Standardized Threat Evidence Record DTO."""
    evidence_id: str
    indicator: str = Field(description="Exact IOC value e.g. paypa1-check.com")
    category: str = Field(description="URL, DOMAIN, EMAIL, PHONE, UPI_ID, BANK, PATTERN, KEYWORD")
    reason: str = Field(description="Human-readable threat explanation")
    severity: str = Field(description="Low, Medium, High, Critical")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score 0.0 to 1.0")
    source: str = Field(description="URL_INTELLIGENCE, DOMAIN_INTELLIGENCE, EMAIL_INTELLIGENCE, PHONE_INTELLIGENCE, UPI_INTELLIGENCE, PATTERN_ENGINE")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class ThreatEvidenceReport(BaseModel):
    """Container for gathered threat evidence records."""
    scan_id: str
    total_evidence_count: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    evidence_list: List[ThreatEvidenceItem] = Field(default_factory=list)

class EvidenceBuilderEngine:
    """Enterprise Evidence Builder System."""

    @classmethod
    def create_evidence_item(
        cls,
        evidence_id: str,
        indicator: str,
        category: str,
        reason: str,
        severity: str,
        confidence: float,
        source: str
    ) -> ThreatEvidenceItem:
        """Helper to instantiate a standardized ThreatEvidenceItem with UTC timestamp."""
        return ThreatEvidenceItem(
            evidence_id=evidence_id,
            indicator=indicator,
            category=category,
            reason=reason,
            severity=severity,
            confidence=confidence,
            source=source,
            timestamp=datetime.now(timezone.utc).isoformat()
        )

    @classmethod
    def build_evidence_report(cls, scan_id: str, items: List[ThreatEvidenceItem]) -> ThreatEvidenceReport:
        """Bundles a list of evidence items into a ThreatEvidenceReport summary."""
        critical_count = sum(1 for i in items if i.severity.capitalize() == "Critical")
        high_count = sum(1 for i in items if i.severity.capitalize() == "High")
        medium_count = sum(1 for i in items if i.severity.capitalize() == "Medium")
        low_count = sum(1 for i in items if i.severity.capitalize() == "Low")

        return ThreatEvidenceReport(
            scan_id=scan_id,
            total_evidence_count=len(items),
            critical_count=critical_count,
            high_count=high_count,
            medium_count=medium_count,
            low_count=low_count,
            evidence_list=items
        )
