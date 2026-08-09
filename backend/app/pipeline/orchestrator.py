"""
GuardianAI Scam Analysis Pipeline Orchestrator
Purpose: Orchestrates the 10-stage Master Scam Analysis Pipeline:
         1. Receive Raw Payload -> 2. Resolve Input Adapter via InputAdapterFactory -> 3. Generate UniversalAnalysisRequest ->
         4. Threat Intelligence Engine -> 5. NLP Entity Extraction -> 6. Multi-Factor Risk Classifier ->
         7. XAI Explainability Engine -> 8. Action Planner & Safe Reply Generator ->
         9. Build Final Scam Report -> 10. Persist Scan History & Analytics Record.
"""

import time
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from app.adapters.factory import InputAdapterFactory
from app.adapters.schemas import UniversalAnalysisRequest
from app.threat_intel.service import ThreatIntelligenceService
from app.nlp.engine import TextIntelligenceEngine
from app.decision_engine.service import DecisionService, DecisionServiceReport
from app.pipeline.logger import PipelineTelemetryLogger
from app.pipeline.history_service import HistoryService
from app.pipeline.analytics_recorder import AnalyticsRecorder
from app.pipeline.validator import InputValidationService
from app.pipeline.context import AnalysisContext
from app.decision_engine.schemas import DecisionResult

class ScamAnalysisPipelineResult(BaseModel):
    """Execution Context and Result Container for Scam Analysis Pipeline."""
    request_id: str
    scan_id: str
    user_id: Optional[str] = None
    input_type: str
    raw_content: str
    analysis_request: UniversalAnalysisRequest
    threat_intel: Any
    nlp_features: Dict[str, Any] = Field(default_factory=dict)
    nlp_entities: List[Any] = Field(default_factory=list)
    decision: DecisionResult
    history_record: Any
    execution_time_ms: float
    modules_executed: List[str] = Field(default_factory=list)
    created_at: str

class ScamAnalysisPipeline:
    """Master Scam Analysis Pipeline Engine."""

    def __init__(
        self,
        threat_intel_service: Optional[ThreatIntelligenceService] = None,
        nlp_engine: Optional[TextIntelligenceEngine] = None,
        decision_service: Optional[DecisionService] = None,
        history_service: Optional[HistoryService] = None,
        analytics_recorder: Optional[AnalyticsRecorder] = None
    ):
        self.threat_intel = threat_intel_service or ThreatIntelligenceService()
        self.nlp_engine = nlp_engine or TextIntelligenceEngine()
        self.decision_service = decision_service or DecisionService()
        self.history_service = history_service or HistoryService()
        self.analytics_recorder = analytics_recorder or AnalyticsRecorder()
        self.validator = InputValidationService()
        self.logger = PipelineTelemetryLogger()

    @classmethod
    async def execute_full_scam_analysis(
        cls,
        raw_input: Any,
        format_type: Optional[str] = None,
        request_id: Optional[str] = None,
        scan_id: Optional[str] = None,
        user_id: Optional[str] = None,
        target_persona: str = "SENIOR_CITIZENS",
        locale: str = "en",
        source: str = "REST_API",
        **kwargs: Any
    ) -> ScamAnalysisPipelineResult:
        """
        Executes complete 10-stage Master Scam Analysis Pipeline integrated with polymorphic Input Adapters.
        """
        req_id = request_id or f"req_{uuid.uuid4().hex[:10]}"
        sid = scan_id or f"scn_{uuid.uuid4().hex[:10]}"
        modules_executed: List[str] = []
        instance = cls()

        # Stage 1 & 2: Resolve Input Adapter & Generate UniversalAnalysisRequest DTO
        modules_executed.append("InputAdapterFactory")
        adapted_request: UniversalAnalysisRequest = InputAdapterFactory.process_payload(
            raw_payload=raw_input,
            format_type=format_type,
            user_id=user_id,
            language=locale,
            source=source,
            **kwargs
        )

        start_time = time.time()

        # Stage 3: Input Validation
        modules_executed.append("InputValidationService")
        instance.validator.validate_payload(
            raw_input=adapted_request.raw_content,
            format_type=adapted_request.input_type,
            language=locale
        )

        # Stage 4: Threat Intelligence Scan
        modules_executed.append("ThreatIntelligenceService")
        threat_intel_result = await instance.threat_intel.analyze_threat_payload(
            scan_id=sid,
            raw_text=adapted_request.raw_content
        )

        # Stage 5: NLP Entity Extraction & Pattern Analysis
        modules_executed.append("TextIntelligenceEngine")
        nlp_res_dto = instance.nlp_engine.analyze_text(
            scan_id=sid,
            raw_text=adapted_request.raw_content
        )
        nlp_result = nlp_res_dto.model_dump()

        # Stage 6, 7 & 8: Master Decision Service (Risk Classifier + XAI + Safe Reply + Action Planner)
        modules_executed.append("DecisionService")
        decision_report_envelope: DecisionServiceReport = await instance.decision_service.process_full_decision_scan(
            scan_id=sid,
            raw_text=adapted_request.raw_content,
            target_persona=target_persona,
            locale=locale,
            precomputed_text_intel=nlp_result,
            precomputed_threat_intel=threat_intel_result.model_dump(mode="json")
        )
        decision_report: DecisionResult = decision_report_envelope.decision

        elapsed_ms = round((time.time() - start_time) * 1000, 2)

        # Stage 9: Persist Scan History Record
        modules_executed.append("HistoryService")
        history_record = instance.history_service.store_scan_history(
            scan_id=sid,
            request_id=req_id,
            original_text=adapted_request.raw_content,
            cleaned_text=adapted_request.raw_content,
            decision_dict=decision_report.model_dump(mode="json"),
            execution_time_ms=elapsed_ms,
            user_id=adapted_request.user_id,
            input_format=adapted_request.input_type
        )

        # Stage 10: Record Analytics Event
        modules_executed.append("AnalyticsRecorder")
        instance.analytics_recorder.record_scan_event(
            risk_level=decision_report.risk_level,
            execution_time_ms=elapsed_ms,
            confidence=decision_report.confidence,
            channel_type=adapted_request.input_type
        )

        # Log Pipeline Execution Telemetry
        instance.logger.log_pipeline_execution(
            scan_id=sid,
            request_id=req_id,
            execution_time_ms=elapsed_ms,
            modules_executed=modules_executed,
            risk_level=decision_report.risk_level,
            risk_score=decision_report.final_scam_probability,
            confidence=decision_report.confidence
        )

        return ScamAnalysisPipelineResult(
            request_id=req_id,
            scan_id=sid,
            user_id=adapted_request.user_id,
            input_type=adapted_request.input_type,
            raw_content=adapted_request.raw_content,
            analysis_request=adapted_request,
            threat_intel=threat_intel_result,
            nlp_features=nlp_result.get("features", {}),
            nlp_entities=nlp_result.get("entities", []),
            decision=decision_report,
            history_record=history_record,
            execution_time_ms=elapsed_ms,
            modules_executed=modules_executed,
            created_at=adapted_request.created_at
        )
