"""
GuardianAI Scan Analysis Endpoints
Purpose: Accepts text and URL payloads, executes heuristic feature checks, enqueues background tasks, and logs AI inference metrics.
"""

import time
import uuid
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user_optional
from app.schemas.scan import TextScanRequest, ScanResponse, TextHighlight
from app.models.user import User
from app.models.scan import Scan
from app.tasks.background import log_audit_event_async
from app.core.logging import log_ai_inference

router = APIRouter()

@router.post("/scan/text", response_model=ScanResponse, summary="Analyze Text or SMS Payload")
def scan_text(
    payload_in: TextScanRequest,
    bg_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional)
):
    """
    Analyzes raw text or SMS payload for scam signals, urgency triggers, and typosquatted links.
    Enqueues non-blocking background telemetry tasks, logs structured AI inference metrics, and returns calculated Threat Index (0-100), Risk Band, and XAI highlights.
    """
    start_time = time.time()
    text_content = payload_in.payload

    threat_score = 15
    risk_band = "safe"
    highlights = []
    remediation = []

    # Heuristic checks (Scaffold Demonstration)
    if "URGENT" in text_content.upper() or "ACCOUNT LOCKED" in text_content.upper():
        threat_score += 45
        highlights.append(TextHighlight(
            startOffset=text_content.upper().find("URGENT") if "URGENT" in text_content.upper() else 0,
            endOffset=6,
            text="URGENT",
            type="urgency_trigger",
            reason="High-urgency manipulation tactic designed to bypass critical thinking."
        ))

    if "http" in text_content.lower() or "paypa1" in text_content.lower():
        threat_score += 35
        highlights.append(TextHighlight(
            startOffset=text_content.lower().find("http") if "http" in text_content.lower() else 0,
            endOffset=len(text_content),
            text=text_content[text_content.lower().find("http"):],
            type="typosquat_url",
            reason="Suspicious or typosquatted web address detected."
        ))

    if threat_score >= 70:
        risk_band = "dangerous"
        plain_rationale = "This message contains an urgent demand and links to a suspicious or typosquatted domain."
        remediation = ["Do NOT click any links.", "Contact the sender using an official published phone number."]
    elif threat_score >= 30:
        risk_band = "caution"
        plain_rationale = "This message contains high urgency indicators. Exercise caution before acting."
        remediation = ["Verify the request independently before proceeding."]
    else:
        plain_rationale = "No obvious scam triggers or malicious domain spoofs detected."
        remediation = ["Standard communication. Remain vigilant."]

    execution_ms = round((time.time() - start_time) * 1000, 2)
    scan_id = f"scn_{uuid.uuid4().hex[:12]}"

    # Structured AI Inference Logging
    log_ai_inference(
        scan_id=scan_id,
        provider="heuristic_v1_groq_fallback",
        threat_score=threat_score,
        risk_band=risk_band,
        latency_ms=execution_ms,
        extra={"payload_length": len(text_content)}
    )

    # Persist scan result to DB unless Zero-Knowledge mode is active
    if not payload_in.zeroKnowledge and current_user:
        new_scan = Scan(
            id=scan_id,
            user_id=current_user.id,
            payload_type="text",
            threat_score=threat_score,
            risk_band=risk_band,
            plain_rationale=plain_rationale,
            execution_ms=int(execution_ms)
        )
        db.add(new_scan)
        db.commit()

        # Enqueue background telemetry audit task
        bg_tasks.add_task(log_audit_event_async, "scan.text.completed", current_user.id, {"scan_id": scan_id})

    return {
        "scanId": scan_id,
        "payloadType": "text",
        "threatScore": threat_score,
        "riskBand": risk_band,
        "plainRationale": plain_rationale,
        "highlights": highlights,
        "remediation": remediation,
        "executionMs": int(execution_ms)
    }
