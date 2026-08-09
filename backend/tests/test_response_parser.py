"""
GuardianAI AI Response Parser Unit Test Suite
Purpose: Tests GeminiResponse parsing, malformed output auto-repair, versioned schema resolution, and exception handling.
"""

import pytest
from pydantic import BaseModel, Field
from app.ai.gemini_client import GeminiResponse
from app.ai.response_parser import (
    AIResponseParserEngine,
    SchemaRegistry,
    SchemaVersionNotFoundError,
    MalformedAIOutputError,
    SchemaValidationError
)

class SampleThreatDTOV1(BaseModel):
    threat_score: int
    risk_band: str

class SampleThreatDTOV2(BaseModel):
    threat_score: int
    risk_band: str
    confidence_score: float

# Register versioned schemas
SchemaRegistry.register("threat_dto", "v1.0.0", SampleThreatDTOV1)
SchemaRegistry.register("threat_dto", "v2.0.0", SampleThreatDTOV2)

def test_parse_gemini_response_object_v1():
    """Tests parsing GeminiResponse object into v1.0.0 DTO."""
    gemini_res = GeminiResponse(
        raw_text='{"threat_score": 90, "risk_band": "dangerous"}',
        model_id="gemini-3.6-flash-high",
        prompt_tokens=40,
        completion_tokens=20,
        total_tokens=60,
        latency_ms=45.0
    )
    parsed = AIResponseParserEngine.parse_gemini_response(
        response_input=gemini_res,
        schema_id_or_class="threat_dto",
        version="v1.0.0"
    )
    assert isinstance(parsed, SampleThreatDTOV1)
    assert parsed.threat_score == 90
    assert parsed.risk_band == "dangerous"

def test_parse_versioned_schema_v2():
    """Tests resolving version v2.0.0 schema."""
    raw = '{"threat_score": 95, "risk_band": "dangerous", "confidence_score": 0.99}'
    parsed = AIResponseParserEngine.parse_gemini_response(
        response_input=raw,
        schema_id_or_class="threat_dto",
        version="v2.0.0"
    )
    assert isinstance(parsed, SampleThreatDTOV2)
    assert parsed.confidence_score == 0.99

def test_unregistered_schema_version_raises_error():
    """Tests requesting an unmapped schema version raises SchemaVersionNotFoundError."""
    with pytest.raises(SchemaVersionNotFoundError):
        AIResponseParserEngine.parse_gemini_response(
            response_input="{}",
            schema_id_or_class="threat_dto",
            version="v9.9.9"
        )

def test_schema_validation_error_handling():
    """Tests missing required fields raises SchemaValidationError."""
    raw = '{"risk_band": "dangerous"}' # Missing threat_score
    with pytest.raises(SchemaValidationError) as exc_info:
        AIResponseParserEngine.parse_gemini_response(
            response_input=raw,
            schema_id_or_class=SampleThreatDTOV1
        )
    assert len(exc_info.value.errors) > 0
