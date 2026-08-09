"""
GuardianAI AIFeedbackService Pytest Suite
"""

import pytest
from app.services.ai_feedback_service import AIFeedbackService, AIFeedbackServiceError
from app.models.feedback import FeedbackCreateSchema

@pytest.fixture
def feedback_service():
    return AIFeedbackService()

def test_feedback_service_instantiation(feedback_service):
    assert feedback_service is not None
