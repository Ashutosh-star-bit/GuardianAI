"""
GuardianAI Text Intelligence Output Schemas
Purpose: Defines Pydantic v2 DTOs for Feature Vectors, Detected Entities, Pattern Matches, XAI Rationale, and Text Intelligence Results.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class FeatureVector(BaseModel):
    """Extracted text features metrics DTO."""
    urgency_score: float = Field(ge=0.0, le=1.0, description="Urgency intensity score")
    financial_coercion_score: float = Field(ge=0.0, le=1.0, description="Financial demand intensity score")
    caps_ratio: float = Field(ge=0.0, le=1.0, description="Uppercase character ratio")
    link_count: int = Field(ge=0, description="Count of URLs/links in text")
    homoglyph_detected: bool = Field(default=False, description="Flag for spoofed homoglyph characters")

class DetectedEntity(BaseModel):
    """Named Entity (Brand, Contact, Money, Link) DTO."""
    entity_type: str = Field(description="BRAND, MONEY, PHONE, URL, UPI_HANDLE")
    text: str = Field(description="Extracted raw entity text")
    confidence: float = Field(ge=0.0, le=1.0)
    context: Optional[str] = None

class PatternMatch(BaseModel):
    """Pattern Detection Match DTO."""
    category: str = Field(description="Category e.g. URGENCY_PHRASE, BANK_SPOOF, COURIER_SCAM, JOB_SCAM")
    pattern_name: str
    matched_text: str
    severity: str = Field(description="Low, Medium, High, Critical")

class XAIRationale(BaseModel):
    """Explainable AI Rationale DTO."""
    plain_summary: str = Field(description="Non-technical plain language explanation")
    manipulation_tactics: List[str] = Field(default_factory=list, description="Tactics used e.g. Artificial Urgency")
    actionable_advice: str = Field(description="Recommended safe user action")

class TextIntelligenceResult(BaseModel):
    """Complete Text Intelligence Analysis Output DTO."""
    scan_id: str
    channel_type: str = Field(description="SMS, Email, WhatsApp, Telegram")
    scam_category_hint: Optional[str] = Field(default="GENERIC_FRAUD", description="Job, Lottery, Bank, Courier, etc.")
    features: FeatureVector
    entities: List[DetectedEntity] = Field(default_factory=list)
    patterns: List[PatternMatch] = Field(default_factory=list)
    explainability: XAIRationale
    language: str = Field(default="en")
