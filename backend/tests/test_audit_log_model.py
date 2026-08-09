"""
GuardianAI AuditLog Model Pytest Suite
"""

import pytest
from app.models.audit_log import AuditLog

def test_audit_log_record_hash_computation():
    prev_hash = "0" * 64
    h1 = AuditLog.compute_record_hash("usr_admin", "LOGIN_SUCCESS", "AUTH", "2026-08-01T03:54:00Z", prev_hash)
    assert len(h1) == 64

    # Tamper Attempt Check
    h1_tampered = AuditLog.compute_record_hash("usr_admin", "LOGIN_SUCCESS_TAMPERED", "AUTH", "2026-08-01T03:54:00Z", prev_hash)
    assert h1 != h1_tampered
