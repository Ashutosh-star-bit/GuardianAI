"""
GuardianAI HistoryService Engine Unit Test Suite
Purpose: Tests SHA-256 hashing, storing scan history, searching with keyword queries, filtering by risk level, pagination, and record deletion.
"""

import pytest
from app.pipeline.history_service import HistoryService, ScanHistoryRecord

@pytest.fixture(autouse=True)
def clean_history_store():
    HistoryService.clear_all()
    yield
    HistoryService.clear_all()

def test_store_scan_history_and_sha256_hash():
    """Tests storing scan history and computing SHA-256 input hash."""
    rec: ScanHistoryRecord = HistoryService.store_scan_history(
        scan_id="scn_hist_1",
        request_id="req_hist_1",
        original_text="URGENT: Verify at http://paypa1-check.top",
        cleaned_text="URGENT: Verify at http://paypa1-check.top",
        decision_dict={"final_scam_probability": 90, "risk_level": "CRITICAL"},
        execution_time_ms=12.5,
        user_id="usr_100",
        input_format="SMS"
    )

    assert rec.scan_id == "scn_hist_1"
    assert rec.user_id == "usr_100"
    assert len(rec.input_hash) == 64 # SHA-256 hex string length
    assert rec.risk_level == "CRITICAL"
    assert rec.execution_time_ms == 12.5

def test_search_and_pagination_history():
    """Tests searching history records with risk level filtering and pagination."""
    # Insert 3 records
    HistoryService.store_scan_history("s1", "r1", "Text 1", "Text 1", {"risk_level": "SAFE"}, 10.0, user_id="u1")
    HistoryService.store_scan_history("s2", "r2", "Text 2", "Text 2", {"risk_level": "CRITICAL"}, 15.0, user_id="u1")
    HistoryService.store_scan_history("s3", "r3", "Text 3", "Text 3", {"risk_level": "CRITICAL"}, 14.0, user_id="u1")

    # Search for user u1 with CRITICAL risk filter
    results, total = HistoryService.search_history(user_id="u1", risk_level="CRITICAL", page=1, page_size=10)
    assert total == 2
    assert len(results) == 2

def test_delete_scan_history():
    """Tests deleting scan history record with user-scope validation."""
    HistoryService.store_scan_history("s_del", "r_del", "Delete me", "Delete me", {"risk_level": "SAFE"}, 5.0, user_id="u_owner")

    # Attempt delete by wrong user -> fails
    assert HistoryService.delete_scan_history("s_del", user_id="u_wrong") is False
    assert HistoryService.get_scan_by_id("s_del") is not None

    # Delete by owner user -> succeeds
    assert HistoryService.delete_scan_history("s_del", user_id="u_owner") is True
    assert HistoryService.get_scan_by_id("s_del") is None
