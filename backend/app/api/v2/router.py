"""
GuardianAI API v2 Router Placeholder & Future Subsystem Gateway
Purpose: Future major version API v2 router supporting streaming WebSocket scan responses,
         enhanced multi-modal graph payloads, and backward-compatible fallbacks.
"""

from fastapi import APIRouter, status
from app.schemas.response import APIResponse

api_v2_router = APIRouter(prefix="/v2", tags=["API v2 (Preview)"])

@api_v2_router.get(
    "/status",
    response_model=APIResponse[dict],
    status_code=status.HTTP_200_OK,
    summary="API v2 Preview Health Probe"
)
async def get_v2_status():
    """Health probe for API v2 preview features."""
    return APIResponse(
        success=True,
        message="GuardianAI API v2 (Preview) is operational.",
        data={
            "version": "v2.0.0-alpha",
            "supported_features": ["streaming_scans", "graph_xai", "grpc_tunneling"]
        }
    )
