"""
GuardianAI Master Decision Engine Pipeline Orchestrator
Purpose: Orchestrates complete 8-step Multi-Modal Fusion Decision Pipeline:
         Receive Analysis -> Merge Evidence -> Calculate Confidence -> Calculate Risk ->
         Generate Recommendations -> Generate XAI Explanation -> Generate Safe Reply -> Return DecisionResult DTO.
"""

import uuid
from typing import Optional, List, Dict, Any
from app.decision_engine.schemas import (
    DecisionRequest,
    DecisionResult,
    RiskMetricsSchema,
    ConfidenceMetricsSchema,
    EvidenceItemSchema,
    ActionPlanSchema,
    DecisionXAISummary
)
from app.decision_engine.evidence_aggregator import EvidenceFusionEngine
from app.decision_engine.confidence import ConfidenceEngine
from app.decision_engine.risk_classifier import RiskClassifierEngine
from app.decision_engine.action_planner import RecommendationEngine
from app.decision_engine.safe_reply import SafeReplyGenerator
from app.decision_engine.xai import DecisionXAIEngine

class DecisionPipeline:
    """Master Multi-Modal Fusion Decision Pipeline Orchestrator."""

    @classmethod
    async def evaluate_decision(
        cls,
        request: DecisionRequest,
        target_persona: str = "SENIOR_CITIZENS",
        locale: str = "en"
    ) -> DecisionResult:
        """
        Executes end-to-end 8-step decision evaluation pipeline.
        """
        sid = request.scan_id or f"scn_dec_{uuid.uuid4().hex[:10]}"

        # Extract intelligence subsystems data if available
        text_intel = request.text_intelligence or {}
        threat_intel = request.threat_intelligence or {}
        gemini = request.gemini_analysis or {}

        # 1. Gather Raw Evidence Lists
        threat_evidence_raw = threat_intel.get("evidence_report", {}).get("evidence_list", [])
        converted_evidence: List[EvidenceItemSchema] = []

        for e in threat_evidence_raw:
            converted_evidence.append(
                EvidenceItemSchema(
                    evidence_id=e.get("evidence_id", f"ev_{uuid.uuid4().hex[:6]}"),
                    indicator=e.get("indicator", "unknown"),
                    category=e.get("category", "THREAT"),
                    reason=e.get("reason", "Suspicious IOC indicator"),
                    severity=e.get("severity", "High"),
                    confidence=float(e.get("confidence", 0.95)),
                    source=e.get("source", "THREAT_INTELLIGENCE")
                )
            )

        # 2. Merge & Deduplicate Evidence
        fused_evidence_report = EvidenceFusionEngine.fuse_multi_source_evidence(
            scan_id=sid,
            threat_intel_evidence=converted_evidence
        )
        unified_evidence = fused_evidence_report.unified_evidence_list

        # 3. Calculate Confidence
        ai_conf = float(gemini.get("confidence", 0.90))
        ti_conf = float(threat_intel.get("scoring_result", {}).get("confidence", 0.95))
        confidence_result = ConfidenceEngine.calculate_confidence(
            gemini_confidence=ai_conf,
            threat_intel_confidence=ti_conf
        )

        # 4. Calculate Risk & Scam Probability
        technical_score = int(threat_intel.get("scoring_result", {}).get("technical_risk_score", 0))
        gemini_score = int(gemini.get("threat_score", 0))
        final_scam_prob = max(technical_score, gemini_score)

        risk_level_def = RiskClassifierEngine.classify_score(final_scam_prob)
        risk_level_str = risk_level_def.level_key

        # 5. Generate Recommendations & Action Plan
        scam_category = text_intel.get("scam_category_hint", "GENERIC_FRAUD")
        threat_keys = [e.reason for e in unified_evidence]
        rec_report = RecommendationEngine.generate_recommendations(
            scan_id=sid,
            risk_level=risk_level_str,
            scam_category=scam_category,
            detected_threat_keys=threat_keys
        )

        # 6. Generate Persona-Tailored XAI Explanation
        xai_report = DecisionXAIEngine.generate_full_xai_report(
            scan_id=sid,
            risk_level=risk_level_str,
            confidence=confidence_result.overall_confidence,
            evidence_list=[e.indicator for e in unified_evidence],
            scam_category=scam_category,
            target_persona=target_persona
        )

        # 7. Generate Safe Reply Template
        safe_reply_template = SafeReplyGenerator.generate_reply(
            scam_category=scam_category,
            locale=locale
        )

        # Construct Sub-DTO Metrics
        risk_metrics = RiskMetricsSchema(
            final_scam_probability=final_scam_prob,
            risk_level=risk_level_str,
            technical_risk_score=technical_score,
            psychological_risk_score=gemini_score
        )

        confidence_metrics = ConfidenceMetricsSchema(
            overall_confidence=confidence_result.overall_confidence,
            cross_modal_agreement=confidence_result.cross_modal_agreement,
            certainty_band=confidence_result.certainty_band
        )

        xai_summary_dto = DecisionXAISummary(
            summary=xai_report.primary_explanation.risk_summary,
            detected_factors=[k for k, v in gemini.get("psychological_factors", {}).items() if isinstance(v, dict) and v.get("detected")],
            key_threat_vectors=[e.category for e in unified_evidence]
        )

        reasons = [e.reason for e in unified_evidence] or [risk_level_def.user_header_message]

        # 8. Return Structured DecisionResult Output
        return DecisionResult(
            scan_id=sid,
            final_scam_probability=final_scam_prob,
            confidence=confidence_result.overall_confidence,
            risk_level=risk_level_str,
            risk_metrics=risk_metrics,
            confidence_metrics=confidence_metrics,
            reasons=reasons,
            evidence=unified_evidence,
            recommendations=rec_report.things_not_to_do + rec_report.reporting_suggestions,
            safe_reply=safe_reply_template.safe_reply_text,
            action_plan=rec_report.immediate_actions,
            explainability=xai_summary_dto
        )
