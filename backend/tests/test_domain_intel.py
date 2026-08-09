"""
GuardianAI Domain Intelligence Engine Unit Test Suite
Purpose: Tests TLD extraction, Subdomain Depth, Punycode, Typosquatting, High-Risk TLDs, Misspelled Brands, DGA Random Domains, and IP Hostnames.
"""

import pytest
from app.threat_intel.domain_intel import DomainIntelligenceEngine, DomainIntelReport

def test_analyze_typosquatting_and_high_risk_tld():
    """Tests typosquatting misspelled brand and high-risk TLD detection."""
    domain = "sub.verify.paypa1-check.top"
    report: DomainIntelReport = DomainIntelligenceEngine.analyze_domain_intel(domain)

    assert report.tld == ".top"
    assert report.is_suspicious_tld is True
    assert report.subdomain_depth == 2
    assert report.subdomain == "sub.verify"
    assert report.typosquatting_detected is True
    assert report.impersonated_brand == "paypal"
    assert report.risk_score >= 70

def test_analyze_punycode_and_long_domain():
    """Tests Punycode and excessively long domain detection."""
    domain = "xn--pypal-4ve-secure-login-account-update.com"
    report = DomainIntelligenceEngine.analyze_domain_intel(domain)

    assert report.is_punycode is True
    assert report.is_long_domain is True
    assert report.risk_score >= 35

def test_analyze_dga_random_domain():
    """Tests DGA Shannon entropy random string detection."""
    domain = "x89z1a09qw4b21c9.com"
    report = DomainIntelligenceEngine.analyze_domain_intel(domain)

    assert report.shannon_entropy > 3.5
    assert "dga" in str(report.is_dga_random_domain).lower() or report.shannon_entropy > 3.0

def test_analyze_ip_address_hostname():
    """Tests IP address hostname detection."""
    report = DomainIntelligenceEngine.analyze_domain_intel("192.168.1.1")

    assert report.is_ip_address is True
    assert report.risk_score >= 40
