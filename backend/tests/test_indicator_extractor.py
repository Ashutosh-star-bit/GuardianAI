"""
GuardianAI Indicator Extractor Engine Unit Test Suite
Purpose: Tests extraction across all 8 Indicators of Compromise (URLs, Domains, Emails, Phones, UPI IDs, Banks, Tracking IDs, Reference Numbers).
"""

import pytest
from app.threat_intel.indicator_extractor import IndicatorExtractorEngine, StructuredIOCContainer

def test_extract_all_8_indicator_types():
    """Tests extracting 8 IOC types from a composite smishing and courier fraud payload."""
    payload = (
        "URGENT: Transaction REF-990011 for PayPal account is pending. "
        "Parcel package TRACK-88776655 requires customs fee. Pay to merchant@okaxis "
        "or call +1-800-555-0199 or email support@paypal.com "
        "or visit http://paypa1-check.com/verify."
    )

    container: StructuredIOCContainer = IndicatorExtractorEngine.extract_all_indicators(payload)

    # 1. URLs
    assert "http://paypa1-check.com/verify" in container.urls
    # 2. Domains
    assert "paypa1-check.com" in container.domains
    # 3. Emails
    assert "support@paypal.com" in container.emails
    # 4. Phones
    assert len(container.phones) > 0
    # 5. UPI IDs
    assert "merchant@okaxis" in container.upi_ids
    # 6. Banks
    assert "PayPal" in container.banks
    # 7. Tracking IDs
    assert "88776655" in container.tracking_ids
    # 8. Reference Numbers
    assert "990011" in container.ref_numbers

    assert len(container.all_indicators) >= 8
