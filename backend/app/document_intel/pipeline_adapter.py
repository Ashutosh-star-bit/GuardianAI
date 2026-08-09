"""
GuardianAI Document Pipeline Adapter
Purpose: Converts DocumentAnalysisResult DTO into UniversalAnalysisRequest DTO for ScamAnalysisPipeline consumption.
"""

from typing import Optional
from app.adapters.schemas import UniversalAnalysisRequest, AdapterMetadata, AttachmentMetadata
from app.document_intel.schemas import DocumentAnalysisResult

class DocumentPipelineAdapter:
    """Converts Document Analysis outputs into standard UniversalAnalysisRequest DTO."""

    @classmethod
    def adapt_to_universal_request(
        cls,
        doc_result: DocumentAnalysisResult,
        user_id: Optional[str] = None,
        source: str = "DOCUMENT_INTEL"
    ) -> UniversalAnalysisRequest:
        """
        Transforms DocumentAnalysisResult DTO into UniversalAnalysisRequest DTO.
        """
        metadata = AdapterMetadata(
            original_format=doc_result.metadata.file_format,
            mime_type=doc_result.metadata.mime_type,
            file_size_bytes=doc_result.metadata.file_size_bytes,
            sender_info=doc_result.metadata.filename,
            extracted_urls_count=0,
            extra_attributes={
                "doc_id": doc_result.doc_id,
                "width": doc_result.metadata.width,
                "height": doc_result.metadata.height,
                "dpi": doc_result.metadata.dpi,
                "page_count": doc_result.metadata.page_count,
                "script_type": doc_result.script_type,
                "layout_block_count": len(doc_result.layout_blocks),
                "ocr_confidence": doc_result.ocr_result.confidence
            }
        )

        return UniversalAnalysisRequest(
            user_id=user_id,
            input_type=doc_result.metadata.file_format if doc_result.metadata.file_format in ["PDF", "IMAGE"] else "IMAGE",
            raw_content=doc_result.cleaned_text or doc_result.raw_extracted_text,
            metadata=metadata,
            language=doc_result.detected_language,
            source=source
        )
