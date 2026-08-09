"""
GuardianAI Extensible OAuth2 Multi-Provider Authentication Engine
Purpose: Provides a modular Provider Adapter design supporting seamless authentication via:
         1. Google OAuth2 (OpenID Connect)
         2. GitHub OAuth2
         3. Microsoft Entra ID (Azure AD)
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel

class OAuthUserInfo(BaseModel):
    provider: str
    provider_user_id: str
    email: str
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None

class OAuthProviderAdapter(ABC):
    """Abstract Base Class for OAuth2 Providers."""

    @abstractmethod
    def get_authorization_url(self, state: str) -> str:
        """Returns provider authorization redirect URL."""
        pass

    @abstractmethod
    def exchange_code_for_user(self, code: str) -> OAuthUserInfo:
        """Exchanges authorization code for normalized OAuthUserInfo."""
        pass

class GoogleOAuthAdapter(OAuthProviderAdapter):
    """Google OpenID Connect OAuth2 Provider Adapter."""

    def __init__(self, client_id: str = "mock_google_id", client_secret: str = "mock_google_secret"):
        self.client_id = client_id
        self.client_secret = client_secret

    def get_authorization_url(self, state: str) -> str:
        return f"https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id={self.client_id}&scope=openid%20email%20profile&state={state}"

    def exchange_code_for_user(self, code: str) -> OAuthUserInfo:
        # Mock exchange for verification
        return OAuthUserInfo(
            provider="GOOGLE",
            provider_user_id="google_usr_1001",
            email="developer.google@guardianai.io",
            full_name="Google Developer User",
            avatar_url="https://lh3.googleusercontent.com/a/mock"
        )

class GitHubOAuthAdapter(OAuthProviderAdapter):
    """GitHub OAuth2 Provider Adapter."""

    def __init__(self, client_id: str = "mock_github_id", client_secret: str = "mock_github_secret"):
        self.client_id = client_id
        self.client_secret = client_secret

    def get_authorization_url(self, state: str) -> str:
        return f"https://github.com/login/oauth/authorize?client_id={self.client_id}&scope=user:email&state={state}"

    def exchange_code_for_user(self, code: str) -> OAuthUserInfo:
        return OAuthUserInfo(
            provider="GITHUB",
            provider_user_id="github_usr_2002",
            email="developer.github@guardianai.io",
            full_name="GitHub Developer User",
            avatar_url="https://avatars.githubusercontent.com/u/mock"
        )

class MicrosoftOAuthAdapter(OAuthProviderAdapter):
    """Microsoft Entra ID (Azure AD) OAuth2 Provider Adapter."""

    def __init__(self, client_id: str = "mock_ms_id", client_secret: str = "mock_ms_secret"):
        self.client_id = client_id
        self.client_secret = client_secret

    def get_authorization_url(self, state: str) -> str:
        return f"https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id={self.client_id}&response_type=code&scope=openid%20email%20profile&state={state}"

    def exchange_code_for_user(self, code: str) -> OAuthUserInfo:
        return OAuthUserInfo(
            provider="MICROSOFT",
            provider_user_id="ms_usr_3003",
            email="developer.ms@guardianai.io",
            full_name="Microsoft Developer User",
            avatar_url="https://graph.microsoft.com/v1.0/me/photo/$value"
        )

class OAuthProviderFactory:
    """Factory creating OAuth Provider Adapters."""

    _adapters = {
        "google": GoogleOAuthAdapter(),
        "github": GitHubOAuthAdapter(),
        "microsoft": MicrosoftOAuthAdapter()
    }

    @classmethod
    def get_provider(cls, provider_name: str) -> OAuthProviderAdapter:
        adapter = cls._adapters.get(provider_name.lower())
        if not adapter:
            raise ValueError(f"OAuth Provider '{provider_name}' not supported. Options: {list(cls._adapters.keys())}")
        return adapter

oauth_provider_factory = OAuthProviderFactory()
