"""
GuardianAI Decision Engine REST API Endpoints Unit Test Suite
Purpose: Tests all 3 decision REST API endpoints (/decision/analyse, /decision/explain, /decision/report).
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
        id="usr_test_dec",
        email="test.user@guardianai.io",
        full_name="Test User",
        hashed_password="hashed_password",
        is_active=True
    )

app.dependency_overrides[get_current_user] = mock_get_current_user

def test_decision_analyse_endpoint():
    """Tests POST /api/v1/decision/analyse endpoint."""
    res = client.post(
        "/api/v1/decision/analyse",
        json={
            "message": "URGENT: Your PayPal account is suspended. Verify at http://paypa1-check.top or send $500 to support.refund@okaxis",
            "channel_type": "SMS",
            "target_persona": "SENIOR_CITIZENS",
            "locale": "en"
        }
    )
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["final_scam_probability"] >= 50
    assert data["risk_level"] in ["HIGH", "CRITICAL"]
    assert len(data["evidence"]) > 0
    assert len(data["action_plan"]) > 0

def test_decision_explain_endpoint():
    """Tests POST /api/v1/decision/explain endpoint."""
    res = client.post(
        "/api/v1/decision/explain",
        json={
            "risk_level": "CRITICAL",
            "confidence": 0.98,
            "evidence_list": ["paypa1-check.top typosquatting link"],
            "target_persona": "SENIOR_CITIZENS"
        }
    )
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["active_persona"] == "SENIOR_CITIZENS"
    assert "CAUTION: This message looks like a scam attempt" in data["primary_explanation"]["risk_summary"]

def test_decision_report_endpoint():
    """Tests POST /api/v1/decision/report endpoint."""
    res = client.post(
        "/api/v1/decision/report",
        json={
            "message": "URGENT: Verify at http://paypa1-check.top",
            "channel_type": "SMS",
            "target_persona": "SENIOR_CITIZENS",
            "locale": "en"
        }
    )
    assert res.status_code == 200
    data = res.json()["data"]
    assert "decision" in data
    assert "text_intelligence_summary" in data
    assert "threat_intelligence_summary" in data
