"""
GuardianAI Threat Intelligence Dataset Fixture Unit Test Suite
Purpose: Consumes dataset fixtures to verify Threat Intelligence engine behavior across all 10 threat scenarios.
"""

import pytest

from app.threat_intel.url_intel import URLIntelligenceEngine
from app.threat_intel.domain_intel import DomainIntelligenceEngine
from app.threat_intel.email_intel import EmailIntelligenceEngine
from app.threat_intel.upi_intel import UPIIntelligenceEngine
from app.threat_intel.phone_intel import PhoneIntelligenceEngine

from tests.fixtures.threat_intelligence_dataset import (
    dataset_safe_urls,
    dataset_phishing_urls,
    dataset_typosquatting_domains,
    dataset_suspicious_emails,
    dataset_upi_data,
    dataset_phone_data
)

def test_fixture_safe_urls(dataset_safe_urls):
    """Tests URL Intelligence against dataset of safe URLs (risk_score == 0)."""
    for url in dataset_safe_urls:
        report = URLIntelligenceEngine.analyze_url(url)
        assert report.risk_score == 0

def test_fixture_phishing_urls(dataset_phishing_urls):
    """Tests URL Intelligence against dataset of phishing URLs (risk_score >= 35)."""
    for url in dataset_phishing_urls:
        report = URLIntelligenceEngine.analyze_url(url)
        assert report.risk_score >= 35

def test_fixture_typosquatting_domains(dataset_typosquatting_domains):
    """Tests Domain Intelligence against dataset of typosquatting domains."""
    for item in dataset_typosquatting_domains:
        report = DomainIntelligenceEngine.analyze_domain_intel(item["domain"])
        assert report.typosquatting_detected is True
        assert getattr(report, "impersonated_brand_candidate", getattr(report, "impersonated_brand", None)) == item["expected_brand"]

def test_fixture_suspicious_emails(dataset_suspicious_emails):
    """Tests Email Intelligence against dataset of suspicious email headers."""
    for item in dataset_suspicious_emails:
        report = EmailIntelligenceEngine.analyze_email(item["header"])
        assert report.risk_score >= 40

def test_fixture_upi_data(dataset_upi_data):
    """Tests UPI Intelligence against dataset of UPI VPA handles."""
    for item in dataset_upi_data:
        report = UPIIntelligenceEngine.analyze_upi(item["upi_id"])
        if item["suspicious"]:
            assert report.risk_score >= 35

def test_fixture_phone_data(dataset_phone_data):
    """Tests Phone Intelligence against dataset of phone numbers."""
    for item in dataset_phone_data:
        report = PhoneIntelligenceEngine.parse_phone_number(item["phone"])
        if item.get("premium"):
            assert report.is_premium_rate is True
