"""
GuardianAI Decoupled AI Infrastructure Package
"""

from app.ai.config import ai_settings
from app.ai.client import BaseAIClient, GeminiFlashClient, MockAIClient
from app.ai.gemini_client import (
    GeminiClient,
    GeminiClientManager,
    get_gemini_client,
    GeminiResponse,
    GeminiClientException,
    GeminiTimeoutException,
    GeminiAuthenticationException
)
from app.ai.registry import ModelRegistry
from app.ai.prompts import PromptRegistry, VersionedPromptTemplate
from app.ai.prompt_engine import PromptTemplateEngine
from app.ai.parser import AIResponseParser
from app.ai.json_validator import JSONValidationEngine
from app.ai.response_parser import AIResponseParserEngine
from app.ai.telemetry import AITelemetryTracker, AITelemetryMetrics
from app.ai.logging import AILogger
from app.ai.service import AIService, get_ai_service

__all__ = [
    "ai_settings",
    "BaseAIClient",
    "GeminiFlashClient",
    "MockAIClient",
    "GeminiClient",
    "GeminiClientManager",
    "get_gemini_client",
    "GeminiResponse",
    "GeminiClientException",
    "GeminiTimeoutException",
    "GeminiAuthenticationException",
    "ModelRegistry",
    "PromptRegistry",
    "VersionedPromptTemplate",
    "PromptTemplateEngine",
    "AIResponseParser",
    "JSONValidationEngine",
    "AIResponseParserEngine",
    "AITelemetryTracker",
    "AITelemetryMetrics",
    "AILogger",
    "AIService",
    "get_ai_service",
]
