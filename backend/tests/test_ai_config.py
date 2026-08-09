"""
GuardianAI AI Configuration Unit Test Suite
Purpose: Tests environment profile selection (dev, testing, production) and safety filter matrices.
"""

from app.ai.config import (
    get_ai_config,
    DEVELOPMENT_AI_CONFIG,
    TESTING_AI_CONFIG,
    PRODUCTION_AI_CONFIG
)

def test_development_ai_config():
    """Tests development environment AI configuration parameters."""
    config = DEVELOPMENT_AI_CONFIG
    assert config.environment == "development"
    assert config.TEMPERATURE == 0.2
    assert config.MAX_RETRIES == 2

def test_testing_ai_config():
    """Tests testing environment AI configuration parameters."""
    config = TESTING_AI_CONFIG
    assert config.environment == "testing"
    assert config.TEMPERATURE == 0.0 # Deterministic
    assert config.DEFAULT_MODEL == "mock-ai-engine"
    assert config.MAX_RETRIES == 0

def test_production_ai_config():
    """Tests production environment AI configuration parameters."""
    config = PRODUCTION_AI_CONFIG
    assert config.environment == "production"
    assert config.TEMPERATURE == 0.1
    assert config.DEFAULT_MODEL == "gemini-3.6-flash-high"
    assert config.TIMEOUT_SECONDS == 10.0
    assert config.MAX_RETRIES == 3
    assert config.safety_settings.category_hate_speech == "BLOCK_MEDIUM_AND_ABOVE"

def test_dynamic_config_loader():
    """Tests dynamic get_ai_config function returns a valid AIEnvironmentConfig."""
    active_config = get_ai_config()
    assert active_config.DEFAULT_MODEL in ["gemini-3.6-flash-high", "mock-ai-engine"]
    assert active_config.MAX_TOKENS >= 1024
