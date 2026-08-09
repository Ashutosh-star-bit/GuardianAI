"""
GuardianAI AI Dependency Injection Unit Test Suite
Purpose: Tests dependency injection providers for GeminiClient, AIService, Prompt Engine, Response Parser, and Config.
"""

from app.ai.di import (
    get_ai_config_dep,
    get_gemini_client_dep,
    get_prompt_engine_dep,
    get_json_validator_dep,
    get_response_parser_dep,
    get_token_tracker_dep,
    get_ai_service_dep
)
from app.ai.gemini_client import GeminiClient
from app.ai.service import AIService

def test_ai_di_providers():
    """Tests all AI Dependency Injection providers return valid instances."""
    config = get_ai_config_dep()
    assert config is not None

    client = get_gemini_client_dep()
    assert isinstance(client, GeminiClient)

    prompt_engine = get_prompt_engine_dep()
    assert prompt_engine is not None

    json_validator = get_json_validator_dep()
    assert json_validator is not None

    response_parser = get_response_parser_dep()
    assert response_parser is not None

    token_tracker = get_token_tracker_dep()
    assert token_tracker is not None

    ai_service = get_ai_service_dep(gemini_client=client)
    assert isinstance(ai_service, AIService)
    assert ai_service.gemini_client == client
