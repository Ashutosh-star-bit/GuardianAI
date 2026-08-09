"""
GuardianAI Backend Optimization Pytest Suite
"""

import pytest
import asyncio
from app.core.backend_optimization import backend_optimization_engine

def test_cached_scan_result_l1_lru():
    call_count = 0

    @backend_optimization_engine.cached_scan_result(ttl_seconds=10)
    def mock_scan(payload_hash: str):
        nonlocal call_count
        call_count += 1
        return {"threat_score": 98, "recommendation": "BLOCK_AND_REPORT"}

    res1 = mock_scan("hash_hdfc_verify")
    assert res1["threat_score"] == 98
    assert call_count == 1

    # Second call uses L1 cache
    res2 = mock_scan("hash_hdfc_verify")
    assert res2["threat_score"] == 98
    assert call_count == 1

@pytest.mark.asyncio
async def test_run_concurrent_scanners():
    def scanner_url():
        return "URL_OK"

    def scanner_text():
        return "TEXT_OK"

    results = await backend_optimization_engine.run_concurrent_scanners([scanner_url, scanner_text])
    assert len(results) == 2
    assert "URL_OK" in results
    assert "TEXT_OK" in results
