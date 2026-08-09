"""
GuardianAI Stress Testing & Self-Healing Pytest Suite
"""

import time
import pytest
from app.core.rate_limiter import tiered_rate_limiter, UserTier

def test_rate_limiter_throttling_under_stress():
    # Simulate high-rate stress hitting rate limiter (ANONYMOUS limit = 20 req/min)
    for _ in range(25):
        tiered_rate_limiter.check_rate_limit(identifier="stress_test_ip", tier=UserTier.ANONYMOUS)

    allowed, limit, remaining, reset_sec = tiered_rate_limiter.check_rate_limit(identifier="stress_test_ip", tier=UserTier.ANONYMOUS)
    assert allowed is False
    assert remaining == 0
    assert reset_sec > 0
