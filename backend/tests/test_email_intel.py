"""
GuardianAI Email Intelligence Engine Unit Test Suite
Purpose: Tests email header parsing, disposable email detection, free webmail detection, domain classification, and executive display name spoofing.
"""

import pytest
from app.threat_intel.email_intel import EmailIntelligenceEngine, EmailIntelReport

def test_analyze_executive_spoofing_email():
    """Tests executive display name spoofing ("CEO John" <john@gmail.com>)."""
    raw_header = '"CEO John Smith" <john.smith@gmail.com>'
    report: EmailIntelReport = EmailIntelligenceEngine.analyze_email(raw_header)

    assert report.display_name == "CEO John Smith"
    assert report.email_address == "john.smith@gmail.com"
    assert report.domain == "gmail.com"
    assert report.is_free_provider is True
    assert report.spoofing_detected is True
    assert report.impersonated_title_or_brand == "CEO"
    assert report.risk_score >= 45

def test_analyze_disposable_email():
    """Tests disposable email provider detection (mailinator.com)."""
    raw_header = "user123@mailinator.com"
    report = EmailIntelligenceEngine.analyze_email(raw_header)

    assert report.is_disposable is True
    assert report.domain == "mailinator.com"
    assert report.risk_score >= 45

def test_analyze_government_and_educational_domains():
    """Tests classification of government (.gov) and educational (.edu) domains."""
    report_gov = EmailIntelligenceEngine.analyze_email("agent@irs.gov")
    assert report_gov.is_government is True
    assert report_gov.is_corporate is False

    report_edu = EmailIntelligenceEngine.analyze_email("student@mit.edu")
    assert report_edu.is_educational is True
    assert report_edu.is_corporate is False

def test_analyze_legitimate_corporate_email():
    """Tests classification of legitimate corporate email address."""
    report = EmailIntelligenceEngine.analyze_email("security@paypal.com")

    assert report.is_corporate is True
    assert report.is_free_provider is False
    assert report.is_disposable is False
    assert report.spoofing_detected is False
    assert report.risk_score == 0
