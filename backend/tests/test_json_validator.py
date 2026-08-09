"""
GuardianAI JSON Validation & Auto-Repair Unit Test Suite
Purpose: Tests clean JSON parsing, syntax auto-repair heuristics (fences, trailing commas, single quotes), and Pydantic schema validation.
"""

import pytest
from pydantic import BaseModel, Field
from app.ai.json_validator import JSONValidationEngine, JSONValidationError

class DemoThreatSchema(BaseModel):
    threat_score: int = Field(ge=0, le=100)
    risk_band: str
    confidence: float

def test_clean_json_parsing():
    """Tests parsing valid clean JSON."""
    raw = '{"threat_score": 85, "risk_band": "dangerous", "confidence": 0.95}'
    model = JSONValidationEngine.validate_and_repair(raw, DemoThreatSchema)
    assert model.threat_score == 85
    assert model.risk_band == "dangerous"

def test_auto_repair_markdown_fences():
    """Tests auto-repair stripping markdown triple backticks."""
    raw = """
    ```json
    {
      "threat_score": 90,
      "risk_band": "dangerous",
      "confidence": 0.98
    }
    ```
    """
    model = JSONValidationEngine.validate_and_repair(raw, DemoThreatSchema)
    assert model.threat_score == 90

def test_auto_repair_trailing_commas():
    """Tests auto-repair removing trailing commas before closing braces."""
    raw = '{"threat_score": 75, "risk_band": "caution", "confidence": 0.90,}'
    model = JSONValidationEngine.validate_and_repair(raw, DemoThreatSchema)
    assert model.threat_score == 75

def test_auto_repair_unquoted_keys():
    """Tests auto-repair fixing unquoted keys."""
    raw = '{threat_score: 80, risk_band: "dangerous", confidence: 0.92}'
    model = JSONValidationEngine.validate_and_repair(raw, DemoThreatSchema)
    assert model.threat_score == 80

def test_schema_validation_error_reporting():
    """Tests detailed error list reporting when required fields are missing."""
    raw = '{"risk_band": "dangerous"}' # Missing threat_score and confidence
    with pytest.raises(JSONValidationError) as exc_info:
        JSONValidationEngine.validate_and_repair(raw, DemoThreatSchema)

    assert "schema validation failed" in exc_info.value.message.lower()
    assert len(exc_info.value.errors) > 0
    fields = [err["field"] for err in exc_info.value.errors]
    assert "threat_score" in fields
    assert "confidence" in fields
