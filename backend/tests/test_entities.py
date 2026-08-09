"""
GuardianAI Entity Extractor Unit Test Suite
Purpose: Tests extraction of 12 entity types (URLs, Domains, Emails, Phones, UPI IDs, Banks, Gov Orgs, Currencies, Dates, Times, People, Companies).
"""

import pytest
from app.nlp.entities import EntityExtractor, ExtractedEntitiesReport

def test_extract_all_12_entity_types():
    """Tests extraction across all 12 entity categories in a rich scam payload."""
    payload = (
        "URGENT NOTICE from IRS and PayPal: Officer John states your account is suspended today at 12:00 PM. "
        "Pay $500 to merchant@okaxis or call +1-800-555-0199 or email support@paypal.com "
        "or visit http://paypa1-check.com/verify. Delivery handled by FedEx."
    )

    report: ExtractedEntitiesReport = EntityExtractor.extract_all_entities(payload)

    # 1. URLs
    assert "http://paypa1-check.com/verify" in report.urls
    # 2. Domains
    assert "paypa1-check.com" in report.domains
    # 3. Emails
    assert "support@paypal.com" in report.emails
    # 4. Phones
    assert len(report.phones) > 0
    # 5. UPI IDs
    assert "merchant@okaxis" in report.upi_ids
    # 6. Banks
    assert "PayPal" in report.banks
    # 7. Gov Orgs
    assert "IRS" in report.gov_orgs
    # 8. Currencies
    assert "$500" in report.currencies
    # 9. Dates
    assert "today" in report.dates
    # 10. Times
    assert "12:00 PM" in report.times
    # 11. People
    assert "Officer John" in report.people
    # 12. Companies
    assert "FedEx" in report.companies

    assert len(report.all_entities) >= 12
