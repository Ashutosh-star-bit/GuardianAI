"""
GuardianAI File Upload API Endpoint
Purpose: Exposes HTTP POST /api/v1/upload for processing secure PDF, PNG, JPG, JPEG, and TXT file uploads.
"""

from fastapi import APIRouter, UploadFile, File, Request, Depends, status
from app.services.upload_service import SecureUploadService
from app.core.response import success_response
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/upload", status_code=status.HTTP_201_CREATED, summary="Upload Security Payload File")
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Accepts PDF, PNG, JPG, JPEG, or TXT file upload.
    Validates file size (max 10MB), extension whitelist, MIME type, and stores securely on disk.
    """
    upload_metadata = await SecureUploadService.save_upload(file)
    return success_response(
        data=upload_metadata,
        message="File uploaded and verified successfully.",
        status_code=status.HTTP_201_CREATED,
        request=request
    )
