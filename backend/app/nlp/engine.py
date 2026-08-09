"""
GuardianAI Text Intelligence Engine Orchestrator
Purpose: Orchestrates Text Preprocessing, Feature Extraction, Pattern Detection, Entity Extraction,
         Multilingual Detection, and Explainability Rationale generation into a unified TextIntelligenceResult DTO.
"""

from typing import Optional
from app.nlp.preprocessing import TextPreprocessor
from app.nlp.features import FeatureExtractor
from app.nlp.patterns import PatternDetector
from app.nlp.entities import EntityExtractor
from app.nlp.explainability import ExplainabilityEngine
from app.nlp.multilingual import MultilingualDetector
from app.nlp.schemas import TextIntelligenceResult, PatternMatch

class TextIntelligenceEngine:
    """Master Text Intelligence Pipeline Orchestrator."""

    @classmethod
    def analyze_text(
        cls,
        scan_id: str,
        raw_text: str,
        channel_type: str = "SMS"
    ) -> TextIntelligenceResult:
        """
        Executes complete NLP Text Intelligence Pipeline:
        1. Normalizes and deobfuscates text payload
        2. Detects language locale
        3. Extracts quantitative feature metrics
        4. Detects scam vector patterns across 7 categories
        5. Extracts named entities (Brands, Money, Phones, URLs)
        6. Generates Explainability (XAI) rationale
        """
        # 1. Preprocessing
        clean_text = TextPreprocessor.clean_text(raw_text)
        deobfuscated_text = TextPreprocessor.deobfuscate_homoglyphs(clean_text)

        # 2. Multilingual Detection
        lang = MultilingualDetector.detect_language(clean_text)

        # 3. Feature Extraction
        features = FeatureExtractor.extract_features(deobfuscated_text)

        # 4. Pattern Detection across 7 Categories
        raw_patterns = PatternDetector.detect_patterns(deobfuscated_text)
        patterns = [
            PatternMatch(
                category=p.category,
                pattern_name=p.pattern_name,
                matched_text=p.matched_text,
                severity=p.severity
            ) for p in raw_patterns
        ]

        # 5. Named Entity Recognition (NER)
        entities = EntityExtractor.extract_entities(clean_text)

        # Determine Scam Category Hint
        scam_hint = patterns[0].category if patterns else "GENERIC_FRAUD"

        # 6. Explainability (XAI) Rationale
        rationale = ExplainabilityEngine.generate_rationale(
            features=features,
            patterns=patterns,
            entities=entities
        )

        return TextIntelligenceResult(
            scan_id=scan_id,
            channel_type=channel_type,
            scam_category_hint=scam_hint,
            features=features,
            entities=entities,
            patterns=patterns,
            explainability=rationale,
            language=lang
        )
