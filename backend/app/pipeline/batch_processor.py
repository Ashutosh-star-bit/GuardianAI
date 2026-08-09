"""
GuardianAI High-Performance BatchProcessor Engine
Purpose: Concurrently processes batch analysis requests across multiple payload formats (Text, URL, Email, PDF, QR),
         enforces worker pool semaphore bounds, isolates per-item errors, and generates BatchAnalysisResult DTO.
"""

import uuid
import time
import asyncio
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from app.adapters.factory import InputAdapterFactory
from app.pipeline.orchestrator import ScamAnalysisPipeline, ScamAnalysisPipelineResult
from app.pipeline.execution_manager import ExecutionManager

class BatchItemPayload(BaseModel):
    """Container for a single item in a batch payload request."""
    item_id: str = Field(default_factory=lambda: f"item_{uuid.uuid4().hex[:8]}")
    raw_payload: str
    format_type: Optional[str] = None  # None for auto-sniffing or explicit format key

class BatchItemResult(BaseModel):
    """Container for processing result of a single item in a batch."""
    item_id: str
    status: str = Field(description="SUCCESS or FAILED")
    analysis_result: Optional[ScamAnalysisPipelineResult] = None
    error_message: Optional[str] = None

class BatchAnalysisResult(BaseModel):
    """Container for complete batch execution output."""
    batch_id: str
    total_items: int
    successful_items: int
    failed_items: int
    total_execution_time_ms: float
    avg_latency_per_item_ms: float
    results: List[BatchItemResult]

class BatchProcessorError(ValueError):
    """Exception raised when batch processing fails or exceeds bounds."""
    pass

class BatchProcessor:
    """Enterprise High-Performance Concurrent Batch Processor Engine."""

    MAX_BATCH_SIZE = 100
    DEFAULT_CONCURRENCY = 10

    @classmethod
    async def process_batch(
        cls,
        items: List[BatchItemPayload],
        user_id: Optional[str] = None,
        target_persona: str = "SENIOR_CITIZENS",
        locale: str = "en",
        max_concurrency: int = DEFAULT_CONCURRENCY
    ) -> BatchAnalysisResult:
        """
        Executes concurrent batch scam analysis across multiple items with semaphore concurrency bounds
        and error isolation fallbacks.
        """
        if not items:
            raise BatchProcessorError("Batch payload items list cannot be empty")

        if len(items) > cls.MAX_BATCH_SIZE:
            raise BatchProcessorError(f"Batch items count ({len(items)}) exceeds max limit of {cls.MAX_BATCH_SIZE}")

        batch_id = f"batch_{uuid.uuid4().hex[:10]}"
        start_time = time.perf_counter()
        semaphore = asyncio.Semaphore(max_concurrency)

        async def _process_single_item(item: BatchItemPayload) -> BatchItemResult:
            async with semaphore:
                try:
                    # 1. Adapt polymorphic payload into UniversalAnalysisRequest via InputAdapterFactory
                    adapted_req = await InputAdapterFactory.process_payload(
                        raw_payload=item.raw_payload,
                        format_type=item.format_type,
                        user_id=user_id,
                        language=locale
                    )

                    # 2. Execute Master Scam Analysis Pipeline
                    pipeline_res: ScamAnalysisPipelineResult = await ScamAnalysisPipeline.execute_full_scam_analysis(
                        raw_input=adapted_req.raw_content,
                        format_type=adapted_req.input_type,
                        user_id=user_id,
                        target_persona=target_persona,
                        locale=locale
                    )

                    return BatchItemResult(
                        item_id=item.item_id,
                        status="SUCCESS",
                        analysis_result=pipeline_res
                    )
                except Exception as e:
                    return BatchItemResult(
                        item_id=item.item_id,
                        status="FAILED",
                        error_message=str(e)
                    )

        # Process all batch items concurrently bounded by semaphore
        tasks = [_process_single_item(item) for item in items]
        batch_results: List[BatchItemResult] = await asyncio.gather(*tasks)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        success_count = sum(1 for r in batch_results if r.status == "SUCCESS")
        failed_count = len(batch_results) - success_count
        avg_ms = elapsed_ms / max(len(batch_results), 1)

        return BatchAnalysisResult(
            batch_id=batch_id,
            total_items=len(batch_results),
            successful_items=success_count,
            failed_items=failed_count,
            total_execution_time_ms=elapsed_ms,
            avg_latency_per_item_ms=avg_ms,
            results=batch_results
        )
