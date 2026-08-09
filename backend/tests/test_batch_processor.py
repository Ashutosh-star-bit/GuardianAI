"""
GuardianAI BatchProcessor Unit & Multi-Format Concurrency Pytest Suite
Purpose: Tests concurrent batch processing across Text, URL, Email, and QR formats, concurrency limits, and error isolation.
"""

import pytest
from app.pipeline.batch_processor import BatchProcessor, BatchItemPayload, BatchAnalysisResult, BatchProcessorError

@pytest.mark.asyncio
async def test_batch_processor_multi_format_batch():
    """Tests BatchProcessor concurrently analyzing Text, URL, Email, and QR items."""
    items = [
        BatchItemPayload(item_id="it_1", raw_payload="URGENT: Verify PayPal account at http://paypa1-check.top", format_type="TEXT"),
        BatchItemPayload(item_id="it_2", raw_payload="https://paypa1-check.top", format_type="URL"),
        BatchItemPayload(item_id="it_3", raw_payload="From: support@paypa1-check.top\nSubject: Account Locked\n\nVerify link", format_type="EMAIL"),
        BatchItemPayload(item_id="it_4", raw_payload="upi://pay?pa=merchant@okaxis", format_type="QR")
    ]

    res: BatchAnalysisResult = await BatchProcessor.process_batch(items=items, max_concurrency=4)

    assert res.total_items == 4
    assert res.successful_items == 4
    assert res.failed_items == 0
    assert res.total_execution_time_ms > 0
    assert len(res.results) == 4

    for item_res in res.results:
        assert item_res.status == "SUCCESS"
        assert item_res.analysis_result is not None
        assert item_res.analysis_result.scan_id.startswith("scn_")

@pytest.mark.asyncio
async def test_batch_processor_fault_tolerance():
    """Tests BatchProcessor error isolation when a batch item encounters an invalid input error."""
    items = [
        BatchItemPayload(item_id="valid_1", raw_payload="Normal message", format_type="TEXT"),
        BatchItemPayload(item_id="invalid_1", raw_payload="URGENT\x00Message", format_type="TEXT")  # Contains null byte
    ]

    res = await BatchProcessor.process_batch(items=items)

    assert res.total_items == 2
    assert res.successful_items == 1
    assert res.failed_items == 1

    failed_item = next(r for r in res.results if r.item_id == "invalid_1")
    assert failed_item.status == "FAILED"
    assert "null byte" in failed_item.error_message

@pytest.mark.asyncio
async def test_batch_processor_empty_and_max_limit_errors():
    """Tests BatchProcessor error validation for empty items list and exceeding max batch limit."""
    # Empty items list
    with pytest.raises(BatchProcessorError, match="cannot be empty"):
        await BatchProcessor.process_batch(items=[])

    # Exceeding MAX_BATCH_SIZE (101 items)
    too_many = [BatchItemPayload(raw_payload="Test") for _ in range(101)]
    with pytest.raises(BatchProcessorError, match="exceeds max limit"):
        await BatchProcessor.process_batch(items=too_many)
