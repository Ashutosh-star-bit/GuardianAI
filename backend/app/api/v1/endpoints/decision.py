"""
GuardianAI Decision Engine REST API Router
Purpose: Provides REST API endpoints for Master Decision Evaluation (/decision/analyse),
         Persona-Tailored XAI Explanations (/decision/explain), and Comprehensive Decision Reports (/decision/report).
"""

import uuid
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, Request, Depends, status
from pydantic import BaseModel, Field
from app.core.response import success_response
from app.api.deps import get_current_user
from app.models.user import User

from app.decision_engine.service import DecisionService
from app.decision_engine.pipeline import DecisionPipeline
from app.decision_engine.schemas import DecisionRequest
from app.decision_engine.xai import DecisionXAIEngine

router = APIRouter(prefix="/decision", tags=["Master Decision Engine"])

# 1. Decision Analyse Request Model
class DecisionAnalyseRequest(BaseModel):
    message: str = Field(min_length=5, max_length=10_000, description="Raw message payload body to inspect")
    channel_type: str = Field(default="SMS", description="SMS, Email, WhatsApp, Telegram, or Web")
    target_persona: str = Field(default="SENIOR_CITIZENS", description="SENIOR_CITIZENS, PARENTS, STUDENTS, PROFESSIONALS")
    locale: str = Field(default="en", description="en, es, hi, fr")

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "URGENT: Your PayPal account is suspended. Verify at http://paypa1-check.top or send $500 to support.refund@okaxis",
                "channel_type": "SMS",
                "target_persona": "SENIOR_CITIZENS",
                "locale": "en"
            }
        }
    }

# 2. Decision Explain Request Model
class DecisionExplainRequest(BaseModel):
    risk_level: str = Field(default="HIGH", description="SAFE, LOW, MEDIUM, HIGH, CRITICAL")
    confidence: float = Field(default=0.95, ge=0.0, le=1.0)
    evidence_list: List[str] = Field(default_factory=list, description="List of primary threat evidence items")
    target_persona: str = Field(default="SENIOR_CITIZENS", description="SENIOR_CITIZENS, PARENTS, STUDENTS, PROFESSIONALS")

    model_config = {
        "json_schema_extra": {
            "example": {
                "risk_level": "CRITICAL",
                "confidence": 0.98,
                "evidence_list": ["paypa1-check.top typosquatting link", "support.refund@okaxis UPI handle spoofing"],
                "target_persona": "SENIOR_CITIZENS"
            }
        }
    }

# --- ENDPOINTS ---

@router.post("/analyse", status_code=status.HTTP_200_OK, summary="Execute Master Multi-Modal Fusion Decision Evaluation")
async def execute_decision_analysis(
    payload: DecisionAnalyseRequest,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """
    Executes end-to-end multi-modal fusion decision scan:
    Executes Text Intelligence, Threat Intelligence, and Decision Pipeline Fusion, returning final scam probability,
    risk level, evidence, recommendations, action plan, and safe reply.
    """
    scan_id = f"scn_dec_{uuid.uuid4().hex[:10]}"
    service_report = await DecisionService.process_full_decision_scan(
        scan_id=scan_id,
        raw_text=payload.message,
        channel_type=payload.channel_type,
        target_persona=payload.target_persona,
        locale=payload.locale
    )

    return success_response(
        data=service_report.decision.model_dump(mode="json"),
        message="Master decision evaluation completed successfully.",
        request=request
    )

@router.post("/explain", status_code=status.HTTP_200_OK, summary="Generate Persona-Tailored Human-Friendly XAI Explanation")
async def generate_persona_explanation(
    payload: DecisionExplainRequest,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """
    Generates persona-tailored XAI explanations customized for Senior Citizens, Parents, Students, or Professionals.
    """
    scan_id = f"scn_xai_{uuid.uuid4().hex[:10]}"
    xai_report = DecisionXAIEngine.generate_full_xai_report(
        scan_id=scan_id,
        risk_level=payload.risk_level,
        confidence=payload.confidence,
        evidence_list=payload.evidence_list,
        target_persona=payload.target_persona
    )

    return success_response(
        data=xai_report.model_dump(mode="json"),
        message="Persona-tailored XAI explanation generated successfully.",
        request=request
    )

@router.post("/report", status_code=status.HTTP_200_OK, summary="Generate High-Level Comprehensive Decision Service Report")
async def generate_decision_report(
    payload: DecisionAnalyseRequest,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """
    Generates high-level DecisionServiceReport JSON envelope combining decision DTO, text intelligence summary, and threat intelligence summary.
    """
    scan_id = f"scn_rpt_{uuid.uuid4().hex[:10]}"
    service_report = await DecisionService.process_full_decision_scan(
        scan_id=scan_id,
        raw_text=payload.message,
        channel_type=payload.channel_type,
        target_persona=payload.target_persona,
        locale=payload.locale
    )

    return success_response(
        data=service_report.model_dump(mode="json"),
        message="Comprehensive decision report generated successfully.",
        request=request
    )
