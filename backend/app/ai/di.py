"""
GuardianAI AI Infrastructure Dependency Injection Container
Purpose: Centralizes FastAPI dependency providers for GeminiClient, AIService, Prompt Engine, Response Parser, Validators, and Config.
"""

from typing import Annotated
from fastapi import Depends
from app.ai.config import AIEnvironmentConfig, get_ai_config
from app.ai.gemini_client import GeminiClient, GeminiClientManager
from app.ai.prompt_engine import PromptTemplateEngine
from app.ai.json_validator import JSONValidationEngine
from app.ai.response_parser import AIResponseParserEngine
from app.ai.token_tracker import TokenTracker
from app.ai.service import AIService

# 1. AI Configuration Provider
def get_ai_config_dep() -> AIEnvironmentConfig:
    """Dependency provider returning active AI configuration settings."""
    return get_ai_config()

# 2. Singleton Gemini Client Provider
def get_gemini_client_dep() -> GeminiClient:
    """Dependency provider returning thread-safe Singleton GeminiClient."""
    return GeminiClientManager.get_instance()

# 3. Prompt Template Engine Provider
def get_prompt_engine_dep() -> PromptTemplateEngine:
    """Dependency provider returning PromptTemplateEngine class."""
    return PromptTemplateEngine()

# 4. JSON Validation Engine Provider
def get_json_validator_dep() -> JSONValidationEngine:
    """Dependency provider returning JSONValidationEngine class."""
    return JSONValidationEngine()

# 5. AI Response Parser Engine Provider
def get_response_parser_dep() -> AIResponseParserEngine:
    """Dependency provider returning AIResponseParserEngine class."""
    return AIResponseParserEngine()

# 6. Token Tracker Provider
def get_token_tracker_dep() -> TokenTracker:
    """Dependency provider returning TokenTracker engine."""
    return TokenTracker()

# 7. Fully-Wired AIService Orchestrator Provider
def get_ai_service_dep(
    gemini_client: GeminiClient = Depends(get_gemini_client_dep)
) -> AIService:
    """Dependency provider returning fully-wired AIService instance."""
    return AIService(gemini_client=gemini_client)

# Type Annotations for FastAPI Controllers
AIConfigDep = Annotated[AIEnvironmentConfig, Depends(get_ai_config_dep)]
GeminiClientDep = Annotated[GeminiClient, Depends(get_gemini_client_dep)]
PromptEngineDep = Annotated[PromptTemplateEngine, Depends(get_prompt_engine_dep)]
JSONValidatorDep = Annotated[JSONValidationEngine, Depends(get_json_validator_dep)]
ResponseParserDep = Annotated[AIResponseParserEngine, Depends(get_response_parser_dep)]
TokenTrackerDep = Annotated[TokenTracker, Depends(get_token_tracker_dep)]
AIServiceDep = Annotated[AIService, Depends(get_ai_service_dep)]
