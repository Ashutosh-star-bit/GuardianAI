"""
GuardianAI Feature Flag REST API Endpoints
Endpoints:
  - GET /api/v1/feature-flags        : List all active feature flags
  - PUT /api/v1/feature-flags/{key}  : Toggle feature flag status
"""

from typing import List, Dict, Any
from fastapi import APIRouter, status, Query, Body, HTTPException
from app.core.feature_flags import feature_flag_service, FeatureKey, FeatureFlagDefinition
from app.schemas.response import APIResponse

router = APIRouter(prefix="/feature-flags", tags=["Feature Flags"])

@router.get(
    "",
    response_model=APIResponse[List[FeatureFlagDefinition]],
    status_code=status.HTTP_200_OK,
    summary="List All Platform Feature Flags"
)
async def list_feature_flags():
    """Retrieves all feature flag definitions and current enablement status."""
    flags = feature_flag_service.get_all_flags()
    return APIResponse(
        success=True,
        message=f"Retrieved {len(flags)} platform feature flag definitions.",
        data=flags
    )

@router.put(
    "/{feature_key}",
    response_model=APIResponse[FeatureFlagDefinition],
    status_code=status.HTTP_200_OK,
    summary="Toggle Feature Flag Status (Enable / Disable)"
)
async def toggle_feature_flag(
    feature_key: FeatureKey,
    is_enabled: bool = Query(..., description="Target status: True (Enabled), False (Disabled)")
):
    """Updates feature flag status at runtime with sub-0.1ms thread safety."""
    try:
        updated_flag = feature_flag_service.set_feature_status(feature_key, is_enabled)
        return APIResponse(
            success=True,
            message=f"Feature flag '{feature_key}' status updated to {is_enabled}.",
            data=updated_flag
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
