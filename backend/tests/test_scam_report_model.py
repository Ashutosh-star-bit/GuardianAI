"""
GuardianAI ScamReport Model & Schema Pytest Suite
"""

import pytest
from datetime import datetime, timezone
from app.models.scam_report import ScamReport, ScamReportAttachment, ScamReportVote, ScamReportCreateSchema, ScamReportResponseSchema

def test_scam_report_schema_creation():
    payload = ScamReportCreateSchema(
        category="DIGITAL_ARREST",
        source="PHONE",
        title="Fake Police Digital Arrest Call",
        description="Scammer claimed to be from Police demanding 50000 rupees to avoid digital arrest",
        evidence_data={"phone_number": "+919876543210", "demanded_amount": 50000}
    )

    assert payload.category == "DIGITAL_ARREST"
    assert payload.source == "PHONE"
    assert payload.evidence_data["phone_number"] == "+919876543210"

def test_scam_report_orm_instantiation():
    report = ScamReport(
        user_id="usr_test_100",
        category="BANKING_FRAUD",
        source="SMS",
        title="Fake HDFC Account Blocked SMS",
        description="SMS claiming account blocked with phishing link http://hdfc-verify.top",
        evidence_data={"url": "http://hdfc-verify.top"},
        risk_level="DANGEROUS",
        verification_status="PENDING"
    )

    assert report.category == "BANKING_FRAUD"
    assert report.risk_level == "DANGEROUS"
    assert report.verification_status == "PENDING"
    assert report.upvote_count == 0
    assert report.weighted_score == 0.0
