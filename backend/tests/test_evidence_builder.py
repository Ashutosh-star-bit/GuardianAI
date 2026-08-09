"""
GuardianAI Evidence Builder Unit Test Suite
Purpose: Tests creation of ThreatEvidenceItem records with UTC timestamps and ThreatEvidenceReport aggregation counts.
"""

import pytest
from app.threat_intel.evidence_builder import EvidenceBuilderEngine, ThreatEvidenceItem, ThreatEvidenceReport

def test_create_threat_evidence_item():
    """Tests creating an individual ThreatEvidenceItem."""
    item = EvidenceBuilderEngine.create_evidence_item(
        evidence_id="ev_001",
        indicator="paypa1-check.com",
        category="DOMAIN",
        reason="Typosquatting domain mimicking PayPal brand",
        severity="Critical",
        confidence=0.98,
        source="DOMAIN_INTELLIGENCE"
    )

    assert item.evidence_id == "ev_001"
    assert item.indicator == "paypa1-check.com"
    assert item.category == "DOMAIN"
    assert item.severity == "Critical"
    assert item.confidence == 0.98
    assert item.source == "DOMAIN_INTELLIGENCE"
    assert "T" in item.timestamp # Valid ISO 8601 timestamp

def test_build_evidence_report_aggregation():
    """Tests bundling multiple evidence items into ThreatEvidenceReport with severity counters."""
    item1 = EvidenceBuilderEngine.create_evidence_item("ev_1", "paypa1-check.com", "DOMAIN", "Typosquatting link", "Critical", 0.98, "DOMAIN_INTELLIGENCE")
    item2 = EvidenceBuilderEngine.create_evidence_item("ev_2", "support.refund@okaxis", "UPI_ID", "Support desk handle impersonation", "High", 0.95, "UPI_INTELLIGENCE")
    item3 = EvidenceBuilderEngine.create_evidence_item("ev_3", "http://paypa1-check.com", "URL", "Unencrypted HTTP link", "Medium", 0.85, "URL_INTELLIGENCE")

    report: ThreatEvidenceReport = EvidenceBuilderEngine.build_evidence_report("scn_ev_100", [item1, item2, item3])

    assert report.scan_id == "scn_ev_100"
    assert report.total_evidence_count == 3
    assert report.critical_count == 1
    assert report.high_count == 1
    assert report.medium_count == 1
    assert report.low_count == 0
