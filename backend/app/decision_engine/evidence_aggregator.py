"""
GuardianAI Enterprise Multi-Source Evidence Fusion Engine
Purpose: Merges evidence from AI Gemini, Keyword Rules, Threat Intelligence, Pattern Engine, and Entity Extractor
         into a unified, deduplicated, and severity-sorted evidence report.
"""

from typing import List, Dict, Optional, Any
from app.decision_engine.schemas import EvidenceItemSchema, DecisionXAISummary
from pydantic import BaseModel, Field

SEVERITY_RANK_MAP = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}

class DecisionEvidenceReport(BaseModel):
    """Unified Multi-Source Evidence Fusion Report DTO."""
    scan_id: str
    total_unified_evidence_count: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    unified_evidence_list: List[EvidenceItemSchema] = Field(default_factory=list)

class EvidenceFusionEngine:
    """Enterprise Multi-Source Evidence Fusion Engine."""

    @classmethod
    def deduplicate_and_sort_evidence(cls, items: List[EvidenceItemSchema]) -> List[EvidenceItemSchema]:
        """
        Deduplicates evidence matching on (indicator, category), retaining item with highest severity & confidence,
        then sorts descending by Severity rank (Critical -> High -> Medium -> Low) and Confidence float.
        """
        seen_map: Dict[str, EvidenceItemSchema] = {}

        for item in items:
            key = f"{item.category.upper()}:{item.indicator.lower()}"
            if key not in seen_map:
                seen_map[key] = item
            else:
                existing = seen_map[key]
                existing_rank = SEVERITY_RANK_MAP.get(existing.severity.capitalize(), 1)
                new_rank = SEVERITY_RANK_MAP.get(item.severity.capitalize(), 1)

                # Keep higher severity, or higher confidence if same severity
                if new_rank > existing_rank or (new_rank == existing_rank and item.confidence > existing.confidence):
                    seen_map[key] = item

        deduped = list(seen_map.values())

        # Sort by Severity Rank (descending), then Confidence (descending)
        deduped.sort(
            key=lambda i: (SEVERITY_RANK_MAP.get(i.severity.capitalize(), 1), i.confidence),
            reverse=True
        )

        return deduped

    @classmethod
    def fuse_multi_source_evidence(
        cls,
        scan_id: str,
        ai_evidence: Optional[List[EvidenceItemSchema]] = None,
        rule_evidence: Optional[List[EvidenceItemSchema]] = None,
        threat_intel_evidence: Optional[List[EvidenceItemSchema]] = None,
        pattern_evidence: Optional[List[EvidenceItemSchema]] = None,
        entity_evidence: Optional[List[EvidenceItemSchema]] = None
    ) -> DecisionEvidenceReport:
        """
        Combines evidence lists across 5 sources, deduplicates, sorts by severity, and calculates summary counts.
        """
        all_raw: List[EvidenceItemSchema] = []
        if ai_evidence:
            all_raw.extend(ai_evidence)
        if rule_evidence:
            all_raw.extend(rule_evidence)
        if threat_intel_evidence:
            all_raw.extend(threat_intel_evidence)
        if pattern_evidence:
            all_raw.extend(pattern_evidence)
        if entity_evidence:
            all_raw.extend(entity_evidence)

        unified_sorted = cls.deduplicate_and_sort_evidence(all_raw)

        critical_c = sum(1 for i in unified_sorted if i.severity.capitalize() == "Critical")
        high_c = sum(1 for i in unified_sorted if i.severity.capitalize() == "High")
        medium_c = sum(1 for i in unified_sorted if i.severity.capitalize() == "Medium")
        low_c = sum(1 for i in unified_sorted if i.severity.capitalize() == "Low")

        return DecisionEvidenceReport(
            scan_id=scan_id,
            total_unified_evidence_count=len(unified_sorted),
            critical_count=critical_c,
            high_count=high_c,
            medium_count=medium_c,
            low_count=low_c,
            unified_evidence_list=unified_sorted
        )
