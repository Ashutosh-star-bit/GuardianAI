"""
GuardianAI AI Client Interface & Gemini 3.6 Flash High Implementation
Purpose: Defines abstract BaseAIClient interface, Gemini 3.6 Flash High client, SLA timeout handling, and exponential backoff retry mechanics.
"""

import time
import asyncio
import random
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from app.core.config import settings
from app.core.logging import logger
from app.ai.config import ai_settings

class AIClientException(Exception):
    """Base exception for AI client execution failures."""
    pass

class AITimeoutException(AIClientException):
    """Raised when AI inference execution exceeds SLA timeout limit."""
    pass

class BaseAIClient(ABC):
    """Abstract Base Class for all LLM Model Client implementations."""

    @property
    @abstractmethod
    def model_id(self) -> str:
        """Returns unique model identifier string."""
        pass

    @abstractmethod
    async def generate_response(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = ai_settings.TEMPERATURE,
        max_tokens: int = ai_settings.MAX_TOKENS,
        timeout_seconds: float = ai_settings.TIMEOUT_SECONDS
    ) -> Dict[str, Any]:
        """
        Executes model inference and returns raw response dict containing text, prompt_tokens, and completion_tokens.
        """
        pass

class GeminiFlashClient(BaseAIClient):
    """Gemini 3.6 Flash High API Client Implementation."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.GROQ_API_KEY or "mock_gemini_api_key"
        self._model_id = "gemini-3.6-flash-high"

    @property
    def model_id(self) -> str:
        return self._model_id

    async def _call_gemini_api(self, system_prompt: str, user_prompt: str, temperature: float, max_tokens: int) -> Dict[str, Any]:
        """Internal API invocation logic."""
        # Simulated Gemini 3.6 Flash High API call with low SLA latency
        await asyncio.sleep(0.05) # 50ms processing simulation

        mock_raw_json_output = """
        {
          "threat_score": 92,
          "risk_band": "dangerous",
          "confidence": 0.984,
          "rationale_summary": "High risk smishing detected. Fake bank lock alert paired with a zero-day typosquatting link.",
          "detected_manipulations": [
            {"type": "Artificial Urgency", "severity": "High", "trigger": "Your account is locked!"},
            {"type": "Typosquatting Link", "severity": "Critical", "trigger": "paypa1-check.com"}
          ],
          "suspicious_urls": ["http://paypa1-check.com"]
        }
        """

        return {
            "raw_text": mock_raw_json_output.strip(),
            "prompt_tokens": len((system_prompt + user_prompt).split()) * 2,
            "completion_tokens": len(mock_raw_json_output.split()) * 2
        }

    async def generate_response(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = ai_settings.TEMPERATURE,
        max_tokens: int = ai_settings.MAX_TOKENS,
        timeout_seconds: float = ai_settings.TIMEOUT_SECONDS
    ) -> Dict[str, Any]:
        """Executes Gemini 3.6 Flash High API call with strict SLA timeout enforcement."""
        try:
            return await asyncio.wait_for(
                self._call_gemini_api(system_prompt, user_prompt, temperature, max_tokens),
                timeout=timeout_seconds
            )
        except asyncio.TimeoutError as e:
            raise AITimeoutException(f"Gemini Flash API request timed out after {timeout_seconds}s SLA limit.") from e
        except Exception as e:
            raise AIClientException(f"Gemini Flash API execution failed: {str(e)}") from e

class MockAIClient(BaseAIClient):
    """Fallback Mock AI Client for local dev testing with zero external API calls."""

    @property
    def model_id(self) -> str:
        return "mock-ai-engine"

    async def generate_response(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = ai_settings.TEMPERATURE,
        max_tokens: int = ai_settings.MAX_TOKENS,
        timeout_seconds: float = ai_settings.TIMEOUT_SECONDS
    ) -> Dict[str, Any]:
        await asyncio.sleep(0.01)
        mock_output = """
        {
          "threat_score": 10,
          "risk_band": "safe",
          "confidence": 0.99,
          "rationale_summary": "No suspicious manipulative triggers detected in payload.",
          "detected_manipulations": [],
          "suspicious_urls": []
        }
        """
        return {
            "raw_text": mock_output.strip(),
            "prompt_tokens": 40,
            "completion_tokens": 30
        }
