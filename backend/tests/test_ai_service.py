"""
GuardianAI AIService Orchestrator Unit Test Suite
Purpose: Tests end-to-end AIService request pipeline (prompt rendering, Gemini execution, JSON parsing, Pydantic validation, and telemetry).
"""

import pytest
from pydantic import BaseModel
from app.ai.service import AIService, AIServiceResponse
from app.ai.gemini_client import GeminiClient

class TestThreatSchema(BaseModel):
    threat_score: int
    risk_band: str

@pytest.mark.asyncio
async def test_ai_service_process_request():
    """Tests end-to-end AIService request pipeline execution."""
    service = AIService()

    result: AIServiceResponse[TestThreatSchema] = await service.process_ai_request(
        scan_id="scn_test_888",
        payload_type="Text/SMS",
        template_id="smishing_detector",
        template_variables={"raw_content": "Urgent: Your account is locked! Click http://paypa1-check.com"},
        schema_id_or_class=TestThreatSchema,
        model_id="gemini-3.6-flash-high"
    )

    assert result.data.threat_score > 0
    assert result.data.risk_band in ["safe", "caution", "dangerous"]
    assert result.telemetry.model_id == "gemini-3.6-flash-high"
    assert result.telemetry.total_tokens > 0
    assert result.telemetry.latency_ms > 0
