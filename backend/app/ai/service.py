"""
GuardianAI Infrastructure AI Service Orchestrator
Purpose: Orchestrates prompt template rendering, Gemini LLM invocation, auto-repair JSON parsing,
         Pydantic schema validation, and token/cost telemetry tracking. Zero business logic.
"""

import time
import asyncio
from typing import Type, TypeVar, Generic, Optional, Dict, Any
from pydantic import BaseModel, Field
from app.ai.config import ai_settings
from app.ai.gemini_client import GeminiClient, GeminiClientManager, GeminiResponse
from app.ai.prompt_engine import PromptTemplateEngine
from app.ai.response_parser import AIResponseParserEngine
from app.ai.telemetry import AITelemetryTracker, AITelemetryMetrics

T = TypeVar("T", bound=BaseModel)

class AIServiceResponse(BaseModel, Generic[T]):
    """Unified Typed Response Container emitted by AIService."""
    data: T = Field(description="Typed Pydantic DTO output object")
    raw_text: str = Field(description="Raw LLM text response output")
    telemetry: AITelemetryMetrics = Field(description="Token counts and USD cost metrics")

class AIService:
    """Production Infrastructure AI Service orchestrating LLM execution pipeline."""

    def __init__(self, gemini_client: Optional[GeminiClient] = None):
        self.gemini_client = gemini_client or GeminiClientManager.get_instance()

    async def process_ai_request(
        self,
        scan_id: str,
        payload_type: str,
        template_id: str,
        template_variables: Dict[str, Any],
        schema_id_or_class: Any,
        prompt_version: str = "v1.0.0",
        schema_version: str = "v1.0.0",
        locale: str = "en",
        model_id: str = "gemini-3.6-flash-high"
    ) -> AIServiceResponse[T]:
        """
        Executes end-to-end AI Infrastructure Pipeline:
        1. Renders versioned prompt template with variable validation
        2. Invokes Gemini 3.6 Flash High with timeout SLA & retries
        3. Auto-repairs malformed syntax & parses JSON into typed Pydantic object
        4. Calculates token usage & USD inference cost telemetry
        """
        # 1. Render Prompt Template
        prompts = PromptTemplateEngine.render_prompt(
            template_id=template_id,
            variables=template_variables,
            version=prompt_version,
            locale=locale
        )
        system_prompt = prompts["system_prompt"]
        user_prompt = prompts["user_prompt"]

        start_time = time.perf_counter()

        # 2. Invoke Gemini LLM Client
        gemini_response: GeminiResponse = await self.gemini_client.generate_content(
            user_prompt=user_prompt,
            system_prompt=system_prompt,
            model_id=model_id
        )

        latency_ms = (time.perf_counter() - start_time) * 1000

        # 3. Auto-Repair & Parse Typed Pydantic DTO
        typed_data = AIResponseParserEngine.parse_gemini_response(
            response_input=gemini_response,
            schema_id_or_class=schema_id_or_class,
            version=schema_version
        )

        # Extract threat_score and risk_band for logging telemetry
        threat_score = getattr(typed_data, "threat_score", 0)
        risk_band = getattr(typed_data, "risk_band", "safe")

        # 4. Compute & Log Telemetry
        telemetry = AITelemetryTracker.record_metrics(
            scan_id=scan_id,
            payload_type=payload_type,
            model_id=gemini_response.model_id,
            threat_score=threat_score,
            risk_band=risk_band,
            prompt_tokens=gemini_response.prompt_tokens,
            completion_tokens=gemini_response.completion_tokens,
            latency_ms=latency_ms
        )

        return AIServiceResponse(
            data=typed_data,
            raw_text=gemini_response.raw_text,
            telemetry=telemetry
        )

def get_ai_service() -> AIService:
    """FastAPI Dependency Injection Provider returning AIService instance."""
    return AIService()
