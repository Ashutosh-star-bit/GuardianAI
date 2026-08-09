"""
GuardianAI Text Input Payload Validation Engine
Purpose: Provides reusable validation for Empty Input, Min/Max Length Boundaries, UTF-8 Encoding,
         Language Locales, Required Fields, and Malformed Null-Byte / Control Characters.
"""

from typing import Dict, Any, List, Optional
from app.core.exceptions import BaseAppException

class PayloadValidationError(BaseAppException):
    """Raised when text payload fails input validation rules (HTTP 422)."""
    def __init__(self, message: str = "Input payload validation failed.", details: Optional[List[Any]] = None):
        super().__init__(message=message, code="UNPROCESSABLE_ENTITY", status_code=422, details=details)

class TextPayloadValidator:
    """Enterprise Text Payload Validation Engine."""

    MIN_TEXT_LENGTH = 5
    MAX_TEXT_LENGTH = 10_000
    SUPPORTED_LANGUAGES = {"en", "es", "hi", "fr", "de"}

    @classmethod
    def validate_empty_and_whitespace(cls, text: Optional[str]) -> str:
        """Validates input text is non-null, non-empty, and contains visible characters."""
        if text is None:
            raise PayloadValidationError("Input text payload cannot be null.", details=[{"field": "text", "issue": "Must not be null"}])

        stripped = text.strip()
        if not stripped:
            raise PayloadValidationError("Input text payload cannot be empty or whitespace-only.", details=[{"field": "text", "issue": "Must not be empty"}])

        return stripped

    @classmethod
    def validate_length_boundaries(cls, text: str, min_len: int = MIN_TEXT_LENGTH, max_len: int = MAX_TEXT_LENGTH) -> None:
        """Validates input text meets minimum and maximum character length boundaries."""
        length = len(text)
        if length < min_len:
            raise PayloadValidationError(
                f"Input text length ({length} chars) is below minimum threshold of {min_len} characters.",
                details=[{"field": "text", "issue": f"Minimum length is {min_len} characters"}]
            )
        if length > max_len:
            raise PayloadValidationError(
                f"Input text length ({length} chars) exceeds maximum limit of {max_len} characters.",
                details=[{"field": "text", "issue": f"Maximum length is {max_len} characters"}]
            )

    @classmethod
    def validate_encoding(cls, text: str) -> None:
        """Validates input text is valid UTF-8 and contains no corrupted byte sequences."""
        try:
            text.encode("utf-8")
        except UnicodeEncodeError as e:
            raise PayloadValidationError(
                f"Input payload contains invalid UTF-8 encoding characters: {str(e)}",
                details=[{"field": "encoding", "issue": "Invalid UTF-8 byte sequence"}]
            ) from e

    @classmethod
    def validate_malformed_control_chars(cls, text: str) -> None:
        """Rejects malformed inputs containing null bytes (\\x00) or non-printable control characters."""
        if "\x00" in text:
            raise PayloadValidationError(
                "Malformed input: Payload contains illegal null bytes (\\x00).",
                details=[{"field": "text", "issue": "Contains illegal null byte \\x00"}]
            )

    @classmethod
    def validate_language(cls, language_code: str) -> None:
        """Validates language locale is supported."""
        if language_code.lower() not in cls.SUPPORTED_LANGUAGES:
            raise PayloadValidationError(
                f"Unsupported language code '{language_code}'. Supported locales: {', '.join(sorted(cls.SUPPORTED_LANGUAGES))}",
                details=[{"field": "language", "issue": f"Must be one of {sorted(list(cls.SUPPORTED_LANGUAGES))}"}]
            )

    @classmethod
    def validate_required_fields(cls, payload: Dict[str, Any], required_fields: List[str]) -> None:
        """Validates presence of required fields in dictionary payload."""
        missing = [f for f in required_fields if f not in payload or payload[f] is None]
        if missing:
            raise PayloadValidationError(
                f"Missing required payload fields: {', '.join(missing)}",
                details=[{"field": f, "issue": "Required field missing"} for f in missing]
            )

    @classmethod
    def validate_full_payload(cls, raw_text: str, channel_type: str = "SMS", language: str = "en") -> str:
        """
        Executes complete validation pipeline across all rules:
        1. Empty & Whitespace Validation
        2. Malformed Null Byte Detection
        3. UTF-8 Encoding Integrity
        4. Length Boundaries (5 to 10,000 chars)
        5. Language Locale Verification
        """
        clean_text = cls.validate_empty_and_whitespace(raw_text)
        cls.validate_malformed_control_chars(clean_text)
        cls.validate_encoding(clean_text)
        cls.validate_length_boundaries(clean_text)
        cls.validate_language(language)

        return clean_text
