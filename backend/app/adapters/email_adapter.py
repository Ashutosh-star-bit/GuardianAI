"""
GuardianAI Enterprise Email Input Adapter
Purpose: Parses, extracts RFC 5322 metadata (Subject, Sender, Recipient, Headers, Body, Attachments),
         and converts raw email pastes or .eml byte payloads into a UniversalAnalysisRequest DTO.
"""

import email
from email import policy
from email.message import EmailMessage
from typing import Any, Optional, Dict, List, Union
from app.adapters.base import BaseInputAdapter
from app.adapters.schemas import UniversalAnalysisRequest, AdapterMetadata, AttachmentMetadata

class EmailAdapterError(ValueError):
    """Exception raised when email parsing or validation fails."""
    pass

class EmailAdapter(BaseInputAdapter):
    """Enterprise Email Input Adapter supporting raw text paste and .eml byte payloads."""

    MAX_EMAIL_BYTES = 10 * 1024 * 1024  # 10 MB limit

    async def adapt_to_request(
        self,
        raw_payload: Union[str, bytes],
        user_id: Optional[str] = None,
        language: str = "en",
        source: str = "REST_API",
        **kwargs: Any
    ) -> UniversalAnalysisRequest:
        """
        Parses raw text paste or .eml bytes into standardized UniversalAnalysisRequest DTO.
        """
        if raw_payload is None:
            raise EmailAdapterError("Email payload cannot be None")

        # 1. Byte Size & Null Byte Checks
        if isinstance(raw_payload, str):
            if "\x00" in raw_payload:
                raise EmailAdapterError("Email text contains illegal null byte character (\\x00)")
            payload_bytes = raw_payload.encode("utf-8", errors="replace")
        elif isinstance(raw_payload, bytes):
            payload_bytes = raw_payload
        else:
            raise EmailAdapterError("Email payload must be a string or bytes")

        if len(payload_bytes) > self.MAX_EMAIL_BYTES:
            raise EmailAdapterError(f"Email payload size ({len(payload_bytes)} bytes) exceeds max limit ({self.MAX_EMAIL_BYTES} bytes)")

        # 2. Parse RFC 5322 MIME Message
        try:
            msg: EmailMessage = email.message_from_bytes(payload_bytes, policy=policy.default)
        except Exception as e:
            raise EmailAdapterError(f"Failed to parse email message structure: {str(e)}")

        subject = msg.get("Subject", "(No Subject)")
        sender = msg.get("From", "(Unknown Sender)")
        recipient = msg.get("To", "(Unknown Recipient)")
        date_hdr = msg.get("Date", None)

        # Extract Header Dict
        headers_dict: Dict[str, str] = {}
        for h in ["Message-ID", "DKIM-Signature", "Received-SPF", "Authentication-Results", "Reply-To"]:
            if msg.get(h):
                headers_dict[h] = str(msg.get(h))

        # 3. Extract Body & Attachments Placeholder
        body_parts: List[str] = []
        attachments_list: List[AttachmentMetadata] = []

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                disposition = str(part.get_content_disposition() or "")

                if "attachment" in disposition:
                    fn = part.get_filename() or "unnamed_attachment"
                    sz = len(part.get_payload(decode=True) or b"")
                    attachments_list.append(
                        AttachmentMetadata(
                            filename=fn,
                            mime_type=content_type,
                            file_size_bytes=sz
                        )
                    )
                elif content_type == "text/plain":
                    try:
                        content = part.get_content()
                        if isinstance(content, str):
                            body_parts.append(content)
                    except Exception:
                        pass
        else:
            try:
                content = msg.get_content()
                if isinstance(content, str):
                    body_parts.append(content)
            except Exception:
                body_parts.append(msg.get_payload() or "")

        full_body = "\n\n".join(body_parts).strip()
        if not full_body:
            full_body = raw_payload if isinstance(raw_payload, str) else payload_bytes.decode("utf-8", errors="ignore")

        # 4. Construct Clean Combined Text
        combined_text = f"Subject: {subject}\nFrom: {sender}\nTo: {recipient}\n\n{full_body}"

        metadata = AdapterMetadata(
            original_format="EMAIL",
            mime_type="message/rfc822",
            file_size_bytes=len(payload_bytes),
            sender_info=sender,
            extracted_urls_count=0,
            extra_attributes={
                "subject": subject,
                "sender": sender,
                "recipient": recipient,
                "date": date_hdr,
                "headers": headers_dict,
                "attachment_count": len(attachments_list)
            }
        )

        return UniversalAnalysisRequest(
            user_id=user_id,
            input_type="EMAIL",
            raw_content=combined_text,
            metadata=metadata,
            attachments=attachments_list,
            language=language,
            source=source
        )
