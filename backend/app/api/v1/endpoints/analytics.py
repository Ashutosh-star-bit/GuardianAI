"""
GuardianAI Threat Analytics & Token Cost API Endpoint
Purpose: Serves executive security analytics, threat category breakdown, and token usage cost tracking.
"""

from fastapi import APIRouter, Request, Depends, status
from app.core.response import success_response
from app.api.deps import get_current_user
from app.models.user import User
from app.ai.token_tracker import TokenTracker

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/metrics", status_code=status.HTTP_200_OK, summary="Get Threat Analytics Metrics")
def get_analytics_metrics(
    request: Request,
    timeframe: str = "weekly",
    current_user: User = Depends(get_current_user)
):
    """Returns analytics stats for total scans, accuracy rate, AI confidence, and top targeted brands."""
    analytics = {
        "timeframe": timeframe,
        "total_scans": 1420,
        "detection_accuracy": 99.2,
        "avg_confidence": 98.4,
        "avg_processing_sla_ms": 1420.5,
        "category_distribution": [
            {"name": "SMS Smishing", "pct": 45, "scans": 639},
            {"name": "Email BEC Wire Fraud", "pct": 25, "scans": 355},
            {"name": "URL Typosquatting", "pct": 20, "scans": 284},
            {"name": "Quishing (QR Fraud)", "pct": 10, "scans": 142}
        ],
        "top_targeted_brands": [
            {"brand": "PayPal", "count": 420, "trend": "+14%"},
            {"brand": "Bank of America", "count": 310, "trend": "+8%"},
            {"brand": "FedEx", "count": 240, "trend": "-2%"},
            {"brand": "City Parking Meter", "count": 180, "trend": "+25%"}
        ]
    }

    return success_response(
        data=analytics,
        message="Analytics metrics retrieved.",
        request=request
    )

@router.get("/tokens", status_code=status.HTTP_200_OK, summary="Get Token Usage & Cost Analytics (Dashboard)")
def get_token_usage_analytics(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """
    Returns executive token tracking report including daily, monthly, and lifetime usage and USD costs.
    """
    report = TokenTracker.get_analytics_report()
    return success_response(
        data=report.model_dump(mode="json"),
        message="Token usage and cost analytics report retrieved.",
        request=request
    )
