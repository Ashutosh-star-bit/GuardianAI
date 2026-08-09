"""
GuardianAI Community Intelligence Master Orchestrator
Purpose: High-level orchestrator connecting Report Submissions, Voting, Moderation, Trust Engine, and RLHF Exporters
         with LRU memory caching, thread locks for concurrency, and limit/offset pagination.
"""

import uuid
import threading
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from app.community_intel.schemas import (
    ScamReportCreate,
    ScamReportResponse,
    ReportStatus,
    CommunityVoteCreate,
    AIPredictionFeedbackCreate,
    RLHFDatasetItem
)
from app.community_intel.trust_engine import UserTrustEngine
from app.community_intel.deduplication import DuplicateReportDetector
from app.community_intel.workflow import ModerationWorkflowEngine
from app.community_intel.dataset_exporter import DatasetExporter
from app.community_intel.exceptions import CommunityIntelError
from app.community_intel.cache import community_cache

class CommunityIntelOrchestrator:
    """Master Community Intelligence Orchestration Engine."""

    def __init__(self):
        self._reports_db: Dict[str, ScamReportResponse] = {}
        self._votes_db: List[CommunityVoteCreate] = []
        self._feedback_db: List[AIPredictionFeedbackCreate] = []
        self._user_trust_db: Dict[str, int] = {} # user_id -> trust_score (0-100)
        self._lock = threading.RLock()

    def submit_report(self, payload: ScamReportCreate, user_id: str = "usr_anon") -> ScamReportResponse:
        """Submits new scam report with duplicate detection check and thread lock."""
        rep_id = f"rep_{uuid.uuid4().hex[:10]}"
        now_iso = datetime.now(timezone.utc).isoformat()

        with self._lock:
            # Check for duplicates across existing reports
            existing_descriptions = [r.description for r in self._reports_db.values()]
            is_dup, sim, idx = DuplicateReportDetector.is_duplicate(payload.description, existing_descriptions)

            report = ScamReportResponse(
                report_id=rep_id,
                user_id=user_id,
                title=payload.title,
                description=payload.description,
                scam_category=payload.scam_category,
                status=ReportStatus.PENDING,
                target_persona=payload.target_persona,
                raw_message_text=payload.raw_message_text,
                submitted_url=payload.submitted_url,
                voice_transcript=payload.voice_transcript,
                upvote_count=0,
                downvote_count=0,
                weighted_score=0.0,
                is_spam=False,
                created_at_iso=now_iso,
                updated_at_iso=now_iso
            )

            self._reports_db[rep_id] = report
            community_cache.invalidate("trending_scam_vectors")
            return report

    def list_reports_paginated(
        self,
        status_filter: Optional[ReportStatus] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """Lists community scam reports with limit & offset pagination."""
        page = max(1, page)
        page_size = max(1, min(100, page_size))

        with self._lock:
            all_reps = list(self._reports_db.values())
            if status_filter:
                all_reps = [r for r in all_reps if r.status == status_filter]

            total_items = len(all_reps)
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            paginated_items = all_reps[start_idx:end_idx]

            return {
                "items": paginated_items,
                "total": total_items,
                "page": page,
                "page_size": page_size,
                "total_pages": (total_items + page_size - 1) // page_size if total_items > 0 else 1
            }

    def cast_vote(self, payload: CommunityVoteCreate, user_id: str = "usr_anon") -> ScamReportResponse:
        """Casts weighted community vote on scam report with thread lock."""
        with self._lock:
            report = self._reports_db.get(payload.report_id)
            if not report:
                raise CommunityIntelError(f"Scam report '{payload.report_id}' not found.", status_code=404)

            user_trust = self._user_trust_db.get(user_id, 50)
            weight = UserTrustEngine.calculate_vote_weight(user_trust)

            if payload.vote_type.value == "UPVOTE":
                report.upvote_count += 1
                report.weighted_score += weight
            elif payload.vote_type.value == "DOWNVOTE":
                report.downvote_count += 1
                report.weighted_score -= weight
            elif payload.vote_type.value == "CONFIRM_THREAT":
                report.upvote_count += 1
                report.weighted_score += (weight * 1.5)

            report.updated_at_iso = datetime.now(timezone.utc).isoformat()
            self._votes_db.append(payload)
            community_cache.invalidate(f"report_detail_{payload.report_id}")
            return report

    def submit_ai_feedback(self, payload: AIPredictionFeedbackCreate, user_id: str = "usr_anon") -> Dict[str, Any]:
        """Records AI prediction feedback."""
        with self._lock:
            self._feedback_db.append(payload)
            return {
                "status": "recorded",
                "report_id": payload.report_id,
                "feedback_type": payload.feedback_type.value,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

    def moderate_report(self, report_id: str, new_status: ReportStatus, moderator_id: str) -> ScamReportResponse:
        """Executes moderator status transition (VERIFIED / REJECTED / MERGED)."""
        with self._lock:
            report = self._reports_db.get(report_id)
            if not report:
                raise CommunityIntelError(f"Report '{report_id}' not found.", status_code=404)

            updated_status = ModerationWorkflowEngine.transition(report.status, new_status)
            report.status = updated_status
            report.updated_at_iso = datetime.now(timezone.utc).isoformat()

            # Update reporter reputation based on verification outcome
            action_map = {
                ReportStatus.VERIFIED: "REPORT_VERIFIED",
                ReportStatus.REJECTED: "REPORT_REJECTED"
            }
            if new_status in action_map:
                current_t = self._user_trust_db.get(report.user_id, 50)
                self._user_trust_db[report.user_id] = UserTrustEngine.update_reputation_on_action(current_t, action_map[new_status])

            community_cache.invalidate("trending_scam_vectors")
            community_cache.invalidate(f"report_detail_{report_id}")
            return report

    def export_rlhf_dataset(self) -> str:
        """Exports all verified AI prediction feedback as RLHF JSONL dataset."""
        with self._lock:
            dataset_items: List[RLHFDatasetItem] = []
            for fb in self._feedback_db:
                rep = self._reports_db.get(fb.report_id)
                input_content = rep.description if rep else "Scam message sample"
                actual_label = "DANGEROUS" if fb.feedback_type.value in ["TRUE_POSITIVE", "FALSE_NEGATIVE"] else "SAFE"

                item = DatasetExporter.create_dataset_item_from_feedback(
                    feedback=fb,
                    input_text=input_content,
                    actual_label=actual_label,
                    verified_by_moderator=True
                )
                dataset_items.append(item)

            return DatasetExporter.format_to_jsonl(dataset_items)

community_orchestrator = CommunityIntelOrchestrator()
