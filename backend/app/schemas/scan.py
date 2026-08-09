"""
GuardianAI Scan Pydantic Schemas
Purpose: Data validation schemas for scan requests, highlight attributions, and XAI threat reports.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime

class TextScanRequest(BaseModel):
    payload: str = Field(..., min_length=1, max_length=5000, description="Scam text or SMS payload to evaluate")
    zeroKnowledge: bool = Field(default=False, description="Enforce transient in-memory processing without DB retention")

class URLScanRequest(BaseModel):
    url: str = Field(..., min_length=4, max_length=2048, description="Target Web URL to inspect")

class TextHighlight(BaseModel):
    startOffset: int
    endOffset: int
    text: str
    type: str
    reason: str

class ScanResponse(BaseModel):
    scanId: str
    payloadType: str
    threatScore: int = Field(..., ge=0, le=100)
    riskBand: str # safe, caution, dangerous
    plainRationale: str
    highlights: List[TextHighlight] = []
    remediation: List[str] = []
    executionMs: int
    createdAt: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
