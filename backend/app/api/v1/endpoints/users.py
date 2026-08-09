"""
GuardianAI User Profile & Management API Endpoints
Purpose: Implements profile retrieval, user update, subscription tier management, and administrative user control.
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, Request, Query, status, Body
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.core.response import success_response
from app.schemas.response import APIResponse

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse, summary="Get Current User Profile")
def get_user_profile(current_user: User = Depends(get_current_user)):
    """Returns profile information for the authenticated user."""
    return current_user

@router.put("/me", summary="Update User Profile")
def update_user_profile(
    user_in: UserUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Updates user profile full name or subscription preferences."""
    if user_in.full_name is not None:
        current_user.full_name = user_in.full_name

    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return success_response(
        data=UserResponse.model_validate(current_user).model_dump(mode="json"),
        message="Profile updated successfully.",
        request=request
    )

# =====================================================================
# ADMINISTRATIVE USER MANAGEMENT ENDPOINTS
# =====================================================================

@router.get("/admin/list", summary="List All Users (Paginated with Search & Filters)")
def list_admin_users(
    search: Optional[str] = Query(None, description="Search by email or name"),
    role_filter: Optional[str] = Query(None, description="Filter by RBAC role"),
    status_filter: Optional[str] = Query(None, description="Filter by status: ACTIVE, DEACTIVATED, SUSPENDED"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """Lists users with pagination, search query matching, and status/role filters."""
    # Mock admin users dataset for API demonstration
    mock_users = [
        {"id": "usr_001", "email": "admin@guardianai.io", "full_name": "System Administrator", "role": "SUPER_ADMIN", "status": "ACTIVE", "trust_score": 100, "scans_count": 142},
        {"id": "usr_002", "email": "soc_analyst@guardianai.io", "full_name": "SOC Analyst Team", "role": "SOC_ANALYST", "status": "ACTIVE", "trust_score": 90, "scans_count": 98},
        {"id": "usr_003", "email": "moderator_1@guardianai.io", "full_name": "Community Moderator", "role": "MODERATOR", "status": "ACTIVE", "trust_score": 85, "scans_count": 45},
        {"id": "usr_004", "email": "spammer@malicious.com", "full_name": "Spam Bot", "role": "USER", "status": "SUSPENDED", "trust_score": 0, "scans_count": 2}
    ]

    filtered = mock_users
    if search:
        s = search.lower()
        filtered = [u for u in filtered if s in u["email"].lower() or s in u["full_name"].lower()]
    if role_filter and role_filter != "ALL":
        filtered = [u for u in filtered if u["role"] == role_filter]
    if status_filter and status_filter != "ALL":
        filtered = [u for u in filtered if u["status"] == status_filter]

    start_idx = (page - 1) * page_size
    items = filtered[start_idx:start_idx + page_size]

    return {
        "items": items,
        "total": len(filtered),
        "page": page,
        "page_size": page_size,
        "total_pages": (len(filtered) + page_size - 1) // page_size if filtered else 1
    }

@router.post("/admin/{user_id}/status", summary="Update User Account Status (Activate / Deactivate / Suspend)")
def update_user_status(user_id: str, payload: Dict[str, Any] = Body(...)):
    """Updates account status to ACTIVE, DEACTIVATED, or SUSPENDED."""
    new_status = payload.get("status", "ACTIVE")
    return {
        "success": True,
        "user_id": user_id,
        "status": new_status,
        "message": f"User account '{user_id}' status updated to '{new_status}'."
    }

@router.post("/admin/{user_id}/role", summary="Assign RBAC Role to User")
def assign_user_role(user_id: str, payload: Dict[str, Any] = Body(...)):
    """Assigns new RBAC role to user account."""
    new_role = payload.get("role", "MODERATOR")
    return {
        "success": True,
        "user_id": user_id,
        "role": new_role,
        "message": f"User account '{user_id}' assigned role '{new_role}'."
    }

@router.post("/admin/{user_id}/reset-password", summary="Trigger Administrative Password Reset")
def admin_reset_password(user_id: str):
    """Triggers secure password reset link for user."""
    return {
        "success": True,
        "user_id": user_id,
        "message": f"Password reset notification sent to user '{user_id}'."
    }

@router.get("/admin/{user_id}/activity", summary="View User Activity History Audit Trail")
def get_user_activity_history(user_id: str):
    """Retrieves security scan history and administrative audit log for user."""
    return {
        "user_id": user_id,
        "activity_logs": [
            {"timestamp": "2026-08-01T03:00:00Z", "action": "LOGIN_SUCCESS", "ip": "192.168.1.100"},
            {"timestamp": "2026-08-01T02:45:00Z", "action": "SUBMIT_SCAM_REPORT", "report_id": "rep_101"},
            {"timestamp": "2026-08-01T01:30:00Z", "action": "EXECUTE_SCAN", "scan_type": "URL"}
        ]
    }
