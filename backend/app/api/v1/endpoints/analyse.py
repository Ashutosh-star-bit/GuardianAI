"""
GuardianAI Scam Analysis Pipeline REST API Router
Purpose: Provides REST API endpoints for multi-format input adapters (POST /analyse/text, /analyse/url, /analyse/email,
         /analyse/pdf, /analyse/image, /analyse/qr, /analyse/document, /analyse/batch), scan history query, detail, and deletion.
"""

import uuid
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, Request, Depends, status, Query, HTTPException, UploadFile, File, Form
from pydantic import BaseModel, Field

from app.core.response import success_response
from app.api.deps import get_current_user
from app.models.user import User
from app.pipeline.orchestrator import ScamAnalysisPipeline
from app.pipeline.batch_processor import BatchProcessor, BatchItemPayload
from app.pipeline.history_service import HistoryService
from app.pipeline.analytics_recorder import AnalyticsRecorder
from app.services.ocr_service import OCRService

router = APIRouter(tags=["Scam Analysis Pipeline"])

# --- REQUEST DTO MODELS ---

class TextAnalyseRequest(BaseModel):
    text: str = Field(min_length=1, max_length=10_000, description="Raw plain text payload to analyze")
    target_persona: str = Field(default="SENIOR_CITIZENS", description="SENIOR_CITIZENS, PARENTS, STUDENTS, PROFESSIONALS")
    locale: str = Field(default="en", description="en, es, hi, fr, de")

    model_config = {
        "json_schema_extra": {
            "example": {
                "text": "URGENT: Your PayPal account is suspended. Verify at http://paypa1-check.top or send $500 to support.refund@okaxis",
                "target_persona": "SENIOR_CITIZENS",
                "locale": "en"
            }
        }
    }

class URLAnalyseRequest(BaseModel):
    url: str = Field(min_length=3, max_length=2048, description="Web URL payload string")
    target_persona: str = Field(default="SENIOR_CITIZENS")
    locale: str = Field(default="en")

    model_config = {
        "json_schema_extra": {
            "example": {
                "url": "http://paypa1-check.top/login",
                "target_persona": "SENIOR_CITIZENS",
                "locale": "en"
            }
        }
    }

class EmailAnalyseRequest(BaseModel):
    email_text: str = Field(min_length=4, max_length=50_000, description="RFC 5322 Email headers & body paste")
    target_persona: str = Field(default="SENIOR_CITIZENS")
    locale: str = Field(default="en")

    model_config = {
        "json_schema_extra": {
            "example": {
                "email_text": "From: security@paypa1-check.top\nTo: user@gmail.com\nSubject: Account Suspended\n\nVerify link",
                "target_persona": "SENIOR_CITIZENS",
                "locale": "en"
            }
        }
    }

class QRTextAnalyseRequest(BaseModel):
    qr_payload: str = Field(min_length=1, max_length=2048, description="Decoded QR payload string (URL, UPI, Phone, SMS, Email, WiFi)")
    target_persona: str = Field(default="SENIOR_CITIZENS")
    locale: str = Field(default="en")

    model_config = {
        "json_schema_extra": {
            "example": {
                "qr_payload": "upi://pay?pa=support.refund@okaxis&pn=BankSupport",
                "target_persona": "SENIOR_CITIZENS",
                "locale": "en"
            }
        }
    }

class BatchAnalyseRequest(BaseModel):
    items: List[BatchItemPayload] = Field(min_items=1, max_items=100)
    target_persona: str = Field(default="SENIOR_CITIZENS")
    locale: str = Field(default="en")

# --- REST ENDPOINTS ---

