"""
GuardianAI Text Intelligence NLP Engine Package
"""

from app.nlp.schemas import (
    FeatureVector,
    DetectedEntity,
    PatternMatch,
    XAIRationale,
    TextIntelligenceResult
)
from app.nlp.preprocessing import TextPreprocessor
from app.nlp.features import FeatureExtractor
from app.nlp.patterns import PatternEngine, PatternDetector
from app.nlp.entities import EntityExtractor
from app.nlp.explainability import ExplainabilityEngine
from app.nlp.multilingual import MultilingualDetector
from app.nlp.llm_bridge import LLMAnalysisBridge
from app.nlp.engine import TextIntelligenceEngine

__all__ = [
    "FeatureVector",
    "DetectedEntity",
    "PatternMatch",
    "XAIRationale",
    "TextIntelligenceResult",
    "TextPreprocessor",
    "FeatureExtractor",
    "PatternEngine",
    "PatternDetector",
    "EntityExtractor",
    "ExplainabilityEngine",
    "MultilingualDetector",
    "LLMAnalysisBridge",
    "TextIntelligenceEngine",
]
