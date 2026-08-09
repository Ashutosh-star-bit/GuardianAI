"""
GuardianAI Master Decision Engine Pydantic Models & DTOs
Purpose: Defines Pydantic v2 DTOs for DecisionRequest, DecisionResult, EvidenceItemSchema, ReasonItemSchema,
         RecommendationItemSchema, ConfidenceMetricsSchema, RiskMetricsSchema, ActionPlanSchema, and future modality extensions.
"""

from datetime import datetime, timezone
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, ConfigDict

# --- INPUT MODELS ---

class ModalitySignals(BaseModel):
    """Container for future modality signals (OCR, Voice, Browser, QR, Community)."""
    ocr_text: Optional[str] = None
    voice_transcript: Optional[str] = None
    voice_deepfake_score: Optional[float] = None
    browser_dom_risk: Optional[float] = None
    qr_decoded_url: Optional[str] = None
    community_report_count: Optional[int] = 0

    model_config = ConfigDict(extra="ignore")

class DecisionRequest(BaseModel):
    """Input Request Payload for Master Decision Engine Execution."""
    scan_id: str = Field(description="Unique scan payload identifier e.g. scn_dec_1001")
    raw_text: str = Field(description="Raw text or message payload body")
    channel_type: str = Field(default="SMS", description="SMS, Email, WhatsApp, Telegram, or Web")
    text_intelligence: Optional[Dict[str, Any]] = Field(default=None, description="Pre-computed Text Intelligence output")
    threat_intelligence: Optional[Dict[str, Any]] = Field(default=None, description="Pre-computed Threat Intelligence output")
    gemini_analysis: Optional[Dict[str, Any]] = Field(default=None, description="Pre-computed Gemini LLM analysis output")
    future_modalities: Optional[ModalitySignals] = Field(default_factory=ModalitySignals)

    model_config = ConfigDict(extra="ignore")

# --- OUTPUT SUB-MODELS ---

class EvidenceItemSchema(BaseModel):
    """Standardized Evidence Record DTO."""
    evidence_id: str
    indicator: str = Field(description="Exact IOC value e.g. paypa1-check.com")
    category: str = Field(description="URL, DOMAIN, EMAIL, PHONE, UPI_ID, BANK, PATTERN, KEYWORD")
    reason: str = Field(description="Human-readable threat explanation")
    severity: str = Field(description="Low, Medium, High, Critical")
    confidence: float = Field(ge=0.0, le=1.0)
    source: str = Field(description="Originating subsystem module")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(extra="ignore")

class ConfidenceMetricsSchema(BaseModel):
    """Statistical Confidence Breakdown DTO."""
    overall_confidence: float = Field(ge=0.0, le=1.0, description="Composite confidence rating 0.0 to 1.0")
    cross_modal_agreement: float = Field(ge=0.0, le=1.0, description="Agreement metric between AI and Technical IOC signals")
    certainty_band: str = Field(default="HIGH", description="LOW, MEDIUM, HIGH, VERY_HIGH")

    model_config = ConfigDict(extra="ignore")

class RiskMetricsSchema(BaseModel):
    """Composite Threat Risk Breakdown DTO."""
    final_scam_probability: int = Field(ge=0, le=100, description="Final fused scam probability score 0 to 100")
    risk_level: str = Field(description="SAFE, CAUTION, DANGEROUS")
    technical_risk_score: int = Field(ge=0, le=100)
    psychological_risk_score: int = Field(ge=0, le=100)

    model_config = ConfigDict(extra="ignore")

class ActionPlanSchema(BaseModel):
    """Structured Step-by-Step Security Action Plan DTO."""
    step_number: int
    title: str
    instruction: str
    urgency: str = Field(default="IMMEDIATE", description="IMMEDIATE, RECOMMENDED, OPTIONAL")

    model_config = ConfigDict(extra="ignore")

class DecisionXAISummary(BaseModel):
    """Transparent Explainability Summary DTO."""
    summary: str = Field(description="Non-technical plain language rationale summary")
    detected_factors: List[str] = Field(default_factory=list)
    key_threat_vectors: List[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="ignore")

# --- MASTER DECISION RESULT MODEL ---

class DecisionResult(BaseModel):
    """Complete Master Decision Engine Output DTO."""
    scan_id: str
    final_scam_probability: int = Field(ge=0, le=100, description="Overall scam probability score 0 to 100")
    confidence: float = Field(ge=0.0, le=1.0, description="Aggregate confidence rating")
    risk_level: str = Field(description="SAFE, CAUTION, DANGEROUS")
    risk_metrics: RiskMetricsSchema
    confidence_metrics: ConfidenceMetricsSchema
    reasons: List[str] = Field(default_factory=list, description="Specific threat rationale statements")
    evidence: List[EvidenceItemSchema] = Field(default_factory=list, description="Aggregated evidence list")
    recommendations: List[str] = Field(default_factory=list, description="Actionable safety guidance")
    safe_reply: Optional[str] = Field(default=None, description="AI-generated safe decline reply template")
    action_plan: List[ActionPlanSchema] = Field(default_factory=list, description="Step-by-step security action steps")
    explainability: DecisionXAISummary

    # Future Scalability Guarantee: Ignore extra attributes from future Decision Engine upgrades
    model_config = ConfigDict(extra="ignore", from_attributes=True)
