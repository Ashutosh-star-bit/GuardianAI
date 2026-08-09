"""
GuardianAI Text Intelligence Engine Unit Test Suite
Purpose: Tests Preprocessing, Feature Extraction, Pattern Detection across 7 Scam Vectors, Entity Extractor, XAI Rationale, and Pipeline Orchestrator.
"""

import pytest
from app.nlp import (
    TextPreprocessor,
    FeatureExtractor,
    PatternDetector,
    EntityExtractor,
    ExplainabilityEngine,
    MultilingualDetector,
    TextIntelligenceEngine
)

def test_preprocessing_homoglyphs():
    """Tests homoglyph deobfuscation (P@ypal -> paypal)."""
    raw = "URGENT: P@ypal account locked! Update at paypa1-check.com"
    deobfuscated = TextPreprocessor.deobfuscate_homoglyphs(raw)
    assert "paypal" in deobfuscated.lower()

def test_feature_extraction():
    """Tests quantitative feature metrics extraction."""
    text = "URGENT ACTION REQUIRED! Transfer $500 immediately to account."
    features = FeatureExtractor.extract_features(text)
    assert features.urgency_score > 0.3
    assert features.financial_coercion_score > 0.3
    assert features.caps_ratio > 0.2

def test_pattern_detection_categories():
    """Tests pattern recognition across scam vectors (Bank, Job, Courier, Lottery)."""
    text_bank = "Your bank account is suspended. Update your kyc immediately."
    matches_bank = PatternDetector.detect_patterns(text_bank)
    assert any(m.category == "BANK_SPOOF" for m in matches_bank)

    text_job = "Work from home part-time and earn $500 daily income."
    matches_job = PatternDetector.detect_patterns(text_job)
    assert any(m.category == "JOB_SCAM" for m in matches_job)

    text_courier = "Your parcel delivery is pending. Pay unpaid customs fee."
    matches_courier = PatternDetector.detect_patterns(text_courier)
    assert any(m.category == "COURIER_SCAM" for m in matches_courier)

def test_entity_extractor():
    """Tests Named Entity Extraction for Brands, Money, Phones, and URLs."""
    text = "Contact PayPal support at +1-800-555-0199 or send $250 to http://paypa1-verify.com"
    entities = EntityExtractor.extract_entities(text)
    types = [e.entity_type for e in entities]
    assert "BRAND" in types
    assert "MONEY" in types
    assert "PHONE" in types
    assert "URL" in types

def test_explainability_engine():
    """Tests XAI rationale generation."""
    features = FeatureExtractor.extract_features("URGENT: Transfer $1000 now!")
    patterns = PatternDetector.detect_patterns("URGENT: Transfer $1000 now!")
    entities = EntityExtractor.extract_entities("URGENT: Transfer $1000 now!")

    rationale = ExplainabilityEngine.generate_rationale(features, patterns, entities)
    assert len(rationale.manipulation_tactics) > 0
    assert rationale.actionable_advice is not None

def test_multilingual_detector():
    """Tests language detection (English vs Spanish)."""
    assert MultilingualDetector.detect_language("Your account is locked") == "en"
    assert MultilingualDetector.detect_language("Su cuenta de banco está bloqueada urgente") == "es"

def test_text_intelligence_engine_orchestrator():
    """Tests end-to-end TextIntelligenceEngine pipeline execution."""
    res = TextIntelligenceEngine.analyze_text(
        scan_id="scn_nlp_101",
        raw_text="URGENT: Your PayPal account is suspended. Verify at http://paypa1-check.com",
        channel_type="SMS"
    )
    assert res.scan_id == "scn_nlp_101"
    assert res.channel_type == "SMS"
    assert res.features.urgency_score > 0.0
    assert len(res.entities) > 0
    assert res.explainability.plain_summary is not None
