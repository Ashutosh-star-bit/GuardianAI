"""
GuardianAI Enterprise Admin Auth Pytest Suite
"""

import pytest
from app.core.admin_auth import (
    EnterpriseAdminAuthService,
    AdminRole,
    AdminPermission,
    AdminAuthError
)

@pytest.fixture
def auth_service():
    return EnterpriseAdminAuthService()

def test_admin_authentication_success(auth_service):
    res = auth_service.authenticate_admin("admin_master", "AdminSecurePassword123!", mfa_code="123456")
    assert res["mfa_required"] is False
    assert "access_token" in res
    assert res["role"] == "SUPER_ADMIN"
    assert "session_id" in res

def test_mfa_requirement(auth_service):
    res = auth_service.authenticate_admin("admin_master", "AdminSecurePassword123!")
    assert res["mfa_required"] is True

def test_failed_login_account_lockout(auth_service):
    for _ in range(4):
        with pytest.raises(AdminAuthError) as exc:
            auth_service.authenticate_admin("admin_master", "WrongPassword!")
        assert exc.value.status_code == 401

    # 5th failed attempt triggers account lock
    with pytest.raises(AdminAuthError) as exc_lock:
        auth_service.authenticate_admin("admin_master", "WrongPassword!")
    assert exc_lock.value.status_code == 423
    assert "locked" in exc_lock.value.message.lower()

def test_permission_matrix_verification(auth_service):
    assert auth_service.check_permission(AdminRole.SUPER_ADMIN, AdminPermission.THREAT_INTEL) is True
    assert auth_service.check_permission(AdminRole.MODERATOR, AdminPermission.MODERATE) is True
    assert auth_service.check_permission(AdminRole.MODERATOR, AdminPermission.API_KEYS) is False

def test_session_revocation(auth_service):
    login_res = auth_service.authenticate_admin("admin_master", "AdminSecurePassword123!", mfa_code="123456")
    sess_id = login_res["session_id"]

    revoked = auth_service.revoke_session(sess_id)
    assert revoked is True
    assert sess_id not in auth_service._active_sessions
