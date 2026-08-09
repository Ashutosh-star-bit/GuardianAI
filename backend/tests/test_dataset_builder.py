"""
GuardianAI DatasetBuilder Pytest Suite
"""

import pytest
from app.community_intel.dataset_builder import DatasetBuilder, CuratedDatasetRecord

@pytest.fixture
def sample_raw_data():
    raw_reports = [
        {
            "id": "rep_1",
            "verification_status": "VERIFIED",
            "is_spam": False,
            "title": "Fake CBI Police Call",
            "description": "Caller claimed to be CBI officer demanding 50000 rupees to avoid digital arrest",
            "risk_level": "DANGEROUS",
            "category": "DIGITAL_ARREST",
            "evidence_data": {"phone_number": "+919876543210"}
        },
        {
            "id": "rep_2",
            "verification_status": "REJECTED", # Should be excluded
            "is_spam": False,
            "title": "Invalid Report",
            "description": "Just a normal call from friend"
        },
        {
            "id": "rep_3",
            "verification_status": "VERIFIED",
            "is_spam": True, # Should be excluded (spam)
            "title": "Spam Ad",
            "description": "Buy cheap shoes now at discount"
        }
    ]
    raw_feedbacks = [
        {
            "id": "fb_1",
            "is_verified_by_moderator": True,
            "comment": "AI falsely flagged legitimate bank alert as phishing",
            "actual_risk_level": "SAFE",
            "suggested_category": "OTHER"
        }
    ]
    return raw_reports, raw_feedbacks

def test_filter_and_curate_records(sample_raw_data):
    raw_reports, raw_feedbacks = sample_raw_data
    curated = DatasetBuilder.filter_and_curate_records(raw_reports, raw_feedbacks)

    assert len(curated) == 2 # 1 verified report + 1 verified feedback
    assert curated[0].record_id == "rep_1"
    assert curated[0].scam_category == "DIGITAL_ARREST"
    assert curated[1].record_id == "fb_1"

def test_export_formats(sample_raw_data):
    raw_reports, raw_feedbacks = sample_raw_data
    curated = DatasetBuilder.filter_and_curate_records(raw_reports, raw_feedbacks)

    json_out = DatasetBuilder.export_to_json(curated)
    assert "rep_1" in json_out

    jsonl_out = DatasetBuilder.export_to_jsonl(curated)
    assert "\n" in jsonl_out

    csv_out = DatasetBuilder.export_to_csv(curated)
    assert "record_id" in csv_out
    assert "DIGITAL_ARREST" in csv_out

    parquet_dict = DatasetBuilder.export_to_parquet_dict(curated)
    assert len(parquet_dict["record_id"]) == 2
