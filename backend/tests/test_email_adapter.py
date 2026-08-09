"""
GuardianAI EmailAdapter Unit & MIME Parsing Pytest Suite
Purpose: Tests parsing raw text email paste, .eml MIME byte payloads, attachments extraction, and error handling for EmailAdapter.
"""

import pytest
from app.adapters.email_adapter import EmailAdapter, EmailAdapterError
from app.adapters.schemas import UniversalAnalysisRequest

@pytest.mark.asyncio
async def test_email_adapter_text_paste():
    """Tests EmailAdapter parsing raw text email paste."""
    adapter = EmailAdapter()
    raw = """From: security@paypa1-check.top
To: victim@gmail.com
Subject: URGENT: Your PayPal Account is Suspended

Dear customer, your account has been locked due to unauthorized activity.
Verify at http://paypa1-check.top immediately.
"""

    req: UniversalAnalysisRequest = await adapter.adapt_to_request(raw_payload=raw, source="WEB_APP")

    assert req.input_type == "EMAIL"
    assert "Subject: URGENT: Your PayPal Account is Suspended" in req.raw_content
    assert req.metadata.sender_info == "security@paypa1-check.top"
    assert req.metadata.extra_attributes["subject"] == "URGENT: Your PayPal Account is Suspended"

@pytest.mark.asyncio
async def test_email_adapter_eml_bytes():
    """Tests EmailAdapter parsing .eml MIME binary byte payload."""
    adapter = EmailAdapter()
    eml_bytes = b"""From: support@amazon-security.com
To: user@domain.com
Subject: Action Required: Confirm Order
Content-Type: text/plain; charset="utf-8"

Please confirm your order #100-29384 at http://amazon-confirm.xyz
"""

    req = await adapter.adapt_to_request(raw_payload=eml_bytes)

    assert req.input_type == "EMAIL"
    assert req.metadata.extra_attributes["sender"] == "support@amazon-security.com"
    assert "http://amazon-confirm.xyz" in req.raw_content

@pytest.mark.asyncio
async def test_email_adapter_errors():
    """Tests EmailAdapter error handling for None and invalid types."""
    adapter = EmailAdapter()

    with pytest.raises(EmailAdapterError, match="cannot be None"):
        await adapter.adapt_to_request(None)

    with pytest.raises(EmailAdapterError, match="null byte"):
        await adapter.adapt_to_request("From: test@domain.com\x00\nSubject: Test")
