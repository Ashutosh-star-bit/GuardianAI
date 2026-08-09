"""
GuardianAI End-to-End Text Intelligence AI Pipeline Orchestrator
Purpose: Implements complete 8-step pipeline: Receive Text -> Preprocess -> Extract Entities & Patterns ->
         Render Prompt -> Call Gemini 3.6 Flash High -> Auto-Repair JSON -> Parse Schema -> Return Structured Object.
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from app.nlp.preprocessing import TextPreprocessor
from app.nlp.features import FeatureExtractor
from app.nlp.patterns import PatternDetector
from app.nlp.entities import EntityExtractor
from app.nlp.schema_design import GeminiTextThreatAnalysisSchema
from app.ai.service import AIService, AIServiceResponse, get_ai_service
from app.ai.telemetry import AITelemetryMetrics

class TextIntelligencePipelineResult(BaseModel):
    """End-to-End Pipeline Execution Output Container DTO."""
    scan_id: str
    channel_type: str
    original_text: str
    cleaned_text: str
    analysis: GeminiTextThreatAnalysisSchema
    telemetry: AITelemetryMetrics

class TextIntelligencePipeline:
    """Master 8-Step Text Intelligence Integration Pipeline."""

    def __init__(self, ai_service: Optional[AIService] = None):
        self.ai_service = ai_service or get_ai_service()

    async def execute_pipeline(
        self,
        scan_id: str,
        raw_text: str,
        channel_type: str = "SMS",
        user_id: Optional[str] = None,
        locale: str = "en"
    ) -> TextIntelligencePipelineResult:
        """
        Executes end-to-end 8-step analysis pipeline:
        1. Receive Text
        2. Preprocess (Unicode, Emojis, Whitespace, Homoglyphs)
        3. Extract Features, Patterns & Entities (12 Entity Types)
        4. Render Versioned Prompt Template
        5. Call Gemini 3.6 Flash High (Timeout SLA & Retries)
        6. Validate & Auto-Repair Malformed JSON Syntax
        7. Parse into Typed GeminiTextThreatAnalysisSchema Object
        8. Return Structured Result with Telemetry Metrics
        """
        # 1 & 2. Preprocess Text
        cleaned_text = TextPreprocessor.clean_text(raw_text)
        deobfuscated_text = TextPreprocessor.deobfuscate_homoglyphs(cleaned_text)

        # 3. Extract Features, Patterns & Named Entities
        features = FeatureExtractor.extract_features(deobfuscated_text)
        patterns = PatternDetector.detect_patterns(deobfuscated_text)
        entities_report = EntityExtractor.extract_all_entities(cleaned_text)

        extracted_urls_str = ", ".join(entities_report.urls) or "None"
        extracted_entities_str = ", ".join([f"{e.entity_type}:{e.text}" for e in entities_report.all_entities]) or "None"
        detected_patterns_str = ", ".join([f"{p.category}:{p.pattern_name}" for p in patterns]) or "None"

        # 4, 5, 6, 7. Render Prompt, Call Gemini, Auto-Repair JSON, and Parse Schema via AIService
        ai_service_result: AIServiceResponse[GeminiTextThreatAnalysisSchema] = await self.ai_service.process_ai_request(
            scan_id=scan_id,
            payload_type=f"{channel_type}/Text",
            template_id="psychological_threat_analysis",
            template_variables={
                "channel_type": channel_type,
                "raw_content": deobfuscated_text,
                "extracted_urls": extracted_urls_str,
                "extracted_entities": extracted_entities_str,
                "detected_patterns": detected_patterns_str
            },
            schema_id_or_class=GeminiTextThreatAnalysisSchema,
            prompt_version="v1.0.0",
            schema_version="v1.0.0",
            locale=locale,
            model_id="gemini-3.6-flash-high"
        )

        # Enrich detected features and entities into final analysis DTO
        analysis_data = ai_service_result.data
        analysis_data.detected_features = features.model_dump(mode="json")
        analysis_data.entities = [e.model_dump(mode="json") for e in entities_report.all_entities]

        # 8. Return Typed Pipeline Container Result
        return TextIntelligencePipelineResult(
            scan_id=scan_id,
            channel_type=channel_type,
            original_text=raw_text,
            cleaned_text=deobfuscated_text,
            analysis=analysis_data,
            telemetry=ai_service_result.telemetry
        )
