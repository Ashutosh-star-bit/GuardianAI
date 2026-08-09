"""
GuardianAI Enterprise Image Screenshot Input Adapter
Purpose: Validates image headers (PNG, JPEG, WEBP, GIF), extracts dimensions & MIME metadata,
         prepares payload for OCR recognition, and converts raw image payloads into a UniversalAnalysisRequest DTO.
"""

import struct
from typing import Any, Optional, Dict, Tuple, Union
from app.adapters.base import BaseInputAdapter
from app.adapters.schemas import UniversalAnalysisRequest, AdapterMetadata

class ImageAdapterError(ValueError):
    """Exception raised when image payload validation or header parsing fails."""
    pass

class ImageAdapter(BaseInputAdapter):
    """Enterprise Image Screenshot Input Adapter."""

    MAX_IMAGE_BYTES = 10 * 1024 * 1024  # 10 MB limit

    IMAGE_SIGNATURES = {
        b"\x89PNG\r\n\x1a\n": ("image/png", "PNG"),
        b"\xff\xd8\xff": ("image/jpeg", "JPEG"),
        b"GIF87a": ("image/gif", "GIF"),
        b"GIF89a": ("image/gif", "GIF"),
        b"RIFF": ("image/webp", "WEBP")
    }

    async def adapt_to_request(
        self,
        raw_payload: Union[bytes, str],
        user_id: Optional[str] = None,
        language: str = "en",
        source: str = "REST_API",
        ocr_extracted_text: Optional[str] = None,
        **kwargs: Any
    ) -> UniversalAnalysisRequest:
        """
        Validates image header signature, extracts dimensions metadata, prepares for OCR recognition,
        and constructs UniversalAnalysisRequest DTO.
        """
        if raw_payload is None:
            raise ImageAdapterError("Image payload cannot be None")

        # 1. Resolve Image Bytes
        if isinstance(raw_payload, bytes):
            image_bytes = raw_payload
        elif isinstance(raw_payload, str):
            try:
                with open(raw_payload, "rb") as f:
                    image_bytes = f.read()
            except Exception:
                raise ImageAdapterError(f"Unable to read image file at path '{raw_payload}'")
        else:
            raise ImageAdapterError("Image payload must be bytes or a valid file path string")

        if len(image_bytes) == 0:
            raise ImageAdapterError("Image file payload is empty (0 bytes)")

        if len(image_bytes) > self.MAX_IMAGE_BYTES:
            raise ImageAdapterError(f"Image size ({len(image_bytes)} bytes) exceeds maximum limit ({self.MAX_IMAGE_BYTES} bytes)")

        # 2. Header Magic Signature Check & MIME Detection
        mime_type, format_name = self._sniff_image_format(image_bytes)

        # 3. Extract Image Dimensions (Width x Height)
        width, height = self._extract_image_dimensions(image_bytes, mime_type)

        # 4. Prepare Text Content (OCR extracted text or OCR placeholder)
        if ocr_extracted_text and ocr_extracted_text.strip():
            content_text = ocr_extracted_text.strip()
        else:
            content_text = f"[IMAGE PAYLOAD: {format_name} {width}x{height} - Pending OCR Engine Processing]"

        # 5. Construct Adapter Metadata
        metadata = AdapterMetadata(
            original_format="IMAGE",
            mime_type=mime_type,
            file_size_bytes=len(image_bytes),
            sender_info=None,
            extracted_urls_count=0,
            extra_attributes={
                "width": width,
                "height": height,
                "aspect_ratio": round(width / max(height, 1), 2),
                "format": format_name,
                "ocr_ready": True
            }
        )

        return UniversalAnalysisRequest(
            user_id=user_id,
            input_type="IMAGE",
            raw_content=content_text,
            metadata=metadata,
            language=language,
            source=source
        )

    def _sniff_image_format(self, data: bytes) -> Tuple[str, str]:
        """Sniffs image header magic bytes to detect MIME type and format name."""
        for sig, (mime, fmt) in self.IMAGE_SIGNATURES.items():
            if data.startswith(sig):
                if fmt == "WEBP" and b"WEBP" not in data[:16]:
                    continue
                return mime, fmt
        raise ImageAdapterError("Unsupported image format: Magic header signature not recognized (Must be PNG, JPEG, WEBP, or GIF)")

    def _extract_image_dimensions(self, data: bytes, mime_type: str) -> Tuple[int, int]:
        """Fast header parsing for PNG/JPEG dimensions without PIL dependency."""
        try:
            if mime_type == "image/png" and len(data) >= 24:
                w, h = struct.unpack(">II", data[16:24])
                return w, h
            elif mime_type == "image/jpeg":
                # Find SOF0 / SOF2 marker
                idx = 2
                while idx < len(data) - 9:
                    marker, length = struct.unpack(">HH", data[idx:idx+4])
                    if marker in (0xFFC0, 0xFFC2):
                        h, w = struct.unpack(">HH", data[idx+5:idx+9])
                        return w, h
                    idx += length + 2
        except Exception:
            pass
        return 1024, 768  # Fallback default
