"""
GuardianAI Enterprise QR Code Image Input Adapter
Purpose: Decodes QR payloads across 6 threat payload types (URL, UPI, Phone, SMS, Email, WiFi),
         extracts embedded indicators, and converts raw QR image/data payloads into a UniversalAnalysisRequest DTO.
"""

import re
from typing import Any, Optional, Dict, Tuple, Union
from app.adapters.base import BaseInputAdapter
from app.adapters.schemas import UniversalAnalysisRequest, AdapterMetadata

class QRAdapterError(ValueError):
    """Exception raised when QR code parsing or payload decoding fails."""
    pass

class QRImageAdapter(BaseInputAdapter):
    """Enterprise QR Code Image Input Adapter."""

    MAX_QR_BYTES = 5 * 1024 * 1024  # 5 MB limit

    # Regex Category Decoders
    UPI_URI_REGEX = re.compile(r'^upi://pay\?', re.IGNORECASE)
    URL_REGEX = re.compile(r'^https?://', re.IGNORECASE)
    TEL_REGEX = re.compile(r'^(?:tel:|phone:)', re.IGNORECASE)
    SMS_REGEX = re.compile(r'^(?:smsto:|sms:)', re.IGNORECASE)
    MAILTO_REGEX = re.compile(r'^mailto:', re.IGNORECASE)
    WIFI_REGEX = re.compile(r'^wifi:', re.IGNORECASE)

    async def adapt_to_request(
        self,
        raw_payload: Union[str, bytes],
        user_id: Optional[str] = None,
        language: str = "en",
        source: str = "REST_API",
        qr_decoded_text: Optional[str] = None,
        **kwargs: Any
    ) -> UniversalAnalysisRequest:
        """
        Decodes QR image or text payload, categorizes QR threat vector (URL, UPI, Phone, SMS, Email, WiFi),
        and constructs UniversalAnalysisRequest DTO.
        """
        if raw_payload is None and qr_decoded_text is None:
            raise QRAdapterError("QR payload cannot be None")

        # 1. Resolve QR Payload String
        if qr_decoded_text and qr_decoded_text.strip():
            qr_content = qr_decoded_text.strip()
        elif isinstance(raw_payload, str):
            qr_content = raw_payload.strip()
        elif isinstance(raw_payload, bytes):
            # Check for illegal null bytes
            if b"\x00" in raw_payload:
                raise QRAdapterError("QR payload contains illegal null byte character (\\x00)")
            qr_content = raw_payload.decode("utf-8", errors="ignore").strip()
        else:
            raise QRAdapterError("QR payload must be a string, bytes, or decoded text string")

        if not qr_content:
            raise QRAdapterError("QR code decoded payload is empty")

        if "\x00" in qr_content:
            raise QRAdapterError("QR payload contains illegal null byte character (\\x00)")

        # 2. Categorize QR Threat Payload Type
        qr_category, parsed_details = self._categorize_qr_payload(qr_content)

        # 3. Formulate Raw Content String for downstream NLP & Threat Engines
        clean_raw_content = f"QR Code [{qr_category} Payload]: {qr_content}"

        # 4. Construct Adapter Metadata
        metadata = AdapterMetadata(
            original_format="QR",
            mime_type="image/qr-code",
            file_size_bytes=len(qr_content.encode('utf-8')),
            sender_info=parsed_details.get("handle") or parsed_details.get("recipient") or None,
            extracted_urls_count=1 if qr_category in ["URL", "UPI"] else 0,
            extra_attributes={
                "qr_category": qr_category,
                "decoded_payload": qr_content,
                "parsed_details": parsed_details
            }
        )

        return UniversalAnalysisRequest(
            user_id=user_id,
            input_type="QR",
            raw_content=clean_raw_content,
            metadata=metadata,
            language=language,
            source=source
        )

    def _categorize_qr_payload(self, content: str) -> Tuple[str, Dict[str, Any]]:
        """Categorizes QR payload string into URL, UPI, Phone, SMS, Email, or WiFi."""
        details: Dict[str, Any] = {}

        if self.UPI_URI_REGEX.match(content) or "pa=" in content.lower():
            # Extract UPI VPA Handle and Payee Name
            pa_match = re.search(r'pa=([a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+)', content, re.IGNORECASE)
            pn_match = re.search(r'pn=([^&]+)', content, re.IGNORECASE)
            details["handle"] = pa_match.group(1) if pa_match else None
            details["payee_name"] = pn_match.group(1) if pn_match else None
            return "UPI", details

        elif self.URL_REGEX.match(content) or "www." in content.lower():
            details["target_url"] = content
            return "URL", details

        elif self.TEL_REGEX.match(content):
            phone_num = re.sub(r'^(?:tel:|phone:)', '', content, flags=re.IGNORECASE).strip()
            details["phone_number"] = phone_num
            return "PHONE", details

        elif self.SMS_REGEX.match(content):
            parts = content.split(":", 2)
            phone_num = parts[1] if len(parts) > 1 else ""
            sms_body = parts[2] if len(parts) > 2 else ""
            details["phone_number"] = phone_num
            details["sms_body"] = sms_body
            return "SMS", details

        elif self.MAILTO_REGEX.match(content):
            email_addr = re.sub(r'^mailto:', '', content, flags=re.IGNORECASE).strip()
            details["recipient"] = email_addr
            return "EMAIL", details

        elif self.WIFI_REGEX.match(content):
            ssid_match = re.search(r'S:([^;]+)', content)
            details["ssid"] = ssid_match.group(1) if ssid_match else None
            return "WIFI", details

        return "GENERIC_TEXT", {"payload": content}
