"""
GuardianAI Community Intelligence & HITL Pytest Suite
"""

import pytest
from app.community_intel.schemas import (
    ScamReportCreate,
    ScamCategory,
    CommunityVoteCreate,
    VoteType,
    AIPredictionFeedbackCreate,
    FeedbackType,
    ReportStatus
)
from app.community_intel.orchestrator import CommunityIntelOrchestrator
from app.community_intel.trust_engine import UserTrustEngine
from app.community_intel.deduplication import DuplicateReportDetector

@pytest.fixture
def orchestrator():
    return CommunityIntelOrchestrator()

def test_submit_scam_report(orchestrator):
    payload = ScamReportCreate(
        title="Fake CBI Police Digital Arrest Scam Call",
        description="Caller impersonated CBI officer demanding money transfer to clear illegal charges",
        scam_category=ScamCategory.DIGITAL_ARREST,
        target_persona="SENIOR_CITIZENS"
    )
    report = orchestrator.submit_report(payload, user_id="usr_100")

    assert report.report_id.startswith("rep_")
    assert report.status == ReportStatus.PENDING
    assert report.upvote_count == 0
    assert report.weighted_score == 0.0

def test_community_vote_weight(orchestrator):
    payload = ScamReportCreate(
        title="Phishing URL SMS Scam",
        description="Text message with link http://bank-update.top to steal banking credentials",
        scam_category=ScamCategory.PHISHING_URL
    )
    report = orchestrator.submit_report(payload, user_id="usr_101")

    # Set user trust score to 80 (EXPERT tier, weight = 1.8x)
    orchestrator._user_trust_db["usr_voter"] = 80

    vote = CommunityVoteCreate(report_id=report.report_id, vote_type=VoteType.UPVOTE)
    updated_report = orchestrator.cast_vote(vote, user_id="usr_voter")

    assert updated_report.upvote_count == 1
    assert updated_report.weighted_score == 1.8

def test_duplicate_detection():
    text1 = "Caller impersonated CBI officer demanding money transfer to clear charges"
    text2 = "Caller impersonated CBI officer demanding money transfer to clear charges"

    is_dup, sim, idx = DuplicateReportDetector.is_duplicate(text1, [text2])
    assert is_dup is True
    assert sim == 1.0

def test_moderator_workflow(orchestrator):
    payload = ScamReportCreate(
        title="Fake Job Scam Offer",
        description="Telegram group asking 5000 deposit for online rating work",
        scam_category=ScamCategory.JOB_SCAM
    )
    report = orchestrator.submit_report(payload, user_id="usr_102")

    # Moderator approves report
    updated = orchestrator.moderate_report(report.report_id, ReportStatus.VERIFIED, moderator_id="mod_1")
    assert updated.status == ReportStatus.VERIFIED
    assert orchestrator._user_trust_db["usr_102"] == 55 # 50 default + 5 reward

def test_export_rlhf_dataset(orchestrator):
    payload = ScamReportCreate(
        title="Fake KBC Lottery SMS",
        description="Congratulations you won 25 lakhs pay 10000 processing fee",
        scam_category=ScamCategory.LOTTERY_KBC
    )
    report = orchestrator.submit_report(payload, user_id="usr_103")

    feedback = AIPredictionFeedbackCreate(
        report_id=report.report_id,
        predicted_risk_level="SAFE",
        feedback_type=FeedbackType.FALSE_NEGATIVE,
        correction_reason="Missed lottery processing fee scam vector"
    )
    orchestrator.submit_ai_feedback(feedback, user_id="usr_103")

    jsonl_output = orchestrator.export_rlhf_dataset()
    assert "instruction" in jsonl_output
    assert "FALSE_NEGATIVE" in jsonl_output
    assert "DANGEROUS" in jsonl_output
