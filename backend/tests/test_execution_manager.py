"""
GuardianAI ExecutionManager Unit Test Suite
Purpose: Tests step execution, timeout SLA enforcement, exponential backoff retries, error isolation fallback, and latency metrics.
"""

import asyncio
import pytest
from app.pipeline.execution_manager import ExecutionManager, StepExecutionMetric

@pytest.mark.asyncio
async def test_execution_manager_success():
    """Tests successful step execution with zero retries."""
    async def sample_coro(val: int):
        await asyncio.sleep(0.01)
        return val * 2

    res, metric = await ExecutionManager.execute_step(
        step_name="sample_step",
        coro_func=sample_coro,
        val=5,
        timeout_seconds=2.0
    )

    assert res == 10
    assert metric.success is True
    assert metric.retries_count == 0
    assert metric.step_latency_ms > 0

@pytest.mark.asyncio
async def test_execution_manager_timeout_and_fallback():
    """Tests timeout SLA enforcement and error isolation fallback."""
    async def slow_coro():
        await asyncio.sleep(1.0)
        return "SLOW_RESULT"

    res, metric = await ExecutionManager.execute_step(
        step_name="slow_step",
        coro_func=slow_coro,
        timeout_seconds=0.05,
        max_retries=1,
        fallback_value="FALLBACK_RESULT"
    )

    assert res == "FALLBACK_RESULT"
    assert metric.success is False
    assert metric.retries_count == 1
    assert "Timeout" in metric.error_message or "timeout" in metric.error_message.lower()

@pytest.mark.asyncio
async def test_execution_manager_retry_recovers():
    """Tests transient error retry recovery on second attempt."""
    attempts = 0

    async def flaky_coro():
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise ValueError("Transient error")
        return "SUCCESS_ON_RETRY"

    res, metric = await ExecutionManager.execute_step(
        step_name="flaky_step",
        coro_func=flaky_coro,
        max_retries=2
    )

    assert res == "SUCCESS_ON_RETRY"
    assert metric.success is True
    assert metric.retries_count == 1
