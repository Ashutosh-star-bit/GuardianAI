"""
GuardianAI Reusable Retry & Resiliency Infrastructure
Purpose: Provides exponential backoff retries with jitter, SLA timeout enforcement, transient error filtering,
         and structured logging for external API and database operations.
"""

import time
import asyncio
import random
import functools
from typing import Callable, Type, Tuple, Optional, Any, Union
from app.core.logging import logger

# Transient Error Exception Types (Network timeouts, socket drops, 502/503/504 gateway failures)
TRANSIENT_EXCEPTIONS: Tuple[Type[Exception], ...] = (
    TimeoutError,
    ConnectionError,
    OSError,
    asyncio.TimeoutError,
)

class MaxRetriesExceededError(Exception):
    """Raised when maximum retry attempts are exhausted."""
    pass

class RequestTimeoutException(Exception):
    """Raised when operation execution exceeds SLA timeout limit."""
    pass

def with_retry(
    max_retries: int = 3,
    base_delay: float = 0.1,
    backoff_factor: float = 2.0,
    jitter: float = 0.05,
    retryable_exceptions: Tuple[Type[Exception], ...] = TRANSIENT_EXCEPTIONS
) -> Callable:
    """
    Decorator wrapping async or sync functions with exponential backoff retries and jitter.
    ONLY retries on specified transient exceptions.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        if asyncio.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                attempt = 0
                while attempt <= max_retries:
                    attempt += 1
                    try:
                        return await func(*args, **kwargs)
                    except retryable_exceptions as e:
                        if attempt > max_retries:
                            logger.error(
                                f"[Resiliency Retry] Max retries ({max_retries}) exhausted for {func.__name__}: {str(e)}"
                            )
                            raise MaxRetriesExceededError(
                                f"Operation '{func.__name__}' failed after {max_retries} retries. Last error: {str(e)}"
                            ) from e

                        delay = (base_delay * (backoff_factor ** (attempt - 1))) + random.uniform(0, jitter)
                        logger.warning(
                            f"[Resiliency Retry] Transient failure in {func.__name__} (Attempt {attempt}/{max_retries}). "
                            f"Retrying in {delay:.3f}s. Exception: {str(e)}"
                        )
                        await asyncio.sleep(delay)
            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                attempt = 0
                while attempt <= max_retries:
                    attempt += 1
                    try:
                        return func(*args, **kwargs)
                    except retryable_exceptions as e:
                        if attempt > max_retries:
                            logger.error(
                                f"[Resiliency Retry] Max retries ({max_retries}) exhausted for {func.__name__}: {str(e)}"
                            )
                            raise MaxRetriesExceededError(
                                f"Operation '{func.__name__}' failed after {max_retries} retries. Last error: {str(e)}"
                            ) from e

                        delay = (base_delay * (backoff_factor ** (attempt - 1))) + random.uniform(0, jitter)
                        logger.warning(
                            f"[Resiliency Retry] Transient failure in {func.__name__} (Attempt {attempt}/{max_retries}). "
                            f"Retrying in {delay:.3f}s. Exception: {str(e)}"
                        )
                        time.sleep(delay)
            return sync_wrapper

    return decorator

def with_timeout(seconds: float = 10.0) -> Callable:
    """
    Decorator enforcing SLA execution timeout limits for async functions.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return await asyncio.wait_for(func(*args, **kwargs), timeout=seconds)
            except asyncio.TimeoutError as e:
                logger.error(f"[SLA Timeout] Async function '{func.__name__}' timed out after {seconds}s.")
                raise RequestTimeoutException(f"Operation '{func.__name__}' exceeded {seconds}s SLA timeout.") from e
        return wrapper
    return decorator
