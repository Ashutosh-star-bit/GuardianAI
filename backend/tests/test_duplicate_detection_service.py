"""
GuardianAI DuplicateDetectionService Pytest Suite
"""

import pytest
from app.services.duplicate_detection_service import DuplicateDetectionService

@pytest.fixture
def dup_service():
    return DuplicateDetectionService()

def test_attachment_hash_match(dup_service):
    att_bytes = b"BINARY_AUDIO_PAYLOAD_DATA_12345"
    att_hash = dup_service.compute_sha256(att_bytes)

    existing = [{"id": "rep_100", "attachment_hash": att_hash}]
    match = dup_service.find_duplicate(new_text="Some text", new_attachment_bytes=att_bytes, existing_reports=existing)

    assert match.is_duplicate is True
    assert match.match_reason == "EXACT_ATTACHMENT_HASH_MATCH"
    assert match.existing_report_id == "rep_100"

def test_url_exact_match(dup_service):
    url = "http://hdfc-verify.top/login"
    existing = [{"id": "rep_101", "submitted_url": url}]

    match = dup_service.find_duplicate(new_text="Some text", new_url=url, existing_reports=existing)
    assert match.is_duplicate is True
    assert match.match_reason == "EXACT_URL_MATCH"

def test_domain_match(dup_service):
    url1 = "http://hdfc-verify.top/page1"
    domain = "hdfc-verify.top"
    existing = [{"id": "rep_102", "domain": domain}]

    match = dup_service.find_duplicate(new_text="Some text", new_url=url1, existing_reports=existing)
    assert match.is_duplicate is True
    assert match.match_reason == "EXACT_DOMAIN_MATCH"

def test_text_similarity_match(dup_service):
    text1 = "Caller impersonated CBI officer demanding money transfer to clear illegal charges"
    text2 = "Caller impersonated CBI officer demanding money transfer to clear illegal charges"
    existing = [{"id": "rep_103", "description": text2}]

    match = dup_service.find_duplicate(new_text=text1, existing_reports=existing)
    assert match.is_duplicate is True
    assert match.similarity_score == 1.0
    assert match.match_reason == "HIGH_TEXT_SIMILARITY"
