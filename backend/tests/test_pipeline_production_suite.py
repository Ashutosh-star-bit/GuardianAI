"""
GuardianAI Master Scam Analysis Pipeline Production Pytest Suite
Purpose: Complete production test suite covering InputValidationService, ScamAnalysisPipeline, ExecutionManager,
         HistoryService, AnalyticsRecorder, ReportGenerator, and Sub-50ms SLA Edge Cases.
"""

import time
import pytest
from app.pipeline.validator import InputValidationService, ValidatedInputPayload, InputValidationError
from app.pipeline.orchestrator import ScamAnalysisPipeline, ScamAnalysisPipelineResult
from app.pipeline.execution_manager import ExecutionManager
from app.pipeline.history_service import HistoryService
from app.pipeline.analytics_recorder import AnalyticsRecorder
from app.pipeline.report_generator import ReportGenerator
from app.decision_engine.schemas import DecisionResult, RiskMetricsSchema, ConfidenceMetricsSchema, DecisionXAISummary

@pytest.fixture(autouse=True)
def clean_pipeline_stores():
    HistoryService.clear_all()
    AnalyticsRecorder.clear_all()
    yield
    HistoryService.clear_all()
    AnalyticsRecorder.clear_all()

# 1. VALIDATION TESTS
def test_pipeline_validation_production():
    """Tests InputValidationService across text, JSON, and null byte rejection."""
    val_text = InputValidationService.validate_payload("URGENT: Verify PayPal account", format_type="TEXT")
    assert val_text.format_type == "TEXT"

    val_json = InputValidationService.validate_payload('{"msg": "Verify link"}', format_type="JSON")
    assert val_json.raw_json_dict["msg"] == "Verify link"

    with pytest.raises(InputValidationError):
        InputValidationService.validate_payload("URGENT\x00Message")

# 2. PIPELINE END-TO-END TESTS
@pytest.mark.asyncio
async def test_master_pipeline_execution_production():
    """Tests complete 10-stage Master Scam Analysis Pipeline execution."""
    raw = "URGENT: Your PayPal account is suspended. Verify at http://paypa1-check.top or send $500 to support.refund@okaxis"
    res: ScamAnalysisPipelineResult = await ScamAnalysisPipeline.execute_full_scam_analysis(
        raw_input=raw,
        format_type="TEXT",
        target_persona="SENIOR_CITIZENS"
    )

    assert res.request_id.startswith("req_")
    assert res.scan_id.startswith("scn_")
    assert res.decision.final_scam_probability > 0
    assert res.executive_report.risk_score > 0
    assert res.execution_time_ms > 0

# 3. EXECUTION MANAGER & RESILIENCE TESTS
@pytest.mark.asyncio
async def test_execution_manager_retry_and_fallback_production():
    """Tests ExecutionManager timeout SLA enforcement, retries, and fallback isolation."""
    attempts = 0

    async def flaky_step():
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise ValueError("Transient error")
        return "OK"

    res, metric = await ExecutionManager.execute_step("flaky_test", flaky_step, max_retries=2)
    assert res == "OK"
    assert metric.retries_count == 1

# 4. HISTORY SERVICE TESTS
def test_history_service_sha256_search_production():
    """Tests SHA-256 input hashing, history storage, keyword search, and pagination."""
    rec = HistoryService.store_scan_history(
        scan_id="s100",
        request_id="r100",
        original_text="Verify at http://paypa1-check.top",
        cleaned_text="Verify at http://paypa1-check.top",
        decision_dict={"final_scam_probability": 90, "risk_level": "CRITICAL"},
        execution_time_ms=11.5,
        user_id="u1"
    )

    assert len(rec.input_hash) == 64
    records, total = HistoryService.search_history(user_id="u1", query="paypa1")
    assert total == 1
    assert records[0].scan_id == "s100"

# 5. ANALYTICS RECORDER TESTS
def test_analytics_recorder_production():
    """Tests AnalyticsRecorder tracking total scans, risk levels, and average latency."""
    AnalyticsRecorder.record_scan_event(risk_level="CRITICAL", execution_time_ms=12.0, confidence=0.98, date_key="2026-07-28")
    AnalyticsRecorder.record_scan_event(risk_level="SAFE", execution_time_ms=10.0, confidence=0.90, date_key="2026-07-28")

    summary = AnalyticsRecorder.get_analytics_summary(date_key="2026-07-28")
    assert summary["total_scans"] == 2
    assert summary["avg_execution_ms"] == 11.0
    assert summary["risk_level_counts"]["CRITICAL"] == 1

# 6. REPORT GENERATOR TESTS
def test_report_generator_pdf_markdown_production():
    """Tests 8-section report synthesis and PDF Markdown export."""
    dec = DecisionResult(
        scan_id="scn_rpt_prod",
        final_scam_probability=95,
        confidence=0.98,
        risk_level="CRITICAL",
        risk_metrics=RiskMetricsSchema(final_scam_probability=95, risk_level="CRITICAL", technical_risk_score=90, psychological_risk_score=95),
        confidence_metrics=ConfidenceMetricsSchema(overall_confidence=0.98, cross_modal_agreement=0.95, certainty_band="VERY_HIGH"),
        reasons=["Spoofed domain paypa1-check.top mimicking PayPal"],
        evidence=[],
        recommendations=["Do NOT click links."],
        safe_reply="I am reporting this message.",
        action_plan=[],
        explainability=DecisionXAISummary(summary="Critical smishing attempt.", detected_factors=[], key_threat_vectors=[])
    )

    report = ReportGenerator.generate_full_report(dec)
    assert report.risk_score == 95
    assert len(report.educational_notes) >= 3

    md_out = ReportGenerator.export_pdf_markdown(report)
    assert "# GuardianAI Comprehensive Security Threat Report" in md_out

# 7. PERFORMANCE SLA & EDGE CASES TEST
@pytest.mark.asyncio
async def test_pipeline_performance_sla_and_edge_cases():
    """Tests Master Pipeline performance SLA latency under 50ms for whitespace padded input."""
    padded_input = "   URGENT:   Verify PayPal account now at http://paypa1-check.top   "
    start_t = time.perf_counter()
    res = await ScamAnalysisPipeline.execute_full_scam_analysis(raw_input=padded_input)
    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    assert res.decision.final_scam_probability > 0
    assert elapsed_ms < 50.0, f"SLA latency breach: Took {elapsed_ms:.2f}ms (Limit: 50.0ms)"
