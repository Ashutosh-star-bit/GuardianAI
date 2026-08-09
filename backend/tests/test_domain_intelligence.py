"""
GuardianAI Offline Domain Intelligence Engine Unit Test Suite
Purpose: Tests TLD extraction, Punycode detection, typosquatting candidate analysis, and IP address detection.
"""

import pytest
from app.nlp.domain_intelligence import DomainIntelligenceEngine, DomainIntelligenceReport

def test_detect_typosquatting_candidate():
    """Tests typosquatting candidate detection (paypa1-check.com -> paypal)."""
    report: DomainIntelligenceReport = DomainIntelligenceEngine.analyze_domain("paypa1-check.com")
    assert report.typosquatting_detected is True
    assert report.impersonated_brand_candidate == "paypal"
    assert report.risk_score >= 45

def test_detect_punycode_unicode_domain():
    """Tests Punycode / Unicode homoglyph domain detection."""
    report = DomainIntelligenceEngine.analyze_domain("xn--pypal-4ve.com")
    assert report.is_unicode_punycode is True
    assert report.risk_score >= 35

def test_detect_high_risk_tld():
    """Tests high-risk TLD detection (.top, .xyz)."""
    report = DomainIntelligenceEngine.analyze_domain("security-verify.top")
    assert report.high_risk_tld is True
    assert report.tld == ".top"

def test_detect_ip_address_hostname():
    """Tests IP address hostname detection."""
    report = DomainIntelligenceEngine.analyze_domain("192.168.1.1")
    assert report.is_ip_address is True
    assert report.risk_score >= 40

def test_subdomain_decomposition():
    """Tests subdomain decomposition (verify.security.paypal.com -> subdomain='verify.security', root='paypal.com')."""
    report = DomainIntelligenceEngine.analyze_domain("verify.security.paypal.com")
    assert report.subdomain == "verify.security"
    assert report.root_domain == "paypal.com"
    assert report.tld == ".com"
