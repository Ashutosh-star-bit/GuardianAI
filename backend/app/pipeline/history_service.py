"""
GuardianAI Pipeline HistoryService Engine
Purpose: Provides in-memory and database scan history persistence featuring SHA-256 Input Hashing,
         Search Querying, Risk Level Filtering, User-Scoped Pagination, and Record Deletion.
"""

import hashlib
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Tuple
from pydantic import BaseModel, Field

class ScanHistoryRecord(BaseModel):
    """Structured Scan History Persistence Record DTO."""
    scan_id: str
    request_id: str
    user_id: Optional[str] = None
    input_hash: str = Field(description="SHA-256 hex digest hash of original input payload")
    input_format: str = "TEXT"
    cleaned_text: str
    risk_level: str = "SAFE"
    risk_score: int = 0
    decision_dict: Dict[str, Any]
    execution_time_ms: float
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class HistoryService:
    """Enterprise Pipeline History Persistence & Search Engine."""

    # In-memory history store (production backed by Postgres database model)
    _history_store: Dict[str, ScanHistoryRecord] = {}

    @classmethod
    def compute_sha256(cls, text: str) -> str:
        """Computes SHA-256 hex digest of raw text string."""
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    @classmethod
    def store_scan_history(
        cls,
        scan_id: str,
        request_id: str,
        original_text: str,
        cleaned_text: str,
        decision_dict: Dict[str, Any],
        execution_time_ms: float,
        user_id: Optional[str] = None,
        input_format: str = "TEXT"
    ) -> ScanHistoryRecord:
        """
        Computes SHA-256 input hash and persists scan history record.
        """
        input_hash = cls.compute_sha256(original_text)
        risk_level = decision_dict.get("risk_level", "SAFE")
        risk_score = decision_dict.get("final_scam_probability", 0)

        record = ScanHistoryRecord(
            scan_id=scan_id,
            request_id=request_id,
            user_id=user_id,
            input_hash=input_hash,
            input_format=input_format,
            cleaned_text=cleaned_text,
            risk_level=risk_level,
            risk_score=risk_score,
            decision_dict=decision_dict,
            execution_time_ms=execution_time_ms,
            created_at=datetime.now(timezone.utc).isoformat()
        )

        cls._history_store[scan_id] = record
        return record

    @classmethod
    def get_scan_by_id(cls, scan_id: str) -> Optional[ScanHistoryRecord]:
        """Retrieves a single scan history record by scan_id."""
        return cls._history_store.get(scan_id)

    @classmethod
    def search_history(
        cls,
        user_id: Optional[str] = None,
        query: Optional[str] = None,
        risk_level: Optional[str] = None,
        input_format: Optional[str] = None,
        page: int = 1,
        page_size: int = 10
    ) -> Tuple[List[ScanHistoryRecord], int]:
        """
        Searches scan history with keyword querying, risk level filtering, user isolation, and pagination.
        Returns tuple of (page_records_list, total_count).
        """
        records = list(cls._history_store.values())

        # Filter by User ID if provided
        if user_id:
            records = [r for r in records if r.user_id == user_id]

        # Filter by Risk Level if provided
        if risk_level:
            records = [r for r in records if r.risk_level.upper() == risk_level.upper()]

        # Filter by Input Format if provided
        if input_format:
            records = [r for r in records if r.input_format.upper() == input_format.upper()]

        # Filter by Keyword Query if provided
        if query and query.strip():
            q_lower = query.strip().lower()
            records = [r for r in records if q_lower in r.cleaned_text.lower() or q_lower in r.input_hash]

        total_count = len(records)

        # Sort descending by created_at
        records.sort(key=lambda r: r.created_at, reverse=True)

        # Apply Pagination
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paged_records = records[start_idx:end_idx]

        return paged_records, total_count

    @classmethod
    def delete_scan_history(cls, scan_id: str, user_id: Optional[str] = None) -> bool:
        """
        Deletes a scan history record by scan_id, ensuring user-scope security if user_id provided.
        """
        if scan_id not in cls._history_store:
            return False

        record = cls._history_store[scan_id]
        if user_id and record.user_id != user_id:
            return False # User unauthorized to delete this record

        del cls._history_store[scan_id]
        return True

    @classmethod
    def clear_all(cls) -> None:
        """Clears all records (used for test isolation)."""
        cls._history_store.clear()
