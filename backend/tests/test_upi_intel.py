"""
GuardianAI UPI Intelligence Engine Unit Test Suite
Purpose: Tests UPI VPA handle parsing, PSP provider resolution, sponsor bank mapping, unknown PSP detection, and suspicious support desk naming patterns.
"""

import pytest
from app.threat_intel.upi_intel import UPIIntelligenceEngine, UPIIntelReport

def test_analyze_suspicious_support_upi_handle():
    """Tests personal UPI handle impersonating customer support desk (support.refund@okaxis)."""
    raw_upi = "support.refund@okaxis"
    report: UPIIntelReport = UPIIntelligenceEngine.analyze_upi(raw_upi)

    assert report.upi_id == "support.refund@okaxis"
    assert report.username_handle == "support.refund"
    assert report.psp_handle == "okaxis"
    assert report.psp_provider_name == "Google Pay"
    assert report.sponsor_bank_name == "Axis Bank"
    assert report.is_recognized_psp is True
    assert report.has_suspicious_naming is True
    assert report.impersonated_keyword in ["SUPPORT", "REFUND"]
    assert report.risk_score >= 45

def test_analyze_unknown_unrecognized_psp_handle():
    """Tests unknown/unregistered PSP handle (@scambank)."""
    raw_upi = "merchant@scambank"
    report = UPIIntelligenceEngine.analyze_upi(raw_upi)

    assert report.is_recognized_psp is False
    assert "UNKNOWN_UNRECOGNIZED_UPI_PSP_SCAMBANK" in report.risk_indicators
    assert report.risk_score >= 35

def test_analyze_invalid_upi_vpa_format():
    """Tests broken UPI handle format lacking @ symbol."""
    raw_upi = "merchant.okaxis.com"
    report = UPIIntelligenceEngine.analyze_upi(raw_upi)

    assert report.is_valid_format is False
    assert "INVALID_UPI_VPA_FORMAT" in report.risk_indicators
    assert report.risk_score >= 40
