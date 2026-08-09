"""
GuardianAI CommunityCache Pytest Suite
"""

import time
import pytest
from app.community_intel.cache import CommunityCache

@pytest.fixture
def cache():
    return CommunityCache(max_size=3, default_ttl_seconds=1)

def test_cache_set_and_get(cache):
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"

def test_cache_ttl_expiration(cache):
    cache.set("temp_key", "temp_val", ttl_seconds=1)
    assert cache.get("temp_key") == "temp_val"

    time.sleep(1.1)
    assert cache.get("temp_key") is None

def test_cache_lru_eviction(cache):
    cache.set("k1", "v1")
    cache.set("k2", "v2")
    cache.set("k3", "v3")

    # Access k1 to make k2 the LRU
    _ = cache.get("k1")

    # Insert 4th element -> Should evict k2
    cache.set("k4", "v4")

    assert cache.get("k1") == "v1"
    assert cache.get("k2") is None # Evicted
    assert cache.get("k4") == "v4"
