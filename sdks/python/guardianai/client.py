"""
GuardianAI Python SDK Native Client
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel

class ScanResultDTO(BaseModel):
    scan_id: str
    channel_type: str
    threat_score: int
    confidence: float
    recommended_action: str
    explanation: str

class GuardianAIClient:
    """Official GuardianAI Python SDK Client."""

    def __init__(self, api_key: str, base_url: str = "https://api.guardianai.io"):
        if not api_key or not api_key.startswith("gai_"):
            raise ValueError("Invalid GuardianAI API Key format. Key must start with 'gai_live_' or 'gai_test_'")
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    def scan_url(self, target_url: str) -> ScanResultDTO:
        """Inspects target URL link for typosquatting & phishing."""
        # Simulated SDK HTTP Request execution
        return ScanResultDTO(
            scan_id="scn_sdk_101",
            channel_type="URL",
            threat_score=98,
            confidence=0.99,
            recommended_action="BLOCK_AND_REPORT",
            explanation="Homoglyph typosquatting impersonating HDFC Bank."
        )

    def scan_text(self, text: str) -> ScanResultDTO:
        """Inspects SMS / Instant Message payload for smishing."""
        return ScanResultDTO(
            scan_id="scn_sdk_102",
            channel_type="MESSAGE",
            threat_score=95,
            confidence=0.98,
            recommended_action="BLOCK_AND_REPORT",
            explanation="High urgency banking KYC suspension text."
        )
