"""
GuardianAI Document Intelligence Module Package
Purpose: Public exports for DocumentProcessor, MetadataExtractor, ImagePreprocessor, LayoutAnalyzer, OCRProcessor, and DTO Schemas.
"""

from app.document_intel.orchestrator import DocumentProcessor
from app.document_intel.preprocessor import ImagePreprocessor
from app.document_intel.layout_analyzer import LayoutAnalyzer
from app.document_intel.ocr_processor import OCRProcessor
from app.document_intel.metadata_extractor import MetadataExtractor
from app.document_intel.text_cleaner import TextCleaner
from app.document_intel.language_detector import LanguageDetector
from app.document_intel.pipeline_adapter import DocumentPipelineAdapter
from app.document_intel.schemas import (
    DocumentAnalysisResult,
    DocumentMetadata,
    LayoutBlock,
    BoundingBox,
    OCRResult
)

__all__ = [
    "DocumentProcessor",
    "ImagePreprocessor",
    "LayoutAnalyzer",
    "OCRProcessor",
    "MetadataExtractor",
    "TextCleaner",
    "LanguageDetector",
    "DocumentPipelineAdapter",
    "DocumentAnalysisResult",
    "DocumentMetadata",
    "LayoutBlock",
    "BoundingBox",
    "OCRResult"
]
