"""
GuardianAI Community Intelligence High-Performance LRU Caching Engine
Purpose: Thread-safe content-addressable memory cache providing sub-1ms response times for:
         1. Trending Scam Categories & Cyber Threat Vectors
         2. Scam Report Details Lookups
         3. User Reputation & Trust Score Multipliers.
"""

import time
import threading
from typing import Dict, Any, Optional

class CommunityCache:
    """Thread-safe LRU Caching Engine with TTL Expiration for Community Intel."""

    def __init__(self, max_size: int = 1000, default_ttl_seconds: int = 300):
        self._max_size = max_size
        self._default_ttl_seconds = default_ttl_seconds
        self._store: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()

    def get(self, key: str) -> Optional[Any]:
        """Retrieves cached item if present and not expired."""
        with self._lock:
            entry = self._store.get(key)
            if not entry:
                return None

            # TTL Expiration Check
            if time.time() > entry["expires_at"]:
                del self._store[key]
                return None

            entry["last_accessed"] = time.time()
            return entry["data"]

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None):
        """Stores item in cache with TTL and LRU eviction if full."""
        ttl = ttl_seconds if ttl_seconds is not None else self._default_ttl_seconds
        expires_at = time.time() + ttl

        with self._lock:
            # LRU Eviction if capacity exceeded
            if len(self._store) >= self._max_size and key not in self._store:
                lru_key = min(self._store.keys(), key=lambda k: self._store[k]["last_accessed"])
                del self._store[lru_key]

            self._store[key] = {
                "data": value,
                "expires_at": expires_at,
                "last_accessed": time.time()
            }

    def invalidate(self, key: str):
        """Invalidates target cache key."""
        with self._lock:
            if key in self._store:
                del self._store[key]

    def clear(self):
        """Clears all cached entries."""
        with self._lock:
            self._store.clear()

# Global Thread-Safe Cache Instance
community_cache = CommunityCache()
