"""
GuardianAI AnalyticsRecorder Engine Unit Test Suite
Purpose: Tests recording scan events, tracking risk levels, threat categories, latency SLA metrics, confidence averages, and daily analytics summaries.
"""

import pytest
from app.pipeline.analytics_recorder import AnalyticsRecorder, DailyAnalyticsSnapshot

@pytest.fixture(autouse=True)
def clean_analytics():
    AnalyticsRecorder.clear_all()
    yield
    AnalyticsRecorder.clear_all()

def test_record_scan_events_and_daily_analytics_summary():
    """Tests recording multiple scan events and checking aggregated daily summary metrics."""
    # Event 1: Critical Risk Scan
    AnalyticsRecorder.record_scan_event(
        risk_level="CRITICAL",
        execution_time_ms=12.5,
        confidence=0.98,
        threat_categories=["DOMAIN", "UPI_ID"],
        channel_type="SMS",
        date_key="2026-07-28"
    )

    # Event 2: Safe Risk Scan
    AnalyticsRecorder.record_scan_event(
        risk_level="SAFE",
        execution_time_ms=10.5,
        confidence=0.90,
        channel_type="Email",
        date_key="2026-07-28"
    )

    summary = AnalyticsRecorder.get_analytics_summary(date_key="2026-07-28")

    assert summary["date_key"] == "2026-07-28"
    assert summary["total_scans"] == 2
    assert summary["total_errors"] == 0
    assert summary["risk_level_counts"]["CRITICAL"] == 1
    assert summary["risk_level_counts"]["SAFE"] == 1
    assert summary["channel_usage_counts"]["SMS"] == 1
    assert summary["channel_usage_counts"]["EMAIL"] == 1
    assert summary["threat_category_counts"]["DOMAIN"] == 1
    assert summary["avg_execution_ms"] == 11.5
    assert summary["avg_confidence"] == 0.94
