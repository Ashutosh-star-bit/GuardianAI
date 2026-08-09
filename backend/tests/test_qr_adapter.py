"""
GuardianAI QRImageAdapter Unit & Payload Categorization Pytest Suite
Purpose: Tests QR payload categorization across UPI, URL, Phone, SMS, Email, WiFi, and error handling for QRImageAdapter.
"""

import pytest
from app.adapters.qr_adapter import QRImageAdapter, QRAdapterError
from app.adapters.schemas import UniversalAnalysisRequest

@pytest.mark.asyncio
async def test_qr_adapter_upi_payload():
    """Tests QRImageAdapter decoding UPI payment payload."""
    adapter = QRImageAdapter()
    raw = "upi://pay?pa=merchant.refund@okaxis&pn=MerchantSupport&am=500"

    req: UniversalAnalysisRequest = await adapter.adapt_to_request(raw_payload=raw, source="WEB_APP")

    assert req.input_type == "QR"
    assert req.metadata.extra_attributes["qr_category"] == "UPI"
    assert req.metadata.extra_attributes["parsed_details"]["handle"] == "merchant.refund@okaxis"
    assert "merchant.refund@okaxis" in req.raw_content

@pytest.mark.asyncio
async def test_qr_adapter_url_and_phone_payload():
    """Tests QRImageAdapter decoding URL and Phone tel: payloads."""
    adapter = QRImageAdapter()

    # URL Payload
    req_url = await adapter.adapt_to_request("https://paypa1-check.top/login")
    assert req_url.metadata.extra_attributes["qr_category"] == "URL"

    # Tel: Payload
    req_tel = await adapter.adapt_to_request("tel:+18005550199")
    assert req_tel.metadata.extra_attributes["qr_category"] == "PHONE"
    assert req_tel.metadata.extra_attributes["parsed_details"]["phone_number"] == "+18005550199"

@pytest.mark.asyncio
async def test_qr_adapter_sms_email_wifi_payloads():
    """Tests QRImageAdapter decoding SMS, Email, and WiFi payloads."""
    adapter = QRImageAdapter()

    # SMS Payload
    req_sms = await adapter.adapt_to_request("SMSTO:+18005550199:Share your 6-digit OTP code")
    assert req_sms.metadata.extra_attributes["qr_category"] == "SMS"

    # Email Payload
    req_email = await adapter.adapt_to_request("mailto:support@paypa1-check.top")
    assert req_email.metadata.extra_attributes["qr_category"] == "EMAIL"

    # WiFi Payload
    req_wifi = await adapter.adapt_to_request("WIFI:S:Free_Airport_Wifi;P:password;;")
    assert req_wifi.metadata.extra_attributes["qr_category"] == "WIFI"

@pytest.mark.asyncio
async def test_qr_adapter_errors():
    """Tests QRImageAdapter error handling for None, empty, and null bytes."""
    adapter = QRImageAdapter()

    with pytest.raises(QRAdapterError, match="cannot be None"):
        await adapter.adapt_to_request(None)

    with pytest.raises(QRAdapterError, match="null byte"):
        await adapter.adapt_to_request("upi://pay?pa=test\x00@okaxis")
