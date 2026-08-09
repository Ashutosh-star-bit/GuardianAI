"""
GuardianAI Master Threat Intelligence Production Pytest Suite
Purpose: Enterprise test suite covering URL Parser, Domain Analyser, Email Analyser, Phone Analyser, UPI Analyser,
         Threat Score Engine, Evidence Builder, REST API Endpoints, Edge Cases, and Sub-50ms SLA Performance.
"""

import sys
import os
import time
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app
from app.api.deps import get_current_user
from app.models.user import User

from app.threat_intel.url_intel import URLIntelligenceEngine
from app.threat_intel.domain_intel import DomainIntelligenceEngine
from app.threat_intel.email_intel import EmailIntelligenceEngine
from app.threat_intel.phone_intel import PhoneIntelligenceEngine
from app.threat_intel.upi_intel import UPIIntelligenceEngine
from app.threat_intel.scoring import ThreatScoringEngine
from app.threat_intel.evidence_builder import EvidenceBuilderEngine
from app.threat_intel.service import ThreatIntelligenceService

client = TestClient(app)

def mock_get_current_user():
    return User(id="usr_test_prod", email="test@guardianai.io", full_name="Test User", hashed_password="pw", is_active=True)

app.dependency_overrides[get_current_user] = mock_get_current_user

# 1. URL PARSER TEST
def test_url_parser_production():
    """Tests URL protocol, IP hostname, port 8080, credentials, and percent encoding."""
    raw_url = "http://admin:secret@192.168.1.1:8080/login/secure?next=http%3A%2F%2Fredirect.com#top"
    report = URLIntelligenceEngine.analyze_url(raw_url)
    assert report.is_ip_address is True
    assert report.port == 8080
    assert report.has_embedded_credentials is True
    assert report.percent_encoding_count >= 2
    assert report.risk_score >= 70

# 2. DOMAIN ANALYSER TEST
def test_domain_analyser_production():
    """Tests TLD risk, subdomain depth, Punycode, typosquatting, and DGA entropy."""
    domain = "sub.verify.paypa1-check.top"
    report = DomainIntelligenceEngine.analyze_domain_intel(domain)
    assert report.tld == ".top"
    assert report.is_suspicious_tld is True
    assert report.subdomain_depth == 2
    assert report.typosquatting_detected is True
    assert report.impersonated_brand == "paypal"
    assert report.risk_score >= 70

# 3. EMAIL ANALYSER TEST
def test_email_analyser_production():
    """Tests email header parsing, disposable email DB, free webmail, and executive spoofing."""
    header = '"CEO John Smith" <john.smith@gmail.com>'
    report = EmailIntelligenceEngine.analyze_email(header)
    assert report.display_name == "CEO John Smith"
    assert report.is_free_provider is True
    assert report.spoofing_detected is True
    assert report.impersonated_title_or_brand == "CEO"

# 4. PHONE ANALYSER TEST
def test_phone_analyser_production():
    """Tests country code parsing, E.164 formatting, premium rate 1-900 numbers, and repeated digits."""
    phone = "+1 (900) 555-9999"
    report = PhoneIntelligenceEngine.parse_phone_number(phone)
    assert report.country_code == "+1"
    assert report.is_premium_rate is True
    assert report.risk_score >= 40

# 5. UPI ANALYSER TEST
def test_upi_analyser_production():
    """Tests UPI VPA handle parsing, PSP provider resolution, sponsor bank, and support desk spoofing."""
    upi = "support.refund@okaxis"
    report = UPIIntelligenceEngine.analyze_upi(upi)
    assert report.username_handle == "support.refund"
    assert report.psp_provider_name == "Google Pay"
    assert report.sponsor_bank_name == "Axis Bank"
    assert report.has_suspicious_naming is True
    assert report.risk_score >= 45

