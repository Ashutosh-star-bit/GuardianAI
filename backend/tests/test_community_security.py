"""
GuardianAI Community Security & Privacy Pytest Suite
"""

import pytest
from app.community_intel.security import CommunitySecuritySanitizer, CommunitySecurityError

def test_xss_text_sanitization():
    raw_xss = "<script>alert('xss')</script> Hello <img src=x onerror=alert(1)>"
    sanitized = CommunitySecuritySanitizer.sanitize_text_xss(raw_xss)

    assert "<script>" not in sanitized
    assert "&lt;script&gt;" in sanitized
    assert "onerror=" not in sanitized

def test_pii_scrubbing():
    text_with_pii = "My Aadhaar is 9876 5432 1098 and my PAN is ABCDE1234F and OTP is 889977"
    scrubbed = CommunitySecuritySanitizer.scrub_pii(text_with_pii)

    assert "9876 5432 1098" not in scrubbed
    assert "[REDACTED_AADHAAR]" in scrubbed
    assert "ABCDE1234F" not in scrubbed
    assert "[REDACTED_PAN]" in scrubbed

def test_upload_magic_signature_validation():
    # Valid PNG Magic Signature
    png_bytes = b"\x89PNG\r\n\x1a\nFakeImageData"
    valid, _ = CommunitySecuritySanitizer.validate_upload_attachment(png_bytes, "test.png")
    assert valid is True

    # Malicious Executable Renamed to PNG
    exe_bytes = b"MZ\x90\x00\x03\x00\x00\x00MaliciousExePayload"
    with pytest.raises(CommunitySecurityError) as exc_info:
        CommunitySecuritySanitizer.validate_upload_attachment(exe_bytes, "test.png")
    assert exc_info.value.status_code == 415
