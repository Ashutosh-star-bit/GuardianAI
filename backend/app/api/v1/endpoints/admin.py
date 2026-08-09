"""
GuardianAI Enterprise Admin Platform REST Endpoints
Endpoints:
  - GET  /api/v1/admin/command-center   : Master Command Center Telemetry
  - GET  /api/v1/admin/ai-metrics        : AI Inference & Token Metrics
  - GET  /api/v1/admin/audit-logs        : Administrative Compliance Audit Trail
  - POST /api/v1/admin/broadcast         : Create Platform Security Notification Broadcast
  - GET  /api/v1/admin/roles             : List System & Custom RBAC Roles
  - POST /api/v1/admin/roles             : Create Custom Dynamic Role
  - POST /api/v1/admin/export            : Secure Dataset Exporter (CSV / JSON)
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, Query, status, Security, Body, Response
from app.admin.admin_orchestrator import enterprise_admin_orchestrator
from app.admin.export_center import secure_export_engine
from app.core.role_management import role_management_service, SystemPermission
from app.api.deps import get_current_user_optional
from app.models.user import User
from app.schemas.response import APIResponse

router = APIRouter(prefix="/admin", tags=["Enterprise Admin Platform"])

@router.get(
    "/command-center",
    response_model=APIResponse[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
    summary="Retrieve Master Command Center Real-Time Telemetry"
)
async def get_command_center_telemetry(
    current_user: Optional[User] = Security(get_current_user_optional)
):
    """Retrieves real-time master command center telemetry."""
    metrics = enterprise_admin_orchestrator.get_command_center_metrics()
    return APIResponse(
        success=True,
        message="Retrieved command center real-time telemetry successfully.",
        data=metrics
    )

@router.get(
    "/ai-metrics",
    response_model=APIResponse[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
    summary="Retrieve AI Inference & Token Consumption Metrics"
)
async def get_ai_inference_metrics(
    current_user: Optional[User] = Security(get_current_user_optional)
):
    """Retrieves real-time AI token usage, latency, and cost telemetry."""
    ai_metrics = enterprise_admin_orchestrator.get_ai_token_metrics()
    return APIResponse(
        success=True,
        message="Retrieved AI inference token metrics successfully.",
        data=ai_metrics
    )

@router.get(
    "/audit-logs",
    response_model=APIResponse[List[Dict[str, Any]]],
    status_code=status.HTTP_200_OK,
    summary="List Administrative Compliance Audit Logs"
)
async def list_admin_audit_logs(
    limit: int = Query(50, ge=1, le=500, description="Max log items"),
    current_user: Optional[User] = Security(get_current_user_optional)
):
    """Retrieves recent administrative compliance audit logs."""
    logs = enterprise_admin_orchestrator.get_audit_logs(limit=limit)
    return APIResponse(
        success=True,
        message=f"Retrieved {len(logs)} administrative audit log entries.",
        data=logs
    )

@router.post(
    "/broadcast",
    response_model=APIResponse[Dict[str, Any]],
    status_code=status.HTTP_201_CREATED,
    summary="Dispatch Platform Security Broadcast Banner"
)
async def create_security_broadcast(
    payload: Dict[str, Any] = Body(...),
    current_user: Optional[User] = Security(get_current_user_optional)
):
    """Dispatches global platform security notification broadcast to all users."""
    mod_id = str(current_user.id) if current_user else "admin_master"
    title = payload.get("title", "Security Notification")
    message = payload.get("message", "System security operational announcement")
    severity = payload.get("severity", "INFO")

    b_item = enterprise_admin_orchestrator.create_system_broadcast(title, message, severity)
    enterprise_admin_orchestrator.log_admin_action(mod_id, "CREATE_BROADCAST", b_item["id"], title)

    return APIResponse(
        success=True,
        message="Platform security broadcast dispatched successfully.",
        data=b_item
    )

@router.get(
    "/roles",
    response_model=APIResponse[List[Dict[str, Any]]],
    status_code=status.HTTP_200_OK,
    summary="List All Built-in & Custom RBAC Roles"
)
async def list_admin_roles(
    current_user: Optional[User] = Security(get_current_user_optional)
):
    """Retrieves list of all built-in and dynamic custom RBAC role definitions."""
    roles = [r.model_dump() for r in role_management_service.get_all_roles()]
    return APIResponse(
        success=True,
        message=f"Retrieved {len(roles)} RBAC role definitions.",
        data=roles
    )

@router.post(
    "/roles",
    response_model=APIResponse[Dict[str, Any]],
    status_code=status.HTTP_201_CREATED,
    summary="Create Dynamic Custom RBAC Role"
)
async def create_custom_admin_role(
    payload: Dict[str, Any] = Body(...),
    current_user: Optional[User] = Security(get_current_user_optional)
):
    """Creates a new dynamic custom enterprise role with specified permissions."""
    name = payload.get("name", "Custom Role")
    description = payload.get("description", "Dynamic custom RBAC role")
    permissions_raw = payload.get("permissions", ["global:read_only"])
    perms = [SystemPermission(p) for p in permissions_raw if p in SystemPermission.__members__.values()]

    role_def = role_management_service.create_custom_role(name, description, perms)
    return APIResponse(
        success=True,
        message=f"Custom RBAC role '{role_def.name}' created successfully.",
        data=role_def.model_dump()
    )

@router.post(
    "/export",
    summary="Export Secure Dataset (CSV / JSON)"
)
async def export_admin_dataset(
    dataset: str = Query("REPORTS", description="Target dataset: REPORTS, ANALYTICS, AUDIT_LOGS, COMMUNITY"),
    format_type: str = Query("CSV", description="Output format: CSV, JSON"),
    current_user: Optional[User] = Security(get_current_user_optional)
):
    """Exports dataset with CSV formula injection protection."""
    mock_data = [
        {"id": "exp_01", "title": "Digital Arrest Scam", "risk_score": 98, "status": "VERIFIED"},
        {"id": "exp_02", "title": "HDFC Phishing Link", "risk_score": 90, "status": "PENDING"}
    ]

    if format_type.upper() == "JSON":
        content = secure_export_engine.export_to_json(mock_data)
        media_type = "application/json"
        filename = f"guardianai_{dataset.lower()}_export.json"
    else:
        content = secure_export_engine.export_to_csv(mock_data)
        media_type = "text/csv"
        filename = f"guardianai_{dataset.lower()}_export.csv"

    return Response(
        content=content,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )
