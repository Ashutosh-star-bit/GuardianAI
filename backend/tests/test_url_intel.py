"""
GuardianAI URL Intelligence Engine Unit Test Suite
Purpose: Tests structural URL analysis across all 11 indicators including embedded credentials, IP hostnames, non-standard ports, and percent-encoding.
"""

import pytest
from app.threat_intel.url_intel import URLIntelligenceEngine, URLIntelligenceReport

def test_analyze_suspicious_url_with_credentials_and_port():
    """Tests URL with embedded credentials, non-standard port 8080, and IP address hostname."""
    raw_url = "http://admin:secret@192.168.1.1:8080/login/secure?utm_source=spam#top"
    report: URLIntelligenceReport = URLIntelligenceEngine.analyze_url(raw_url)

    assert report.is_ip_address is True
    assert report.port == 8080
    assert report.has_embedded_credentials is True
    assert "utm_source" in report.tracking_parameters_found
    assert report.risk_score >= 70
    assert "EMBEDDED_CREDENTIALS_IN_URL" in report.risk_indicators
    assert "RAW_IP_ADDRESS_HOSTNAME" in report.risk_indicators

def test_analyze_percent_encoded_and_embedded_redirect_url():
    """Tests percent-encoded URL containing an embedded redirect parameter."""
    raw_url = "https://paypa1-check.com/redirect?next_url=http%3A%2F%2Fmalicious-site.com%2Fpayload%2F%2F%2F%2F"
    report = URLIntelligenceEngine.analyze_url(raw_url)

    assert report.percent_encoding_count >= 5
    assert report.embedded_redirect_detected is True
    assert report.risk_score >= 35

def test_analyze_clean_https_url():
    """Tests clean HTTPS URL has low risk score."""
    raw_url = "https://paypal.com/signin"
    report = URLIntelligenceEngine.analyze_url(raw_url)

    assert report.protocol == "https"
    assert report.hostname == "paypal.com"
    assert report.risk_score == 0
    assert len(report.risk_indicators) == 0
