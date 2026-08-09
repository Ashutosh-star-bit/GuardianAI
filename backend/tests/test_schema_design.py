"""
GuardianAI Gemini JSON Schema Design Unit Test Suite
Purpose: Tests validation of complete Gemini JSON output payloads and future compatibility extra key ignoring.
"""

import pytest
from app.nlp.schema_design import GeminiTextThreatAnalysisSchema

def test_gemini_schema_validation_success():
    """Tests parsing complete Gemini text threat analysis JSON payload."""
    payload = {
        "threat_score": 92,
        "risk_band": "dangerous",
        "confidence": 0.984,
        "detected_features": {"urgency_score": 0.85, "link_count": 1},
        "entities": [{"entity_type": "BRAND", "text": "PayPal"}],
        "reasons": ["High urgency smishing payload detected."],
        "risk_indicators": [{"indicator_key": "TYPOSQUATTING", "severity": "Critical", "description": "Spoofed PayPal link"}],
        "explanation": "High risk scam attempt.",
        "psychological_techniques": {
            "urgency": {"detected": True, "intensity": "high", "evidence": "Immediate action required"},
            "fear": {"detected": True, "intensity": "high", "evidence": "Access revoked"},
            "greed": {"detected": False, "intensity": "low", "evidence": ""},
            "authority": {"detected": False, "intensity": "low", "evidence": ""},
            "trust": {"detected": True, "intensity": "critical", "evidence": "Spoofed PayPal brand"},
            "impersonation": {"detected": True, "intensity": "critical", "evidence": "Mimicking PayPal"},
            "social_engineering": {"detected": True, "intensity": "high", "evidence": "Fake account lock"}
        },
        "recommendations": ["Do NOT click the embedded link."]
    }

    model = GeminiTextThreatAnalysisSchema.model_validate(payload)
    assert model.threat_score == 92
    assert model.risk_band == "dangerous"
    assert model.psychological_techniques.urgency.detected is True

def test_future_compatibility_extra_keys_ignored():
    """Tests future compatibility where extra unexpected LLM attributes are safely ignored."""
    payload = {
        "threat_score": 10,
        "risk_band": "safe",
        "confidence": 0.99,
        "explanation": "Safe message.",
        "psychological_techniques": {
            "urgency": {"detected": False, "intensity": "low", "evidence": ""},
            "fear": {"detected": False, "intensity": "low", "evidence": ""},
            "greed": {"detected": False, "intensity": "low", "evidence": ""},
            "authority": {"detected": False, "intensity": "low", "evidence": ""},
            "trust": {"detected": False, "intensity": "low", "evidence": ""},
            "impersonation": {"detected": False, "intensity": "low", "evidence": ""},
            "social_engineering": {"detected": False, "intensity": "low", "evidence": ""}
        },
        "future_v2_feature_flag": "ENABLED_EXTRA_KEY" # Extra key from future LLM version
    }

    model = GeminiTextThreatAnalysisSchema.model_validate(payload)
    assert model.threat_score == 10
    assert not hasattr(model, "future_v2_feature_flag") # Extra key safely ignored
