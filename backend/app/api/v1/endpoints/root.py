"""
GuardianAI System Root Metadata Endpoint
Purpose: Serves the system root welcome endpoint detailing API status, OpenAPI documentation links, and versioning info.
"""

from fastapi import APIRouter, Request
from app.core.config import settings
from app.core.response import success_response

router = APIRouter()

@router.get("/", summary="System Root Meta Information")
def get_root_info(request: Request):
    """Returns application name, status, environment, and interactive documentation URLs."""
    info = {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "online",
        "environment": settings.ENVIRONMENT,
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "health_url": f"{settings.API_V1_STR}/health",
        "readiness_url": f"{settings.API_V1_STR}/ready",
        "version_url": f"{settings.API_V1_STR}/version"
    }
    return success_response(data=info, message=f"Welcome to {settings.PROJECT_NAME} API Engine", request=request)
