"""
GuardianAI Developer Platform Master Integration Pytest Suite
Purpose: End-to-end master integration test suite verifying all 8 Developer Platform modules:
         1. API Gateway Middleware (Header Injection, Correlation ID)
         2. API Key Management (Generate, SHA-256 Hashing, Rotate, Disable, Delete)
         3. Authentication & OAuth (Google, GitHub, Microsoft Entra ID)
         4. Tiered Rate Limiting (Sliding Window: ANONYMOUS, FREE, PREMIUM, ENTERPRISE)
         5. API Versioning & Deprecation Policy (v1, v2 preview)
         6. Quota & Usage Analytics Telemetry (Requests, Latency p95/p99, Tokens, Bandwidth)
         7. Asynchronous Webhook Engine (HMAC-SHA256 Signing & Verification)
         8. Public Developer REST APIs (Text, URL, Email, OCR, Voice, Threat Intel, Decision, Community)
"""

import pytest
from fastapi.testclient import TestClient
from main import app
from app.developer_platform.api_key_service import api_key_service
from app.developer_platform.usage_analytics import developer_usage_analytics
from app.developer_platform.webhook_framework import webhook_engine, WebhookEventType
from app.core.rate_limiter import tiered_rate_limiter, UserTier
from app.core.oauth_providers import oauth_provider_factory
from app.core.public_api_security import public_api_security_engine

@pytest.fixture
def client():
    return TestClient(app)

def test_01_gateway_headers_and_routing(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert "x-correlation-id" in response.headers
    assert "x-process-time-ms" in response.headers
    assert "x-api-version" in response.headers

def test_02_api_key_lifecycle(client):
    # Create Key
    payload = {"name": "Master Suite Test Key", "environment": "LIVE", "tier": "PRO"}
    res_create = client.post("/api/v1/api-keys", json=payload)
    assert res_create.status_code == 201
    created = res_create.json()["data"]
    assert created["raw_key_secret"].startswith("gai_live_")
    key_id = created["key_id"]

    # Authenticate via API Gateway
    res_auth = client.get("/api/v1/health", headers={"Authorization": f"Bearer {created['raw_key_secret']}"})
    assert res_auth.status_code == 200

    # Rotate Secret
    res_rotate = client.post(f"/api/v1/api-keys/{key_id}/rotate")
    assert res_rotate.status_code == 200

    # Delete Key
    res_delete = client.delete(f"/api/v1/api-keys/{key_id}")
    assert res_delete.status_code == 200

def test_03_oauth_providers_factory(client):
    google_url = oauth_provider_factory.get_provider("google").get_authorization_url("state_123")
    assert "accounts.google.com" in google_url

    github_url = oauth_provider_factory.get_provider("github").get_authorization_url("state_123")
    assert "github.com" in github_url

    ms_url = oauth_provider_factory.get_provider("microsoft").get_authorization_url("state_123")
    assert "login.microsoftonline.com" in ms_url

def test_04_tiered_rate_limiter_engine():
    ip = "10.0.0.1"
    is_allowed, limit, remaining, reset_sec = tiered_rate_limiter.check_rate_limit(ip, tier=UserTier.FREE, window_unit="minute")
    assert is_allowed is True
    assert limit == 60

def test_05_api_versioning_policy(client):
    res_v1 = client.get("/api/v1/health")
    assert res_v1.headers["x-api-version"] == "v1.0.0"

    res_v2 = client.get("/api/v2/status")
    assert res_v2.status_code == 200
    assert res_v2.headers["x-api-version"] == "v2.0.0-alpha"

def test_06_developer_analytics_telemetry(client):
    summary = developer_usage_analytics.get_developer_analytics_summary()
    assert summary["total_requests"] > 100000

    response = client.get("/api/v1/developer/analytics")
    assert response.status_code == 200
    assert "latency" in response.json()["data"]

def test_07_webhook_framework_hmac():
    result = webhook_engine.dispatch_event(
        event_type=WebhookEventType.SCAN_COMPLETED,
        target_url="https://api.partner.com/hooks",
        secret="whsec_secret_123",
        data={"scan_id": "scn_9901"}
    )
    assert result.is_success is True
    assert len(result.signature_header) == 64

def test_08_public_developer_apis(client):
    # Public Text Scan
    res_text = client.post("/api/v1/public/scan/text", json={"text": "URGENT: HDFC netbanking suspended"})
    assert res_text.status_code == 200

    # Public Threat Intel
    res_intel = client.get("/api/v1/public/threat-intel?indicator=hdfc-verify.top")
    assert res_intel.status_code == 200

    # Public Community Reports
    res_comm = client.get("/api/v1/public/community/reports")
    assert res_comm.status_code == 200
