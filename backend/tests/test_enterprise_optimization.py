"""
GuardianAI Enterprise Optimization Pytest Suite
"""

import time
import pytest
from app.core.enterprise_optimization import EnterpriseOptimizationEngine, enterprise_optimization_engine

def test_query_caching_decorator():
    call_count = 0

    @enterprise_optimization_engine.cached_query(ttl_seconds=10)
    def expensive_query(param: str):
        nonlocal call_count
        call_count += 1
        return f"result_{param}_{call_count}"

    res1 = expensive_query("test")
    assert res1 == "result_test_1"

    # Second call uses cached result
    res2 = expensive_query("test")
    assert res2 == "result_test_1"
    assert call_count == 1

def test_stream_dataset_chunks():
    records = [{"id": i} for i in range(250)]
    chunks = list(EnterpriseOptimizationEngine.stream_dataset_chunks(records, chunk_size=100))
    assert len(chunks) == 3
    assert len(chunks[0]) == 100
    assert len(chunks[2]) == 50
