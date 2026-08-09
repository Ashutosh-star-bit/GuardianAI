"""
GuardianAI Environment-Aware AI Engine Configuration
Purpose: Provides environment profiles (development, testing, production) for Gemini model parameters,
         safety settings, SLA timeouts, retry limits, and token pricing.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from app.core.config import settings

class AISafetySettings(BaseModel):
    """Gemini Safety Filter Configuration Matrix."""
    category_hate_speech: str = Field(default="BLOCK_MEDIUM_AND_ABOVE")
    category_harassment: str = Field(default="BLOCK_MEDIUM_AND_ABOVE")
    category_sexually_explicit: str = Field(default="BLOCK_LOW_AND_ABOVE")
    category_dangerous_content: str = Field(default="BLOCK_MEDIUM_AND_ABOVE")

class AIEnvironmentConfig(BaseModel):
    """Complete AI Engine Environment Configuration Profile."""
    environment: str = Field(description="Environment mode: development, testing, production")
    DEFAULT_MODEL: str = Field(default="gemini-3.6-flash-high", description="Primary LLM Model ID")
    FALLBACK_MODEL: str = Field(default="mock-ai-engine", description="Fallback Model ID")
    TEMPERATURE: float = Field(default=0.1, ge=0.0, le=1.0, description="Sampling temperature")
    TOP_P: float = Field(default=0.95, ge=0.0, le=1.0)
    MAX_TOKENS: int = Field(default=2048, ge=128)
    TIMEOUT_SECONDS: float = Field(default=10.0, description="Strict SLA request timeout in seconds")
    MAX_RETRIES: int = Field(default=3, description="Maximum retry attempts with exponential backoff")

    # Pricing Tiers per 1 Million Tokens (USD) for Gemini 3.6 Flash High
    PRICING_PER_1M_INPUT_TOKENS: float = 0.075
    PRICING_PER_1M_OUTPUT_TOKENS: float = 0.300

    # Safety Filter Settings
    safety_settings: AISafetySettings = Field(default_factory=AISafetySettings)

# Profile Definitions
DEVELOPMENT_AI_CONFIG = AIEnvironmentConfig(
    environment="development",
    DEFAULT_MODEL="gemini-3.6-flash-high",
    FALLBACK_MODEL="mock-ai-engine",
    TEMPERATURE=0.2,
    TOP_P=0.95,
    MAX_TOKENS=2048,
    TIMEOUT_SECONDS=15.0,
    MAX_RETRIES=2
)

TESTING_AI_CONFIG = AIEnvironmentConfig(
    environment="testing",
    DEFAULT_MODEL="mock-ai-engine",
    FALLBACK_MODEL="mock-ai-engine",
    TEMPERATURE=0.0, # Deterministic for unit tests
    TOP_P=1.0,
    MAX_TOKENS=1024,
    TIMEOUT_SECONDS=5.0,
    MAX_RETRIES=0
)

PRODUCTION_AI_CONFIG = AIEnvironmentConfig(
    environment="production",
    DEFAULT_MODEL="gemini-3.6-flash-high",
    FALLBACK_MODEL="mock-ai-engine",
    TEMPERATURE=0.1, # Strict XAI precision
    TOP_P=0.95,
    MAX_TOKENS=4096,
    TIMEOUT_SECONDS=10.0, # Strict SLA
    MAX_RETRIES=3
)

def get_ai_config() -> AIEnvironmentConfig:
    """Dynamically loads AI configuration profile based on system settings.ENVIRONMENT."""
    env = getattr(settings, "ENVIRONMENT", "development").lower()

    if env == "testing":
        return TESTING_AI_CONFIG
    elif env == "production":
        return PRODUCTION_AI_CONFIG
    else:
        return DEVELOPMENT_AI_CONFIG

# Active Global AI Settings Instance
ai_settings = get_ai_config()
