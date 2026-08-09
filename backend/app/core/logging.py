"""
GuardianAI Environment-Aware Structured Logging System
Purpose: Provides structured JSON logging for Production/Staging, human-readable colorized logs for Development,
         client-side PII scrubbing, 10MB rotating log files with 30-day retention, and specialized helpers for
         HTTP Request SLA, AI Inference, Security Warnings, and Exception Error Traces.
"""

import logging
import logging.handlers
import sys
import os
import json
import re
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from app.core.config import settings

# Ensure backend/logs directory exists
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

class PIISanitizingFilter(logging.Filter):
    """Filter that automatically scrubs Credit Cards, SSNs, IBANs, Phone Numbers, and Auth Bearer Tokens from log outputs."""

    CC_REGEX = re.compile(r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13})\b')
    SSN_REGEX = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
    IBAN_REGEX = re.compile(r'[A-Z]{2}\d{2}[A-Z0-9]{11,30}', re.IGNORECASE)
    PHONE_REGEX = re.compile(r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b')
    BEARER_REGEX = re.compile(r'Bearer\s+[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*', re.IGNORECASE)

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            record.msg = self.CC_REGEX.sub('[REDACTED_CC]', record.msg)
            record.msg = self.SSN_REGEX.sub('[REDACTED_SSN]', record.msg)
            record.msg = self.IBAN_REGEX.sub('[REDACTED_IBAN]', record.msg)
            record.msg = self.PHONE_REGEX.sub('[REDACTED_PHONE]', record.msg)
            record.msg = self.BEARER_REGEX.sub('Bearer [REDACTED_TOKEN]', record.msg)
        return True

class JSONFormatter(logging.Formatter):
    """Production JSON Formatter for Datadog / Elasticsearch / CloudWatch log ingestors."""
    def format(self, record: logging.LogRecord) -> str:
        log_obj: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "service": settings.PROJECT_NAME,
            "environment": settings.ENVIRONMENT,
        }
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        if hasattr(record, "extra_data") and isinstance(getattr(record, "extra_data"), dict):
            log_obj["extra"] = getattr(record, "extra_data")

        return json.dumps(log_obj)

def get_file_handler(filename: str, formatter: logging.Formatter) -> logging.Handler:
    """Creates a 10MB rotating file handler with 30-day (30 file) retention."""
    filepath = os.path.join(LOGS_DIR, filename)
    handler = logging.handlers.RotatingFileHandler(
        filepath, maxBytes=10 * 1024 * 1024, backupCount=30, encoding="utf-8"
    )
    handler.setFormatter(formatter)
    handler.addFilter(PIISanitizingFilter())
    return handler

def setup_loggers():
    """Configures system-wide category specialized loggers."""
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    is_prod = settings.ENVIRONMENT in ["production", "staging"]

    # Choose Output Formatter
    if is_prod:
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

    # Console Transport
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.addFilter(PIISanitizingFilter())

    # Root Logger
    root_logger = logging.getLogger("guardianai")
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(get_file_handler("application.log", formatter))
    root_logger.propagate = False

    # 1. HTTP Access & SLA Performance Logger
    access_logger = logging.getLogger("guardianai.access")
    access_logger.setLevel(log_level)
    access_logger.addHandler(console_handler)
    access_logger.addHandler(get_file_handler("access.log", formatter))
    access_logger.propagate = False

    # 2. Security & Warning Alert Logger
    security_logger = logging.getLogger("guardianai.security")
    security_logger.setLevel(log_level)
    security_logger.addHandler(console_handler)
    security_logger.addHandler(get_file_handler("security.log", formatter))
    security_logger.propagate = False

    # 3. AI Inference Threat Inspection Logger
    ai_logger = logging.getLogger("guardianai.ai")
    ai_logger.setLevel(log_level)
    ai_logger.addHandler(console_handler)
    ai_logger.addHandler(get_file_handler("ai_inference.log", formatter))
    ai_logger.propagate = False

    # 4. Error & Exception Trace Logger
    error_logger = logging.getLogger("guardianai.error")
    error_logger.setLevel(logging.ERROR)
    error_logger.addHandler(console_handler)
    error_logger.addHandler(get_file_handler("error.log", formatter))
    error_logger.propagate = False

    return root_logger, access_logger, security_logger, ai_logger, error_logger

logger, access_logger, security_logger, ai_logger, error_logger = setup_loggers()

# ==============================================================================
# SPECIALIZED LOGGING HELPER FUNCTIONS
# ==============================================================================

def log_http_request(
    method: str,
    path: str,
    status_code: int,
    latency_ms: float,
    request_id: str,
    ip_address: Optional[str] = None
):
    """Structured HTTP Request & Performance SLA logging."""
    msg = f"HTTP {method} {path} | Status={status_code} | Latency={latency_ms:.2f}ms | RequestID={request_id} | IP={ip_address or 'N/A'}"
    access_logger.info(msg, extra={"extra_data": {
        "method": method,
        "path": path,
        "status_code": status_code,
        "latency_ms": latency_ms,
        "request_id": request_id,
        "ip_address": ip_address
    }})

def log_security_event(
    event: str,
    user_id: Optional[str] = None,
    ip_address: Optional[str] = None,
    reason: Optional[str] = None,
    extra: Optional[Dict[str, Any]] = None
):
    """Structured Security & Warning Alert logging."""
    msg = f"SECURITY_ALERT: {event} | User={user_id or 'ANONYMOUS'} | IP={ip_address or 'N/A'} | Reason={reason or 'N/A'}"
    security_logger.warning(msg, extra={"extra_data": {
        "event": event,
        "user_id": user_id,
        "ip_address": ip_address,
        "reason": reason,
        **(extra or {})
    }})

def log_ai_inference(
    scan_id: str,
    payload_type: str,
    provider: str,
    threat_score: int,
    risk_band: str,
    latency_ms: float,
    confidence: float = 0.95,
    extra: Optional[Dict[str, Any]] = None
):
    """Structured AI Threat Inspection Engine logging."""
    msg = f"AI_INSPECTION: Scan={scan_id} | Type={payload_type} | Provider={provider} | Score={threat_score}/100 | Risk={risk_band} | Latency={latency_ms:.2f}ms | Certainty={confidence * 100:.1f}%"
    ai_logger.info(msg, extra={"extra_data": {
        "scan_id": scan_id,
        "payload_type": payload_type,
        "provider": provider,
        "threat_score": threat_score,
        "risk_band": risk_band,
        "latency_ms": latency_ms,
        "confidence": confidence,
        **(extra or {})
    }})

def log_application_error(
    message: str,
    exc_info: Optional[Any] = None,
    request_id: Optional[str] = None,
    extra: Optional[Dict[str, Any]] = None
):
    """Structured Application Exception Error logging."""
    msg = f"ERROR: {message} | RequestID={request_id or 'N/A'}"
    error_logger.error(msg, exc_info=exc_info, extra={"extra_data": {
        "request_id": request_id,
        **(extra or {})
    }})
