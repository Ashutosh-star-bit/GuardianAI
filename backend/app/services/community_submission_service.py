"""
GuardianAI Community Submission Service Engine
Purpose: Enterprise Service encapsulating Report Validation, Media Upload Safety Checks,
         IOC Evidence Extraction, Moderation Status Assignment, and Database Persistence.
"""

import re
import uuid
import pathlib
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.orm import Session

from app.models.scam_report import ScamReport, ScamReportAttachment, ScamReportCreateSchema, AttachmentCreate
from app.community_intel.trust_engine import UserTrustEngine
from app.voice_intel.security import VoiceSecuritySanitizer
from app.core.exceptions import BaseAppException

class SubmissionValidationError(BaseAppException):
    """Raised when community submission validation fails."""
    def __init__(self, message: str = "Submission validation failed.", details: Optional[list] = None):
        super().__init__(message=message, code="SUBMISSION_VALIDATION_ERROR", status_code=400, details=details)

class CommunitySubmissionService:
    """Enterprise Reusable Community Submission Service."""

    MAX_FILE_SIZE_BYTES = 25 * 1024 * 1024  # 25 MB Limit
    ALLOWED_IMAGE_EXTS = {"png", "jpg", "jpeg", "webp"}
    ALLOWED_DOC_EXTS = {"pdf"}
    ALLOWED_AUDIO_EXTS = {"wav", "mp3", "m4a", "flac", "ogg"}

    # Indicator Extraction Regexes
    URL_REGEX = re.compile(r'https?://[^\s<>"]+|www\.[^\s<>"]+', re.IGNORECASE)
    PHONE_REGEX = re.compile(r'\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}')
    UPI_REGEX = re.compile(r'[a-zA-Z0-9.\-_]+@[a-zA-Z]{3,}')

    @classmethod
    def validate_report_content(cls, payload: ScamReportCreateSchema):
        """Validates textual narrative bounds and category safety."""
        if not payload.title or len(payload.title.strip()) < 5:
            raise SubmissionValidationError("Report title must be at least 5 characters long.")
        if not payload.description or len(payload.description.strip()) < 10:
            raise SubmissionValidationError("Report narrative description must be at least 10 characters long.")

    @classmethod
    def validate_attachment(cls, attachment: AttachmentCreate):
        """Validates attachment bounds and file extension safety."""
        if attachment.file_size_bytes > cls.MAX_FILE_SIZE_BYTES:
            raise SubmissionValidationError(
                f"Attachment size ({attachment.file_size_bytes} bytes) exceeds maximum limit of {cls.MAX_FILE_SIZE_BYTES} bytes."
            )

        clean_url = attachment.file_url.split("?")[0].lower()
        ext = clean_url.split(".")[-1] if "." in clean_url else ""

        allowed = cls.ALLOWED_IMAGE_EXTS.union(cls.ALLOWED_DOC_EXTS).union(cls.ALLOWED_AUDIO_EXTS)
        if ext and ext not in allowed:
            raise SubmissionValidationError(f"Attachment file extension '.{ext}' is blocked for security reasons.")

    @classmethod
    def extract_evidence_iocs(cls, text: str) -> Dict[str, List[str]]:
        """Extracts structured IOCs (URLs, Phone numbers, UPI handles) from text."""
        if not text:
            return {"urls": [], "phone_numbers": [], "upi_handles": []}

        urls = list(set(cls.URL_REGEX.findall(text)))
        phones = list(set(cls.PHONE_REGEX.findall(text)))
        upis = list(set(cls.UPI_REGEX.findall(text)))

        return {
            "urls": urls,
            "phone_numbers": phones,
            "upi_handles": upis
        }

    @classmethod
    def assign_initial_moderation_status(cls, user_trust_score: int, evidence_count: int) -> Tuple[str, bool]:
        """
        Determines initial moderation status based on user trust score:
        - Trust >= 80 & Evidence >= 1 -> VERIFIED (Auto-Approve)
        - Trust < 20 -> UNDER_REVIEW (Requires Manual Review)
        - Else -> PENDING
        """
        if user_trust_score >= 80 and evidence_count >= 1:
            return "VERIFIED", False
        elif user_trust_score < 20:
            return "UNDER_REVIEW", False
        return "PENDING", False

    def create_submission(
        self,
        db: Session,
        payload: ScamReportCreateSchema,
        user_id: Optional[str] = None,
        user_trust_score: int = 50
    ) -> ScamReport:
        """
        Validates, extracts IOCs, assigns status, and persists ScamReport ORM entity.
        """
        # 1. Content & Attachment Validation
        self.validate_report_content(payload)
        for att in payload.attachments:
            self.validate_attachment(att)

        # 2. PII Sanitization
        sanitized_description = VoiceSecuritySanitizer.sanitize_transcript(payload.description)

        # 3. IOC Evidence Extraction
        iocs = self.extract_evidence_iocs(sanitized_description)
        if payload.evidence_data:
            iocs.update(payload.evidence_data)

        total_evidence_count = len(iocs.get("urls", [])) + len(iocs.get("phone_numbers", [])) + len(iocs.get("upi_handles", []))

        # 4. Initial Status Assignment
        initial_status, is_spam = self.assign_initial_moderation_status(user_trust_score, total_evidence_count)

        # 5. ORM Persistence
        report = ScamReport(
            user_id=user_id,
            category=payload.category,
            source=payload.source,
            title=payload.title.strip(),
            description=sanitized_description,
            evidence_data=iocs,
            risk_level="HIGH",
            verification_status=initial_status,
            is_spam=is_spam
        )

        db.add(report)
        db.flush()

        for att in payload.attachments:
            attachment_entity = ScamReportAttachment(
                report_id=report.id,
                file_type=att.file_type,
                file_url=att.file_url,
                mime_type=att.mime_type,
                file_size_bytes=att.file_size_bytes
            )
            db.add(attachment_entity)

        db.commit()
        db.refresh(report)
        return report
