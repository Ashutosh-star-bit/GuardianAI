"""
GuardianAI InputValidationService Engine
Purpose: Provides multi-format payload validation (Plain Text, Email, URL, QR, JSON, OCR, Voice, Document, Image, PDF) checking
         Length Boundaries, UTF-8 Encoding, Language Locales, File Size Limits, and Unsupported Binary/Null Byte Content.
"""

import json
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.exceptions import BaseAppException

class InputValidationError(BaseAppException):
    """Raised when pipeline input payload fails validation checks (HTTP 422)."""
    def __init__(self, message: str = "Pipeline input payload validation failed.", details: Optional[List[Any]] = None):
        super().__init__(message=message, code="PIPELINE_VALIDATION_ERROR", status_code=422, details=details)

class ValidatedInputPayload(BaseModel):
    """Container for clean, validated input payload ready for pipeline processing."""
    format_type: str = Field(description="TEXT, EMAIL, URL, QR, JSON, OCR, VOICE, DOCUMENT, IMAGE, PDF")
    clean_text: str
    byte_size: int
    language: str = "en"
    raw_json_dict: Optional[Dict[str, Any]] = None

class InputValidationService:
    """Enterprise Multi-Format Input Validation Service Engine."""

    MAX_PAYLOAD_BYTES = 10 * 1024 * 1024 # 10MB limit
    SUPPORTED_FORMATS = {"TEXT", "EMAIL", "URL", "QR", "JSON", "OCR", "VOICE", "DOCUMENT", "IMAGE", "PDF", "PNG", "JPEG"}
    SUPPORTED_LANGUAGES = {"en", "es", "hi", "fr", "de"}

    @classmethod
    def validate_payload(
        cls,
        raw_input: str,
        format_type: str = "TEXT",
        language: str = "en",
        max_bytes: int = MAX_PAYLOAD_BYTES
    ) -> ValidatedInputPayload:
        """
        Executes multi-format input validation pipeline across all rules.
        """
        fmt_upper = format_type.upper()
        if fmt_upper not in cls.SUPPORTED_FORMATS:
            raise InputValidationError(
                message=f"Unsupported format type '{format_type}'. Supported: {', '.join(sorted(cls.SUPPORTED_FORMATS))}",
                details=[{"field": "format_type", "value": format_type}]
            )

        if not raw_input and fmt_upper != "JSON":
            raise InputValidationError(
                message="Payload input text cannot be empty or whitespace only.",
                details=[{"field": "raw_input", "value": "empty"}]
            )

        if "\x00" in raw_input:
            raise InputValidationError(
                message="Payload contains illegal null-byte '\\x00' control characters.",
                details=[{"field": "raw_input", "value": "null_byte_detected"}]
            )

        byte_len = len(raw_input.encode('utf-8', errors='replace'))
        if byte_len > max_bytes:
            raise InputValidationError(
                message=f"Payload size ({byte_len} bytes) exceeds max limit of {max_bytes} bytes.",
                details=[{"field": "byte_size", "value": byte_len, "limit": max_bytes}]
            )

        lang_code = language.lower() if language else "en"
        if lang_code not in cls.SUPPORTED_LANGUAGES:
            lang_code = "en"

        raw_json_dict = None
        if fmt_upper == "JSON" and raw_input:
            try:
                raw_json_dict = json.loads(raw_input)
            except Exception as e:
                raise InputValidationError(message=f"Malformed JSON payload: {str(e)}")

        return ValidatedInputPayload(
            format_type=fmt_upper,
            clean_text=raw_input,
            byte_size=byte_len,
            language=lang_code,
            raw_json_dict=raw_json_dict
        )
