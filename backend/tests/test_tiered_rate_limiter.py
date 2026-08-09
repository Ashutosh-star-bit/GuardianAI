"""
GuardianAI Tiered Rate Limiter Pytest Suite
"""

import pytest
from app.core.rate_limiter import TieredRateLimiterEngine, UserTier

@pytest.fixture
def limiter():
    return TieredRateLimiterEngine()

def test_anonymous_rate_limit_minute(limiter):
    # Anonymous limit is 20 req/min
    ip = "192.168.1.50"
    for i in range(20):
        is_allowed, limit, remaining, reset_sec = limiter.check_rate_limit(ip, tier=UserTier.ANONYMOUS, window_unit="minute")
        assert is_allowed is True
        assert limit == 20
        assert remaining == 19 - i

    # 21st request exceeds limit
    is_allowed, limit, remaining, reset_sec = limiter.check_rate_limit(ip, tier=UserTier.ANONYMOUS, window_unit="minute")
    assert is_allowed is False
    assert remaining == 0
    assert reset_sec > 0

def test_premium_rate_limit_minute(limiter):
    user_id = "usr_premium_101"
    is_allowed, limit, remaining, reset_sec = limiter.check_rate_limit(user_id, tier=UserTier.PREMIUM, window_unit="minute")
    assert is_allowed is True
    assert limit == 300
    assert remaining == 299

def test_enterprise_rate_limit_hour(limiter):
    corp_id = "corp_acme_inc"
    is_allowed, limit, remaining, reset_sec = limiter.check_rate_limit(corp_id, tier=UserTier.ENTERPRISE, window_unit="hour")
    assert is_allowed is True
    assert limit == 100000
    assert remaining == 99999
