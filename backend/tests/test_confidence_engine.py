"""
GuardianAI Statistical Confidence Engine Unit Test Suite
Purpose: Tests weighted multi-source confidence fusion, cross-modal agreement, certainty bands, and dynamic fallback handling.
"""

import pytest
from app.decision_engine.confidence import ConfidenceEngine, ConfidenceAnalysisResult

def test_high_agreement_confidence_fusion():
    """Tests high confidence when Gemini AI and Threat Intel agree closely."""
    res: ConfidenceAnalysisResult = ConfidenceEngine.calculate_confidence(
        gemini_confidence=0.98,
        threat_intel_confidence=0.95,
        pattern_confidence=0.90,
        entity_confidence=0.92
    )

    assert res.overall_confidence >= 0.94
    assert res.cross_modal_agreement >= 0.95
    assert res.certainty_band == "VERY_HIGH"
    assert "Very high confidence" in res.explanation

def test_dynamic_fallback_missing_inputs():
    """Tests dynamic fallback handling when optional inputs are omitted."""
    res = ConfidenceEngine.calculate_confidence(
        gemini_confidence=0.90,
        threat_intel_confidence=0.85
    )

    assert res.overall_confidence > 0.80
    assert res.certainty_band in ["HIGH", "VERY_HIGH"]
    assert res.cross_modal_agreement >= 0.90
