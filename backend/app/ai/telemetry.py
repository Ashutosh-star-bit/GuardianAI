"""
GuardianAI AI Telemetry, Token & Cost Tracking System
Purpose: Tracks prompt tokens, completion tokens, total tokens, calculates exact USD inference costs, and emits structured logs.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from app.ai.config import ai_settings
from app.core.logging import log_ai_inference

class AITelemetryMetrics(BaseModel):
    """Telemetry metrics DTO for an AI model execution."""
    model_id: str
    prompt_tokens: int = Field(default=0, ge=0)
    completion_tokens: int = Field(default=0, ge=0)
    total_tokens: int = Field(default=0, ge=0)
    estimated_cost_usd: float = Field(default=0.0, ge=0.0)
    latency_ms: float = Field(default=0.0, ge=0.0)
    retries_count: int = Field(default=0, ge=0)

class AITelemetryTracker:
    """Calculates token counts, computes cost in USD, and logs telemetry."""

    @staticmethod
    def calculate_cost(prompt_tokens: int, completion_tokens: int) -> float:
        """Calculates inference cost in USD based on Gemini Flash pricing tiers."""
        input_cost = (prompt_tokens / 1_000_000.0) * ai_settings.PRICING_PER_1M_INPUT_TOKENS
        output_cost = (completion_tokens / 1_000_000.0) * ai_settings.PRICING_PER_1M_OUTPUT_TOKENS
        return round(input_cost + output_cost, 6)

    @classmethod
    def record_metrics(
        cls,
        scan_id: str,
        payload_type: str,
        model_id: str,
        threat_score: int,
        risk_band: str,
        prompt_tokens: int,
        completion_tokens: int,
        latency_ms: float,
        confidence: float = 0.95,
        retries_count: int = 0
    ) -> AITelemetryMetrics:
        """Computes metrics, records telemetry logs, and returns metrics object."""
        total_tokens = prompt_tokens + completion_tokens
        cost_usd = cls.calculate_cost(prompt_tokens, completion_tokens)

        metrics = AITelemetryMetrics(
            model_id=model_id,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            estimated_cost_usd=cost_usd,
            latency_ms=latency_ms,
            retries_count=retries_count
        )

        log_ai_inference(
            scan_id=scan_id,
            payload_type=payload_type,
            provider=model_id,
            threat_score=threat_score,
            risk_band=risk_band,
            latency_ms=latency_ms,
            confidence=confidence,
            extra={
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
                "estimated_cost_usd": cost_usd,
                "retries_count": retries_count
            }
        )

        return metrics
