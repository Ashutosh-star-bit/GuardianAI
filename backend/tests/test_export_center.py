"""
GuardianAI Secure Export Center Pytest Suite
"""

import pytest
from app.admin.export_center import SecureExportEngine

def test_csv_formula_injection_sanitization():
    unsafe_val = "=1+1"
    sanitized = SecureExportEngine.sanitize_csv_value(unsafe_val)
    assert sanitized.startswith("'=")

def test_csv_export():
    records = [
        {"id": "rep_1", "title": "Phishing URL", "risk": "=CMD"},
        {"id": "rep_2", "title": "Digital Arrest", "risk": "HIGH"}
    ]
    csv_str = SecureExportEngine.export_to_csv(records)
    assert "id,title,risk" in csv_str
    assert "'=CMD" in csv_str

def test_json_export():
    records = [{"id": "log_1", "action": "LOGIN"}]
    json_str = SecureExportEngine.export_to_json(records)
    assert '"id": "log_1"' in json_str
