"""
GuardianAI Threat Intelligence REST API Router
Purpose: Provides REST API endpoints for URL, Domain, Email, Phone, UPI, and Full Payload Threat Intelligence analysis.
"""

import uuid
from fastapi import APIRouter, Request, Depends, status
from pydantic import BaseModel, Field
from app.core.response import success_response
from app.api.deps import get_current_user
from app.models.user import User

from app.threat_intel.url_intel import URLIntelligenceEngine
from app.threat_intel.domain_intel import DomainIntelligenceEngine
from app.threat_intel.email_intel import EmailIntelligenceEngine
from app.threat_intel.phone_intel import PhoneIntelligenceEngine
from app.threat_intel.upi_intel import UPIIntelligenceEngine
from app.threat_intel.service import ThreatIntelligenceService

router = APIRouter(prefix="/threat", tags=["Threat Intelligence"])

# 1. URL Request Model
class URLThreatRequest(BaseModel):
    url: str = Field(min_length=4, max_length=2048, description="URL string to inspect")
    model_config = {
        "json_schema_extra": {
            "example": {"url": "http://admin:secret@192.168.1.1:8080/login/secure?utm_source=spam#top"}
        }
    }

# 2. Domain Request Model
class DomainThreatRequest(BaseModel):
    domain: str = Field(min_length=3, max_length=253, description="Domain hostname to inspect")
    model_config = {
        "json_schema_extra": {
            "example": {"domain": "sub.verify.paypa1-check.top"}
        }
    }

# 3. Email Request Model
class EmailThreatRequest(BaseModel):
    email_header: str = Field(min_length=5, max_length=500, description="Raw email address or header string")
    model_config = {
        "json_schema_extra": {
            "example": {"email_header": '"CEO John Smith" <john.smith@gmail.com>'}
        }
    }

# 4. Phone Request Model
class PhoneThreatRequest(BaseModel):
    phone_number: str = Field(min_length=7, max_length=30, description="Phone number string to inspect")
    model_config = {
        "json_schema_extra": {
            "example": {"phone_number": "+1 (900) 555-9999"}
        }
    }

# 5. UPI Request Model
class UPIThreatRequest(BaseModel):
    upi_id: str = Field(min_length=4, max_length=100, description="UPI Virtual Payment Address (VPA) handle")
    model_config = {
        "json_schema_extra": {
            "example": {"upi_id": "support.refund@okaxis"}
        }
    }

# 6. Full Payload Request Model
class FullThreatAnalyseRequest(BaseModel):
    text: str = Field(min_length=5, max_length=10_000, description="Raw text payload to analyze across all threat vectors")
    model_config = {
        "json_schema_extra": {
            "example": {
                "text": "URGENT: Your PayPal account is suspended. Verify at http://paypa1-check.top or send $500 to support.refund@okaxis"
            }
        }
    }

# --- ENDPOINTS ---

@router.post("/url", status_code=status.HTTP_200_OK, summary="Inspect URL Structural Threats")
async def inspect_url_threat(
    payload: URLThreatRequest,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Inspects URL protocol, IP hostname, non-standard ports, embedded credentials, and percent-encoding."""
    report = URLIntelligenceEngine.analyze_url(payload.url)
    return success_response(data=report.model_dump(mode="json"), message="URL threat inspection completed.", request=request)

@router.post("/domain", status_code=status.HTTP_200_OK, summary="Inspect Domain Intelligence & Typosquatting")
async def inspect_domain_threat(
    payload: DomainThreatRequest,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Inspects domain TLD risk, subdomain depth, Punycode homoglyphs, and brand typosquatting."""
    report = DomainIntelligenceEngine.analyze_domain_intel(payload.domain)
    return success_response(data=report.model_dump(mode="json"), message="Domain intelligence inspection completed.", request=request)

@router.post("/email", status_code=status.HTTP_200_OK, summary="Inspect Email Header Spoofing")
async def inspect_email_threat(
    payload: EmailThreatRequest,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Inspects email formatting, disposable email databases, webmail providers, and executive display name spoofing."""
    report = EmailIntelligenceEngine.analyze_email(payload.email_header)
    return success_response(data=report.model_dump(mode="json"), message="Email threat inspection completed.", request=request)

@router.post("/phone", status_code=status.HTTP_200_OK, summary="Inspect Phone Number Risk")
async def inspect_phone_threat(
    payload: PhoneThreatRequest,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Inspects international country code, E.164 formatting, premium rate numbers, and hidden digits."""
    report = PhoneIntelligenceEngine.parse_phone_number(payload.phone_number)
    return success_response(data=report.model_dump(mode="json"), message="Phone threat inspection completed.", request=request)

@router.post("/upi", status_code=status.HTTP_200_OK, summary="Inspect UPI VPA Handle Risk")
async def inspect_upi_threat(
    payload: UPIThreatRequest,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Inspects UPI VPA handle formatting, PSP provider, sponsor bank, and customer support desk spoofing."""
    report = UPIIntelligenceEngine.analyze_upi(payload.upi_id)
    return success_response(data=report.model_dump(mode="json"), message="UPI threat inspection completed.", request=request)

@router.post("/analyse", status_code=status.HTTP_200_OK, summary="Analyze Full Multi-Vector Threat Payload")
async def analyze_full_threat_payload(
    payload: FullThreatAnalyseRequest,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Executes end-to-end multi-vector Threat Intelligence pipeline across URLs, Domains, Emails, Phones, UPI IDs, Evidence, Scoring, and XAI."""
    scan_id = f"scn_th_{uuid.uuid4().hex[:10]}"
    pipeline_result = await ThreatIntelligenceService.analyze_threat_payload(scan_id=scan_id, raw_text=payload.text)
    return success_response(data=pipeline_result.model_dump(mode="json"), message="Multi-vector threat intelligence analysis completed.", request=request)
