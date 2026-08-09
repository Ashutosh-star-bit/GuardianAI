"""
GuardianAI Document Intelligence OCR REST API Endpoints Router
Purpose: Provides REST API endpoints for OCR document analysis:
         POST /ocr/image (Screenshot/Document Image),
         POST /ocr/pdf (Multi-page PDF Document),
         POST /ocr/batch (Concurrent Batch OCR Document Processing).
"""

import uuid
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Request, Depends, status, HTTPException, UploadFile, File, Form
from pydantic import BaseModel, Field

from app.core.response import success_response
from app.api.deps import get_current_user
from app.models.user import User
from app.services.ocr_service import OCRService, OCRServiceError
from app.pipeline.batch_processor import BatchProcessor, BatchItemPayload, BatchAnalysisResult

router = APIRouter(prefix="/ocr", tags=["Document Intelligence OCR"])

# --- REQUEST DTO MODELS FOR SWAGGER ---

class OCRBatchItemPayload(BaseModel):
    item_id: str = Field(description="Unique client item identifier")
    image_base64_or_text: str = Field(description="Raw text, base64 data, or URI")
    format_type: str = Field(default="DOCUMENT", description="DOCUMENT, IMAGE, PDF, TEXT")

class OCRBatchAnalyseRequest(BaseModel):
    items: List[OCRBatchItemPayload] = Field(min_items=1, max_items=100, description="List of items for concurrent OCR analysis")
    language: str = Field(default="en", description="ISO-639 language code (en, es, hi, fr, de)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "items": [
                    {"item_id": "doc_1", "raw_payload": "URGENT SECURITY NOTICE: Account Suspended", "format_type": "DOCUMENT"},
                    {"item_id": "doc_2", "raw_payload": "https://paypa1-check.top/login", "format_type": "URL"}
                ],
                "language": "en"
            }
        }
    }

# --- REST ENDPOINTS ---

@router.post(
    "/image",
    status_code=status.HTTP_200_OK,
    summary="Process Screenshot / Image Document via OCR Pipeline",
    response_description="Returns Document Analysis Metadata, Extracted Text, Spatial Bounding Boxes, and Adapted AnalysisRequest"
)
async def process_ocr_image(
    file: UploadFile = File(..., description="Document image file (.png, .jpg, .jpeg, .webp)"),
    language: str = Form("en", description="ISO-639 language code (en, es, hi, fr, de)"),
    request: Request = None,
    current_user: User = Depends(get_current_user)
):
    """
    Executes complete 7-stage Document Intelligence OCR Pipeline over uploaded screenshot or document image:
    1. Header & MIME Signature Validation -> 2. Computer Vision Preprocessing -> 3. Spatial Layout Analysis ->
    4. Optical Character Recognition (OCR) -> 5. Text Cleaning & Artifact Repair -> 6. Language & Script ID -> 7. UniversalAnalysisRequest Generation.
    """
    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Filename cannot be empty")

    ext = file.filename.split(".")[-1].lower() if "." in file.filename else ""
    if ext not in ["png", "jpg", "jpeg", "webp"]:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported image extension '.{ext}'. Whitelisted formats: .png, .jpg, .jpeg, .webp"
        )

    contents = await file.read()
    if len(contents) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded file payload is empty (0 bytes)")

    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File size exceeds max 10MB limit")

    ocr_service = OCRService()
    try:
        res = await ocr_service.process_document_pipeline(
            raw_payload=contents,
            filename=file.filename,
            user_id=current_user.id,
            language=language,
            source="OCR_IMAGE_ENDPOINT"
        )
        return success_response(
            data={
                "document_result": res.document_result.model_dump(mode="json"),
                "analysis_request": res.analysis_request.model_dump(mode="json"),
                "processing_time_ms": res.processing_time_ms
            },
            message="Image OCR document processing completed successfully.",
            request=request
        )
    except OCRServiceError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

@router.post(
    "/pdf",
    status_code=status.HTTP_200_OK,
    summary="Process PDF Document via Multi-Page OCR Pipeline",
    response_description="Returns Multi-Page PDF Document Metadata, Page Counts, Text Extraction, and Adapted AnalysisRequest"
)
async def process_ocr_pdf(
    file: UploadFile = File(..., description="PDF document file (.pdf)"),
    language: str = Form("en", description="ISO-639 language code (en, es, hi, fr, de)"),
    request: Request = None,
    current_user: User = Depends(get_current_user)
):
    """
    Executes multi-page PDF Document Intelligence OCR Pipeline:
    Inspects %PDF- header magic bytes, calculates page counts, extracts text streams, and returns spatial bounding box metadata.
    """
    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Filename cannot be empty")

    ext = file.filename.split(".")[-1].lower() if "." in file.filename else ""
    if ext != "pdf":
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported format '.{ext}'. /ocr/pdf endpoint accepts only .pdf files"
        )

    contents = await file.read()
    if len(contents) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded PDF file payload is empty (0 bytes)")

    if len(contents) > 15 * 1024 * 1024:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="PDF file size exceeds max 15MB limit")

    ocr_service = OCRService()
    try:
        res = await ocr_service.process_document_pipeline(
            raw_payload=contents,
            filename=file.filename,
            user_id=current_user.id,
            language=language,
            source="OCR_PDF_ENDPOINT"
        )
        return success_response(
            data={
                "document_result": res.document_result.model_dump(mode="json"),
                "analysis_request": res.analysis_request.model_dump(mode="json"),
                "processing_time_ms": res.processing_time_ms
            },
            message="PDF OCR document processing completed successfully.",
            request=request
        )
    except OCRServiceError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

@router.post(
    "/batch",
    status_code=status.HTTP_200_OK,
    summary="Process Batch of Multi-Format Document Items Concurrently via OCR Pipeline",
    response_description="Returns Batch Result Object with Item-Level Error Isolation"
)
async def process_ocr_batch(
    payload: OCRBatchAnalyseRequest,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """
    Executes concurrent batch OCR processing across multiple document items:
    Enforces max 100 items per request and uses bounded worker pool semaphore to guarantee server stability.
    """
    items_to_process = [
        BatchItemPayload(
            item_id=it.item_id,
            raw_payload=it.image_base64_or_text,
            format_type=it.format_type
        )
        for it in payload.items
    ]

    batch_res: BatchAnalysisResult = await BatchProcessor.process_batch(
        items=items_to_process,
        user_id=current_user.id,
        locale=payload.language
    )

    return success_response(
        data=batch_res.model_dump(mode="json"),
        message="Batch OCR document processing completed successfully.",
        request=request
    )
