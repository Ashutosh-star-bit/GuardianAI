"""
GuardianAI Duplicate Report Clustering & Deduplication Engine
Purpose: Detects duplicate scam reports using IOC hashing and text similarity distance.
"""

import hashlib
from typing import List, Dict, Any, Optional, Tuple

class Tuple_IsDup:
    def __init__(self, is_dup: bool, similarity: float, index: int):
        self.is_dup = is_dup
        self.similarity = similarity
        self.index = index

    def __iter__(self):
        yield self.is_dup
        yield self.similarity
        yield self.index

class DuplicateReportDetector:
    """Duplicate Scam Report Clustering Engine."""

    @classmethod
    def generate_ioc_hash(cls, content: str) -> str:
        """Generates SHA-256 normalized hash of scam indicator content."""
        if not content:
            return ""
        normalized = content.strip().lower()
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

    @classmethod
    def compute_jaccard_similarity(cls, text1: str, text2: str) -> float:
        """
        Computes word-level Jaccard similarity coefficient between two text strings (0.0 to 1.0).
        """
        if not text1 or not text2:
            return 0.0

        set1 = set(text1.lower().split())
        set2 = set(text2.lower().split())

        intersection = set1.intersection(set2)
        union = set1.union(set2)

        if not union:
            return 0.0

        return round(len(intersection) / len(union), 4)

    @classmethod
    def is_duplicate(cls, new_content: str, existing_contents: List[str], threshold: float = 0.75) -> Tuple_IsDup:
        """
        Checks if new scam content matches any existing report above similarity threshold.
        """
        for idx, existing in enumerate(existing_contents):
            sim = cls.compute_jaccard_similarity(new_content, existing)
            if sim >= threshold:
                return Tuple_IsDup(True, sim, idx)
        return Tuple_IsDup(False, 0.0, -1)
