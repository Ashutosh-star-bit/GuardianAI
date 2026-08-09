"""
GuardianAI Abstract Base Classes & Interfaces for Document Intelligence
Purpose: Defines abstract BaseImagePreprocessor, BaseLayoutAnalyzer, BaseOCREngine, and BaseDocumentProcessor contracts.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple, Optional, Union
from app.document_intel.schemas import DocumentMetadata, OCRResult, LayoutBlock, DocumentAnalysisResult

class BaseImagePreprocessor(ABC):
    """Abstract Base Class for Image Preprocessor Computer Vision Operations."""

    @abstractmethod
    def preprocess_image(self, image_bytes: bytes) -> Tuple[bytes, Dict[str, Any]]:
        """
        Executes grayscale conversion, noise reduction, binarization, deskewing, and rescaling.
        Returns Tuple[preprocessed_bytes, preprocessing_metadata].
        """
        pass

class BaseLayoutAnalyzer(ABC):
    """Abstract Base Class for Spatial Layout Analysis and Document Segmentation."""

    @abstractmethod
    def analyze_layout(self, image_bytes: bytes, width: int, height: int) -> List[LayoutBlock]:
        """
        Analyzes image layout and segments document into spatial bounding box blocks.
        """
        pass

class BaseOCREngine(ABC):
    """Abstract Base Class for OCR Engine Providers (Tesseract, EasyOCR, PaddleOCR, Cloud Vision)."""

    @abstractmethod
    def recognize_text(
        self,
        image_bytes: bytes,
        language: str = "en",
        layout_blocks: Optional[List[LayoutBlock]] = None
    ) -> OCRResult:
        """
        Executes optical character recognition over visual image bytes.
        """
        pass

class BaseDocumentProcessor(ABC):
    """Abstract Base Contract for Master DocumentProcessor Orchestrator."""

    @abstractmethod
    async def process_document(
        self,
        raw_payload: Union[bytes, str],
        filename: Optional[str] = None,
        language: str = "en",
        **kwargs: Any
    ) -> DocumentAnalysisResult:
        """
        Processes document payload through metadata extraction, preprocessing, layout analysis, OCR, and cleaning.
        """
        pass
