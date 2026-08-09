"""
GuardianAI Community REST API Endpoints Pytest Suite
"""

import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_submit_report_api(client):
    payload = {
        "title": "Fake Police Digital Arrest Call",
        "description": "Caller impersonated CBI officer demanding money transfer to clear charges",
        "scam_category": "DIGITAL_ARREST",
        "target_persona": "SENIOR_CITIZENS"
    }

    response = client.post("/api/v1/community/report", json=payload)
    assert response.status_code == 201
    res = response.json()
    assert res["success"] is True
    assert res["data"]["title"] == "Fake Police Digital Arrest Call"
    assert res["data"]["status"] == "PENDING"

def test_list_reports_api(client):
    response = client.get("/api/v1/community/reports")
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True
    assert isinstance(res["data"], list)

def test_vote_on_report_api(client):
    # First submit report
    rep_res = client.post("/api/v1/community/report", json={
        "title": "Phishing SMS Scam Link",
        "description": "Text claiming account blocked with link http://bank-update.top",
        "scam_category": "PHISHING_URL"
    })
    rep_id = rep_res.json()["data"]["report_id"]

    # Vote on report
    vote_res = client.post("/api/v1/community/vote", json={
        "report_id": rep_id,
        "vote_type": "UPVOTE"
    })
    assert vote_res.status_code == 200
    res = vote_res.json()
    assert res["data"]["upvote_count"] == 1

def test_ai_feedback_api(client):
    fb_res = client.post("/api/v1/community/feedback", json={
        "report_id": "rep_100",
        "predicted_risk_level": "SAFE",
        "feedback_type": "FALSE_NEGATIVE",
        "correction_reason": "Missed digital arrest scam pattern"
    })
    assert fb_res.status_code == 200
    res = fb_res.json()
    assert res["success"] is True

    # GET feedback list
    get_res = client.get("/api/v1/community/feedback")
    assert get_res.status_code == 200
    assert len(get_res.json()["data"]) > 0

def test_trending_scams_api(client):
    response = client.get("/api/v1/community/trending")
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True
    assert "total_active_reports" in res["data"]
    assert "top_scam_categories" in res["data"]
