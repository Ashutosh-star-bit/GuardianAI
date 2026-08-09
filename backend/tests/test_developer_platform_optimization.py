"""
GuardianAI Developer Platform Optimization Pytest Suite
"""

import pytest
from app.developer_platform.developer_optimization import DeveloperPlatformOptimizationEngine, developer_optimization_engine
from app.developer_platform.api_key_service import APIKeyRecord

def test_cached_key_lookup():
    call_count = 0

    @developer_optimization_engine.cached_key_lookup(ttl_seconds=10)
    def mock_lookup(raw_key: str):
        nonlocal call_count
        call_count += 1
        return APIKeyRecord(
            key_id="key_cached_101",
            name="Cached Key",
            key_prefix="gai_live_88f9",
            key_hash="hash_value",
            environment="LIVE",
            tier="PRO",
            created_at_iso="2026-08-01T00:00:00Z"
        )

    rec1 = mock_lookup("gai_live_secret_123")
    assert rec1.key_id == "key_cached_101"
    assert call_count == 1

    # Second call uses L1 LRU cache
    rec2 = mock_lookup("gai_live_secret_123")
    assert rec2.key_id == "key_cached_101"
    assert call_count == 1
