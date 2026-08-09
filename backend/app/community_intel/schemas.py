"""
GuardianAI Community Intelligence Pydantic Schemas & DTOs
"""

from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict

class ReportStatus(str, Enum):
    PENDING = "PENDING"
    UNDER_REVIEW = "UNDER_REVIEW"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"
    MERGED = "MERGED"

class ScamCategory(str, Enum):
    BANKING_FRAUD = "BANKING_FRAUD"
    DIGITAL_ARREST = "DIGITAL_ARREST"
    PHISHING_URL = "PHISHING_URL"
    JOB_SCAM = "JOB_SCAM"
    INVESTMENT_CRYPTO = "INVESTMENT_CRYPTO"
    LOTTERY_KBC = "LOTTERY_KBC"
    TECH_SUPPORT = "TECH_SUPPORT"
    OTHER = "OTHER"

class AttachmentType(str, Enum):
    SCREENSHOT = "SCREENSHOT"
    PDF_DOCUMENT = "PDF_DOCUMENT"
    AUDIO_RECORDING = "AUDIO_RECORDING"

class VoteType(str, Enum):
    UPVOTE = "UPVOTE"
    DOWNVOTE = "DOWNVOTE"
    CONFIRM_THREAT = "CONFIRM_THREAT"

class FeedbackType(str, Enum):
    TRUE_POSITIVE = "TRUE_POSITIVE"
    TRUE_NEGATIVE = "TRUE_NEGATIVE"
    FALSE_POSITIVE = "FALSE_POSITIVE"
    FALSE_NEGATIVE = "FALSE_NEGATIVE"

# --- REQUEST SCHEMAS ---

class ScamReportCreate(BaseModel):
    title: str = Field(min_length=5, max_length=150, description="Short descriptive title of the scam")
    description: str = Field(min_length=10, description="Detailed context of the scam encounter")
    scam_category: ScamCategory = Field(default=ScamCategory.OTHER)
    target_persona: str = Field(default="SENIOR_CITIZENS")
    raw_message_text: Optional[str] = Field(default=None, description="Scam text message content")
    submitted_url: Optional[str] = Field(default=None, description="Phishing URL link")
    voice_transcript: Optional[str] = Field(default=None, description="Cleaned transcript of voice call")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Fake Police Digital Arrest Scam Call",
                "description": "Caller claimed to be from CBI demanding money to prevent digital arrest",
                "scam_category": "DIGITAL_ARREST",
                "target_persona": "SENIOR_CITIZENS",
                "voice_transcript": "Hello sir your Aadhaar is linked to illegal money laundering pay 50000 rupees"
            }
        }
    )

class CommunityVoteCreate(BaseModel):
    report_id: str
    vote_type: VoteType

class AIPredictionFeedbackCreate(BaseModel):
    report_id: str
    scan_id: Optional[str] = None
    predicted_risk_level: str
    feedback_type: FeedbackType
    correction_reason: Optional[str] = None
    suggested_category: Optional[ScamCategory] = None

class MergeReportsRequest(BaseModel):
    source_report_ids: List[str] = Field(min_items=1, description="Reports to be merged into primary report")
    target_primary_report_id: str = Field(description="Primary report receiving merged duplicate indicators")

# --- RESPONSE SCHEMAS ---

class ScamReportResponse(BaseModel):
    report_id: str
    user_id: str
    title: str
    description: str
    scam_category: ScamCategory
    status: ReportStatus
    target_persona: str
    raw_message_text: Optional[str] = None
    submitted_url: Optional[str] = None
    voice_transcript: Optional[str] = None
    upvote_count: int = 0
    downvote_count: int = 0
    weighted_score: float = 0.0
    is_spam: bool = False
    created_at_iso: str
    updated_at_iso: str

class RLHFDatasetItem(BaseModel):
    instruction: str
    input_text: str
    predicted_label: str
    actual_label: str
    feedback_type: str
    verified_by_moderator: bool
    confidence: float
    metadata: Dict[str, Any]
