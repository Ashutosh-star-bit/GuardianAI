"""
GuardianAI Multi-Source Evidence Fusion Engine Unit Test Suite
Purpose: Tests merging evidence across 5 sources, deduplicating on (indicator, category), and sorting by Severity hierarchy.
"""

import pytest
from app.decision_engine.schemas import EvidenceItemSchema
from app.decision_engine.evidence_aggregator import EvidenceFusionEngine, DecisionEvidenceReport

def test_fuse_and_deduplicate_evidence_sources():
    """Tests merging multi-source evidence, deduplicating duplicate IOC entries, and sorting by Critical > High > Medium."""
    item_ai = EvidenceItemSchema(
        evidence_id="ev_ai_1",
        indicator="paypa1-check.top",
        category="DOMAIN",
        reason="AI detected typosquatting brand spoofing",
        severity="High",
        confidence=0.90,
        source="GEMINI_AI"
    )

    item_threat = EvidenceItemSchema(
        evidence_id="ev_th_1",
        indicator="paypa1-check.top",
        category="DOMAIN",
        reason="Confirmed typosquatting domain link in threat DB",
        severity="Critical", # Higher severity for same indicator
        confidence=0.98,
        source="DOMAIN_INTELLIGENCE"
    )

    item_upi = EvidenceItemSchema(
        evidence_id="ev_upi_1",
        indicator="support.refund@okaxis",
        category="UPI_ID",
        reason="Customer support handle impersonation",
        severity="High",
        confidence=0.95,
        source="UPI_INTELLIGENCE"
    )

    report: DecisionEvidenceReport = EvidenceFusionEngine.fuse_multi_source_evidence(
        scan_id="scn_fuse_100",
        ai_evidence=[item_ai],
        threat_intel_evidence=[item_threat],
        pattern_evidence=[item_upi]
    )

    # 1. Total deduplicated count should be 2 (paypa1-check.top deduplicated)
    assert report.total_unified_evidence_count == 2

    # 2. Critical severity item should be sorted FIRST
    first_item = report.unified_evidence_list[0]
    assert first_item.indicator == "paypa1-check.top"
    assert first_item.severity == "Critical" # Retained Critical severity from Threat Intel

    # 3. Second item should be UPI High severity
    second_item = report.unified_evidence_list[1]
    assert second_item.indicator == "support.refund@okaxis"
    assert second_item.severity == "High"
