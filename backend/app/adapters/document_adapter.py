"""
GuardianAI Enterprise Document Intelligence Input Adapter
Purpose: Converts raw document bytes, screenshots, or pre-computed DocumentAnalysisResult objects
         into a standardized UniversalAnalysisRequest DTO for the Scam Analysis Pipeline.
"""

from typing import Any, Optional, Union
from app.adapters.base import BaseInputAdapter
from app.adapters.schemas import UniversalAnalysisRequest, AdapterMetadata
from app.document_intel.orchestrator import DocumentProcessor
from app.document_intel.schemas import DocumentAnalysisResult
from app.document_intel.pipeline_adapter import DocumentPipelineAdapter

class DocumentAdapterError(ValueError):
    """Exception raised when document payload adaptation fails."""
    pass

class DocumentAdapter(BaseInputAdapter):
    """Enterprise Document Intelligence Input Adapter."""

    def __init__(self, doc_processor: Optional[DocumentProcessor] = None):
        self.doc_processor = doc_processor or DocumentProcessor()

    async def adapt_to_request(
        self,
        raw_payload: Any,
        user_id: Optional[str] = None,
        language: str = "en",
        source: str = "DOCUMENT_INTEL",
        filename: Optional[str] = None,
        **kwargs: Any
    ) -> UniversalAnalysisRequest:
        """
        Validates document payload, executes DocumentProcessor OCR/Layout pipeline,
        and returns UniversalAnalysisRequest DTO.
        """
        if raw_payload is None:
            raise DocumentAdapterError("Document payload cannot be None")

        # Handle pre-processed DocumentAnalysisResult DTO
        if isinstance(raw_payload, DocumentAnalysisResult):
            return DocumentPipelineAdapter.adapt_to_universal_request(
                doc_result=raw_payload,
                user_id=user_id,
                source=source
            )

        # Handle raw payload bytes or string
        if isinstance(raw_payload, (bytes, str)):
            if len(raw_payload) == 0:
                raise DocumentAdapterError("Document payload cannot be empty")
            
            # Execute Document Processor OCR Engine Pipeline
            doc_result: DocumentAnalysisResult = await self.doc_processor.process_document(
                raw_payload=raw_payload,
                filename=filename or "document.png",
                language=language,
                **kwargs
            )

            return DocumentPipelineAdapter.adapt_to_universal_request(
                doc_result=doc_result,
                user_id=user_id,
                source=source
            )

        raise DocumentAdapterError(f"Unsupported document payload type: {type(raw_payload)}")
