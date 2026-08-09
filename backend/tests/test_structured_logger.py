"""
GuardianAI Structured Logger Pytest Suite
"""

import json
import logging
import pytest
from app.core.structured_logger import StructuredJSONFormatter, structured_logger

def test_structured_json_formatter():
    formatter = StructuredJSONFormatter()
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test.py",
        lineno=42,
        msg="Scanning suspicious URL payload",
        args=(),
        exc_info=None
    )
    record.correlation_id = "req_88a91102"

    json_output = formatter.format(record)
    data = json.loads(json_output)

    assert data["log.level"] == "INFO"
    assert data["message"] == "Scanning suspicious URL payload"
    assert data["correlation_id"] == "req_88a91102"
    assert "trace.id" in data
