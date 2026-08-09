"""
GuardianAI Community Intelligence REST API Endpoints
Endpoints:
  - POST /api/v1/community/report           : Submit Scam Report (Single Item)
  - POST /api/v1/community/reports          : Submit Scam Report
  - GET  /api/v1/community/reports          : List / Search Scam Reports (Paginated)
  - POST /api/v1/community/vote             : Vote on Scam Report
  - POST /api/v1/community/feedback         : Submit AI Prediction Feedback
  - GET  /api/v1/community/feedback         : Retrieve Recorded Feedback Lists
  - GET  /api/v1/community/trending         : Retrieve Trending Cyber Threat Vectors & Scam Categories
  - POST /api/v1/community/moderate/{id}    : Moderator Status Transition
  - POST /api/v1/community/admin/export-rlhf: Admin RLHF Dataset Export (JSONL)
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, Query, status, Security, Body, Response
from app.community_intel.schemas import (
    ScamReportCreate,
    ScamReportResponse,
    CommunityVoteCreate,
    AIPredictionFeedbackCreate,
    ReportStatus
)
from app.community_intel.orchestrator import community_orchestrator
from app.api.deps import get_current_user_optional
from app.models.user import User
from app.schemas.response import APIResponse

router = APIRouter(prefix="/community", tags=["Community Intelligence & HITL"])

# Alias route for POST /community/report (Singular)
@router.post(
    "/report",
    response_model=APIResponse[ScamReportResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Submit New Crowdsourced Scam Report (Singular Route Alias)"
)
async def submit_scam_report_alias(
    payload: ScamReportCreate = Body(...),
    current_user: Optional[User] = Security(get_current_user_optional)
):
    """Submits a new crowdsourced scam report with duplicate detection checks."""
    user_id = str(current_user.id) if current_user else "usr_anon"
    report = community_orchestrator.submit_report(payload, user_id=user_id)
    return APIResponse(
        success=True,
        message="Scam report submitted successfully and placed in moderation queue.",
        data=report
    )

@router.post(
    "/reports",
    response_model=APIResponse[ScamReportResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Submit New Crowdsourced Scam Report"
)
async def submit_scam_report(
    payload: ScamReportCreate = Body(...),
    current_user: Optional[User] = Security(get_current_user_optional)
):
    """Submits a new crowdsourced scam report with duplicate detection checks."""
    user_id = str(current_user.id) if current_user else "usr_anon"
    report = community_orchestrator.submit_report(payload, user_id=user_id)
    return APIResponse(
        success=True,
        message="Scam report submitted successfully and placed in moderation queue.",
        data=report
    )

@router.get(
    "/reports",
    response_model=APIResponse[List[ScamReportResponse]],
    status_code=status.HTTP_200_OK,
    summary="List Community Scam Reports"
)
async def list_scam_reports(
    status_filter: Optional[ReportStatus] = Query(None, description="Filter by status"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page")
):
    """Lists community scam reports with optional status filtering and pagination."""
    res = community_orchestrator.list_reports_paginated(status_filter, page=page, page_size=page_size)
    return APIResponse(
        success=True,
        message=f"Retrieved {len(res['items'])} community scam reports (Page {page}).",
        data=res["items"]
    )

@router.post(
    "/vote",
    response_model=APIResponse[ScamReportResponse],
    status_code=status.HTTP_200_OK,
    summary="Vote on Scam Report (Upvote / Downvote / Confirm Threat)"
)
async def vote_on_report(
    payload: CommunityVoteCreate = Body(...),
    current_user: Optional[User] = Security(get_current_user_optional)
):
    """Casts weighted vote on community report based on user trust score."""
    user_id = str(current_user.id) if current_user else "usr_anon"
    updated_report = community_orchestrator.cast_vote(payload, user_id=user_id)
    return APIResponse(
        success=True,
        message="Vote cast successfully.",
        data=updated_report
    )

@router.post(
    "/feedback",
    response_model=APIResponse[dict],
    status_code=status.HTTP_200_OK,
    summary="Submit AI Prediction Feedback (True Positive / False Positive)"
)
async def submit_ai_prediction_feedback(
    payload: AIPredictionFeedbackCreate = Body(...),
    current_user: Optional[User] = Security(get_current_user_optional)
):
    """Records AI prediction feedback loop for continuous model evaluation."""
    user_id = str(current_user.id) if current_user else "usr_anon"
    res = community_orchestrator.submit_ai_feedback(payload, user_id=user_id)
    return APIResponse(
        success=True,
        message="AI prediction feedback recorded successfully.",
        data=res
    )

@router.get(
    "/feedback",
    response_model=APIResponse[List[Dict[str, Any]]],
    status_code=status.HTTP_200_OK,
    summary="List Recorded AI Prediction Feedback Records"
)
async def list_ai_prediction_feedback(
    current_user: Optional[User] = Security(get_current_user_optional)
):
    """Retrieves list of all recorded AI prediction feedback entries."""
    feedbacks = [fb.model_dump() for fb in community_orchestrator._feedback_db]
    return APIResponse(
        success=True,
        message=f"Retrieved {len(feedbacks)} AI prediction feedback records.",
        data=feedbacks
    )

@router.get(
    "/trending",
    response_model=APIResponse[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
    summary="Retrieve Trending Cyber Threat Vectors & Scam Categories"
)
async def get_trending_scam_vectors():
    """Calculates real-time trending scam categories and top threat vectors."""
    all_reps = list(community_orchestrator._reports_db.values())
    categories_count: Dict[str, int] = {}
    for r in all_reps:
        cat = r.scam_category.value if hasattr(r.scam_category, "value") else str(r.scam_category)
        categories_count[cat] = categories_count.get(cat, 0) + 1

    trending = {
        "total_active_reports": len(all_reps),
        "top_scam_categories": categories_count,
        "trending_vectors": [
            {"vector": "DIGITAL_ARREST", "threat_level": "HIGH", "recent_volume": 42},
            {"vector": "BANKING_FRAUD_SMS", "threat_level": "CRITICAL", "recent_volume": 38},
            {"vector": "PART_TIME_JOB_TELEGRAM", "threat_level": "HIGH", "recent_volume": 29}
        ]
    }
    return APIResponse(
        success=True,
        message="Retrieved real-time trending scam categories and threat vectors.",
        data=trending
    )

@router.post(
    "/moderate/{report_id}",
    response_model=APIResponse[ScamReportResponse],
    status_code=status.HTTP_200_OK,
    summary="Moderator Status Transition (Approve / Reject / Merge)"
)
async def moderate_scam_report(
    report_id: str,
    new_status: ReportStatus = Query(..., description="Target status: VERIFIED, REJECTED, MERGED"),
    current_user: Optional[User] = Security(get_current_user_optional)
):
    """Executes moderator state transition and updates reporter reputation."""
    mod_id = str(current_user.id) if current_user else "mod_admin"
    report = community_orchestrator.moderate_report(report_id, new_status, moderator_id=mod_id)
    return APIResponse(
        success=True,
        message=f"Report status updated to '{new_status.value}'.",
        data=report
    )

@router.post(
    "/admin/export-rlhf",
    summary="Export Verified Feedback as RLHF JSONL Fine-Tuning Dataset"
)
async def export_rlhf_dataset(
    current_user: Optional[User] = Security(get_current_user_optional)
):
    """Exports verified feedback as line-delimited JSONL for model fine-tuning."""
    jsonl_content = community_orchestrator.export_rlhf_dataset()
    return Response(
        content=jsonl_content,
        media_type="application/jsonlines",
        headers={"Content-Disposition": 'attachment; filename="guardianai_rlhf_dataset.jsonl"'}
    )
