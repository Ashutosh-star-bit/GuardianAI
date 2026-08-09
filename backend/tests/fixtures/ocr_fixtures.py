"""
GuardianAI Reusable Pytest Fixtures for Comprehensive OCR & Document Intelligence Testing
Purpose: Generates reusable mock fixtures for image quality edge cases, document formats,
         scam domain categories, and multi-script language text samples.
"""

import pytest

@pytest.fixture
def low_res_image_bytes():
    """72 DPI low-resolution 100x100 PNG image bytes."""
    return b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x64\x00\x00\x00\x64\x08\x02\x00\x00\x00\x25\xdb\x56\xca"

@pytest.fixture
def blurred_image_bytes():
    """Simulated low-contrast blurred image bytes."""
    return b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x02\x00\x00\x00\x02\x00\x08\x00\x00\x00\x00"

@pytest.fixture
def dark_image_bytes():
    """Underexposed low-brightness dark image bytes."""
    return b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x01\x00\x00\x00\x01\x00"

@pytest.fixture
def bright_image_bytes():
    """Overexposed high-brightness image bytes."""
    return b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x03\x00\x00\x00\x03\x00"

@pytest.fixture
def large_pdf_bytes():
    """Multi-page 5-page PDF document file bytes."""
    pages = ["/Type /Page"] * 5
    page_str = "\n".join(pages)
    return f"%PDF-1.7\n{page_str}\n%%EOF".encode("utf-8")

@pytest.fixture
def hindi_text_sample():
    """Pure Hindi (Devanagari script) scam text notice."""
    return (
        "अति आवश्यक: आपका एसबीआई बैंक खाता ब्लॉक कर दिया गया है। "
        "अपना केवाईसी अपडेट करने के लिए तुरंत क्लिक करें http://sbi-kyc-update.online "
        "या 5000 रुपये भेजें।"
    )

@pytest.fixture
def english_text_sample():
    """Pure English (Latin script) bank phishing scam notice."""
    return (
        "URGENT: Your PayPal account has been temporarily restricted due to unauthorized login attempts. "
        "Verify your account immediately at http://paypa1-check.top or contact support@paypa1-check.top"
    )

@pytest.fixture
def mixed_language_sample():
    """Mixed English-Hindi (Hinglish multi-script) scam message."""
    return (
        "URGENT ALERT: Aapka HDFC Bank account suspend ho gaya hai. "
        "Kripya 24 ghante ke andar KYC update karein at http://hdfc-verify.top "
        "nahi toh 10,000 rupees penalty lagegi."
    )

@pytest.fixture
def mobile_screenshot_bytes():
    """Standard 1080x2400 mobile screenshot PNG image bytes."""
    return b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x04\x38\x00\x00\x09\x60\x08\x06\x00\x00\x00"

@pytest.fixture
def bank_notice_scam_payload():
    """Bank security alert scam document text payload."""
    return (
        "OFFICIAL BANK NOTICE - ACCOUNT SUSPENSION\n\n"
        "Dear Customer, your bank account access has been frozen due to unverified PAN/Aadhaar card.\n"
        "Click the official portal link to unblock: http://netbanking-sbi.top\n"
        "Pay non-compliance fee of Rs 500 to upi://pay?pa=bank.verify@okaxis"
    )

@pytest.fixture
def courier_scam_payload():
    """Courier delivery (FedEx/IndiaPost) scam document text payload."""
    return (
        "INDIA POST / FEDEX PACKAGE DELIVERY SUSPENDED\n\n"
        "Tracking ID: IN-88912-US\n"
        "Status: Held at customs warehouse due to incomplete address details.\n"
        "Pay address verification fee of Rs 48 immediately at http://indiapost-track.top/pay"
    )

@pytest.fixture
def fake_job_poster_payload():
    """Fake work-from-home / YouTube review job offer poster text payload."""
    return (
        "PART-TIME WORK FROM HOME JOB OFFER!\n\n"
        "Earn Rs 2,500 - 5,000 daily by liking YouTube videos and reviewing Google maps places!\n"
        "No experience required. Daily payout via UPI / Telegram.\n"
        "Contact HR Manager via Telegram: @job_recruiter_fast or pay Registration Fee Rs 1,000 to hr.payout@okaxis"
    )
