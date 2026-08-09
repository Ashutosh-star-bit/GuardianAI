"""
GuardianAI Enterprise Web URL Input Adapter
Purpose: Validates, parses, normalizes, extracts domain/hostname metadata, and converts raw URL payloads into a UniversalAnalysisRequest DTO.
"""

import re
from typing import Any, Optional
from urllib.parse import urlparse, unquote
from app.adapters.base import BaseInputAdapter
from app.adapters.schemas import UniversalAnalysisRequest, AdapterMetadata

class URLAdapterError(ValueError):
    """Exception raised when web URL payload validation or parsing fails."""
    pass

class URLAdapter(BaseInputAdapter):
    """Enterprise Web URL Input Adapter."""

    MAX_URL_LENGTH = 2048
    URL_REGEX = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )

    async def adapt_to_request(
        self,
        raw_payload: Any,
        user_id: Optional[str] = None,
        language: str = "en",
        source: str = "REST_API",
        **kwargs: Any
    ) -> UniversalAnalysisRequest:
        """
        Validates, parses, normalizes, and extracts hostname metadata from URL into UniversalAnalysisRequest DTO.
        """
        if raw_payload is None:
            raise URLAdapterError("URL payload cannot be None")

        if not isinstance(raw_payload, str):
            raw_payload = str(raw_payload)

        # 1. Null Byte Guard
        if "\x00" in raw_payload:
            raise URLAdapterError("URL payload contains illegal null byte character (\\x00)")

        stripped = raw_payload.strip()
        if not stripped:
            raise URLAdapterError("URL payload cannot be empty or whitespace only")

        if len(stripped) > self.MAX_URL_LENGTH:
            raise URLAdapterError(f"URL length ({len(stripped)}) exceeds maximum limit ({self.MAX_URL_LENGTH})")

        # 2. Scheme Normalization
        normalized_url = stripped
        if not normalized_url.startswith(("http://", "https://", "ftp://", "ftps://")):
            normalized_url = "http://" + normalized_url

        # Unquote URL encoding
        try:
            normalized_url = unquote(normalized_url)
        except Exception:
            pass

        # 3. Parse URL Structure
        try:
            parsed = urlparse(normalized_url)
        except Exception as e:
            raise URLAdapterError(f"Malformed URL string: {str(e)}")

        hostname = parsed.hostname
        if not hostname:
            raise URLAdapterError(f"Malformed URL: Unable to extract valid hostname from '{raw_payload}'")

        # Normalize Hostname to lowercase
        hostname_clean = hostname.lower()
        if hostname_clean.startswith("www."):
            domain_name = hostname_clean[4:]
        else:
            domain_name = hostname_clean

        # Check for valid TLD or IP structure
        if "." not in domain_name and domain_name != "localhost":
            raise URLAdapterError(f"Malformed URL: Invalid domain/TLD structure in '{hostname}'")

        # 4. Construct Adapter Metadata
        metadata = AdapterMetadata(
            original_format="URL",
            mime_type="text/uri-list",
            file_size_bytes=len(raw_payload.encode('utf-8')),
            sender_info=None,
            extracted_urls_count=1,
            extra_attributes={
                "normalized_url": normalized_url,
                "scheme": parsed.scheme.lower(),
                "hostname": hostname_clean,
                "domain": domain_name,
                "port": parsed.port,
                "path": parsed.path or "/",
                "query": parsed.query or None
            }
        )

        return UniversalAnalysisRequest(
            user_id=user_id,
            input_type="URL",
            raw_content=normalized_url,
            metadata=metadata,
            language=language,
            source=source
        )
