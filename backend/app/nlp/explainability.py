"""
GuardianAI Explainability (XAI) Engine
Purpose: Generates plain-language rationale summaries, manipulation tactics breakdown, and actionable safety advice.
"""

from typing import List
from app.nlp.schemas import FeatureVector, PatternMatch, DetectedEntity, XAIRationale

class ExplainabilityEngine:
    """Generates non-technical plain language XAI explanations for end-users."""

    @classmethod
    def generate_rationale(
        cls,
        features: FeatureVector,
        patterns: List[PatternMatch],
        entities: List[DetectedEntity]
    ) -> XAIRationale:
        """Synthesizes extracted features, pattern matches, and entities into a human-readable explanation."""
        tactics: List[str] = []

        if features.urgency_score > 0.4:
            tactics.append("Artificial Urgency & Pressure Tactics")

        if features.financial_coercion_score > 0.4:
            tactics.append("Financial Coercion / Money Request")

        if features.homoglyph_detected or any(p.pattern_name for p in patterns if "Spoof" in p.pattern_name):
            tactics.append("Brand Impersonation & Typosquatting Link")

        for p in patterns:
            if p.category not in tactics:
                tactics.append(p.category.replace("_", " ").title())

        # Construct Plain Language Summary
        if not tactics:
            plain_summary = "No suspicious coercion or manipulation patterns were detected in this message."
            advice = "You can safely review this message."
        else:
            tactic_str = ", ".join(tactics)
            plain_summary = f"High risk scam indicator detected. Message employs {tactic_str} to manipulate user action."
            advice = "Do NOT click any embedded links or send payments. Independently contact the organization using their official website."

        return XAIRationale(
            plain_summary=plain_summary,
            manipulation_tactics=tactics,
            actionable_advice=advice
        )
