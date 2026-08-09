"""
GuardianAI AIPredictionFeedback Model & Schema Pytest Suite
"""

import pytest
from app.models.feedback import AIPredictionFeedback, FeedbackCreateSchema, FeedbackResponseSchema

def test_feedback_schema_validation():
    payload = FeedbackCreateSchema(
        scan_id="scn_12345",
        feedback_type="FALSE_POSITIVE",
        predicted_risk_level="DANGEROUS",
        actual_risk_level="SAFE",
        suggested_category="OTHER",
        rating=4,
        comment="This email was a legitimate flight confirmation."
    )

    assert payload.feedback_type == "FALSE_POSITIVE"
    assert payload.rating == 4
    assert payload.actual_risk_level == "SAFE"

def test_feedback_orm_instantiation():
    feedback = AIPredictionFeedback(
        scan_id="scn_67890",
        user_id="usr_test_200",
        feedback_type="FALSE_NEGATIVE",
        predicted_risk_level="SAFE",
        actual_risk_level="DANGEROUS",
        suggested_category="DIGITAL_ARREST",
        rating=1,
        comment="AI missed digital arrest threat language in phone transcript"
    )

    assert feedback.feedback_type == "FALSE_NEGATIVE"
    assert feedback.rating == 1
    assert feedback.is_verified_by_moderator is False
