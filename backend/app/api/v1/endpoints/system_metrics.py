"""
GuardianAI Real-Time System Metrics REST Endpoints
"""

from typing import Dict, Any, Optional
from fastapi import APIRouter, status, Security
from app.core.system_metrics_collector import system_metrics_collector
from app.api.deps import get_current_user_optional
from app.models.user import User
from app.schemas.response import APIResponse

router = APIRouter(prefix="/system", tags=["System Metrics Telemetry"])

@router.get(
    "/metrics",
    response_model=APIResponse[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
    summary="Retrieve Real-Time Host & Application Telemetry Metrics"
)
async def get_system_realtime_metrics(
    current_user: Optional[User] = Security(get_current_user_optional)
):
    """Retrieves real-time CPU, RAM, Latency, Requests, Error rates, Tokens, and Scan counts."""
    metrics = system_metrics_collector.collect_realtime_metrics()
    return APIResponse(
        success=True,
        message="Retrieved system telemetry metrics successfully.",
        data=metrics
    )
