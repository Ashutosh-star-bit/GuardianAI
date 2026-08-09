"""
GuardianAI OAuth Multi-Provider Pytest Suite
"""

import pytest
from fastapi.testclient import TestClient
from main import app
from app.core.oauth_providers import oauth_provider_factory

@pytest.fixture
def client():
    return TestClient(app)

def test_oauth_factory_providers():
    google = oauth_provider_factory.get_provider("google")
    assert "accounts.google.com" in google.get_authorization_url("state_123")

    github = oauth_provider_factory.get_provider("github")
    assert "github.com" in github.get_authorization_url("state_123")

    ms = oauth_provider_factory.get_provider("microsoft")
    assert "login.microsoftonline.com" in ms.get_authorization_url("state_123")

def test_oauth_unsupported_provider():
    with pytest.raises(ValueError):
        oauth_provider_factory.get_provider("unsupported_provider")

def test_oauth_authorize_api(client):
    response = client.get("/api/v1/oauth/authorize/google")
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True
    assert "accounts.google.com" in res["data"]["auth_url"]

def test_oauth_callback_api(client):
    response = client.post("/api/v1/oauth/callback/github?code=mock_code_123")
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True
    assert "access_token" in res["data"]
    assert res["data"]["user"]["provider"] == "GITHUB"
