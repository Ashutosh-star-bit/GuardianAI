"""
GuardianAI Pipeline AnalyticsRecorder Engine
Purpose: Real-time telemetry analytics recorder tracking Total Scans, Risk Levels Breakdown, Threat Categories,
         Execution Time SLA Latencies, Confidence Averages, Error Counts, Channel Usage, and Daily Statistics.
"""

from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class DailyAnalyticsSnapshot(BaseModel):
    """Snapshot container for daily aggregated telemetry metrics."""
    date_key: str = Field(description="YYYY-MM-DD UTC date key")
    total_scans: int = 0
    total_errors: int = 0
    risk_level_counts: Dict[str, int] = Field(default_factory=lambda: {"SAFE": 0, "LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0})
    threat_category_counts: Dict[str, int] = Field(default_factory=dict)
    channel_usage_counts: Dict[str, int] = Field(default_factory=dict)
    total_execution_ms: float = 0.0
    min_execution_ms: float = 999999.0
    max_execution_ms: float = 0.0
    total_confidence_sum: float = 0.0

    @property
    def avg_execution_ms(self) -> float:
        return round(self.total_execution_ms / self.total_scans, 2) if self.total_scans > 0 else 0.0

    @property
    def avg_confidence(self) -> float:
        return round(self.total_confidence_sum / self.total_scans, 3) if self.total_scans > 0 else 0.0

class AnalyticsRecorder:
    """Enterprise Pipeline Telemetry Analytics Engine."""

    _daily_store: Dict[str, DailyAnalyticsSnapshot] = {}

    @classmethod
    def _get_current_date_key(cls) -> str:
        """Returns YYYY-MM-DD UTC date string."""
        return datetime.now(timezone.utc).strftime("%Y-%m-%d")

    @classmethod
    def get_or_create_daily_snapshot(cls, date_key: Optional[str] = None) -> DailyAnalyticsSnapshot:
        """Retrieves or initializes a DailyAnalyticsSnapshot for the given date key."""
        d_key = date_key or cls._get_current_date_key()
        if d_key not in cls._daily_store:
            cls._daily_store[d_key] = DailyAnalyticsSnapshot(date_key=d_key)
        return cls._daily_store[d_key]

    @classmethod
    def record_scan_event(
        cls,
        risk_level: str,
        execution_time_ms: float,
        confidence: float = 0.95,
        threat_categories: Optional[List[str]] = None,
        channel_type: str = "SMS",
        is_error: bool = False,
        date_key: Optional[str] = None
    ) -> DailyAnalyticsSnapshot:
        """
        Records a single pipeline scan event into daily telemetry analytics counters.
        """
        snapshot = cls.get_or_create_daily_snapshot(date_key)
        snapshot.total_scans += 1

        if is_error:
            snapshot.total_errors += 1

        # 1. Update Risk Level Counter
        r_upper = risk_level.upper() if risk_level else "SAFE"
        if r_upper in snapshot.risk_level_counts:
            snapshot.risk_level_counts[r_upper] += 1
        else:
            snapshot.risk_level_counts[r_upper] = 1

        # 2. Update Channel Usage Counter
        c_upper = channel_type.upper() if channel_type else "SMS"
        snapshot.channel_usage_counts[c_upper] = snapshot.channel_usage_counts.get(c_upper, 0) + 1

        # 3. Update Threat Categories Counter
        if threat_categories:
            for cat in threat_categories:
                cat_upper = cat.upper()
                snapshot.threat_category_counts[cat_upper] = snapshot.threat_category_counts.get(cat_upper, 0) + 1

        # 4. Update Latency SLA Metrics
        snapshot.total_execution_ms += execution_time_ms
        if execution_time_ms < snapshot.min_execution_ms:
            snapshot.min_execution_ms = round(execution_time_ms, 2)
        if execution_time_ms > snapshot.max_execution_ms:
            snapshot.max_execution_ms = round(execution_time_ms, 2)

        # 5. Update Confidence Metrics
        snapshot.total_confidence_sum += confidence

        return snapshot

    @classmethod
    def get_analytics_summary(cls, date_key: Optional[str] = None) -> Dict[str, Any]:
        """
        Returns structured dictionary summary of analytics for the specified date key.
        """
        snapshot = cls.get_or_create_daily_snapshot(date_key)
        return {
            "date_key": snapshot.date_key,
            "total_scans": snapshot.total_scans,
            "total_errors": snapshot.total_errors,
            "avg_execution_ms": snapshot.avg_execution_ms,
            "min_execution_ms": snapshot.min_execution_ms if snapshot.min_execution_ms < 999999.0 else 0.0,
            "max_execution_ms": snapshot.max_execution_ms,
            "avg_confidence": snapshot.avg_confidence,
            "risk_level_counts": snapshot.risk_level_counts,
            "channel_usage_counts": snapshot.channel_usage_counts,
            "threat_category_counts": snapshot.threat_category_counts
        }

    @classmethod
    def clear_all(cls) -> None:
        """Clears telemetry store (used for test isolation)."""
        cls._daily_store.clear()
