"""
GuardianAI Developer API Key Management REST Endpoints
Endpoints:
  - GET    /api/v1/api-keys           : List developer keys
  - POST   /api/v1/api-keys           : Generate new API key
  - POST   /api/v1/api-keys/{id}/rotate: Rotate API key secret
  - POST   /api/v1/api-keys/{id}/toggle: Enable / Disable API key
  - DELETE /api/v1/api-keys/{id}       : Delete API key
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, Query, status, Security, Body, HTTPException
from app.developer_platform.api_key_service import api_key_service, APIKeyRecord
from app.api.deps import get_current_user_optional
from app.models.user import User
from app.schemas.response import APIResponse

router = APIRouter(prefix="/api-keys", tags=["Developer Platform API Keys"])

@router.get(
    "",
    response_model=APIResponse[List[Dict[str, Any]]],
    status_code=status.HTTP_200_OK,
    summary="List All Developer API Keys"
)
async def list_developer_api_keys(
    current_user: Optional[User] = Security(get_current_user_optional)
):
    """Retrieves all API keys configured for the developer account."""
    raw_keys = list(api_key_service._keys_db.values())
    # Omit raw_key_secret for security when listing!
    data = []
    for k in raw_keys:
        d = k.model_dump()
        d.pop("raw_key_secret", None)
        data.append(d)

    return APIResponse(
        success=True,
        message=f"Retrieved {len(data)} developer API keys.",
        data=data
    )

@router.post(
    "",
    response_model=APIResponse[Dict[str, Any]],
    status_code=status.HTTP_201_CREATED,
    summary="Generate New Developer API Key"
)
async def create_developer_api_key(
    payload: Dict[str, Any] = Body(...),
    current_user: Optional[User] = Security(get_current_user_optional)
):
    """Generates a new API Key returning the raw secret ONCE."""
    name = payload.get("name", "New Production API Key")
    environment = payload.get("environment", "LIVE")
    tier = payload.get("tier", "PRO")

    record = api_key_service.create_api_key(name=name, environment=environment, tier=tier)
    return APIResponse(
        success=True,
        message=f"API Key '{name}' generated successfully. Copy your secret key now; it will not be displayed again!",
        data=record.model_dump()
    )

@router.post(
    "/{key_id}/rotate",
    response_model=APIResponse[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
    summary="Rotate API Key Secret"
)
async def rotate_developer_api_key(
    key_id: str,
    current_user: Optional[User] = Security(get_current_user_optional)
):
    """Rotates API key secret immediately invalidating old secret."""
    # Find existing record
    target_rec = None
    old_hash = None
    for h, rec in api_key_service._keys_db.items():
        if rec.key_id == key_id:
            target_rec = rec
            old_hash = h
            break

    if not target_rec or not old_hash:
        raise HTTPException(status_code=404, detail=f"API Key ID '{key_id}' not found.")

    # Remove old hash, create rotated key
    del api_key_service._keys_db[old_hash]
    new_rec = api_key_service.create_api_key(name=target_rec.name, environment=target_rec.environment, tier=target_rec.tier)
    new_rec.key_id = key_id  # Preserve ID

    return APIResponse(
        success=True,
        message="API Key secret rotated successfully.",
        data=new_rec.model_dump()
    )

@router.post(
    "/{key_id}/toggle",
    response_model=APIResponse[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
    summary="Disable or Enable API Key"
)
async def toggle_developer_api_key(
    key_id: str,
    is_active: bool = Query(..., description="Target status: True (Active), False (Disabled)"),
    current_user: Optional[User] = Security(get_current_user_optional)
):
    """Toggles API key active status."""
    for rec in api_key_service._keys_db.values():
        if rec.key_id == key_id:
            rec.is_active = is_active
            d = rec.model_dump()
            d.pop("raw_key_secret", None)
            return APIResponse(
                success=True,
                message=f"API Key status updated to {is_active}.",
                data=d
            )
    raise HTTPException(status_code=404, detail=f"API Key ID '{key_id}' not found.")

@router.delete(
    "/{key_id}",
    response_model=APIResponse[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
    summary="Permanently Delete API Key"
)
async def delete_developer_api_key(
    key_id: str,
    current_user: Optional[User] = Security(get_current_user_optional)
):
    """Permanently revokes and deletes API Key record."""
    target_hash = None
    for h, rec in api_key_service._keys_db.items():
        if rec.key_id == key_id:
            target_hash = h
            break

    if target_hash:
        del api_key_service._keys_db[target_hash]
        return APIResponse(
            success=True,
            message=f"API Key ID '{key_id}' permanently deleted.",
            data={"key_id": key_id}
        )
    raise HTTPException(status_code=404, detail=f"API Key ID '{key_id}' not found.")
