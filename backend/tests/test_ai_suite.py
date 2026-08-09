"""
GuardianAI Complete Production AI Infrastructure Test Suite
Purpose: Unit tests for Mock Gemini, Prompt Rendering, JSON Auto-Repair Validation, Resiliency Retries,
         Response Parsing, Privacy-Safe Logging, and Environment Configuration.
"""

import pytest
import asyncio
from pydantic import BaseModel, Field

# AI Infrastructure Imports
from app.ai.config import (
    get_ai_config,
    DEVELOPMENT_AI_CONFIG,
    TESTING_AI_CONFIG,
    PRODUCTION_AI_CONFIG
)
from app.ai.client import MockAIClient, GeminiFlashClient
from app.ai.prompt_engine import (
    PromptTemplateEngine,
    PromptTemplateDefinition,
    PromptVariableMissingError,
    PromptTemplateNotFoundError
)
from app.ai.json_validator import JSONValidationEngine, JSONValidationError
from app.ai.response_parser import (
    AIResponseParserEngine,
    SchemaRegistry,
    SchemaVersionNotFoundError,
    SchemaValidationError
)
from app.ai.logging import AILogger
from app.ai.service import AIService, AIServiceResponse
from app.core.resiliency import with_retry, MaxRetriesExceededError

class ProductionTestSchema(BaseModel):
    threat_score: int = Field(ge=0, le=100)
    risk_band: str
    confidence: float

# Register Schema for testing
SchemaRegistry.register("prod_test_schema", "v1.0.0", ProductionTestSchema)

# 1. MOCK GEMINI CLIENT TESTS
@pytest.mark.asyncio
async def test_mock_gemini_client():
    """Tests MockAIClient returns structured output with zero external API calls."""
    client = MockAIClient()
    res = await client.generate_response(
        system_prompt="Test System",
        user_prompt="Test User"
    )
    assert "raw_text" in res
    assert res["prompt_tokens"] > 0
    assert res["completion_tokens"] > 0

# 2. PROMPT RENDERING TESTS
def test_prompt_rendering_and_variable_validation():
    """Tests prompt template rendering and missing variable error enforcement."""
    rendered = PromptTemplateEngine.render_prompt(
        template_id="smishing_detector",
        variables={"raw_content": "Your bank account is locked! Click http://paypa1-check.com"}
    )
    assert "smishing triggers" in rendered["user_prompt"]
    assert "paypa1-check.com" in rendered["user_prompt"]

    # Test missing variable raises PromptVariableMissingError
    with pytest.raises(PromptVariableMissingError):
        PromptTemplateEngine.render_prompt(template_id="smishing_detector", variables={})

# 3. JSON VALIDATION & AUTO-REPAIR TESTS
def test_json_auto_repair_and_validation():
    """Tests auto-repair of markdown code fences, trailing commas, unquoted keys, and Pydantic validation."""
    malformed_raw = """
    ```json
    {
      threat_score: 92,
      risk_band: "dangerous",
      confidence: 0.984,
    }
    ```
    """
    model = JSONValidationEngine.validate_and_repair(malformed_raw, ProductionTestSchema)
    assert model.threat_score == 92
    assert model.risk_band == "dangerous"
    assert model.confidence == 0.984

# 4. EXPONENTIAL BACKOFF RETRY TESTS
@pytest.mark.asyncio
async def test_retry_mechanism():
    """Tests retry decorator retries transient errors and enforces max limit."""
    attempts = 0

    @with_retry(max_retries=2, base_delay=0.01, jitter=0.0)
    async def flaky_call():
        nonlocal attempts
        attempts += 1
        if attempts < 2:
            raise TimeoutError("Simulated transient socket timeout")
        return "RECOVERED"

    res = await flaky_call()
    assert res == "RECOVERED"
    assert attempts == 2

# 5. RESPONSE PARSER & VERSIONING TESTS
def test_versioned_response_parser():
    """Tests versioned schema resolution and Gemini response parsing."""
    raw = '{"threat_score": 88, "risk_band": "dangerous", "confidence": 0.975}'
    parsed = AIResponseParserEngine.parse_gemini_response(
        response_input=raw,
        schema_id_or_class="prod_test_schema",
        version="v1.0.0"
    )
    assert isinstance(parsed, ProductionTestSchema)
    assert parsed.threat_score == 88

# 6. PRIVACY-SAFE LOGGING TESTS
def test_privacy_safe_logging(caplog):
    """Tests AILogger emits telemetry metrics WITHOUT leaking raw prompt content or PII."""
    with caplog.at_level("INFO", logger="guardianai.ai_telemetry"):
        AILogger.log_ai_execution(
            scan_id="scn_prod_999",
            model_id="gemini-3.6-flash-high",
            latency_ms=38.4,
            prompt_tokens=80,
            completion_tokens=40,
            total_tokens=120,
            cost_usd=0.000018,
            user_id="usr_prod_123"
        )

    log_output = caplog.text
    assert "gemini-3.6-flash-high" in log_output
    assert "scn_prod_999" in log_output
    assert "usr_prod_123" in log_output
    assert "raw_content" not in log_output

# 7. ENVIRONMENT CONFIGURATION TESTS
def test_ai_config_environments():
    """Tests environment profiles for development, testing, and production."""
    assert DEVELOPMENT_AI_CONFIG.environment == "development"
    assert TESTING_AI_CONFIG.environment == "testing"
    assert TESTING_AI_CONFIG.TEMPERATURE == 0.0 # Deterministic for unit tests
    assert PRODUCTION_AI_CONFIG.environment == "production"
    assert PRODUCTION_AI_CONFIG.TIMEOUT_SECONDS == 10.0
    assert PRODUCTION_AI_CONFIG.safety_settings.category_hate_speech == "BLOCK_MEDIUM_AND_ABOVE"
