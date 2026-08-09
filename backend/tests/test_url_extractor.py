"""
GuardianAI URL Extractor Unit Test Suite
Purpose: Tests extraction of Full URLs, Short URLs, Domains, Subdomains, Protocols, Paths, and Query Parameters.
"""

import pytest
from app.nlp.url_extractor import URLExtractorEngine, ParsedURLComponents

def test_parse_complex_url_components():
    """Tests parsing a full URL with subdomain, port, path, query params, and fragment."""
    raw = "https://sub.paypa1-check.com:8080/verify/login?user=123&token=abc#section"
    parsed: ParsedURLComponents = URLExtractorEngine.parse_url_components(raw)

    assert parsed is not None
    assert parsed.protocol == "https"
    assert parsed.domain == "sub.paypa1-check.com"
    assert parsed.subdomain == "sub"
    assert parsed.root_domain == "paypa1-check.com"
    assert parsed.port == 8080
    assert parsed.path == "/verify/login"
    assert parsed.query_params["user"] == ["123"]
    assert parsed.query_params["token"] == ["abc"]
    assert parsed.fragment == "section"
    assert parsed.is_shortened is False

def test_shortened_url_detection():
    """Tests URL shortener detection for bit.ly and t.me."""
    raw_bitly = "http://bit.ly/3xXz9"
    parsed = URLExtractorEngine.parse_url_components(raw_bitly)
    assert parsed.is_shortened is True
    assert parsed.domain == "bit.ly"

def test_extract_embedded_urls_from_text():
    """Tests extracting multiple embedded URLs from a scam message."""
    text = (
        "URGENT: Click http://sub.paypa1-check.com/login?token=xyz or "
        "short link bit.ly/3xXz9 to claim prize!"
    )
    urls = URLExtractorEngine.extract_urls(text)
    assert len(urls) == 2
    domains = [u.root_domain for u in urls]
    assert "paypa1-check.com" in domains
    assert "bit.ly" in domains
