"""
GuardianAI Threat Intelligence REST API Endpoints Unit Test Suite
Purpose: Tests all 6 threat REST API endpoints (/threat/url, /threat/domain, /threat/email, /threat/phone, /threat/upi, /threat/analyse).
"""

import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app
from app.api.deps import get_current_user
from app.models.user import User

client = TestClient(app)

def mock_get_current_user():
    return User(
        id="usr_test_999",
        email="test.user@guardianai.io",
        full_name="Test User",
        hashed_password="hashed_password",
        is_active=True
    )

app.dependency_overrides[get_current_user] = mock_get_current_user

def test_threat_url_endpoint():
    """Tests POST /api/v1/threat/url endpoint."""
    res = client.post(
        "/api/v1/threat/url",
        json={"url": "http://admin:secret@192.168.1.1:8080/login/secure"}
    )
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["is_ip_address"] is True
    assert data["port"] == 8080
    assert data["has_embedded_credentials"] is True

def test_threat_domain_endpoint():
    """Tests POST /api/v1/threat/domain endpoint."""
    res = client.post(
        "/api/v1/threat/domain",
        json={"domain": "sub.verify.paypa1-check.top"}
    )
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["tld"] == ".top"
    assert data["typosquatting_detected"] is True
    assert data["impersonated_brand_candidate"] == "paypal"

def test_threat_email_endpoint():
    """Tests POST /api/v1/threat/email endpoint."""
    res = client.post(
        "/api/v1/threat/email",
        json={"email_header": '"CEO John Smith" <john.smith@gmail.com>'}
    )
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["spoofing_detected"] is True
    assert data["impersonated_title_or_brand"] == "CEO"

def test_threat_phone_endpoint():
    """Tests POST /api/v1/threat/phone endpoint."""
    res = client.post(
        "/api/v1/threat/phone",
        json={"phone_number": "+1 (900) 555-9999"}
    )
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["is_premium_rate"] is True

def test_threat_upi_endpoint():
    """Tests POST /api/v1/threat/upi endpoint."""
    res = client.post(
        "/api/v1/threat/upi",
        json={"upi_id": "support.refund@okaxis"}
    )
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["has_suspicious_naming"] is True
    assert data["psp_provider_name"] == "Google Pay"

def test_threat_analyse_endpoint():
    """Tests POST /api/v1/threat/analyse endpoint."""
    res = client.post(
        "/api/v1/threat/analyse",
        json={"text": "URGENT: Your PayPal account is suspended! Update at http://paypa1-check.top or send $500 to support.refund@okaxis"}
    )
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["scoring_result"]["technical_risk_score"] >= 50
    assert len(data["evidence_report"]["evidence_list"]) > 0
