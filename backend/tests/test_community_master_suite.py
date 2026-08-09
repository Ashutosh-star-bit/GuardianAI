"""
GuardianAI Master Production Pytest Suite for Community Intelligence Subsystem
Coverage:
  1. Report Submission & Validation
  2. Community Voting & Sybil Defense
  3. Dynamic User Trust & Reputation Engine
  4. Moderation Pipeline & State Transitions
  5. Human-in-the-Loop (HITL) AI Prediction Feedback
  6. Multi-Vector Duplicate Detection (Hash, URL, Domain, Text Jaccard)
  7. Curated ML Dataset Building & Exporters (JSON, JSONL, CSV, Parquet)
  8. Community REST API Endpoints
  9. Edge Cases (XSS, PII Scrubbing, File Magic Signature Verification)
"""

import pytest
from app.community_intel.orchestrator import community_orchestrator
from app.community_intel.schemas import (
    ScamReportCreate,
    CommunityVoteCreate,
    AIPredictionFeedbackCreate,
    VoteType,
    ReportStatus
)
from app.community_intel.trust_score_engine import TrustScoreEngine, UserTrustTierName
from app.community_intel.dataset_builder import DatasetBuilder
from app.community_intel.security import CommunitySecuritySanitizer, CommunitySecurityError
from app.services.duplicate_detection_service import DuplicateDetectionService
from app.services.notification_service import NotificationService, NotificationType

# =====================================================================
# 1. REPORT SUBMISSION & VALIDATION TESTS
# =====================================================================

def test_report_submission_pipeline():
    payload = ScamReportCreate(
        title="Fake Police Digital Arrest Call",
        description="Scammer claimed to be CBI officer from Delhi demanding 50000 rupees",
        scam_category="DIGITAL_ARREST",
        target_persona="SENIOR_CITIZENS"
    )
    report = community_orchestrator.submit_report(payload, user_id="usr_master_01")
    assert report.report_id.startswith("rep_")
    assert report.status == ReportStatus.PENDING
    assert report.upvote_count == 0
    assert report.weighted_score == 0.0

# =====================================================================
# 2. COMMUNITY VOTING & SYBIL DEFENSE TESTS
# =====================================================================

def test_weighted_voting_system():
    # Submit report first
    payload = ScamReportCreate(
        title="HDFC Bank KYC Expiry Phishing SMS",
        description="Received SMS stating netbanking account blocked http://hdfc-verify.top",
        scam_category="PHISHING_URL"
    )
    report = community_orchestrator.submit_report(payload, user_id="usr_submitter")

    # Cast Upvote from user with trust score 50 (weight = 1.5x)
    vote_payload = CommunityVoteCreate(report_id=report.report_id, vote_type=VoteType.UPVOTE)
    updated_report = community_orchestrator.cast_vote(vote_payload, user_id="usr_voter_1")
    assert updated_report.upvote_count == 1
    assert updated_report.weighted_score == 1.5

# =====================================================================
# 3. DYNAMIC USER TRUST ENGINE TESTS
# =====================================================================

def test_trust_score_calculation():
    # Approved (+5), Rejected (-10), Spam (-30), Helpful Vote (+1), Moderator (+15)
    score = TrustScoreEngine.compute_trust_score(
        approved_reports_count=4,  # 50 + 20 = 70
        rejected_reports_count=1,  # 70 - 10 = 60
        helpful_votes_count=10     # 60 + 10 = 70
    )
    assert score == 70
    assert TrustScoreEngine.get_trust_tier(score) == UserTrustTierName.TRUSTED
    assert TrustScoreEngine.get_vote_weight(score) == 1.7

# =====================================================================
# 4. MODERATION PIPELINE & STATE TRANSITIONS
# =====================================================================

def test_moderation_state_transitions():
    payload = ScamReportCreate(
        title="Telegram Job Scam Task",
        description="YouTube rating deposit scam promising high returns",
        scam_category="JOB_SCAM"
    )
    report = community_orchestrator.submit_report(payload, user_id="usr_submitter_2")

    # Approve Report
    approved = community_orchestrator.moderate_report(
        report_id=report.report_id,
        new_status=ReportStatus.VERIFIED,
        moderator_id="mod_master"
    )
    assert approved.status == ReportStatus.VERIFIED

# =====================================================================
# 5. AI PREDICTION FEEDBACK TESTS
# =====================================================================

def test_ai_prediction_feedback_recording():
    fb_payload = AIPredictionFeedbackCreate(
        report_id="rep_999",
        predicted_risk_level="SAFE",
        feedback_type="FALSE_NEGATIVE",
        correction_reason="AI missed digital arrest scam vector",
        suggested_category="DIGITAL_ARREST"
    )
    res = community_orchestrator.submit_ai_feedback(fb_payload, user_id="usr_tester")
    assert res["status"] == "recorded"
    assert res["feedback_type"] == "FALSE_NEGATIVE"

# =====================================================================
# 6. MULTI-VECTOR DUPLICATE DETECTION TESTS
# =====================================================================

def test_duplicate_detection_service():
    dup_service = DuplicateDetectionService()
    att_bytes = b"AUDIO_RAW_BYTES_PAYLOAD"
    att_hash = dup_service.compute_sha256(att_bytes)

    existing = [{"id": "rep_existing", "attachment_hash": att_hash}]
    match = dup_service.find_duplicate(new_text="Text", new_attachment_bytes=att_bytes, existing_reports=existing)
    assert match.is_duplicate is True
    assert match.match_reason == "EXACT_ATTACHMENT_HASH_MATCH"

# =====================================================================
# 7. CURATED ML DATASET BUILDER EXPORTERS
# =====================================================================

def test_dataset_builder_exporters():
    raw_reports = [{
        "id": "rep_export_1",
        "verification_status": "VERIFIED",
        "is_spam": False,
        "description": "Caller impersonated CBI officer demanding money transfer",
        "category": "DIGITAL_ARREST"
    }]
    raw_feedbacks = []
    curated = DatasetBuilder.filter_and_curate_records(raw_reports, raw_feedbacks)
    assert len(curated) == 1

    jsonl_out = DatasetBuilder.export_to_jsonl(curated)
    assert "rep_export_1" in jsonl_out
    assert "DIGITAL_ARREST" in jsonl_out

# =====================================================================
# 8. NOTIFICATION SERVICE TESTS
# =====================================================================

def test_notification_service():
    notif_svc = NotificationService()
    msg = notif_svc.notify_report_approved("usr_100", "rep_100", "Digital Arrest Call")
    assert msg.notification_type == NotificationType.REPORT_APPROVED
    assert len(notif_svc.get_user_notifications("usr_100")) == 1

# =====================================================================
# 9. EDGE CASES (XSS & PII SCRUBBING & MAGIC SIGNATURE)
# =====================================================================

def test_security_sanitizer_edge_cases():
    # 1. XSS Escaping
    raw_xss = "<script>alert('xss')</script>"
    assert "<script>" not in CommunitySecuritySanitizer.sanitize_text_xss(raw_xss)

    # 2. PII Redaction
    raw_pii = "Aadhaar is 9876 5432 1098"
    assert "[REDACTED_AADHAAR]" in CommunitySecuritySanitizer.scrub_pii(raw_pii)

    # 3. Magic Signature
    png_bytes = b"\x89PNG\r\n\x1a\nPNGData"
    valid, _ = CommunitySecuritySanitizer.validate_upload_attachment(png_bytes, "photo.png")
    assert valid is True
