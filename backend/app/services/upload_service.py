"""
GuardianAI Enterprise Secure File Upload Service
Purpose: Handles file extension whitelist (.txt, .pdf, .png, .jpg, .jpeg, .eml), MIME content-type validation,
         magic byte inspection, 10MB size limits, path traversal sanitization, SHA-256 duplicate detection,
         virus scanning placeholder, and secure local disk persistence.
"""

import os
import uuid
import re
import hashlib
import logging
from typing import Dict, Any, Set, Tuple, Optional
from fastapi import UploadFile, HTTPException, status
from pydantic import BaseModel, Field

logger = logging.getLogger("guardianai.upload")

# Sandbox directory for uploaded files
UPLOADS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Validation Constants
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB max limit
ALLOWED_EXTENSIONS: Set[str] = {".txt", ".pdf", ".png", ".jpg", ".jpeg", ".eml"}
ALLOWED_MIME_TYPES: Set[str] = {
    "application/pdf",
    "image/png",
    "image/jpeg",
    "text/plain",
    "message/rfc822"
}

class VirusScannerPlaceholder:
    """Enterprise Virus / Malware Scanner Integration Placeholder."""

    @classmethod
    def scan_file_bytes(cls, data: bytes, filename: str = "upload") -> Tuple[bool, Optional[str]]:
        """
        Scans uploaded file byte payload for malicious executable signatures / malware.
        Returns Tuple[is_clean: bool, threat_name: Optional[str]].
        """
        # Rejection of Windows / Linux executable signatures
        if data.startswith((b"MZ", b"\x7fELF", b"\xca\xfe\xba\xbe")):
            return False, "EXECUTABLE_BINARY_MALWARE"
        return True, None

class SecureUploadService:
    """Enterprise Secure File Upload Service with SHA-256 Duplicate Detection & Virus Guard."""

    # In-memory SHA-256 Hash Cache for duplicate detection
    _file_hash_cache: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def clear_cache(cls) -> None:
        """Clears in-memory duplicate file hash cache."""
        cls._file_hash_cache.clear()

    @staticmethod
    def calculate_sha256(data: bytes) -> str:
        """Computes 64-character SHA-256 hex digest hash of file bytes."""
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitizes raw filenames to prevent path traversal and shell injection attacks."""
        basename = os.path.basename(filename)
        # Strip null bytes and non-printable characters
        clean_name = re.sub(r'[^a-zA-Z0-9_.-]', '_', basename)
        return clean_name or "uploaded_file"

    @classmethod
    def validate_file(cls, file: UploadFile, contents: bytes) -> str:
        """
        Validates file size, extension whitelist, MIME content-type headers, and null byte guards.
        Returns the sanitized file extension.
        """
        # 1. Null Byte Control Guard
        if b"\x00" in contents[:512]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File payload contains illegal null byte characters."
            )

        # 2. Size Validation
        if len(contents) > MAX_FILE_SIZE_BYTES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File size ({len(contents) / (1024 * 1024):.2f} MB) exceeds maximum allowed limit of {MAX_FILE_SIZE_BYTES / (1024 * 1024):.1f} MB."
            )
        if len(contents) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Empty file uploads are not allowed."
            )

        # 3. Extension Whitelist Check
        filename = file.filename or "file.txt"
        _, ext = os.path.splitext(filename.lower())
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file extension '{ext}'. Allowed extensions: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
            )

        # 4. MIME Content-Type Validation
        mime_type = (file.content_type or "").lower()
        if mime_type and mime_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid MIME type '{mime_type}'. Supported formats: PDF, PNG, JPG, JPEG, TXT, EML."
            )

        # 5. Virus & Malware Inspection
        is_clean, threat_name = VirusScannerPlaceholder.scan_file_bytes(contents, filename)
        if not is_clean:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Security Alert: Malicious file payload signature detected ({threat_name}). Upload rejected."
            )

        return ext

    @classmethod
    async def save_upload(cls, file: UploadFile) -> Dict[str, Any]:
        """
        Reads, validates, scans, and securely persists uploaded file to sandbox disk.
        Provides SHA-256 duplicate detection.
        """
        try:
            contents = await file.read()
            ext = cls.validate_file(file, contents)

            # Compute SHA-256 Content Hash
            sha256_hash = cls.calculate_sha256(contents)

            # Check Duplicate Detection Cache
            if sha256_hash in cls._file_hash_cache:
                cached_res = cls._file_hash_cache[sha256_hash].copy()
                cached_res["is_duplicate"] = True
                logger.info(f"Duplicate file upload detected (SHA-256: {sha256_hash[:12]}). Returning cached upload record.")
                return cached_res

            # Generate collision-proof unique filename
            unique_id = f"upl_{uuid.uuid4().hex[:12]}"
            clean_original = cls.sanitize_filename(file.filename or "file")
            clean_base, _ = os.path.splitext(clean_original)
            saved_filename = f"{unique_id}_{clean_base}{ext}"

            destination_path = os.path.join(UPLOADS_DIR, saved_filename)

            # Save file to disk securely
            with open(destination_path, "wb") as f:
                f.write(contents)

            upload_result = {
                "file_id": unique_id,
                "filename": saved_filename,
                "original_filename": file.filename,
                "mime_type": file.content_type or "application/octet-stream",
                "file_size_bytes": len(contents),
                "sha256_hash": sha256_hash,
                "is_duplicate": False,
                "file_path": destination_path,
                "url": f"/static/uploads/{saved_filename}"
            }

            # Update Duplicate Cache
            cls._file_hash_cache[sha256_hash] = upload_result

            logger.info(f"Successfully saved uploaded file: {saved_filename} ({len(contents)} bytes, SHA-256: {sha256_hash[:12]})")
            return upload_result

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to process upload file {file.filename}: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An internal error occurred while processing the uploaded file."
            )
