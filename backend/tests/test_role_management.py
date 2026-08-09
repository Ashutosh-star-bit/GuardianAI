"""
GuardianAI RoleManagement Pytest Suite
"""

import pytest
from app.core.role_management import RoleManagementService, SystemPermission

@pytest.fixture
def role_service():
    return RoleManagementService()

def test_builtin_roles(role_service):
    roles = role_service.get_all_roles()
    assert len(roles) >= 6
    role_ids = [r.role_id for r in roles]
    assert "SUPER_ADMIN" in role_ids
    assert "READ_ONLY" in role_ids

def test_custom_role_creation(role_service):
    custom = role_service.create_custom_role(
        name="Security Auditor",
        description="Custom audit team role",
        permissions=[SystemPermission.AUDIT_READ, SystemPermission.ANALYTICS_READ]
    )
    assert custom.is_custom is True
    assert custom.role_id == "CUSTOM_SECURITY_AUDITOR"
    assert role_service.has_permission("CUSTOM_SECURITY_AUDITOR", SystemPermission.AUDIT_READ) is True
    assert role_service.has_permission("CUSTOM_SECURITY_AUDITOR", SystemPermission.ALL_ACCESS) is False

def test_super_admin_unrestricted_permission(role_service):
    assert role_service.has_permission("SUPER_ADMIN", SystemPermission.ADMIN_MANAGE_ROLES) is True
    assert role_service.has_permission("SUPER_ADMIN", SystemPermission.THREAT_INTEL_WRITE) is True
