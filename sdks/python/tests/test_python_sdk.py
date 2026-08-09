"""
GuardianAI Python SDK Pytest Suite
"""

import sys
import os
import pytest

# Add SDK path to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from guardianai import GuardianAIClient

def test_sdk_invalid_api_key():
    with pytest.raises(ValueError):
        GuardianAIClient(api_key="invalid_key_without_prefix")

def test_sdk_scan_url():
    client = GuardianAIClient(api_key="gai_live_88f92a110099xza21_prod")
    result = client.scan_url("http://hdfc-verify.top")
    assert result.scan_id == "scn_sdk_101"
    assert result.threat_score == 98
    assert result.recommended_action == "BLOCK_AND_REPORT"

def test_sdk_scan_text():
    client = GuardianAIClient(api_key="gai_test_44e11b882200abc12_test")
    result = client.scan_text("URGENT KYC UPDATE")
    assert result.scan_id == "scn_sdk_102"
    assert result.threat_score == 95
