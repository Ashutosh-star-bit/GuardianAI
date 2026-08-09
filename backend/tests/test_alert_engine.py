"""
GuardianAI Alert Engine Pytest Suite
"""

import pytest
from app.core.alert_engine import alert_engine, AlertCategory, AlertSeverity

def test_trigger_security_alert():
    alert = alert_engine.trigger_alert(
        category=AlertCategory.SECURITY_EVENT,
        severity=AlertSeverity.CRITICAL,
        title="SQL Injection Attack Blocked",
        summary="Malicious UNION SELECT payload blocked on /api/v1/public/scan/text",
        correlation_id="req_99881100",
        metadata={"ip": "192.168.1.100"}
    )
    assert alert.alert_id.startswith("alt_")
    assert alert.severity == AlertSeverity.CRITICAL
    assert alert.category == AlertCategory.SECURITY_EVENT

def test_trigger_high_latency_alert():
    alert = alert_engine.trigger_alert(
        category=AlertCategory.HIGH_LATENCY,
        severity=AlertSeverity.MEDIUM,
        title="p95 Latency SLA Breach",
        summary="p95 latency reached 620ms on OCR Scanner",
        correlation_id="req_99881101"
    )
    assert alert.severity == AlertSeverity.MEDIUM
    assert len(alert_engine.get_recent_alerts()) >= 2
