"""
GuardianAI Model Registry & Switcher Factory
Purpose: Registers and manages available AI model client implementations, supporting seamless future model switching.
"""

from typing import Dict, Type, Optional
from app.ai.client import BaseAIClient, GeminiFlashClient, MockAIClient
from app.ai.config import ai_settings

class ModelRegistry:
    """Registry maintaining available LLM model client classes."""

    _models: Dict[str, Type[BaseAIClient]] = {
        "gemini-3.6-flash-high": GeminiFlashClient,
        "mock-ai-engine": MockAIClient,
    }

    @classmethod
    def register_model(cls, model_id: str, client_class: Type[BaseAIClient]) -> None:
        """Registers a new model client class in the global registry."""
        cls._models[model_id] = client_class

    @classmethod
    def get_client(cls, model_id: Optional[str] = None) -> BaseAIClient:
        """
        Factory method instantiating requested model client or default Gemini 3.6 Flash High.
        """
        target_model = model_id or ai_settings.DEFAULT_MODEL

        if target_model not in cls._models:
            # Fallback to Mock Client if requested model is unconfigured
            target_model = ai_settings.FALLBACK_MODEL

        client_class = cls._models[target_model]
        return client_class()
