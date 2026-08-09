"""
GuardianAI DecisionService Enterprise Service Layer
Purpose: High-level application service accepting multi-modal analysis modules, executing Text Intelligence,
         Threat Intelligence, and Decision Pipelines, and returning structured JSON Decision Reports.
"""

import uuid
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

from app.nlp.engine import TextIntelligenceEngine
from app.threat_intel.service import ThreatIntelligenceService
from app.decision_engine.schemas import DecisionRequest, DecisionResult
from app.decision_engine.pipeline import DecisionPipeline

class DecisionServiceReport(BaseModel):
    """High-Level Decision Service Execution Output Envelope DTO."""
    scan_id: str
    channel_type: str
    target_persona: str
    locale: str
    decision: DecisionResult
    text_intelligence_summary: Optional[Dict[str, Any]] = None
    threat_intelligence_summary: Optional[Dict[str, Any]] = None

class DecisionService:
    """Enterprise Master Decision Service Orchestrator."""

    @classmethod
    async def process_full_decision_scan(
        cls,
        scan_id: Optional[str] = None,
        raw_text: str = "",
        channel_type: str = "SMS",
        target_persona: str = "SENIOR_CITIZENS",
        locale: str = "en",
        precomputed_text_intel: Optional[Dict[str, Any]] = None,
        precomputed_threat_intel: Optional[Dict[str, Any]] = None,
        precomputed_gemini_analysis: Optional[Dict[str, Any]] = None
    ) -> DecisionServiceReport:
        """
        Executes end-to-end multi-modal scan:
        1. Executes Text Intelligence Engine if precomputed output omitted
        2. Executes Threat Intelligence Service if precomputed output omitted
        3. Executes Master Decision Pipeline Fusion
        4. Returns structured DecisionServiceReport DTO ready for JSON serialization
        """
        sid = scan_id or f"scn_srv_{uuid.uuid4().hex[:10]}"

        # 1. Text Intelligence Engine Step
        if precomputed_text_intel:
            text_intel_data = precomputed_text_intel
        else:
            text_result = TextIntelligenceEngine.analyze_text(
                scan_id=sid,
                raw_text=raw_text,
                channel_type=channel_type
            )
            text_intel_data = text_result.model_dump(mode="json")

        # 2. Threat Intelligence Service Step
        if precomputed_threat_intel:
            threat_intel_data = precomputed_threat_intel
        else:
            threat_result = await ThreatIntelligenceService.analyze_threat_payload(
                scan_id=sid,
                raw_text=raw_text
            )
            threat_intel_data = threat_result.model_dump(mode="json")

        # Mock / Precomputed Gemini Analysis if omitted
        if precomputed_gemini_analysis:
            gemini_data = precomputed_gemini_analysis
        else:
            gemini_data = {
                "threat_score": threat_intel_data.get("scoring_result", {}).get("technical_risk_score", 50),
                "confidence": 0.95,
                "psychological_factors": {
                    "urgency": {"detected": True},
                    "fear": {"detected": True},
                    "impersonation": {"detected": True}
                }
            }

        # 3. Master Decision Pipeline Execution
        decision_request = DecisionRequest(
            scan_id=sid,
            raw_text=raw_text,
            channel_type=channel_type,
            text_intelligence=text_intel_data,
            threat_intelligence=threat_intel_data,
            gemini_analysis=gemini_data
        )

        decision_result: DecisionResult = await DecisionPipeline.evaluate_decision(
            request=decision_request,
            target_persona=target_persona,
            locale=locale
        )

        # 4. Return DecisionServiceReport Envelope DTO
        return DecisionServiceReport(
            scan_id=sid,
            channel_type=channel_type,
            target_persona=target_persona,
            locale=locale,
            decision=decision_result,
            text_intelligence_summary={
                "scam_category_hint": text_intel_data.get("scam_category_hint"),
                "urgency_score": text_intel_data.get("features", {}).get("urgency_score", 0.0),
                "entities_count": len(text_intel_data.get("entities", []))
            },
            threat_intelligence_summary={
                "technical_risk_score": threat_intel_data.get("scoring_result", {}).get("technical_risk_score", 0),
                "evidence_count": threat_intel_data.get("evidence_report", {}).get("total_evidence_count", 0)
            }
        )
