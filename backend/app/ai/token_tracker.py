"""
GuardianAI Enterprise Token Tracking & Cost Analytics Engine
Purpose: Tracks prompt, completion, and total token usage, calculates USD inference costs,
         aggregates daily/monthly usage metrics, and provides data structures for executive dashboards.
"""

from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from app.ai.config import ai_settings

class TokenUsageRecord(BaseModel):
    """Single token usage transaction record."""
    scan_id: str
    user_id: Optional[str] = "ANONYMOUS"
    model_id: str
    prompt_tokens: int = Field(ge=0)
    completion_tokens: int = Field(ge=0)
    total_tokens: int = Field(ge=0)
    estimated_cost_usd: float = Field(ge=0.0)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class PeriodUsageSummary(BaseModel):
    """Usage summary for a specific time period (daily or monthly)."""
    period_key: str = Field(description="Format YYYY-MM-DD for daily or YYYY-MM for monthly")
    total_requests: int = Field(default=0, ge=0)
    prompt_tokens: int = Field(default=0, ge=0)
    completion_tokens: int = Field(default=0, ge=0)
    total_tokens: int = Field(default=0, ge=0)
    estimated_cost_usd: float = Field(default=0.0, ge=0.0)

class ExecutiveTokenAnalyticsReport(BaseModel):
    """Dashboard-ready Token Analytics Report DTO."""
    total_lifetime_requests: int
    total_lifetime_tokens: int
    total_lifetime_cost_usd: float
    today_summary: PeriodUsageSummary
    current_month_summary: PeriodUsageSummary
    daily_history: List[PeriodUsageSummary]
    monthly_history: List[PeriodUsageSummary]

class TokenTracker:
    """In-Memory / Persistent Token Tracking & Analytics Engine."""

    _records: List[TokenUsageRecord] = []

    @staticmethod
    def calculate_usd_cost(
        prompt_tokens: int,
        completion_tokens: int,
        price_per_1m_prompt: float = ai_settings.PRICING_PER_1M_INPUT_TOKENS,
        price_per_1m_completion: float = ai_settings.PRICING_PER_1M_OUTPUT_TOKENS
    ) -> float:
        """Calculates inference cost in USD based on model pricing tiers."""
        prompt_cost = (prompt_tokens / 1_000_000.0) * price_per_1m_prompt
        completion_cost = (completion_tokens / 1_000_000.0) * price_per_1m_completion
        return round(prompt_cost + completion_cost, 6)

    @classmethod
    def record_usage(
        cls,
        scan_id: str,
        prompt_tokens: int,
        completion_tokens: int,
        model_id: str = "gemini-3.6-flash-high",
        user_id: Optional[str] = None
    ) -> TokenUsageRecord:
        """Records a token usage transaction and returns record object."""
        total_tokens = prompt_tokens + completion_tokens
        cost_usd = cls.calculate_usd_cost(prompt_tokens, completion_tokens)

        record = TokenUsageRecord(
            scan_id=scan_id,
            user_id=user_id or "ANONYMOUS",
            model_id=model_id,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            estimated_cost_usd=cost_usd
        )

        cls._records.append(record)
        return record

    @classmethod
    def get_analytics_report(cls) -> ExecutiveTokenAnalyticsReport:
        """Generates executive dashboard analytics report aggregating daily and monthly metrics."""
        now = datetime.now(timezone.utc)
        today_key = now.strftime("%Y-%m-%d")
        current_month_key = now.strftime("%Y-%m")

        daily_map: Dict[str, PeriodUsageSummary] = {}
        monthly_map: Dict[str, PeriodUsageSummary] = {}

        total_requests = len(cls._records)
        total_tokens = 0
        total_cost = 0.0

        for r in cls._records:
            dt = datetime.fromisoformat(r.timestamp)
            d_key = dt.strftime("%Y-%m-%d")
            m_key = dt.strftime("%Y-%m")

            total_tokens += r.total_tokens
            total_cost += r.estimated_cost_usd

            # Aggregate Daily
            if d_key not in daily_map:
                daily_map[d_key] = PeriodUsageSummary(period_key=d_key)
            daily_map[d_key].total_requests += 1
            daily_map[d_key].prompt_tokens += r.prompt_tokens
            daily_map[d_key].completion_tokens += r.completion_tokens
            daily_map[d_key].total_tokens += r.total_tokens
            daily_map[d_key].estimated_cost_usd = round(daily_map[d_key].estimated_cost_usd + r.estimated_cost_usd, 6)

            # Aggregate Monthly
            if m_key not in monthly_map:
                monthly_map[m_key] = PeriodUsageSummary(period_key=m_key)
            monthly_map[m_key].total_requests += 1
            monthly_map[m_key].prompt_tokens += r.prompt_tokens
            monthly_map[m_key].completion_tokens += r.completion_tokens
            monthly_map[m_key].total_tokens += r.total_tokens
            monthly_map[m_key].estimated_cost_usd = round(monthly_map[m_key].estimated_cost_usd + r.estimated_cost_usd, 6)

        today_summary = daily_map.get(today_key, PeriodUsageSummary(period_key=today_key))
        current_month_summary = monthly_map.get(current_month_key, PeriodUsageSummary(period_key=current_month_key))

        return ExecutiveTokenAnalyticsReport(
            total_lifetime_requests=total_requests,
            total_lifetime_tokens=total_tokens,
            total_lifetime_cost_usd=round(total_cost, 6),
            today_summary=today_summary,
            current_month_summary=current_month_summary,
            daily_history=sorted(list(daily_map.values()), key=lambda x: x.period_key, reverse=True),
            monthly_history=sorted(list(monthly_map.values()), key=lambda x: x.period_key, reverse=True)
        )
