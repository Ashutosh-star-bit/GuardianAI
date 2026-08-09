"""
GuardianAI Risk Classifier Engine Unit Test Suite
Purpose: Tests classification of scores (0-100) into 5 risk tiers (Safe, Low, Medium, High, Critical) with UI colors and icons.
"""

import pytest
from app.decision_engine.risk_classifier import RiskClassifierEngine, RiskLevelDefinition

def test_classify_safe_tier():
    """Tests score 10 yields SAFE risk tier."""
    res: RiskLevelDefinition = RiskClassifierEngine.classify_score(10)
    assert res.level_key == "SAFE"
    assert res.hex_color == "#10B981"
    assert res.icon_svg_name == "shield-check"
    assert "No Scam Threat Detected" in res.user_header_message

def test_classify_low_tier():
    """Tests score 30 yields LOW risk tier."""
    res = RiskClassifierEngine.classify_score(30)
    assert res.level_key == "LOW"
    assert res.hex_color == "#3B82F6"

def test_classify_medium_tier():
    """Tests score 50 yields MEDIUM risk tier."""
    res = RiskClassifierEngine.classify_score(50)
    assert res.level_key == "MEDIUM"
    assert res.hex_color == "#F59E0B"

def test_classify_high_tier():
    """Tests score 70 yields HIGH risk tier."""
    res = RiskClassifierEngine.classify_score(70)
    assert res.level_key == "HIGH"
    assert res.hex_color == "#F97316"

def test_classify_critical_tier():
    """Tests score 95 yields CRITICAL risk tier."""
    res = RiskClassifierEngine.classify_score(95)
    assert res.level_key == "CRITICAL"
    assert res.hex_color == "#EF4444"
    assert res.icon_svg_name == "octagon-alert"
    assert "CRITICAL SCAM WARNING" in res.user_header_message
