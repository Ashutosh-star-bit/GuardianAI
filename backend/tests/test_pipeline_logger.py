"""
GuardianAI Pipeline Logger Unit Test Suite
Purpose: Tests emission of structured telemetry logs, module lists, risk levels, SLA status calculations, and errors.
"""

import pytest
from app.pipeline.logger import PipelineTelemetryLogger

def test_pipeline_telemetry_logger_pass_sla():
    """Tests logging a successful pipeline execution passing 50ms SLA."""
    payload = PipelineTelemetryLogger.log_pipeline_execution(
        scan_id="scn_log_1",
        request_id="req_log_1",
        execution_time_ms=11.85,
        modules_executed=["Validator", "Prepro", "ThreatIntel", "DecisionPipeline"],
        risk_level="CRITICAL",
        risk_score=94,
        confidence=0.98
    )

    assert payload["scan_id"] == "scn_log_1"
    assert payload["execution_time_ms"] == 11.85
    assert payload["sla_status"] == "PASS (<50ms SLA)"
    assert payload["risk_level"] == "CRITICAL"
    assert len(payload["modules_executed"]) == 4

def test_pipeline_telemetry_logger_warn_sla():
    """Tests logging a pipeline execution breaching SLA threshold with warnings."""
    payload = PipelineTelemetryLogger.log_pipeline_execution(
        scan_id="scn_log_warn",
        request_id="req_log_warn",
        execution_time_ms=65.20,
        modules_executed=["Validator", "Prepro", "ThreatIntel"],
        risk_level="HIGH",
        risk_score=75,
        confidence=0.90,
        warnings=["Threat Intel API timeout"]
    )

    assert payload["sla_status"] == "WARN (SLA Exceeded)"
    assert payload["warnings_count"] == 1
    assert "Threat Intel API timeout" in payload["warnings"]
