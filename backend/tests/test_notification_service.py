"""
GuardianAI NotificationService Pytest Suite
"""

import pytest
from app.services.notification_service import NotificationService, NotificationType

@pytest.fixture
def notification_service():
    return NotificationService()

def test_notify_report_approved(notification_service):
    msg = notification_service.notify_report_approved(
        user_id="usr_100",
        report_id="rep_200",
        report_title="Fake CBI Police Call"
    )

    assert msg.user_id == "usr_100"
    assert msg.notification_type == NotificationType.REPORT_APPROVED
    assert "Scam Report Approved" in msg.title

    inbox = notification_service.get_user_notifications("usr_100")
    assert len(inbox) == 1
    assert inbox[0]["notification_type"] == "REPORT_APPROVED"

def test_notify_trust_score_changed(notification_service):
    msg = notification_service.notify_trust_score_changed(
        user_id="usr_101",
        old_score=50,
        new_score=75,
        new_tier="EXPERT"
    )

    assert msg.user_id == "usr_101"
    assert msg.notification_type == NotificationType.TRUST_SCORE_CHANGED

    inbox = notification_service.get_user_notifications("usr_101")
    assert len(inbox) == 1
    assert inbox[0]["data_payload"]["new_tier"] == "EXPERT"
