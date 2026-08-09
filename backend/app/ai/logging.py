"""
GuardianAI Privacy-Safe AI Telemetry & Audit Logger
Purpose: Logs AI model execution metadata (Timestamp, Model, Latency, Token counts, Cost, Retries, Prompt version, User ID)
         WITHOUT writing raw user prompt content, payload bodies, or PII to disk or console.
"""

import logging
import json
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from app.core.logging import PIISanitizingFilter

# Initialize dedicated AI Telemetry Logger
ai_telemetry_logger = logging.getLogger("guardianai.ai_telemetry")

# Attach PII Sanitizing Filter for Zero-Knowledge Privacy Compliance
ai_telemetry_logger.addFilter(PIISanitizingFilter())

class AILogger:
    """Privacy-Safe AI Execution Telemetry Logger."""

    @staticmethod
    def log_ai_execution(
        scan_id: str,
        model_id: str,
        latency_ms: float,
        prompt_tokens: int,
        completion_tokens: int,
        total_tokens: int,
        cost_usd: float,
        prompt_version: str = "v1.0.0",
        user_id: Optional[str] = None,
        retries_count: int = 0,
        threat_score: Optional[int] = None,
        risk_band: Optional[str] = None,
        error: Optional[str] = None
    ) -> None:
        """
        Emits structured JSON telemetry log for AI execution.
        PRIVACY GUARANTEE: Raw user prompt text and payload content are STRICTLY EXCLUDED.
        """
        log_payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "scan_id": scan_id,
            "model": model_id,
            "latency_ms": round(latency_ms, 2),
            "tokens": {
                "prompt": prompt_tokens,
                "completion": completion_tokens,
                "total": total_tokens
            },
            "cost_usd": round(cost_usd, 6),
            "prompt_version": prompt_version,
            "user_id": user_id or "ANONYMOUS",
            "retries": retries_count,
            "threat_score": threat_score,
            "risk_band": risk_band,
            "status": "ERROR" if error else "SUCCESS",
            "error": error
        }

        # Render structured JSON telemetry line
        json_log_line = json.dumps(log_payload)

        if error:
            ai_telemetry_logger.error(f"[AI TELEMETRY] {json_log_line}")
        else:
            ai_telemetry_logger.info(f"[AI TELEMETRY] {json_log_line}")
