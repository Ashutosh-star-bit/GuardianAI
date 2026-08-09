"""
GuardianAI Pipeline Logging & Telemetry Engine
Purpose: Provides structured JSON logging of Execution Time, Modules Executed, Errors, Warnings,
         Model Confidence, Risk Level Classifications, and SLA Performance Latency metrics.
"""

import json
import logging
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any

logger = logging.getLogger("guardianai.pipeline.telemetry")

class PipelineTelemetryLogger:
    """Enterprise Pipeline Telemetry & Structured Logging Engine."""

    @classmethod
    def log_pipeline_execution(
        cls,
        scan_id: str,
        request_id: str,
        execution_time_ms: float,
        modules_executed: List[str],
        risk_level: str,
        risk_score: int,
        confidence: float,
        errors: Optional[List[str]] = None,
        warnings: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Emits structured JSON telemetry log event for a completed pipeline execution.
        """
        sla_pass = execution_time_ms < 50.0
        sla_status = "PASS (<50ms SLA)" if sla_pass else "WARN (SLA Exceeded)"

        log_payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": "PIPELINE_EXECUTION_TELEMETRY",
            "scan_id": scan_id,
            "request_id": request_id,
            "execution_time_ms": round(execution_time_ms, 2),
            "sla_status": sla_status,
            "modules_executed": modules_executed,
            "risk_level": risk_level,
            "risk_score": risk_score,
            "confidence": round(confidence, 3),
            "errors_count": len(errors or []),
            "errors": errors or [],
            "warnings_count": len(warnings or []),
            "warnings": warnings or []
        }

        log_msg = f"[PipelineTelemetry] Scan '{scan_id}' finished in {execution_time_ms:.2f}ms [{sla_status}] | Risk: {risk_level} ({risk_score}/100) | Conf: {confidence:.2f}"

        if errors:
            logger.error(f"{log_msg} | ERRORS: {', '.join(errors)}")
        elif warnings:
            logger.warning(f"{log_msg} | WARNINGS: {', '.join(warnings)}")
        else:
            logger.info(log_msg)

        logger.debug(f"[PipelineTelemetryJSON] {json.dumps(log_payload)}")

        return log_payload
