"""
GuardianAI Modular Threat Scoring Engine
Purpose: Calculates composite Technical Risk Score, Domain Risk, URL Risk, UPI Risk, Email Risk, Phone Risk,
         Evidence Count, and Aggregate Confidence without forcing a final binary scam decision.
"""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from app.threat_intel.evidence_builder import ThreatEvidenceReport

# Component Risk Weights
WEIGHT_DOMAIN = 0.25
WEIGHT_URL = 0.25
WEIGHT_UPI = 0.20
WEIGHT_EMAIL = 0.15
WEIGHT_PHONE = 0.15

class ComponentRiskBreakdown(BaseModel):
    """Individual component risk scores breakdown (0 - 100)."""
    domain_risk: int = Field(default=0, ge=0, le=100)
    url_risk: int = Field(default=0, ge=0, le=100)
    upi_risk: int = Field(default=0, ge=0, le=100)
    email_risk: int = Field(default=0, ge=0, le=100)
    phone_risk: int = Field(default=0, ge=0, le=100)

class ThreatScoreResult(BaseModel):
    """Modular Threat Scoring Engine Output DTO."""
    scan_id: str
    technical_risk_score: int = Field(ge=0, le=100, description="Composite weighted Technical Risk Score 0 - 100")
    risk_band: str = Field(description="safe (0-29), caution (30-69), dangerous (70-100)")
    confidence: float = Field(ge=0.0, le=1.0, description="Aggregate confidence 0.0 - 1.0")
    evidence_count: int
    component_risks: ComponentRiskBreakdown

class ThreatScoringEngine:
    """Enterprise Modular Threat Scoring Engine."""

    @classmethod
    def calculate_threat_score(
        cls,
        scan_id: str,
        domain_risk: int = 0,
        url_risk: int = 0,
        upi_risk: int = 0,
        email_risk: int = 0,
        phone_risk: int = 0,
        evidence_report: Optional[ThreatEvidenceReport] = None
    ) -> ThreatScoreResult:
        """
        Calculates composite Technical Risk Score using weighted component risk inputs.
        Does NOT enforce final binary scam decision.
        """
        # Weighted combination calculation
        weighted_score = (
            (domain_risk * WEIGHT_DOMAIN) +
            (url_risk * WEIGHT_URL) +
            (upi_risk * WEIGHT_UPI) +
            (email_risk * WEIGHT_EMAIL) +
            (phone_risk * WEIGHT_PHONE)
        )
        max_component = max(domain_risk, url_risk, upi_risk, email_risk, phone_risk)
        composite_score = max(weighted_score, max_component * 0.75)
        technical_risk_score = min(100, int(round(composite_score)))

        # Qualitative Risk Band Assignment
        if technical_risk_score >= 70:
            risk_band = "dangerous"
        elif technical_risk_score >= 30:
            risk_band = "caution"
        else:
            risk_band = "safe"

        # Evidence Count & Confidence Calculation
        ev_count = evidence_report.total_evidence_count if evidence_report else 0
        if ev_count >= 3 or technical_risk_score >= 70:
            confidence = 0.95
        elif ev_count >= 1 or technical_risk_score >= 30:
            confidence = 0.85
        else:
            confidence = 0.70

        components = ComponentRiskBreakdown(
            domain_risk=domain_risk,
            url_risk=url_risk,
            upi_risk=upi_risk,
            email_risk=email_risk,
            phone_risk=phone_risk
        )

        return ThreatScoreResult(
            scan_id=scan_id,
            technical_risk_score=technical_risk_score,
            risk_band=risk_band,
            confidence=confidence,
            evidence_count=ev_count,
            component_risks=components
        )
