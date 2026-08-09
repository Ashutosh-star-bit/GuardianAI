"""
GuardianAI Asynchronous Logging Background Tasks
Purpose: Asynchronously records security audit telemetry and access events off the main HTTP loop.
"""

from typing import Dict, Any, Optional
from app.core.logging import logger, log_security_event

async def record_audit_log_async(
    event_name: str,
    user_id: Optional[str] = None,
    ip_address: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
):
    """Background task handler for asynchronously recording security audit events."""
    try:
        log_security_event(
            event=event_name,
            user_id=user_id,
            ip_address=ip_address,
            extra=details or {}
        )
        logger.info(f"[Background Task] Audit Event '{event_name}' logged for User={user_id or 'ANONYMOUS'}")
    except Exception as e:
        logger.error(f"[Background Task Error] Failed to record audit log: {str(e)}", exc_info=True)
