"""
GuardianAI Universal AnalysisRequest DTO & Adapter Metadata Schemas
Purpose: Provides standardized, Pydantic v2 schemas for AnalysisRequest, AdapterMetadata, and AttachmentMetadata with strict validators.
"""

import uuid
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, ConfigDict, field_validator

SUPPORTED_INPUT_TYPES = {
    "TEXT", "URL", "EMAIL", "IMAGE", "PDF", "QR",
    "VOICE", "BROWSER", "WHATSAPP", "TELEGRAM", "JSON", "CSV"
}

SUPPORTED_LANGUAGES = {"en", "es", "hi", "fr", "de"}

class AttachmentMetadata(BaseModel):
    """Metadata DTO for file attachments inside input payloads (e.g. Email / PDF attachments)."""
    attachment_id: str = Field(default_factory=lambda: f"att_{uuid.uuid4().hex[:8]}")
    filename: str
    mime_type: str
    file_size_bytes: int = Field(ge=0)
    file_path: Optional[str] = None
    url: Optional[str] = None

class AdapterMetadata(BaseModel):
    """Metadata container for format-specific adapter properties."""
    original_format: str = Field(description="TEXT, URL, EMAIL, IMAGE, PDF, QR, VOICE, etc.")
    mime_type: Optional[str] = None
    file_size_bytes: int = Field(default=0, ge=0)
    sender_info: Optional[str] = Field(default=None, description="Sender email or phone number if available")
    extracted_urls_count: int = Field(default=0, ge=0)
    extra_attributes: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(extra="ignore", from_attributes=True)

class UniversalAnalysisRequest(BaseModel):
    """Universal AnalysisRequest DTO normalized across all input formats."""
    request_id: str = Field(default_factory=lambda: f"req_{uuid.uuid4().hex[:10]}")
    scan_id: str = Field(default_factory=lambda: f"scn_{uuid.uuid4().hex[:10]}")
    user_id: Optional[str] = Field(default=None, description="Authenticated User ID if present")
    input_type: str = Field(default="TEXT", description="TEXT, URL, EMAIL, IMAGE, PDF, QR, VOICE, BROWSER, WHATSAPP, TELEGRAM, JSON, CSV")
    raw_content: str = Field(min_length=1, description="Extracted clean text ready for analysis")
    metadata: AdapterMetadata
    attachments: List[AttachmentMetadata] = Field(default_factory=list)
    language: str = Field(default="en", description="en, es, hi, fr, de")
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    source: str = Field(default="REST_API", description="REST_API, WEB_APP, MOBILE_APP, CHROME_EXTENSION")

    @field_validator("input_type")
    @classmethod
    def validate_input_type(cls, val: str) -> str:
        upper_val = val.upper()
        if upper_val not in SUPPORTED_INPUT_TYPES:
            raise ValueError(f"Unsupported input_type '{val}'. Supported types: {sorted(list(SUPPORTED_INPUT_TYPES))}")
        return upper_val

    @field_validator("raw_content")
    @classmethod
    def validate_raw_content(cls, val: str) -> str:
        if "\x00" in val:
            raise ValueError("raw_content contains illegal null byte character (\\x00)")
        return val

    @field_validator("language")
    @classmethod
    def validate_language(cls, val: str) -> str:
        lower_val = val.lower()
        if lower_val not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language '{val}'. Supported languages: {sorted(list(SUPPORTED_LANGUAGES))}")
        return lower_val

    model_config = {
        "json_schema_extra": {
            "example": {
                "request_id": "req_8f92a11009",
                "scan_id": "scn_9901a11009",
                "user_id": "usr_9901",
                "input_type": "EMAIL",
                "raw_content": "Subject: URGENT Account Suspended\nVerify at http://paypa1-check.top",
                "metadata": {
                    "original_format": "EMAIL",
                    "mime_type": "message/rfc822",
                    "file_size_bytes": 1024,
                    "sender_info": "security@paypa1-check.top",
                    "extracted_urls_count": 1
                },
                "attachments": [],
                "language": "en",
                "created_at": "2026-07-28T22:44:42.120Z",
                "source": "WEB_APP"
            }
        }
    }
