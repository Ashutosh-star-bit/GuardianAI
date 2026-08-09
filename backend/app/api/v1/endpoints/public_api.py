"""
GuardianAI Public Developer REST APIs
Endpoints:
  - POST /api/v1/public/scan/text       : Text / Message Smishing Inspection
  - POST /api/v1/public/scan/url        : URL Typosquatting & Phishing Inspection
  - POST /api/v1/public/scan/email      : BEC Email Header & Wire Fraud Inspection
  - POST /api/v1/public/scan/ocr        : Document & Image OCR Scam Extraction
  - POST /api/v1/public/scan/voice      : Voice Deepfake & STT Audio Inspection
  - GET  /api/v1/public/threat-intel    : Threat Intelligence Indicator Lookup
  - POST /api/v1/public/decision        : Master Explainable Decision Engine Evaluation
  - GET  /api/v1/public/community/reports: Read-Only Public Community Scam Feed
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, status, Depends, Query, Body, Security, HTTPException
from pydantic import BaseModel, Field
from app.api.deps import get_current_user_optional
from app.models.user import User
from app.schemas.response import APIResponse
from app.decision_engine.service import DecisionService
from app.threat_intel.service import ThreatIntelligenceService

router = APIRouter(prefix="/public", tags=["Public Developer API"])

# Request Schemas
class PublicTextScanRequest(BaseModel):
    text: str = Field(..., example="URGENT: Your HDFC netbanking account is suspended. Update KYC at http://hdfc-update.top")

class PublicURLScanRequest(BaseModel):
    url: str = Field(..., example="http://hdfc-bank-login.top")

class PublicEmailScanRequest(BaseModel):
    subject: str = Field(..., example="Urgent Wire Transfer Authorization Needed")
    body: str = Field(..., example="Please wire $50,000 to account 99887766 immediately.")

class PublicOCRScanRequest(BaseModel):
    document_text: str = Field(..., example="POLICE NOTICE: You are under digital arrest by Delhi Cyber Cell.")

class PublicVoiceScanRequest(BaseModel):
    audio_transcript: str = Field(..., example="This is Officer Sharma from Crime Branch. Pay fine via UPI.")

@router.post(
    "/scan/text",
    response_model=APIResponse[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
    summary="Public API: Inspect Text Message Payload"
)
async def public_scan_text(
    payload: PublicTextScanRequest,
    current_user: Optional[User] = Security(get_current_user_optional)
):
    """Analyzes text payload for smishing, urgency signals, and suspicious URLs."""
    report = await DecisionService.process_full_decision_scan(raw_text=payload.text, channel_type="SMS")
    return APIResponse(
        success=True,
        message="Text payload analysis complete.",
        data=report.model_dump(mode="json")
    )

@router.post(
    "/scan/url",
    response_model=APIResponse[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
    summary="Public API: Inspect URL Link"
)
async def public_scan_url(
    payload: PublicURLScanRequest,
    current_user: Optional[User] = Security(get_current_user_optional)
):
    """Analyzes URL for domain age, homoglyph typosquatting, and SSL validity."""
    report = await DecisionService.process_full_decision_scan(raw_text=payload.url, channel_type="URL")
    return APIResponse(
        success=True,
        message="URL payload analysis complete.",
        data=report.model_dump(mode="json")
    )

@router.post(
    "/scan/email",
    response_model=APIResponse[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
    summary="Public API: Inspect Email Payload"
)
async def public_scan_email(
    payload: PublicEmailScanRequest,
    current_user: Optional[User] = Security(get_current_user_optional)
):
    """Analyzes email subject and body for BEC wire transfer fraud."""
    report = await DecisionService.process_full_decision_scan(raw_text=f"{payload.subject}\n{payload.body}", channel_type="EMAIL")
    return APIResponse(
        success=True,
        message="Email payload analysis complete.",
        data=report.model_dump(mode="json")
    )

@router.post(
    "/scan/ocr",
    response_model=APIResponse[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
    summary="Public API: Inspect Document OCR Text"
)
async def public_scan_ocr(
    payload: PublicOCRScanRequest,
    current_user: Optional[User] = Security(get_current_user_optional)
):
    """Analyzes document OCR extracted text for digital arrest & official impersonation."""
    report = await DecisionService.process_full_decision_scan(raw_text=payload.document_text, channel_type="OCR")
    return APIResponse(
        success=True,
        message="OCR document analysis complete.",
        data=report.model_dump(mode="json")
    )

@router.post(
    "/scan/voice",
    response_model=APIResponse[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
    summary="Public API: Inspect Voice Transcript"
)
async def public_scan_voice(
    payload: PublicVoiceScanRequest,
    current_user: Optional[User] = Security(get_current_user_optional)
):
    """Analyzes voice audio transcript for voice deepfakes and extortion scripts."""
    report = await DecisionService.process_full_decision_scan(raw_text=payload.audio_transcript, channel_type="VOICE")
    return APIResponse(
        success=True,
        message="Voice transcript analysis complete.",
        data=report.model_dump(mode="json")
    )

@router.get(
    "/threat-intel",
    response_model=APIResponse[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
    summary="Public API: Threat Intelligence IOC Lookup"
)
async def public_threat_intel_lookup(
    indicator: str = Query(..., example="hdfc-verify.top", description="URL, domain, email, or UPI VPA"),
    current_user: Optional[User] = Security(get_current_user_optional)
):
    """Queries threat intelligence database for known malicious IOCs."""
    intel = await ThreatIntelligenceService.analyze_threat_payload(raw_text=indicator)
    return APIResponse(
        success=True,
        message=f"Threat intelligence lookup completed for '{indicator}'.",
        data=intel.model_dump(mode="json")
    )

@router.post(
    "/decision",
    response_model=APIResponse[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
    summary="Public API: Master Decision Engine Evaluation"
)
async def public_master_decision_evaluation(
    payload: PublicTextScanRequest,
    current_user: Optional[User] = Security(get_current_user_optional)
):
    """Evaluates master explainable AI risk classification with risk breakdown & recommended action."""
    report = await DecisionService.process_full_decision_scan(raw_text=payload.text, channel_type="MASTER")
    return APIResponse(
        success=True,
        message="Master decision engine evaluation complete.",
        data=report.model_dump(mode="json")
    )

@router.get(
    "/community/reports",
    response_model=APIResponse[List[Dict[str, Any]]],
    status_code=status.HTTP_200_OK,
    summary="Public API: Read-Only Community Scam Feed"
)
async def public_community_reports_feed(
    limit: int = Query(20, ge=1, le=100),
    current_user: Optional[User] = Security(get_current_user_optional)
):
    """Retrieves verified public crowdsourced scam reports feed."""
    mock_reports = [
        {"id": "rep_101", "type": "DIGITAL_ARREST", "title": "Fake CBI Police Video Call", "upvotes": 42, "status": "VERIFIED"},
        {"id": "rep_102", "type": "PHISHING_URL", "title": "Fake HDFC Netbanking Link", "upvotes": 38, "status": "VERIFIED"}
    ]
    return APIResponse(
        success=True,
        message=f"Retrieved {len(mock_reports)} verified community scam reports.",
        data=mock_reports[:limit]
    )
