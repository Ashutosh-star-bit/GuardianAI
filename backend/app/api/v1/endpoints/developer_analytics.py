"""
GuardianAI Developer API Usage Analytics REST Endpoints
Endpoints:
  - GET /api/v1/developer/analytics : Developer API Usage Telemetry Summary
"""

from typing import Dict, Any, Optional
from fastapi import APIRouter, status, Security
from app.developer_platform.usage_analytics import developer_usage_analytics
from app.api.deps import get_current_user_optional
from app.models.user import User
from app.schemas.response import APIResponse

router = APIRouter(prefix="/developer", tags=["Developer Platform Analytics"])

@router.get(
    "/analytics",
    response_model=APIResponse[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
    summary="Retrieve Developer API Usage Telemetry Summary"
)
async def get_developer_api_analytics(
    current_user: Optional[User] = Security(get_current_user_optional)
):
    """Retrieves real-time telemetry for requests, latency, errors, tokens, and bandwidth."""
    metrics = developer_usage_analytics.get_developer_analytics_summary()
    return APIResponse(
        success=True,
        message="Retrieved developer API usage telemetry successfully.",
        data=metrics
    )
