"""
GuardianAI Health, Readiness & Version Diagnostic Endpoints
Purpose: Implements Liveness Probe (/health), Deep Readiness Probe (/ready), and Versioning info (/version).
"""

import sys
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.health import check_database_health
from app.core.config import settings
from app.core.response import success_response, error_response

router = APIRouter()
START_TIME = datetime.now(timezone.utc)

@router.get("/health", summary="System Liveness Health Probe")
def health_liveness_check(request: Request):
    """
    Liveness Health Check Endpoint.
    Returns overall system status, uptime duration in seconds, service version, and environment mode.
    """
    uptime_seconds = int((datetime.now(timezone.utc) - START_TIME).total_seconds())
    payload = {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "uptime_seconds": uptime_seconds,
        "start_time": START_TIME.isoformat()
    }
    return success_response(data=payload, message="System is operational.", request=request)

@router.get("/ready", summary="Deep Kubernetes Readiness Diagnostic Probe")
def health_readiness_check(request: Request, db: Session = Depends(get_db)):
    """
    Deep Readiness Diagnostic Endpoint.
    Executes SELECT 1 query on database engine, measuring query latency and connection pool viability.
    Returns HTTP 200 OK when ready or HTTP 503 Service Unavailable when degraded.
    """
    db_health = check_database_health(db)
    is_ready = db_health.get("status") == "healthy"

    payload = {
        "status": "ready" if is_ready else "degraded",
        "service": settings.PROJECT_NAME,
        "components": {
            "database": db_health
        }
    }

    if is_ready:
        return success_response(data=payload, message="Service is ready to handle traffic.", request=request)
    else:
        return error_response(
            message="Service is degraded. Database connection failed.",
            errors=[db_health],
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            request=request
        )

@router.get("/version", summary="System Version & Runtime Info")
def get_system_version(request: Request):
    """
    Returns system build version, Python runtime version, SLA guarantees, and environment configuration.
    """
    payload = {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "python_version": sys.version.split()[0],
        "api_prefix": settings.API_V1_STR,
        "sla_target": "sub-1.8s response time",
        "privacy_certification": "Zero-Knowledge Certified"
    }
    return success_response(data=payload, message="Version info retrieved.", request=request)
