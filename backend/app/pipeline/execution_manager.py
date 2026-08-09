"""
GuardianAI Pipeline ExecutionManager & Resilience Engine
Purpose: Provides robust pipeline step execution featuring SLA Timeout Enforcement, Exponential Backoff Retries,
         Subsystem Error Isolation, Asynchronous Cancellation Support, Structured Logging, and Step Performance Metrics.
"""

import time
import asyncio
import logging
from typing import Callable, Any, Optional, Dict, Tuple
from pydantic import BaseModel, Field

logger = logging.getLogger("guardianai.pipeline.execution_manager")

class StepExecutionMetric(BaseModel):
    """Performance & Health Metric DTO for an individual pipeline step execution."""
    step_name: str
    success: bool
    retries_count: int = 0
    step_latency_ms: float
    error_message: Optional[str] = None

class ExecutionManager:
    """Enterprise Pipeline Step Execution & Resilience Engine."""

    @classmethod
    async def execute_step(
        cls,
        step_name: str,
        coro_func: Callable[..., Any],
        *args: Any,
        timeout_seconds: float = 5.0,
        max_retries: int = 2,
        fallback_value: Optional[Any] = None,
        **kwargs: Any
    ) -> Tuple[Any, StepExecutionMetric]:
        """
        Executes a pipeline step coroutine with timeout SLA, exponential backoff retries, and error isolation.
        Returns tuple of (step_result, StepExecutionMetric).
        """
        start_time = time.perf_counter()
        retries_count = 0
        last_exception: Optional[Exception] = None

        for attempt in range(max_retries + 1):
            try:
                logger.debug(f"[PipelineStep: {step_name}] Starting attempt {attempt + 1}/{max_retries + 1}...")

                # Enforce per-step timeout SLA
                result = await asyncio.wait_for(coro_func(*args, **kwargs), timeout=timeout_seconds)
                elapsed_ms = round((time.perf_counter() - start_time) * 1000.0, 2)

                metric = StepExecutionMetric(
                    step_name=step_name,
                    success=True,
                    retries_count=retries_count,
                    step_latency_ms=elapsed_ms
                )
                logger.debug(f"[PipelineStep: {step_name}] Completed in {elapsed_ms}ms (Retries: {retries_count}).")
                return result, metric

            except asyncio.CancelledError:
                logger.warning(f"[PipelineStep: {step_name}] Execution CANCELLED by caller.")
                raise # Propagate cancellation cleanly

            except asyncio.TimeoutError as e:
                last_exception = e
                logger.warning(f"[PipelineStep: {step_name}] Attempt {attempt + 1} breached SLA timeout ({timeout_seconds}s).")

            except Exception as e:
                last_exception = e
                logger.error(f"[PipelineStep: {step_name}] Attempt {attempt + 1} encountered error: {str(e)}")

            # Exponential backoff pause if retries remaining
            if attempt < max_retries:
                retries_count += 1
                backoff_delay = 0.1 * (2 ** attempt)
                await asyncio.sleep(backoff_delay)

        # Error Isolation: Return fallback value if retries exhausted
        elapsed_ms = round((time.perf_counter() - start_time) * 1000.0, 2)
        err_msg = str(last_exception) if last_exception else "Step execution failed."
        logger.error(f"[PipelineStep: {step_name}] EXHAUSTED ALL RETRIES. Isolated error: {err_msg}")

        metric = StepExecutionMetric(
            step_name=step_name,
            success=False,
            retries_count=retries_count,
            step_latency_ms=elapsed_ms,
            error_message=err_msg
        )

        return fallback_value, metric
