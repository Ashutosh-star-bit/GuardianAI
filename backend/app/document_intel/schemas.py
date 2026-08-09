"""
GuardianAI Document Intelligence DTO Schemas
Purpose: Standardized Pydantic v2 models for spatial BoundingBoxes, LayoutBlocks, DocumentMetadata, and DocumentAnalysisResult.
"""

import uuid
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class BoundingBox(BaseModel):
    """Spatial bounding box coordinates normalized to image width/height (0.0 to 1.0) or pixels."""
    xmin: float = Field(ge=0.0)
    ymin: float = Field(ge=0.0)
    xmax: float = Field(ge=0.0)
    ymax: float = Field(ge=0.0)
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)

class LayoutBlock(BaseModel):
    """Segmented visual document block (e.g. Header, Paragraph, Table, Logo, Footer)."""
    block_id: str = Field(default_factory=lambda: f"blk_{uuid.uuid4().hex[:8]}")
    block_type: str = Field(default="PARAGRAPH", description="HEADER, PARAGRAPH, TABLE, FOOTER, LOGO, QR_CODE")
    bounding_box: BoundingBox
    raw_text: str = Field(default="")
    confidence: float = Field(default=0.9, ge=0.0, le=1.0)

class DocumentMetadata(BaseModel):
    """Extracted file and visual image attributes metadata."""
    filename: Optional[str] = None
    file_format: str = Field(description="PNG, JPEG, WEBP, GIF, PDF")
    mime_type: str
    file_size_bytes: int = Field(ge=0)
    width: int = Field(default=1024, ge=1)
    height: int = Field(default=768, ge=1)
    dpi: int = Field(default=72, ge=1)
    page_count: int = Field(default=1, ge=1)
    has_exif: bool = Field(default=False)
    exif_orientation: int = Field(default=1)
    extra_meta: Dict[str, Any] = Field(default_factory=dict)

class OCRResult(BaseModel):
    """Raw OCR Engine output object."""
    engine_name: str = Field(default="MOCK_OCR_STUB")
    raw_text: str
    cleaned_text: str
    confidence: float = Field(default=0.95, ge=0.0, le=1.0)
    blocks: List[LayoutBlock] = Field(default_factory=list)
    word_count: int = Field(default=0)

class DocumentAnalysisResult(BaseModel):
    """Master Document Intelligence Processing Result DTO."""
    doc_id: str = Field(default_factory=lambda: f"doc_{uuid.uuid4().hex[:10]}")
    metadata: DocumentMetadata
    raw_extracted_text: str
    cleaned_text: str
    detected_language: str = Field(default="en", description="ISO-639 language code")
    script_type: str = Field(default="LATIN", description="LATIN, DEVANAGARI, CYRILLIC")
    ocr_result: OCRResult
    layout_blocks: List[LayoutBlock] = Field(default_factory=list)
    processing_time_ms: float = Field(ge=0.0)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
