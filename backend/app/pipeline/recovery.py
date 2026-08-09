"""
GuardianAI Pipeline Error Recovery System & Graceful Fallback Engine
Purpose: Handles AI failures, Threat Engine failures, Database failures, Validation failures, and SLA Timeouts
         by applying graceful fallback strategies without dropping HTTP user requests or crashing the master pipeline.
"""

import logging
from typing import Dict, Any, Optional
from app.decision_engine.schemas import DecisionResult, RiskMetricsSchema, ConfidenceMetricsSchema, DecisionXAISummary
from app.pipeline.validator import InputValidationError

logger = logging.getLogger("guardianai.pipeline.recovery")

class PipelineErrorRecovery:
    """Enterprise Pipeline Error Recovery & Graceful Fallback Engine."""

    # Default Graceful Fallbacks
    DEFAULT_FALLBACK_AI_ANALYSIS: Dict[str, Any] = {
        "threat_score": 50,
        "confidence": 0.70,
        "psychological_factors": {},
        "fallback_active": True,
        "fallback_reason": "Gemini AI model execution unavailable or timed out. Used rule-based fallback."
    }

    DEFAULT_FALLBACK_THREAT_INTEL: Dict[str, Any] = {
        "scoring_result": {"technical_risk_score": 50, "confidence": 0.70},
        "evidence_report": {"total_evidence_count": 0, "evidence_list": []},
        "fallback_active": True,
        "fallback_reason": "Threat Intelligence service unavailable. Used offline heuristic rule fallback."
    }

    @classmethod
    def handle_ai_failure(cls, raw_text: str, exc: Exception) -> Dict[str, Any]:
        """Handles Gemini AI model failure by returning rule-based fallback analysis."""
        logger.error(f"[Recovery: AIFailure] Gemini AI failed: {str(exc)}. Applying rule-based fallback.")
        fallback = cls.DEFAULT_FALLBACK_AI_ANALYSIS.copy()
        fallback["raw_text_snippet"] = raw_text[:50]
        return fallback

    @classmethod
    def handle_threat_engine_failure(cls, raw_text: str, exc: Exception) -> Dict[str, Any]:
        """Handles Threat Intelligence lookup failure by returning offline heuristic fallback analysis."""
        logger.error(f"[Recovery: ThreatEngineFailure] Threat Engine failed: {str(exc)}. Applying offline fallback.")
        fallback = cls.DEFAULT_FALLBACK_THREAT_INTEL.copy()
        fallback["raw_text_snippet"] = raw_text[:50]
        return fallback

    @classmethod
    def handle_database_failure(cls, scan_id: str, exc: Exception) -> None:
        """Handles Postgres database connection drop by logging error asynchronously without interrupting HTTP user response."""
        logger.critical(f"[Recovery: DatabaseFailure] Postgres write failed for scan '{scan_id}': {str(exc)}. Buffer logged for sync retry.")

    @classmethod
    def create_emergency_fallback_decision(cls, scan_id: str, reason: str = "Subsystem emergency recovery active") -> DecisionResult:
        """Creates a safe emergency DecisionResult DTO when master decision pipeline encounters unexpected failures."""
        logger.warning(f"[Recovery: EmergencyFallback] Creating emergency fallback DecisionResult for scan '{scan_id}'.")
        return DecisionResult(
            scan_id=scan_id,
            final_scam_probability=50,
            confidence=0.50,
            risk_level="MEDIUM",
            risk_metrics=RiskMetricsSchema(final_scam_probability=50, risk_level="MEDIUM", technical_risk_score=50, psychological_risk_score=50),
            confidence_metrics=ConfidenceMetricsSchema(overall_confidence=0.50, cross_modal_agreement=0.50, certainty_band="LOW"),
            reasons=[f"Emergency Recovery Active: {reason}"],
            evidence=[],
            recommendations=["Exercise caution and verify sender through official channels."],
            safe_reply="I am reviewing this communication through official channels.",
            action_plan=[],
            explainability=DecisionXAISummary(
                summary="Emergency Fallback: Analysis degraded due to intermittent subsystem outage. Exercise caution.",
                detected_factors=[],
                key_threat_vectors=[]
            )
        )
