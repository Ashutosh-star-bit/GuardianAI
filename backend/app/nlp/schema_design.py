"""
GuardianAI Text Intelligence Gemini JSON Response Schema Design
Purpose: Defines Pydantic v2 DTOs for Gemini LLM threat analysis responses supporting 7 psychological techniques,
         detected features, entities, risk indicators, XAI explanations, recommendations, and future compatibility.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, ConfigDict

class PsychologicalFactorDetail(BaseModel):
    """Detailed breakdown for a single psychological manipulation factor."""
    detected: bool = Field(description="Flag indicating if factor is present")
    intensity: str = Field(default="low", description="low, medium, high, critical")
    evidence: Optional[str] = Field(default="", description="Supporting text evidence from payload")

    model_config = ConfigDict(extra="ignore")

class PsychologicalTechniquesBreakdown(BaseModel):
    """Container for 7 psychological manipulation factors."""
    urgency: PsychologicalFactorDetail
    fear: PsychologicalFactorDetail
    greed: PsychologicalFactorDetail
    authority: PsychologicalFactorDetail
    trust: PsychologicalFactorDetail
    impersonation: PsychologicalFactorDetail
    social_engineering: PsychologicalFactorDetail

    model_config = ConfigDict(extra="ignore")

class RiskIndicatorItem(BaseModel):
    """Individual risk indicator flag."""
    indicator_key: str
    severity: str = Field(description="Low, Medium, High, Critical")
    description: str

    model_config = ConfigDict(extra="ignore")

class GeminiTextThreatAnalysisSchema(BaseModel):
    """Complete Production JSON Schema for Gemini Text Intelligence Analysis Output."""
    threat_score: int = Field(ge=0, le=100, description="Overall threat score 0 to 100")
    risk_band: str = Field(description="safe, caution, or dangerous")
    confidence: float = Field(ge=0.0, le=1.0, description="Model confidence level")
    detected_features: Dict[str, Any] = Field(default_factory=dict, description="Extracted NLP technical features")
    entities: List[Dict[str, Any]] = Field(default_factory=list, description="Extracted named entities")
    reasons: List[str] = Field(default_factory=list, description="List of threat rationale statements")
    risk_indicators: List[RiskIndicatorItem] = Field(default_factory=list, description="Categorized risk indicators")
    explanation: str = Field(description="Plain-language non-technical explanation")
    psychological_techniques: PsychologicalTechniquesBreakdown = Field(description="7 psychological manipulation factors")
    recommendations: List[str] = Field(default_factory=list, description="Actionable safety guidance for user")

    # Future Compatibility: Ignore extra unexpected keys added by future model versions
    model_config = ConfigDict(extra="ignore", from_attributes=True)