@router.post("/analyse/text", status_code=status.HTTP_200_OK, summary="Analyze Plain Text Message")
async def analyse_text(
    payload: TextAnalyseRequest,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Executes Scam Analysis Pipeline on raw plain text / SMS message."""
    res = await ScamAnalysisPipeline.execute_full_scam_analysis(
        raw_input=payload.text,
        format_type="TEXT",
        user_id=current_user.id,
        target_persona=payload.target_persona,
        locale=payload.locale
    )
    return success_response(data=res.model_dump(mode="json"), message="Text scam analysis completed successfully.", request=request)

@router.post("/analyse/url", status_code=status.HTTP_200_OK, summary="Analyze Web URL Link")
async def analyse_url(
    payload: URLAnalyseRequest,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Executes Scam Analysis Pipeline on web URL link."""
    res = await ScamAnalysisPipeline.execute_full_scam_analysis(
        raw_input=payload.url,
        format_type="URL",
        user_id=current_user.id,
        target_persona=payload.target_persona,
        locale=payload.locale
    )
    return success_response(data=res.model_dump(mode="json"), message="URL scam analysis completed successfully.", request=request)

@router.post("/analyse/email", status_code=status.HTTP_200_OK, summary="Analyze Email Message")
async def analyse_email(
    payload: EmailAnalyseRequest,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Executes Scam Analysis Pipeline on email text or raw MIME content."""
    res = await ScamAnalysisPipeline.execute_full_scam_analysis(
        raw_input=payload.email_text,
        format_type="EMAIL",
        user_id=current_user.id,
        target_persona=payload.target_persona,
        locale=payload.locale
    )
    return success_response(data=res.model_dump(mode="json"), message="Email scam analysis completed successfully.", request=request)

@router.post("/analyse/pdf", status_code=status.HTTP_200_OK, summary="Analyze PDF Document File")
async def analyse_pdf(
    file: UploadFile = File(...),
    target_persona: str = Form("SENIOR_CITIZENS"),
    locale: str = Form("en"),
    request: Request = None,
    current_user: User = Depends(get_current_user)
):
    """Executes Scam Analysis Pipeline on uploaded PDF file bytes."""
    contents = await file.read()
    res = await ScamAnalysisPipeline.execute_full_scam_analysis(
        raw_input=contents,
        format_type="PDF",
        user_id=current_user.id,
        target_persona=target_persona,
        locale=locale
    )
    return success_response(data=res.model_dump(mode="json"), message="PDF document scam analysis completed successfully.", request=request)

@router.post("/analyse/image", status_code=status.HTTP_200_OK, summary="Analyze Screenshot Image File")
async def analyse_image(
    file: UploadFile = File(...),
    target_persona: str = Form("SENIOR_CITIZENS"),
    locale: str = Form("en"),
    request: Request = None,
    current_user: User = Depends(get_current_user)
):
    """Executes Scam Analysis Pipeline on uploaded screenshot image bytes."""
    contents = await file.read()
    res = await ScamAnalysisPipeline.execute_full_scam_analysis(
        raw_input=contents,
        format_type="IMAGE",
        user_id=current_user.id,
        target_persona=target_persona,
        locale=locale
    )
    return success_response(data=res.model_dump(mode="json"), message="Image scam analysis completed successfully.", request=request)

@router.post("/analyse/document", status_code=status.HTTP_200_OK, summary="Analyze Visual Document File via OCR Service")
async def analyse_document_ocr(
    file: UploadFile = File(...),
    target_persona: str = Form("SENIOR_CITIZENS"),
    locale: str = Form("en"),
    request: Request = None,
    current_user: User = Depends(get_current_user)
):
    """Executes OCRService 7-stage Document Intelligence pipeline on uploaded document bytes."""
    contents = await file.read()
    ocr_service = OCRService()
    ocr_res = await ocr_service.process_document_pipeline(
        raw_payload=contents,
        filename=file.filename,
        user_id=current_user.id,
        language=locale
    )
    
    # Execute Master Scam Analysis Pipeline on adapted request
    pipeline_res = await ScamAnalysisPipeline.execute_full_scam_analysis(
        raw_input=ocr_res.analysis_request,
        user_id=current_user.id,
        target_persona=target_persona,
        locale=locale
    )

    data = {
        "pipeline_result": pipeline_res.model_dump(mode="json"),
        "document_intelligence": ocr_res.document_result.model_dump(mode="json"),
        "ocr_processing_time_ms": ocr_res.processing_time_ms
    }
    return success_response(data=data, message="Visual document OCR scam analysis completed successfully.", request=request)

@router.post("/analyse/qr", status_code=status.HTTP_200_OK, summary="Analyze Decoded QR Code Payload")
async def analyse_qr(
    payload: QRTextAnalyseRequest,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Executes Scam Analysis Pipeline on decoded QR payload string (URL, UPI, Phone, SMS, Email, WiFi)."""
    res = await ScamAnalysisPipeline.execute_full_scam_analysis(
        raw_input=payload.qr_payload,
        format_type="QR",
        user_id=current_user.id,
        target_persona=payload.target_persona,
        locale=payload.locale
    )
    return success_response(data=res.model_dump(mode="json"), message="QR code payload analysis completed successfully.", request=request)

# --- 7. BATCH CONCURRENT ANALYSE ENDPOINT ---
@router.post("/analyse/batch", status_code=status.HTTP_200_OK, summary="Analyze Batch of Multi-Format Items Concurrently")
async def analyse_batch(
    payload: BatchAnalyseRequest,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Executes concurrent batch scam analysis across multiple items with worker pool concurrency bounds."""
    batch_res = await BatchProcessor.process_batch(
        items=payload.items,
        user_id=current_user.id,
        target_persona=payload.target_persona,
        locale=payload.locale
    )
    return success_response(data=batch_res.model_dump(mode="json"), message="Batch scam analysis completed successfully.", request=request)

# --- SCAN HISTORY ENDPOINTS ---
@router.get("/analysis/history", status_code=status.HTTP_200_OK, summary="Query Authenticated User Scan History")
async def get_user_scan_history(
    request: Request,
    q: Optional[str] = Query(None, description="Keyword search query"),
    risk_level: Optional[str] = Query(None, description="SAFE, LOW, MEDIUM, HIGH, CRITICAL"),
    format_type: Optional[str] = Query(None, description="TEXT, EMAIL, URL, QR, PDF, IMAGE"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """Searches user scan history with keyword query, risk level filtering, format type filtering, and pagination."""
    records, total_count = HistoryService.search_history(
        user_id=current_user.id,
        query=q,
        risk_level=risk_level,
        input_format=format_type,
        page=page,
        page_size=page_size
    )

    return success_response(
        data={
            "total_count": total_count,
            "page": page,
            "page_size": page_size,
            "records": [r.model_dump(mode="json") for r in records]
        },
        message="Scan history retrieved successfully.",
        request=request
    )

@router.get("/analysis/{scan_id}", status_code=status.HTTP_200_OK, summary="Get Single Scan Analysis History Detail")
async def get_scan_detail(
    scan_id: str,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Retrieves detailed scan history record by scan_id."""
    record = HistoryService.get_scan_by_id(scan_id)
    if not record or (record.user_id and record.user_id != current_user.id):
        raise HTTPException(status_code=404, detail=f"Scan record '{scan_id}' not found.")

    return success_response(data=record.model_dump(mode="json"), message="Scan detail retrieved successfully.", request=request)

@router.delete("/analysis/{scan_id}", status_code=status.HTTP_200_OK, summary="Delete Scan Analysis History Record")
async def delete_scan_record(
    scan_id: str,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Deletes a scan history record by scan_id."""
    success = HistoryService.delete_scan_history(scan_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Scan record '{scan_id}' not found or unauthorized.")

    return success_response(data={"deleted": True, "scan_id": scan_id}, message="Scan history record deleted successfully.", request=request)
