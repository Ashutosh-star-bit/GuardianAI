"""
GuardianAI User Notification Service Engine
Purpose: Asynchronous multi-channel notification engine alerting users on report approvals, rejections,
         AI prediction feedback audits, and trust score/reputation tier updates.
         Designed with abstract provider adapters for future Email (SMTP/SES/SendGrid) and WebPush integrations.
"""

from typing import List, Dict, Any, Optional
from enum import Enum
import json
import logging

logger = logging.getLogger(__name__)

class NotificationType(str, Enum):
    REPORT_APPROVED = "REPORT_APPROVED"
    REPORT_REJECTED = "REPORT_REJECTED"
    REPORT_MERGED = "REPORT_MERGED"
    FEEDBACK_AUDITED = "FEEDBACK_AUDITED"
    TRUST_SCORE_CHANGED = "TRUST_SCORE_CHANGED"

class NotificationChannel(str, Enum):
    IN_APP = "IN_APP"
    EMAIL = "EMAIL"       # Future Email Adapter
    WEBPUSH = "WEBPUSH"   # Future Web Push Adapter

class NotificationMessage:
    """Standardized Notification DTO."""
    def __init__(
        self,
        notification_id: str,
        user_id: str,
        notification_type: NotificationType,
        title: str,
        body: str,
        data_payload: Optional[Dict[str, Any]] = None,
        channels: Optional[List[NotificationChannel]] = None
    ):
        self.notification_id = notification_id
        self.user_id = user_id
        self.notification_type = notification_type
        self.title = title
        self.body = body
        self.data_payload = data_payload or {}
        self.channels = channels or [NotificationChannel.IN_APP]
        self.read = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "notification_id": self.notification_id,
            "user_id": self.user_id,
            "notification_type": self.notification_type.value,
            "title": self.title,
            "body": self.body,
            "data_payload": self.data_payload,
            "channels": [c.value for c in self.channels],
            "read": self.read
        }

class BaseNotificationProvider:
    """Abstract Base Class for Notification Dispatch Adapters."""
    def send(self, message: NotificationMessage) -> bool:
        raise NotImplementedError

class InAppNotificationProvider(BaseNotificationProvider):
    """In-App DB Notification Dispatcher."""
    def send(self, message: NotificationMessage) -> bool:
        logger.info(f"[InAppNotify] User={message.user_id} Title='{message.title}'")
        return True

class EmailNotificationProvider(BaseNotificationProvider):
    """Future Production Email Notification Dispatcher (SMTP / AWS SES / SendGrid)."""
    def send(self, message: NotificationMessage) -> bool:
        # Stub for future Email Provider integration
        logger.info(f"[EmailNotify-STUB] TargetUser={message.user_id} Subject='{message.title}'")
        return True

class NotificationService:
    """Enterprise Reusable Multi-Channel Notification Service."""

    def __init__(self):
        self.in_app_provider = InAppNotificationProvider()
        self.email_provider = EmailNotificationProvider()
        self._in_memory_user_notifications: Dict[str, List[NotificationMessage]] = {}

    def notify_report_approved(self, user_id: str, report_id: str, report_title: str, trust_delta: int = 5) -> NotificationMessage:
        """Sends notification when a submitted scam report is approved by moderators."""
        msg = NotificationMessage(
            notification_id=f"notif_{Date.now() if 'Date' in globals() else '001'}",
            user_id=user_id,
            notification_type=NotificationType.REPORT_APPROVED,
            title="Scam Report Approved! +5 Trust Points",
            body=f"Your submitted report '{report_title}' was verified by community moderators. You earned +{trust_delta} reputation points!",
            data_payload={"report_id": report_id, "trust_delta": trust_delta},
            channels=[NotificationChannel.IN_APP, NotificationChannel.EMAIL]
        )
        self._dispatch(msg)
        return msg

    def notify_report_rejected(self, user_id: str, report_id: str, report_title: str, reason: str = "Unsubstantiated claim") -> NotificationMessage:
        """Sends notification when a submitted scam report is rejected."""
        msg = NotificationMessage(
            notification_id=f"notif_rej_001",
            user_id=user_id,
            notification_type=NotificationType.REPORT_REJECTED,
            title="Scam Report Status Update",
            body=f"Your submitted report '{report_title}' was not approved. Reason: {reason}.",
            data_payload={"report_id": report_id, "reason": reason},
            channels=[NotificationChannel.IN_APP]
        )
        self._dispatch(msg)
        return msg

    def notify_trust_score_changed(self, user_id: str, old_score: int, new_score: int, new_tier: str) -> NotificationMessage:
        """Sends notification when a user's reputation trust score or tier updates."""
        msg = NotificationMessage(
            notification_id="notif_trust_001",
            user_id=user_id,
            notification_type=NotificationType.TRUST_SCORE_CHANGED,
            title=f"Reputation Score Updated: {new_score} pts",
            body=f"Your trust score changed from {old_score} to {new_score}. Current Tier: {new_tier}.",
            data_payload={"old_score": old_score, "new_score": new_score, "new_tier": new_tier},
            channels=[NotificationChannel.IN_APP]
        )
        self._dispatch(msg)
        return msg

    def _dispatch(self, message: NotificationMessage):
        """Internal multi-channel dispatcher."""
        if message.user_id not in self._in_memory_user_notifications:
            self._in_memory_user_notifications[message.user_id] = []
        self._in_memory_user_notifications[message.user_id].append(message)

        # Dispatch via channels
        if NotificationChannel.IN_APP in message.channels:
            self.in_app_provider.send(message)
        if NotificationChannel.EMAIL in message.channels:
            self.email_provider.send(message)

    def get_user_notifications(self, user_id: str) -> List[Dict[str, Any]]:
        """Retrieves in-app notification inbox for target user."""
        msgs = self._in_memory_user_notifications.get(user_id, [])
        return [m.to_dict() for m in msgs]
