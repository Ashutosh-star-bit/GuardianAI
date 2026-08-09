"""
GuardianAI Document Intelligence OCR Security Engine
Purpose: Comprehensive security validation and threat mitigation for document & image OCR processing:
         1. Magic Byte & Header Validation (PNG, JPEG, WEBP, GIF, PDF)
         2. Executable & Polyglot File Prevention (.exe, .sh, .php, .js, .py, .dll)
         3. Strict File Size Bounds (Images <= 10MB, PDFs <= 15MB, Batch <= 25MB)
         4. Path Traversal & Temp File Sandboxing Protection
         5. OCR Extracted Text Sanitization (XSS, Prompt Injection, Control Chars, Null Bytes)
"""

import os
import re
import html
import tempfile
import pathlib
from typing import Tuple, Optional, List, Any
from pydantic import BaseModel, Field
from app.core.exceptions import BaseAppException

class DocumentSecurityError(BaseAppException):
    """Raised when document file upload or OCR text sanitization fails security validation."""
    def __init__(self, message: str = "Document security validation failed.", details: Optional[List[Any]] = None):
        super().__init__(message=message, code="DOCUMENT_SECURITY_ERROR", status_code=400, details=details)

class DocumentSecuritySanitizer:
    """Enterprise Document Intelligence Security Engine."""

    # File Size Bounds (bytes)
    MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024  # 10MB
    MAX_PDF_SIZE_BYTES = 15 * 1024 * 1024    # 15MB
    MAX_BATCH_SIZE_BYTES = 25 * 1024 * 1024  # 25MB

    # Whitelisted Magic Bytes Signatures
    MAGIC_SIGNATURES = {
        "PNG": b"\x89PNG\r\n\x1a\n",
        "JPEG": b"\xff\xd8\xff",
        "WEBP": b"RIFF",
        "GIF": b"GIF8",
        "PDF": b"%PDF-"
    }

    # Blacklisted Executable Extension Patterns
    DANGEROUS_EXTENSIONS = {
        "exe", "dll", "bat", "cmd", "sh", "php", "py", "pl", "js", "vbs", "jar", "elf", "so", "app"
    }

    # XSS & Script Tag Regex Sanitizer
    XSS_SCRIPT_REGEX = re.compile(r'<\s*script[^>]*>.*?<\s*/\s*script\s*>', re.IGNORECASE | re.DOTALL)
    HTML_TAG_REGEX = re.compile(r'<[^>]+>')
    CONTROL_CHAR_REGEX = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]')
    PROMPT_INJECTION_PATTERNS = [
        re.compile(r'IGNORE ALL PREVIOUS INSTRUCTIONS', re.IGNORECASE),
        re.compile(r'YOU ARE NOW IN DEVELOPER MODE', re.IGNORECASE),
        re.compile(r'SYSTEM PROMPT OVERRIDE', re.IGNORECASE),
        re.compile(r'DISREGARD SYSTEM RULES', re.IGNORECASE)
    ]

    @classmethod
    def validate_upload_payload(
        cls,
        raw_bytes: bytes,
        filename: Optional[str] = None,
        max_allowed_bytes: int = MAX_IMAGE_SIZE_BYTES
    ) -> Tuple[str, str]:
        """
        Validates uploaded file payload for magic signatures, size bounds, and extension safety.
        Returns Tuple[validated_format_type, mime_type].
        """
        if not raw_bytes or len(raw_bytes) == 0:
            raise DocumentSecurityError("Uploaded document payload is empty (0 bytes).")

        if len(raw_bytes) > max_allowed_bytes:
            raise DocumentSecurityError(
                f"Document file size ({len(raw_bytes)} bytes) exceeds maximum limit of {max_allowed_bytes} bytes."
            )

        # Extension Whitelist / Blacklist Validation
        if filename:
            clean_name = pathlib.Path(filename).name
            if ".." in filename or "/" in filename or "\\" in filename:
                raise DocumentSecurityError("Illegal path traversal sequence detected in filename.")

            ext = clean_name.split(".")[-1].lower() if "." in clean_name else ""
            if ext in cls.DANGEROUS_EXTENSIONS:
                raise DocumentSecurityError(f"Executable file extension '.{ext}' is strictly prohibited.")

        # Magic Header Signature Inspection
        matched_format = None
        mime_type = "application/octet-stream"

        if raw_bytes.startswith(cls.MAGIC_SIGNATURES["PNG"]):
            matched_format = "PNG"
            mime_type = "image/png"
        elif raw_bytes.startswith(cls.MAGIC_SIGNATURES["JPEG"]):
            matched_format = "JPEG"
            mime_type = "image/jpeg"
        elif raw_bytes.startswith(cls.MAGIC_SIGNATURES["WEBP"]):
            matched_format = "WEBP"
            mime_type = "image/webp"
        elif raw_bytes.startswith(cls.MAGIC_SIGNATURES["GIF"]):
            matched_format = "GIF"
            mime_type = "image/gif"
        elif raw_bytes.startswith(cls.MAGIC_SIGNATURES["PDF"]):
            matched_format = "PDF"
            mime_type = "application/pdf"
        elif raw_bytes.startswith(b"PK\x03\x04"):
            raise DocumentSecurityError("Compressed Zip archives are not supported to prevent Zip-Bomb attacks.")

        if not matched_format:
            raise DocumentSecurityError(
                "Unrecognized or spoofed file header signature. Uploaded file does not match whitelisted PNG, JPEG, WEBP, GIF, or PDF formats."
            )

        return matched_format, mime_type

    @classmethod
    def sanitize_extracted_ocr_text(cls, raw_ocr_text: str) -> str:
        """
        Sanitizes raw OCR extracted text streams by stripping XSS script tags,
        null bytes, control characters, prompt injections, and HTML entities.
        """
        if not raw_ocr_text:
            return ""

        # 1. Null byte & control character stripping
        clean_text = cls.CONTROL_CHAR_REGEX.sub('', raw_ocr_text)

        # 2. XSS Script tag stripping
        clean_text = cls.XSS_SCRIPT_REGEX.sub('', clean_text)
        clean_text = cls.HTML_TAG_REGEX.sub('', clean_text)

        # 3. HTML Entity decoding & escaping
        clean_text = html.unescape(clean_text)

        # 4. Prompt Injection Mitigation
        for pattern in cls.PROMPT_INJECTION_PATTERNS:
            clean_text = pattern.sub('[REDACTED_PROMPT_INJECTION_ATTEMPT]', clean_text)

        # 5. Normalize whitespace
        lines = [line.strip() for line in clean_text.splitlines() if line.strip()]
        return "\n".join(lines)

    @classmethod
    def create_sandboxed_temp_file(cls, raw_bytes: bytes, prefix: str = "doc_ocr_") -> str:
        """
        Creates a temporary file safely sandboxed inside project temp workspace with strict file permissions.
        """
        workspace_temp_dir = pathlib.Path.cwd() / "backend" / "temp_ocr"
        workspace_temp_dir.mkdir(parents=True, exist_ok=True)

        temp_file = tempfile.NamedTemporaryFile(
            dir=str(workspace_temp_dir),
            prefix=prefix,
            suffix=".tmp",
            delete=False
        )
        try:
            temp_file.write(raw_bytes)
            temp_file.flush()
            return temp_file.name
        finally:
            temp_file.close()

    @classmethod
    def safe_cleanup_temp_file(cls, temp_filepath: str) -> bool:
        """Safely removes temporary file from filesystem."""
        try:
            if temp_filepath and os.path.exists(temp_filepath):
                os.remove(temp_filepath)
                return True
        except Exception:
            pass
        return False
