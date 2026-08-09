"""
GuardianAI Curated ML Dataset Builder Engine
Purpose: Filters, curates, and exports high-quality Human-in-the-Loop (HITL) fine-tuning datasets
         from approved scam reports, verified feedback, and moderator corrections.
         Excludes spam, duplicates, and rejected records.
         Supports JSON/JSONL, CSV, and Parquet export representations.
"""

import json
import csv
import io
from typing import List, Dict, Any, Optional
from app.voice_intel.security import VoiceSecuritySanitizer

class CuratedDatasetRecord:
    """Standardized Curated ML Training Sample DTO."""
    def __init__(
        self,
        record_id: str,
        instruction: str,
        input_text: str,
        target_label: str,
        scam_category: str,
        extracted_iocs: Dict[str, Any],
        verified_by: str = "MODERATOR",
        quality_score: float = 1.0
    ):
        self.record_id = record_id
        self.instruction = instruction
        self.input_text = VoiceSecuritySanitizer.sanitize_transcript(input_text)
        self.target_label = target_label
        self.scam_category = scam_category
        self.extracted_iocs = extracted_iocs
        self.verified_by = verified_by
        self.quality_score = quality_score

    def to_dict(self) -> Dict[str, Any]:
        return {
            "record_id": self.record_id,
            "instruction": self.instruction,
            "input_text": self.input_text,
            "target_label": self.target_label,
            "scam_category": self.scam_category,
            "extracted_iocs": json.dumps(self.extracted_iocs),
            "verified_by": self.verified_by,
            "quality_score": self.quality_score
        }

class DatasetBuilder:
    """Enterprise Curated ML Dataset Builder & Multi-Format Exporter."""

    @classmethod
    def filter_and_curate_records(
        cls,
        raw_reports: List[Dict[str, Any]],
        raw_feedbacks: List[Dict[str, Any]]
    ) -> List[CuratedDatasetRecord]:
        """
        Curates raw database records by enforcing strict data quality filters:
        - Include ONLY verified reports & moderator-approved feedback.
        - Exclude spam, rejected, and merged duplicate reports.
        """
        curated: List[CuratedDatasetRecord] = []
        seen_inputs = set()

        # 1. Process Approved Scam Reports
        for rep in raw_reports:
            status = rep.get("verification_status") or rep.get("status")
            is_spam = rep.get("is_spam", False)

            if status != "VERIFIED" or is_spam:
                continue

            text_content = rep.get("description") or rep.get("title") or ""
            if not text_content or len(text_content.strip()) < 10:
                continue

            # Deduplication Check
            input_hash = hash(text_content.strip().lower())
            if input_hash in seen_inputs:
                continue
            seen_inputs.add(input_hash)

            record = CuratedDatasetRecord(
                record_id=rep.get("id") or rep.get("report_id") or "rep_000",
                instruction="Classify the following text for scam threat risk, scam vector category, and extract IOCs:",
                input_text=text_content,
                target_label=rep.get("risk_level", "DANGEROUS"),
                scam_category=rep.get("category") or rep.get("scam_category", "OTHER"),
                extracted_iocs=rep.get("evidence_data") or {},
                verified_by="COMMUNITY_MODERATOR",
                quality_score=1.0
            )
            curated.append(record)

        # 2. Process Verified Feedback Loop Records
        for fb in raw_feedbacks:
            if not fb.get("is_verified_by_moderator", True):
                continue

            text_content = fb.get("comment") or fb.get("input_text") or ""
            if not text_content:
                continue

            input_hash = hash(text_content.strip().lower())
            if input_hash in seen_inputs:
                continue
            seen_inputs.add(input_hash)

            record = CuratedDatasetRecord(
                record_id=fb.get("id") or "fb_000",
                instruction="Analyze user feedback and correct scam prediction vector:",
                input_text=text_content,
                target_label=fb.get("actual_risk_level", "DANGEROUS"),
                scam_category=fb.get("suggested_category", "OTHER"),
                extracted_iocs={},
                verified_by="MODERATOR_AUDIT",
                quality_score=0.95
            )
            curated.append(record)

        return curated

    @classmethod
    def export_to_json(cls, records: List[CuratedDatasetRecord]) -> str:
        """Exports curated records as formatted JSON array string."""
        return json.dumps([r.to_dict() for r in records], indent=2, ensure_ascii=False)

    @classmethod
    def export_to_jsonl(cls, records: List[CuratedDatasetRecord]) -> str:
        """Exports curated records as line-delimited JSONL string."""
        return "\n".join([json.dumps(r.to_dict(), ensure_ascii=False) for r in records])

    @classmethod
    def export_to_csv(cls, records: List[CuratedDatasetRecord]) -> str:
        """Exports curated records as CSV string."""
        output = io.StringIO()
        if not records:
            return ""

        fieldnames = ["record_id", "instruction", "input_text", "target_label", "scam_category", "extracted_iocs", "verified_by", "quality_score"]
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        for r in records:
            writer.writerow(r.to_dict())

        return output.getvalue()

    @classmethod
    def export_to_parquet_dict(cls, records: List[CuratedDatasetRecord]) -> Dict[str, List[Any]]:
        """
        Exports curated records as column-oriented dictionary representation for Pandas/PyArrow Parquet serialization.
        """
        dict_data = {
            "record_id": [],
            "instruction": [],
            "input_text": [],
            "target_label": [],
            "scam_category": [],
            "extracted_iocs": [],
            "verified_by": [],
            "quality_score": []
        }
        for r in records:
            d = r.to_dict()
            for key in dict_data.keys():
                dict_data[key].append(d[key])

        return dict_data
