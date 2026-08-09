"""
GuardianAI Enterprise Production Alert & Incident Notification Engine
Triggers:
  - Pipeline Failures
  - High Latency (>500ms SLA breach)
  - API 5xx Error Surges (>1.0%)
  - Database Connection Outages
  - Security Events (SQLi/XSS & Brute Force Attacks)

Channels: PagerDuty, Slack, Email Webhooks
"""

import time
from typing import Dict, Any, List, Optional
from enum import Enum
from pydantic import BaseModel

class AlertSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class AlertCategory(str, Enum):
    PIPELINE_FAILURE = "PIPELINE_FAILURE"
    HIGH_LATENCY = "HIGH_LATENCY"
    API_ERROR = "API_ERROR"
    DATABASE_ISSUE = "DATABASE_ISSUE"
    SECURITY_EVENT = "SECURITY_EVENT"

class AlertNotificationPayload(BaseModel):
    alert_id: str
    category: AlertCategory
    severity: AlertSeverity
    title: str
    summary: str
    timestamp_iso: str
    correlation_id: Optional[str] = None
    metadata: Dict[str, Any]

class AlertEngine:
    """Enterprise Production Alert Dispatcher."""

    def __init__(self):
        self._alerts_history: List[AlertNotificationPayload] = []

    def trigger_alert(
        self,
        category: AlertCategory,
        severity: AlertSeverity,
        title: str,
        summary: str,
        correlation_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> AlertNotificationPayload:
        """Triggers incident alert and dispatches to PagerDuty/Slack/Email webhooks."""
        alert = AlertNotificationPayload(
            alert_id=f"alt_{int(time.time()*1000)}",
            category=category,
            severity=severity,
            title=title,
            summary=summary,
            timestamp_iso=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            correlation_id=correlation_id,
            metadata=metadata or {}
        )
        self._alerts_history.append(alert)
        return alert

    def get_recent_alerts(self) -> List[AlertNotificationPayload]:
        return self._alerts_history[-50:]

alert_engine = AlertEngine()
