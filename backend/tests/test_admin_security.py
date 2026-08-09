"""
GuardianAI Enterprise Admin Security Pytest Suite
"""

import pytest
from app.core.admin_security import EnterpriseAdminSecurityEngine, AdminSecurityException
from app.core.admin_auth import AdminRole

def test_xss_sanitization():
    raw = "<script>alert('XSS')</script>"
    clean = EnterpriseAdminSecurityEngine.sanitize_xss_input(raw)
    assert "<script>" not in clean
    assert "&lt;script&gt;" in clean

def test_sqli_detection():
    safe_str = "normal_user_query"
    assert EnterpriseAdminSecurityEngine.validate_sqli_safety(safe_str) is True

    unsafe_str = "SELECT * FROM users WHERE 1=1 --"
    with pytest.raises(AdminSecurityException) as exc:
        EnterpriseAdminSecurityEngine.validate_sqli_safety(unsafe_str)
    assert exc.value.status_code == 400

def test_privilege_escalation_guard():
    # MODERATOR trying to elevate someone to SUPER_ADMIN
    with pytest.raises(AdminSecurityException) as exc:
        EnterpriseAdminSecurityEngine.verify_privilege_escalation_guard(AdminRole.MODERATOR, AdminRole.SUPER_ADMIN)
    assert exc.value.status_code == 403

    # SUPER_ADMIN elevating someone to SUPER_ADMIN
    EnterpriseAdminSecurityEngine.verify_privilege_escalation_guard(AdminRole.SUPER_ADMIN, AdminRole.SUPER_ADMIN)

def test_audit_log_chain_integrity():
    logs = [
        {"id": "1", "previous_hash": "0"*64, "record_hash": "hash_a"},
        {"id": "2", "previous_hash": "hash_a", "record_hash": "hash_b"}
    ]
    assert EnterpriseAdminSecurityEngine.verify_audit_log_chain_integrity(logs) is True

    # Tampered logs chain
    tampered_logs = [
        {"id": "1", "previous_hash": "0"*64, "record_hash": "hash_a"},
        {"id": "2", "previous_hash": "WRONG_PREV", "record_hash": "hash_b"}
    ]
    assert EnterpriseAdminSecurityEngine.verify_audit_log_chain_integrity(tampered_logs) is False
