"""
GuardianAI SMS & Text Smishing Threat Inspection Endpoint
Purpose: Analyzes raw text payload for artificial urgency, impersonation, typosquatting links, and psychological triggers via TextIntelligencePipeline.
"""

import uuid
from fastapi import APIRouter, Request, Depends, status
from pydantic import BaseModel, Field
from app.core.response import success_response
from app.api.deps import get_current_user
from app.models.user import User
from app.nlp.pipeline import TextIntelligencePipeline, TextIntelligencePipelineResult

router = APIRouter(prefix="/scan", tags=["Message Scans"])

class MessageScanRequest(BaseModel):
    message: str = Field(min_length=5, description="Raw SMS or text message body to inspect")
    channel_type: str = Field(default="SMS", description="SMS, WhatsApp, Telegram, or Email")

@router.post("/message", status_code=status.HTTP_200_OK, summary="Inspect Text/SMS Payload with Gemini AI")
async def scan_message_payload(
    payload: MessageScanRequest,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """
    Executes end-to-end 8-step Text Intelligence AI Pipeline:
    Preprocesses text, extracts entities/patterns, renders versioned prompt, calls Gemini 3.6 Flash High,
    auto-repairs JSON, and returns structured threat analysis DTO.
    """
    scan_id = f"scn_msg_{uuid.uuid4().hex[:10]}"
    pipeline = TextIntelligencePipeline()

    pipeline_result: TextIntelligencePipelineResult = await pipeline.execute_pipeline(
        scan_id=scan_id,
        raw_text=payload.message,
        channel_type=payload.channel_type,
        user_id=current_user.id
    )

    return success_response(
        data=pipeline_result.model_dump(mode="json"),
        message="Message scan threat analysis completed successfully.",
        request=request
    )
