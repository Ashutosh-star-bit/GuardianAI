"""
GuardianAI LLM Analysis Bridge
Purpose: Formats extracted preprocessing features, pattern matches, and entities into structured prompts for Gemini 3.6 Flash High.
"""

from typing import Dict, Any, List
from app.nlp.schemas import FeatureVector, PatternMatch, DetectedEntity

class LLMAnalysisBridge:
    """Formats NLP extracted metadata for LLM prompt context."""

    @staticmethod
    def build_llm_prompt_context(
        raw_text: str,
        channel_type: str,
        features: FeatureVector,
        patterns: List[PatternMatch],
        entities: List[DetectedEntity]
    ) -> Dict[str, Any]:
        """Bundles NLP analysis features into a dictionary for AIService execution."""
        pattern_summaries = [f"{p.category}: {p.pattern_name} ('{p.matched_text}')" for p in patterns]
        entity_summaries = [f"{e.entity_type}: {e.text}" for e in entities]

        return {
            "channel_type": channel_type,
            "raw_content": raw_text,
            "urgency_score": features.urgency_score,
            "financial_score": features.financial_coercion_score,
            "caps_ratio": features.caps_ratio,
            "link_count": features.link_count,
            "detected_patterns": pattern_summaries,
            "detected_entities": entity_summaries
        }
