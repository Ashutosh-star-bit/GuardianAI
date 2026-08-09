"""
GuardianAI OAuth2 REST Endpoints
Endpoints:
  - GET  /api/v1/oauth/authorize/{provider}  : Generate Authorization Redirect URL
  - POST /api/v1/oauth/callback/{provider}   : Exchange Code for JWT Session Token
"""

import uuid
from typing import Dict, Any
from fastapi import APIRouter, status, HTTPException, Query, Body
from app.core.oauth_providers import oauth_provider_factory
from app.schemas.response import APIResponse

router = APIRouter(prefix="/oauth", tags=["OAuth Authentication"])

@router.get(
    "/authorize/{provider}",
    response_model=APIResponse[Dict[str, str]],
    status_code=status.HTTP_200_OK,
    summary="Generate OAuth Provider Authorization Redirect URL"
)
async def get_oauth_authorization_url(provider: str):
    """Generates provider authorization URL (Google, GitHub, Microsoft)."""
    try:
        adapter = oauth_provider_factory.get_provider(provider)
        state = f"st_{uuid.uuid4().hex[:16]}"
        auth_url = adapter.get_authorization_url(state=state)
        return APIResponse(
            success=True,
            message=f"Generated authorization URL for {provider.upper()}.",
            data={"provider": provider.upper(), "auth_url": auth_url, "state": state}
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post(
    "/callback/{provider}",
    response_model=APIResponse[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
    summary="Exchange OAuth Code for Session JWT"
)
async def process_oauth_callback(
    provider: str,
    code: str = Query(..., description="Authorization code returned by provider")
):
    """Exchanges code for normalized user profile and issues JWT access token."""
    try:
        adapter = oauth_provider_factory.get_provider(provider)
        user_info = adapter.exchange_code_for_user(code)

        # Mock JWT Token Generation for OAuth Login
        mock_jwt = f"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.oauth_{user_info.provider_user_id}.sig"

        return APIResponse(
            success=True,
            message=f"OAuth authentication successful via {provider.upper()}.",
            data={
                "access_token": mock_jwt,
                "token_type": "Bearer",
                "user": user_info.model_dump()
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
