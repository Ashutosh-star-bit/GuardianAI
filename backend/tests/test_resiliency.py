"""
GuardianAI Retry & Resiliency Infrastructure Unit Test Suite
Purpose: Tests exponential backoff retries, transient error filtering, non-transient exception passthrough, and SLA timeouts.
"""

import pytest
import asyncio
from app.core.resiliency import with_retry, with_timeout, MaxRetriesExceededError, RequestTimeoutException

class FlakyTransientService:
    def __init__(self, failures_before_success: int = 2):
        self.attempts = 0
        self.failures_before_success = failures_before_success

    @with_retry(max_retries=3, base_delay=0.01, jitter=0.0)
    async def flaky_async_call(self):
        self.attempts += 1
        if self.attempts <= self.failures_before_success:
            raise TimeoutError("Transient network glitch")
        return "SUCCESS"

    @with_retry(max_retries=2, base_delay=0.01, jitter=0.0)
    async def failing_async_call(self):
        self.attempts += 1
        raise ConnectionError("Persistent connection failure")

    @with_retry(max_retries=3, base_delay=0.01, jitter=0.0)
    async def non_transient_call(self):
        self.attempts += 1
        raise ValueError("Non-retryable invalid argument error")

@pytest.mark.asyncio
async def test_retry_transient_success():
    """Tests function retries on transient TimeoutError and eventually succeeds."""
    service = FlakyTransientService(failures_before_success=2)
    res = await service.flaky_async_call()
    assert res == "SUCCESS"
    assert service.attempts == 3

@pytest.mark.asyncio
async def test_retry_exhaustion_raises_error():
    """Tests MaxRetriesExceededError is raised when retries exceed limit."""
    service = FlakyTransientService()
    with pytest.raises(MaxRetriesExceededError):
        await service.failing_async_call()
    assert service.attempts == 3 # Initial attempt + 2 retries

@pytest.mark.asyncio
async def test_non_transient_error_no_retry():
    """Tests non-transient exceptions (e.g. ValueError) fail immediately without retrying."""
    service = FlakyTransientService()
    with pytest.raises(ValueError):
        await service.non_transient_call()
    assert service.attempts == 1 # Zero retries executed

@pytest.mark.asyncio
async def test_timeout_decorator_enforcement():
    """Tests with_timeout decorator raises RequestTimeoutException on SLA breach."""
    @with_timeout(seconds=0.05)
    async def slow_operation():
        await asyncio.sleep(0.2)
        return "DONE"

    with pytest.raises(RequestTimeoutException):
        await slow_operation()
