"""
GuardianAI High-Performance PDF Document Input Adapter
Purpose: Fast, zero-external-dependency PDF parser extracting page counts, text streams, metadata (Author/Title),
         handling encrypted PDFs gracefully, and generating UniversalAnalysisRequest DTO.
"""

import re
from typing import Any, Optional, Dict, Union, List
from app.adapters.base import BaseInputAdapter
from app.adapters.schemas import UniversalAnalysisRequest, AdapterMetadata
from app.nlp.preprocessing import TextPreprocessor

class PDFAdapterError(ValueError):
    """Exception raised when PDF document parsing or validation fails."""
    pass

class PDFAdapter(BaseInputAdapter):
    """Enterprise Ultra-Fast PDF Document Input Adapter."""

    MAX_PDF_BYTES = 15 * 1024 * 1024  # 15 MB limit

    async def adapt_to_request(
        self,
        raw_payload: Union[bytes, str],
        user_id: Optional[str] = None,
        language: str = "en",
        source: str = "REST_API",
        **kwargs: Any
    ) -> UniversalAnalysisRequest:
        """
        Parses raw PDF bytes or file path into standardized UniversalAnalysisRequest DTO.
        """
        if raw_payload is None:
            raise PDFAdapterError("PDF payload cannot be None")

        # 1. Resolve PDF Bytes
        if isinstance(raw_payload, bytes):
            pdf_bytes = raw_payload
        elif isinstance(raw_payload, str):
            try:
                with open(raw_payload, "rb") as f:
                    pdf_bytes = f.read()
            except Exception:
                raise PDFAdapterError(f"Unable to read PDF file at path '{raw_payload}'")
        else:
            raise PDFAdapterError("PDF payload must be bytes or a valid file path string")

        if len(pdf_bytes) == 0:
            raise PDFAdapterError("PDF file payload is empty (0 bytes)")

        if len(pdf_bytes) > self.MAX_PDF_BYTES:
            raise PDFAdapterError(f"PDF size ({len(pdf_bytes)} bytes) exceeds maximum limit ({self.MAX_PDF_BYTES} bytes)")

        # 2. Header Signature Validation
        if not pdf_bytes.startswith(b"%PDF-"):
            raise PDFAdapterError("Invalid or corrupted PDF file structure: Missing %PDF header signature")

        # 3. Graceful Encrypted PDF Check
        if b"/Encrypt" in pdf_bytes or b"/Filter/Standard" in pdf_bytes:
            raise PDFAdapterError("Encrypted PDF document: Password required to unlock content")

        # 4. Page Count Calculation
        page_matches = re.findall(rb'/Type\s*/Page\b', pdf_bytes)
        page_count = max(len(page_matches), 1)

        # 5. Fast Text Extraction from PDF Streams
        text_chunks: List[str] = []
        # Find stream content between BT (Begin Text) and ET (End Text)
        bt_et_matches = re.findall(rb'BT(.*?)ET', pdf_bytes, re.DOTALL)
        for chunk in bt_et_matches:
            # Find parenthesized string literals (Text)
            str_matches = re.findall(rb'\((.*?)\)', chunk)
            for s in str_matches:
                try:
                    decoded = s.decode('latin-1', errors='ignore')
                    if len(decoded.strip()) > 1:
                        text_chunks.append(decoded)
                except Exception:
                    continue

        raw_extracted_text = " ".join(text_chunks).strip()
        cleaned_text = TextPreprocessor.clean_text(raw_extracted_text) if raw_extracted_text else f"(PDF Document - {page_count} Pages)"

        # 6. Extract Metadata (Title, Author, Producer)
        title = self._extract_pdf_meta_field(pdf_bytes, b"/Title")
        author = self._extract_pdf_meta_field(pdf_bytes, b"/Author")
        creator = self._extract_pdf_meta_field(pdf_bytes, b"/Creator")

        metadata = AdapterMetadata(
            original_format="PDF",
            mime_type="application/pdf",
            file_size_bytes=len(pdf_bytes),
            sender_info=author,
            extracted_urls_count=0,
            extra_attributes={
                "page_count": page_count,
                "title": title,
                "author": author,
                "creator": creator
            }
        )

        return UniversalAnalysisRequest(
            user_id=user_id,
            input_type="PDF",
            raw_content=cleaned_text,
            metadata=metadata,
            language=language,
            source=source
        )

    def _extract_pdf_meta_field(self, data: bytes, key: bytes) -> Optional[str]:
        """Helper to extract PDF metadata string fields."""
        try:
            match = re.search(key + rb'\s*\((.*?)\)', data)
            if match:
                return match.group(1).decode('latin-1', errors='ignore')
        except Exception:
            pass
        return None
