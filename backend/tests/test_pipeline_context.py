"""
GuardianAI AnalysisContext State Manager Unit Test Suite
Purpose: Tests state tracking of Request ID, Scan ID, User ID, original input, metadata attachments, and latency measurement.
"""

import time
import pytest
from app.pipeline.context import AnalysisContext

def test_analysis_context_state_and_latency():
    """Tests creating AnalysisContext, setting metadata, and marking completion latency."""
    ctx = AnalysisContext(
        request_id="req_test_100",
        scan_id="scn_test_100",
        user_id="usr_999",
        input_type="SMS",
        original_input="URGENT: Verify at http://paypa1-check.top"
    )

    assert ctx.request_id == "req_test_100"
    assert ctx.scan_id == "scn_test_100"
    assert ctx.user_id == "usr_999"
    assert ctx.original_input == "URGENT: Verify at http://paypa1-check.top"

    # Set metadata
    ctx.set_metadata("locale", "en")
    assert ctx.metadata["locale"] == "en"

    # Simulate 10ms work
    time.sleep(0.01)
    latency_ms = ctx.mark_completed()

    assert latency_ms >= 8.0
    assert ctx.execution_time_ms == latency_ms
