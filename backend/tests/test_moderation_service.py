"""
GuardianAI ModerationService Pytest Suite
"""

import pytest
from app.services.moderation_service import ModerationService, ModerationServiceError
from app.models.scam_report import ScamReport

@pytest.fixture
def moderation_service():
    return ModerationService()

def test_moderation_service_instantiation(moderation_service):
    assert moderation_service is not None
