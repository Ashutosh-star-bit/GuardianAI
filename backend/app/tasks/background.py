"""
GuardianAI Master Background Task Dispatcher & Helper Utilities
Purpose: Collects logging, AI processing, file cleanup, and security notification task runners,
         providing clean enqueue helpers for FastAPI route controllers.
"""

from typing import Callable, Any
from fastapi import BackgroundTasks
from app.tasks.logging_tasks import record_audit_log_async
from app.tasks.ai_tasks import process_ai_threat_enrichment_async
from app.tasks.cleanup_tasks import cleanup_expired_uploads_async
from app.tasks.notification_tasks import send_security_alert_notification_async, dispatch_fraud_agency_report_async

def enqueue_background_task(bg_tasks: BackgroundTasks, func: Callable[..., Any], *args: Any, **kwargs: Any):
    """
    Helper function to cleanly schedule async background tasks within FastAPI route controllers.
    """
    bg_tasks.add_task(func, *args, **kwargs)

__all__ = [
    "enqueue_background_task",
    "record_audit_log_async",
    "process_ai_threat_enrichment_async",
    "cleanup_expired_uploads_async",
    "send_security_alert_notification_async",
    "dispatch_fraud_agency_report_async",
]
