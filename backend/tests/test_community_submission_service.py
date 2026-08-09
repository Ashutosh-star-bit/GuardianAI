"""
GuardianAI CommunitySubmissionService Pytest Suite
"""

import pytest
from app.services.community_submission_service import CommunitySubmissionService, SubmissionValidationError
from app.models.scam_report import ScamReportCreateSchema, AttachmentCreate

def test_validate_report_content_success():
    payload = ScamReportCreateSchema(
        category="DIGITAL_ARREST",
        source="PHONE",
        title="Fake Police Digital Arrest Scam Call",
        description="Caller impersonated CBI officer demanding money transfer"
    )
    CommunitySubmissionService.validate_report_content(payload) # Should not raise

def test_validate_report_content_invalid_title():
    with pytest.raises(Exception):
        ScamReportCreateSchema(
            category="DIGITAL_ARREST",
            source="PHONE",
            title="Bad",
            description="Caller impersonated CBI officer demanding money transfer"
        )

def test_extract_evidence_iocs():
    text = "Visit phishing site http://hdfc-verify.top or pay UPI handle scammer@upi or call +919876543210"
    iocs = CommunitySubmissionService.extract_evidence_iocs(text)

    assert "http://hdfc-verify.top" in iocs["urls"]
    assert "scammer@upi" in iocs["upi_handles"]
    assert len(iocs["phone_numbers"]) > 0

def test_assign_initial_moderation_status():
    status, is_spam = CommunitySubmissionService.assign_initial_moderation_status(user_trust_score=90, evidence_count=2)
    assert status == "VERIFIED"

    status_low, _ = CommunitySubmissionService.assign_initial_moderation_status(user_trust_score=10, evidence_count=0)
    assert status_low == "UNDER_REVIEW"
