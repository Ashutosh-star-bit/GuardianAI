"""
GuardianAI Central Input Adapter Factory Registry
Purpose: Registers and resolves input format adapters (Text, URL, Email, PDF, Image, QR, Document, Audio)
         and provides MIME-type sniffing for polymorphic payload processing.
"""

import re
from typing import Dict, Type, Any, Optional
from app.adapters.base import BaseInputAdapter
from app.adapters.text_adapter import TextAdapter
from app.adapters.url_adapter import URLAdapter
from app.adapters.email_adapter import EmailAdapter
from app.adapters.pdf_adapter import PDFAdapter
from app.adapters.image_adapter import ImageAdapter
from app.adapters.qr_adapter import QRImageAdapter
from app.adapters.document_adapter import DocumentAdapter
from app.adapters.audio_adapter import AudioAdapter
from app.adapters.schemas import UniversalAnalysisRequest

class InputAdapterFactoryError(ValueError):
    """Exception raised when adapter resolution or format sniffing fails."""
    pass

class InputAdapterFactory:
    """Central Polymorphic Input Adapter Factory."""

    _registry: Dict[str, Type[Any]] = {
        "TEXT": TextAdapter,
        "URL": URLAdapter,
        "EMAIL": EmailAdapter,
        "PDF": PDFAdapter,
        "IMAGE": ImageAdapter,
        "QR": QRImageAdapter,
        "DOCUMENT": DocumentAdapter,
        "AUDIO": AudioAdapter,
        "VOICE": AudioAdapter
    }

    @classmethod
    def register_adapter(cls, format_type: str, adapter_cls: Type[Any]) -> None:
        """Dynamically registers a new format adapter."""
        cls._registry[format_type.upper()] = adapter_cls

    @classmethod
    def get_adapter(cls, format_type: str) -> Any:
        """Resolves appropriate BaseInputAdapter instance for format_type."""
        fmt_key = format_type.upper()
        adapter_cls = cls._registry.get(fmt_key)
        if not adapter_cls:
            raise InputAdapterFactoryError(f"Unsupported format type '{format_type}'. Registered formats: {sorted(list(cls._registry.keys()))}")
        return adapter_cls()

    @classmethod
    def sniff_and_get_adapter(cls, raw_payload: Any, declared_format: Optional[str] = None) -> Any:
        """
        Auto-detects payload format signature or falls back to declared format string.
        """
        if declared_format and declared_format.upper() in cls._registry:
            return cls.get_adapter(declared_format)

        if isinstance(raw_payload, bytes):
            if raw_payload.startswith(b"%PDF-"):
                return cls.get_adapter("PDF")
            elif raw_payload.startswith((b"RIFF", b"ID3", b"\xff\xfb", b"fLaC", b"OggS")) or b"ftyp" in raw_payload[:12]:
                return cls.get_adapter("AUDIO")
            elif raw_payload.startswith((b"\x89PNG", b"\xff\xd8\xff", b"GIF8")):
                return cls.get_adapter("DOCUMENT")
            elif b"From:" in raw_payload and b"Subject:" in raw_payload:
                return cls.get_adapter("EMAIL")
        elif isinstance(raw_payload, str):
            stripped = raw_payload.strip()
            if stripped.startswith(("http://", "https://", "www.")):
                return cls.get_adapter("URL")
            elif stripped.startswith(("upi://", "SMSTO:", "mailto:", "WIFI:")):
                return cls.get_adapter("QR")
            elif "From:" in stripped and "Subject:" in stripped:
                return cls.get_adapter("EMAIL")

        # Fallback to TextAdapter
        return cls.get_adapter("TEXT")

    @classmethod
    def process_payload(
        cls,
        raw_payload: Any,
        format_type: Optional[str] = None,
        user_id: Optional[str] = None,
        language: str = "en",
        source: str = "REST_API",
        **kwargs: Any
    ) -> UniversalAnalysisRequest:
        """
        High-level helper resolving adapter and executing payload adaptation into UniversalAnalysisRequest DTO.
        """
        adapter = cls.sniff_and_get_adapter(raw_payload, declared_format=format_type)
        return adapter.adapt(
            raw_bytes=raw_payload if isinstance(raw_payload, bytes) else str(raw_payload).encode('utf-8'),
            language=language
        ) if hasattr(adapter, 'adapt') else adapter.adapt_to_request(
            raw_payload=raw_payload,
            user_id=user_id,
            language=language,
            source=source,
            **kwargs
        )
