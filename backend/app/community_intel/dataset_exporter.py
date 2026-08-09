"""
GuardianAI RLHF & Fine-Tuning Dataset Exporter
Purpose: Exports verified human-in-the-loop scam feedback datasets into JSONL format
         for fine-tuning Gemini and open LLM models.
"""

import json
from typing import List, Dict, Any
from app.community_intel.schemas import RLHFDatasetItem, AIPredictionFeedbackCreate

class DatasetExporter:
    """Enterprise RLHF Fine-Tuning Dataset Exporter Engine."""

    @classmethod
    def format_to_jsonl(cls, items: List[RLHFDatasetItem]) -> str:
        """Converts list of RLHFDatasetItem DTOs into line-delimited JSONL format."""
        lines = []
        for item in items:
            line_dict = {
                "instruction": item.instruction,
                "input": item.input_text,
                "predicted_label": item.predicted_label,
                "corrected_label": item.actual_label,
                "feedback_type": item.feedback_type,
                "verified_by_moderator": item.verified_by_moderator,
                "confidence": item.confidence,
                "metadata": item.metadata
            }
            lines.append(json.dumps(line_dict, ensure_ascii=False))
        return "\n".join(lines)

    @classmethod
    def create_dataset_item_from_feedback(
        cls,
        feedback: AIPredictionFeedbackCreate,
        input_text: str,
        actual_label: str,
        verified_by_moderator: bool = True
    ) -> RLHFDatasetItem:
        """
        Creates a structured RLHF dataset item from user/moderator feedback.
        """
        return RLHFDatasetItem(
            instruction="Analyze the following message for scam indicators, impersonation vectors, and threat risk levels:",
            input_text=input_text,
            predicted_label=feedback.predicted_risk_level,
            actual_label=actual_label,
            feedback_type=feedback.feedback_type.value,
            verified_by_moderator=verified_by_moderator,
            confidence=0.98,
            metadata={
                "report_id": feedback.report_id,
                "scan_id": feedback.scan_id,
                "correction_reason": feedback.correction_reason,
                "suggested_category": feedback.suggested_category.value if feedback.suggested_category else None
            }
        )
