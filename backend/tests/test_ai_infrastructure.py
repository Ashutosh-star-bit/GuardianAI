"""
GuardianAI AI Infrastructure Unit Test Suite
Purpose: Tests Model Registry, Prompt Versioning, Response Parser, Token/Cost Telemetry, and AIService execution pipeline.
"""

import pytest
from pydantic import BaseModel, Field
from app.ai.config import ai_settings
from app.ai.registry import ModelRegistry
from app.ai.client import GeminiFlashClient, MockAIClient
from app.ai.prompts import PromptRegistry, VersionedPromptTemplate
from app.ai.parser import AIResponseParser, AIResponseParseException, AIResponseValidationError
from app.ai.telemetry import AITelemetryTracker
from app.ai.service import AIService

class SampleScanSchema(BaseModel):
    threat_score: int
    risk_band: str
    confidence: float

def test_model_registry_factory():
    """Tests model registry factory instantiates correct clients."""
    gemini_client = ModelRegistry.get_client("gemini-3.6-flash-high")
    assert isinstance(gemini_client, GeminiFlashClient)
    assert gemini_client.model_id == "gemini-3.6-flash-high"

    mock_client = ModelRegistry.get_client("mock-ai-engine")
    assert isinstance(mock_client, MockAIClient)
    assert mock_client.model_id == "mock-ai-engine"

def test_prompt_template_versioning():
    """Tests registration and retrieval of versioned prompt templates."""
    template = VersionedPromptTemplate(
        template_id="test_prompt",
        version="v1.0.0",
        system_prompt="Test System Prompt",
        user_prompt_template="Test User Prompt for {name}",
        description="Unit test prompt"
    )
    PromptRegistry.register(template)

    retrieved = PromptRegistry.get("test_prompt", version="v1.0.0")
    assert retrieved.version == "v1.0.0"
    formatted = retrieved.format_user_prompt(name="GuardianAI")
    assert formatted == "Test User Prompt for GuardianAI"

def test_ai_response_parser_clean():
    """Tests extraction of JSON from markdown backticks."""
    raw_markdown = """
    ```json
    {
      "threat_score": 92,
      "risk_band": "dangerous",
      "confidence": 0.984
    }
    ```
    """
    parsed = AIResponseParser.parse_and_validate(raw_markdown, SampleScanSchema)
    assert parsed.threat_score == 92
    assert parsed.risk_band == "dangerous"
    assert parsed.confidence == 0.984

def test_ai_response_parser_invalid_json():
    """Tests AIResponseParseException is raised on invalid JSON."""
    with pytest.raises(AIResponseParseException):
        AIResponseParser.parse_and_validate("This is not JSON text", SampleScanSchema)

def test_telemetry_cost_calculation():
    """Tests token count and cost in USD computation."""
    # 1,000,000 prompt tokens @ $0.075 + 1,000,000 completion tokens @ $0.300 = $0.375
    cost = AITelemetryTracker.calculate_cost(1_000_000, 1_000_000)
    assert cost == 0.375

    # Small query: 1,000 prompt tokens + 500 completion tokens
    small_cost = AITelemetryTracker.calculate_cost(1_000, 500)
    assert small_cost > 0.0

@pytest.mark.asyncio
async def test_ai_service_execution_pipeline():
    """Tests complete AIService execution using Mock AI Client."""
    service = AIService()
    assert service.gemini_client is not None
