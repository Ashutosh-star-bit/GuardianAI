"""
GuardianAI Enterprise Plain Text Input Adapter
Purpose: Validates, cleans, normalizes, and converts raw plain text / SMS / message payloads into a UniversalAnalysisRequest DTO.
"""

import re
from typing import Any, Optional
from app.adapters.base import BaseInputAdapter
from app.adapters.schemas import UniversalAnalysisRequest, AdapterMetadata
from app.nlp.preprocessing import TextPreprocessor

class TextAdapterError(ValueError):
    """Exception raised when plain text payload validation fails."""
    pass

class TextAdapter(BaseInputAdapter):
    """Enterprise Plain Text Input Adapter."""

    MAX_TEXT_LENGTH = 10000

    async def adapt_to_request(
        self,
        raw_payload: Any,
        user_id: Optional[str] = None,
        language: str = "en",
        source: str = "REST_API",
        **kwargs: Any
    ) -> UniversalAnalysisRequest:
        """
        Validates, cleans, and normalizes plain text payload into UniversalAnalysisRequest DTO.
        """
        if raw_payload is None:
            raise TextAdapterError("Text payload cannot be None")

        if not isinstance(raw_payload, str):
            raw_payload = str(raw_payload)

        # 1. Null Byte Control Check
        if "\x00" in raw_payload:
            raise TextAdapterError("Text payload contains illegal null byte character (\\x00)")

        # 2. Length & Empty Check
        stripped = raw_payload.strip()
        if not stripped:
            raise TextAdapterError("Text payload cannot be empty or whitespace only")

        if len(stripped) > self.MAX_TEXT_LENGTH:
            raise TextAdapterError(f"Text payload length ({len(stripped)}) exceeds max limit ({self.MAX_TEXT_LENGTH})")

        # 3. Preprocessing & Homoglyph Deobfuscation
        cleaned_text = TextPreprocessor.clean_text(stripped)
        deobfuscated_text = TextPreprocessor.deobfuscate_homoglyphs(cleaned_text)
        homoglyphs_detected = (cleaned_text != deobfuscated_text)

        # Count extracted URLs
        url_matches = re.findall(r'https?://[^\s]+|www\.[^\s]+', deobfuscated_text, re.IGNORECASE)

        metadata = AdapterMetadata(
            original_format="TEXT",
            mime_type="text/plain",
            file_size_bytes=len(raw_payload.encode('utf-8')),
            extracted_urls_count=len(url_matches),
            extra_attributes={
                "char_count": len(deobfuscated_text),
                "word_count": len(deobfuscated_text.split()),
                "deobfuscated_text": deobfuscated_text,
                "homoglyphs_detected": homoglyphs_detected
            }
        )

        return UniversalAnalysisRequest(
            user_id=user_id,
            input_type="TEXT",
            raw_content=deobfuscated_text,
            metadata=metadata,
            language=language,
            source=source
        )
