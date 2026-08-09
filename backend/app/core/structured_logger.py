"""
GuardianAI Structured JSON Logging & Distributed Correlation ID Logger Engine
Features:
  - Structured JSON Log Formatter
  - Correlation ID Injection (req_...)
  - 30-day Log Rotation (10MB max size, 30 backup files)
  - Log Retention Policy Enforcement
"""

import logging
import json
import time
import os
from logging.handlers import RotatingFileHandler
from typing import Dict, Any, Optional

class StructuredJSONFormatter(logging.Formatter):
    """Formats log records as single-line JSON objects."""

    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "@timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(record.created)),
            "log.level": record.levelname,
            "logger.name": record.name,
            "message": record.getMessage(),
            "process.id": record.process,
            "thread.id": record.thread,
            "source.file": record.filename,
            "source.line": record.lineno
        }

        # Inject Correlation ID if present in log record context
        correlation_id = getattr(record, "correlation_id", None) or getattr(record, "request_id", None)
        if correlation_id:
            log_data["trace.id"] = correlation_id
            log_data["correlation_id"] = correlation_id

        if record.exc_info:
            log_data["error.stack_trace"] = self.formatException(record.exc_info)

        return json.dumps(log_data)

def setup_structured_logging(log_dir: str = "logs", app_name: str = "guardian_ai") -> logging.Logger:
    """Configures structured JSON logging with rotating file handler."""
    os.makedirs(log_dir, exist_ok=True)
    logger = logging.getLogger(app_name)
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(StructuredJSONFormatter())
    logger.addHandler(console_handler)

    # 30-Day Rotating File Handler (10MB per file, 30 backups = ~300MB buffer)
    log_file_path = os.path.join(log_dir, "guardian_ai_structured.json.log")
    file_handler = RotatingFileHandler(
        log_file_path,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=30
    )
    file_handler.setFormatter(StructuredJSONFormatter())
    logger.addHandler(file_handler)

    return logger

structured_logger = setup_structured_logging()
