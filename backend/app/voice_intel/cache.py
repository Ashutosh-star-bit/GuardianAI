"""
GuardianAI Thread-Safe High-Performance Audio LRU Cache Engine
Purpose: Content-Addressable SHA-256 Audio LRU Cache delivering sub-1ms response times
         for duplicate audio lookups with O(1) eviction and TTL expiry.
"""

import hashlib
import time
import threading
from collections import OrderedDict
from typing import Optional, Tuple
from app.voice_intel.schemas import VoiceAnalysisResult

class VoiceCache:
    """Enterprise Thread-Safe Content-Addressable Audio LRU Cache."""

    def __init__(self, max_capacity: int = 2000, ttl_seconds: int = 3600):
        self.max_capacity = max_capacity
        self.ttl_seconds = ttl_seconds
        self._cache: OrderedDict[str, Tuple[VoiceAnalysisResult, float]] = OrderedDict()
        self._lock = threading.Lock()
        self.hits = 0
        self.misses = 0

    def _hash_audio(self, raw_bytes: bytes) -> str:
        """Calculates SHA-256 hex digest of raw binary audio stream."""
        return hashlib.sha256(raw_bytes).hexdigest()

    def get(self, raw_bytes: bytes) -> Optional[VoiceAnalysisResult]:
        """
        Retrieves cached VoiceAnalysisResult in O(1) time if unexpired.
        """
        if not raw_bytes:
            return None

        key = self._hash_audio(raw_bytes)
        now = time.time()

        with self._lock:
            if key in self._cache:
                result, timestamp = self._cache[key]
                if now - timestamp < self.ttl_seconds:
                    self._cache.move_to_end(key) # Mark as recently used
                    self.hits += 1
                    return result
                del self._cache[key] # Expire stale entry

            self.misses += 1
            return None

    def set(self, raw_bytes: bytes, result: VoiceAnalysisResult):
        """
        Stores VoiceAnalysisResult in LRU cache with capacity eviction.
        """
        if not raw_bytes or not result:
            return

        key = self._hash_audio(raw_bytes)
        now = time.time()

        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
            self._cache[key] = (result, now)

            # Evict oldest entry if capacity exceeded
            if len(self._cache) > self.max_capacity:
                self._cache.popitem(last=False)

    def clear(self):
        """Purges all entries from cache."""
        with self._lock:
            self._cache.clear()

voice_cache_instance = VoiceCache()
