"""
GuardianAI Statistical Confidence Engine
Purpose: Combines confidence scores from Gemini AI, Threat Intelligence, Pattern Detection, and Entity Detection
         into a weighted aggregate confidence rating, cross-modal agreement score, certainty band, and human-readable explanation.
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

# Multi-Source Confidence Fusion Weights
WEIGHT_GEMINI = 0.35
WEIGHT_THREAT_INTEL = 0.35
WEIGHT_PATTERNS = 0.15
WEIGHT_ENTITIES = 0.15

class ConfidenceAnalysisResult(BaseModel):
    """Structured Statistical Confidence Analysis Output DTO."""
    overall_confidence: float = Field(ge=0.0, le=1.0, description="Weighted aggregate confidence 0.0 to 1.0")
    cross_modal_agreement: float = Field(ge=0.0, le=1.0, description="Agreement metric between AI and Technical signals")
    certainty_band: str = Field(description="LOW (0.0-0.69), MEDIUM (0.70-0.84), HIGH (0.85-0.94), VERY_HIGH (0.95-1.0)")
    explanation: str = Field(description="Human-readable confidence derivation explanation")
    gemini_confidence: float
    threat_intel_confidence: float
    pattern_confidence: float
    entity_confidence: float

class ConfidenceEngine:
    """Enterprise Statistical Confidence Engine."""

    @classmethod
    def calculate_confidence(
        cls,
        gemini_confidence: Optional[float] = None,
        threat_intel_confidence: Optional[float] = None,
        pattern_confidence: Optional[float] = None,
        entity_confidence: Optional[float] = None
    ) -> ConfidenceAnalysisResult:
        """
        Calculates weighted aggregate confidence, cross-modal agreement score, and certainty band.
        Handles missing inputs gracefully via dynamic weight redistribution.
        """
        # Default Fallback Values
        g_conf = gemini_confidence if gemini_confidence is not None else 0.85
        t_conf = threat_intel_confidence if threat_intel_confidence is not None else 0.90
        p_conf = pattern_confidence if pattern_confidence is not None else 0.85
        e_conf = entity_confidence if entity_confidence is not None else 0.90

        # Dynamic Weight Calculation
        total_weight = 0.0
        weighted_sum = 0.0

        if gemini_confidence is not None:
            weighted_sum += g_conf * WEIGHT_GEMINI
            total_weight += WEIGHT_GEMINI

        if threat_intel_confidence is not None:
            weighted_sum += t_conf * WEIGHT_THREAT_INTEL
            total_weight += WEIGHT_THREAT_INTEL

        if pattern_confidence is not None:
            weighted_sum += p_conf * WEIGHT_PATTERNS
            total_weight += WEIGHT_PATTERNS

        if entity_confidence is not None:
            weighted_sum += e_conf * WEIGHT_ENTITIES
            total_weight += WEIGHT_ENTITIES

        # Fallback if zero inputs provided
        if total_weight == 0.0:
            overall_confidence = 0.85
        else:
            overall_confidence = weighted_sum / total_weight

        overall_confidence = round(min(1.0, max(0.0, overall_confidence)), 3)

        # Cross-Modal Signal Agreement Calculation (|Gemini - ThreatIntel| delta)
        agreement_delta = abs(g_conf - t_conf)
        cross_modal_agreement = round(max(0.0, 1.0 - agreement_delta), 3)

        # Certainty Band Assignment
        if overall_confidence >= 0.90 and cross_modal_agreement >= 0.85:
            certainty_band = "VERY_HIGH"
            exp = "Very high confidence. Strong cross-modal agreement between Gemini AI and technical IOC threat analyzers."
        elif overall_confidence >= 0.85:
            certainty_band = "HIGH"
            exp = "High confidence derived from multi-source AI and technical indicator analysis."
        elif overall_confidence >= 0.70:
            certainty_band = "MEDIUM"
            exp = "Medium confidence. Modest signal correlation between AI evaluation and technical indicators."
        else:
            certainty_band = "LOW"
            exp = "Low confidence due to missing or conflicting multi-source intelligence signals."

        return ConfidenceAnalysisResult(
            overall_confidence=overall_confidence,
            cross_modal_agreement=cross_modal_agreement,
            certainty_band=certainty_band,
            explanation=exp,
            gemini_confidence=g_conf,
            threat_intel_confidence=t_conf,
            pattern_confidence=p_conf,
            entity_confidence=e_conf
        )