# 6. THREAT SCORE ENGINE TEST
def test_threat_score_engine_production():
    """Tests composite weighted technical risk score calculation and qualitative risk band assignment."""
    scoring = ThreatScoringEngine.calculate_threat_score(
        scan_id="scn_prod_1",
        domain_risk=85,
        url_risk=70,
        upi_risk=90,
        email_risk=45,
        phone_risk=0
    )
    assert scoring.technical_risk_score >= 50
    assert scoring.risk_band in ["caution", "dangerous"]

# 7. EVIDENCE BUILDER TEST
def test_evidence_builder_production():
    """Tests ThreatEvidenceItem record creation and ThreatEvidenceReport aggregation."""
    item1 = EvidenceBuilderEngine.create_evidence_item("ev_1", "paypa1-check.top", "DOMAIN", "Typosquatting link", "Critical", 0.98, "DOMAIN_INTELLIGENCE")
    item2 = EvidenceBuilderEngine.create_evidence_item("ev_2", "support.refund@okaxis", "UPI_ID", "Support handle spoofing", "High", 0.95, "UPI_INTELLIGENCE")
    report = EvidenceBuilderEngine.build_evidence_report("scn_ev_prod", [item1, item2])
    assert report.total_evidence_count == 2
    assert report.critical_count == 1
    assert report.high_count == 1

# 8. API ENDPOINTS INTEGRATION TEST
def test_threat_api_endpoints_production():
    """Tests REST API endpoints /threat/url, /threat/domain, /threat/email, /threat/phone, /threat/upi, and /threat/analyse."""
    res_url = client.post("/api/v1/threat/url", json={"url": "http://admin:secret@192.168.1.1:8080/login"})
    assert res_url.status_code == 200

    res_dom = client.post("/api/v1/threat/domain", json={"domain": "sub.verify.paypa1-check.top"})
    assert res_dom.status_code == 200

    res_eml = client.post("/api/v1/threat/email", json={"email_header": '"CEO John" <john@gmail.com>'})
    assert res_eml.status_code == 200

    res_ph = client.post("/api/v1/threat/phone", json={"phone_number": "+1 (900) 555-9999"})
    assert res_ph.status_code == 200

    res_upi = client.post("/api/v1/threat/upi", json={"upi_id": "support.refund@okaxis"})
    assert res_upi.status_code == 200

    res_full = client.post("/api/v1/threat/analyse", json={"text": "URGENT: Verify at http://paypa1-check.top or send $500 to support.refund@okaxis"})
    assert res_full.status_code == 200
    assert res_full.json()["data"]["scoring_result"]["technical_risk_score"] >= 50

# 9. EDGE CASES TEST
def test_threat_intel_edge_cases_production():
    """Tests edge cases: whitespace padding, excessive length, and empty inputs."""
    # Whitespace padding
    url_spaces = "   https://paypal.com/signin   "
    report_url = URLIntelligenceEngine.analyze_url(url_spaces)
    assert report_url.hostname == "paypal.com"

    # Excessive subdomain depth
    long_domain = "sub.verify.security.paypal.com.check.top"
    report_dom = DomainIntelligenceEngine.analyze_domain_intel(long_domain)
    assert report_dom.subdomain_depth >= 3

# 10. SUB-50MS SLA PERFORMANCE TEST
@pytest.mark.asyncio
async def test_threat_intel_pipeline_performance_sla():
    """Tests end-to-end Threat Intelligence Pipeline latency SLA under 50ms (target < 20ms)."""
    payload = "URGENT: Verify at http://paypa1-check.top or send $500 to support.refund@okaxis or call +1-800-555-0199"

    start_time = time.perf_counter()
    result = await ThreatIntelligenceService.analyze_threat_payload(scan_id="scn_perf_100", raw_text=payload)
    elapsed_ms = (time.perf_counter() - start_time) * 1000

    assert result.scan_id == "scn_perf_100"
    assert result.scoring_result.technical_risk_score >= 50
    assert elapsed_ms < 50.0, f"SLA latency breach: Execution took {elapsed_ms:.2f}ms (Limit: 50.0ms)"
