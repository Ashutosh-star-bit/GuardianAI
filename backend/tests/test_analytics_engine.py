"""
GuardianAI Platform Analytics Engine Pytest Suite
"""

import pytest
from app.analytics.analytics_engine import PlatformAnalyticsEngine

@pytest.fixture
def analytics_engine():
    return PlatformAnalyticsEngine()

def test_realtime_analytics_metrics(analytics_engine):
    summary = analytics_engine.get_realtime_analytics_summary()
    assert summary["daily_active_users_dau"] == 14280
    assert summary["monthly_active_users_mau"] == 128400
    assert summary["total_scans_processed"] > 100000
    assert summary["detection_accuracy_percent"] > 95.0
    assert summary["average_response_time_ms"] < 200.0
    assert "DIGITAL_ARREST" in summary["category_breakdown"]
