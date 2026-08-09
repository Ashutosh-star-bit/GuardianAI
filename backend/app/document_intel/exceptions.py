"""
GuardianAI Document Intelligence Exception Hierarchy
Purpose: Defines custom domain exceptions for document processing, pre-processing, layout analysis, and OCR provider failures.
"""

class DocumentIntelligenceError(ValueError):
    """Base exception for all Document Intelligence errors."""
    pass

class ImagePreprocessingError(DocumentIntelligenceError):
    """Exception raised when computer vision image pre-processing fails."""
    pass

class OCREngineError(DocumentIntelligenceError):
    """Exception raised when OCR provider engine fails or returns invalid text."""
    pass

class LayoutAnalysisError(DocumentIntelligenceError):
    """Exception raised when visual layout block analysis or bounding box extraction fails."""
    pass

class DocumentMetadataExtractionError(DocumentIntelligenceError):
    """Exception raised when metadata or EXIF extraction fails."""
    pass
