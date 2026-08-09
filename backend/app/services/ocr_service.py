"""
GuardianAI Enterprise OCRService Subsystem
Purpose: High-level Service Layer orchestrating the complete 7-stage Document Intelligence OCR Pipeline:
         1. Receive Document -> 2. Image Preprocessing -> 3. OCR Text & Spatial Bounding Box Extraction ->
         4. Text Cleaning -> 5. Language & Script Detection -> 6. Generate UniversalAnalysisRequest -> 7. Return Result DTO.
"""

import time
from typing import Optional, Union, Dict, Any
from pydantic import BaseModel, Field

from app.adapters.schemas import UniversalAnalysisRequest
from app.document_intel.orchestrator import DocumentProcessor
from app.document_intel.schemas import DocumentAnalysisResult
from app.document_intel.pipeline_adapter import DocumentPipelineAdapter
from app.document_intel.exceptions import DocumentIntelligenceError

class OCRServiceResult(BaseModel):
    """Result DTO returned by OCRService containing Document & Pipeline objects."""
    document_result: DocumentAnalysisResult
    analysis_request: UniversalAnalysisRequest
    processing_time_ms: float = Field(ge=0.0)

class OCRServiceError(ValueError):
    """Exception raised when OCRService execution fails."""
    pass

class OCRService:
    """Enterprise High-Level OCR Service Layer Engine."""

    def __init__(self, doc_processor: Optional[DocumentProcessor] = None):
        self.doc_processor = doc_processor or DocumentProcessor()

    async def process_document_pipeline(
        self,
        raw_payload: Union[bytes, str],
        filename: Optional[str] = None,
        user_id: Optional[str] = None,
        language: str = "en",
        source: str = "OCR_SERVICE",
        **kwargs: Any
    ) -> OCRServiceResult:
        """
        Executes end-to-end OCR processing pipeline:
        Receive -> Preprocess -> OCR -> Clean -> Detect Language -> Generate AnalysisRequest -> Return Result.
        """
        if raw_payload is None:
            raise OCRServiceError("Document payload cannot be None")

        start_time = time.perf_counter()

        try:
            # 1. Execute Document Processor (Preprocess -> OCR -> Clean -> Language)
            doc_result: DocumentAnalysisResult = await self.doc_processor.process_document(
                raw_payload=raw_payload,
                filename=filename or "document.png",
                language=language,
                **kwargs
            )

            # 2. Generate UniversalAnalysisRequest DTO
            analysis_req: UniversalAnalysisRequest = DocumentPipelineAdapter.adapt_to_universal_request(
                doc_result=doc_result,
                user_id=user_id,
                source=source
            )

            elapsed_ms = (time.perf_counter() - start_time) * 1000.0

            return OCRServiceResult(
                document_result=doc_result,
                analysis_request=analysis_req,
                processing_time_ms=elapsed_ms
            )
        except DocumentIntelligenceError as die:
            raise OCRServiceError(f"Document Intelligence processing failed: {str(die)}")
        except Exception as e:
            raise OCRServiceError(f"Unexpected OCRService failure: {str(e)}")
