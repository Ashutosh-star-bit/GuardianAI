"""
GuardianAI Role-Based Access Control (RBAC) & Fine-Grained Permission System
Purpose: Defines User Roles (Admin, Moderator, User), Permission Matrices, and reusable FastAPI Dependencies for authorization.
"""

from enum import Enum
from typing import List, Set, Union, Callable
from fastapi import Depends, HTTPException, status
from app.models.user import User

class UserRole(str, Enum):
    """User Role Hierarchy Enumeration."""
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"

class Permission(str, Enum):
    """Granular Permission Actions Enumeration."""
    # Scan Permissions
    SCAN_CREATE = "scan:create"
    SCAN_READ = "scan:read"
    SCAN_DELETE = "scan:delete"
    SCAN_EXPORT = "scan:export"

    # User Management Permissions
    USER_READ = "user:read"
    USER_UPDATE = "user:update"
    USER_DELETE = "user:delete"

    # Analytics & Reports Permissions
    ANALYTICS_READ = "analytics:read"
    REPORTS_GENERATE = "reports:generate"

    # System Administrative Permissions
    SYSTEM_SETTINGS = "system:settings"
    SYSTEM_LOGS = "system:logs"

# Role to Permissions Matrix Definition
ROLE_PERMISSIONS_MATRIX: dict[UserRole, Set[Permission]] = {
    UserRole.ADMIN: set(Permission), # Admin has all permissions
    UserRole.MODERATOR: {
        Permission.SCAN_READ,
        Permission.SCAN_DELETE,
        Permission.SCAN_EXPORT,
        Permission.USER_READ,
        Permission.ANALYTICS_READ,
        Permission.REPORTS_GENERATE,
    },
    UserRole.USER: {
        Permission.SCAN_CREATE,
        Permission.SCAN_READ,
        Permission.SCAN_EXPORT,
        Permission.USER_READ,
        Permission.USER_UPDATE,
    },
}

class PermissionChecker:
    """
    FastAPI Callable Dependency Enforcer checking if current user holds required permissions or roles.
    """
    def __init__(self, permissions: Union[List[Permission], Permission] = None, roles: Union[List[UserRole], UserRole] = None):
        if permissions:
            self.required_permissions = set(permissions) if isinstance(permissions, list) else {permissions}
        else:
            self.required_permissions = set()

        if roles:
            self.required_roles = set(roles) if isinstance(roles, list) else {roles}
        else:
            self.required_roles = set()

    def __call__(self, current_user: User) -> User:
        # 1. Role Check
        if self.required_roles and current_user.role not in [r.value if isinstance(r, UserRole) else r for r in self.required_roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation requires one of the following roles: {[r.value if isinstance(r, UserRole) else r for r in self.required_roles]}"
            )

        # 2. Fine-Grained Permission Check
        if self.required_permissions:
            user_role_enum = UserRole(current_user.role) if current_user.role in [r.value for r in UserRole] else UserRole.USER
            user_permissions = ROLE_PERMISSIONS_MATRIX.get(user_role_enum, set())

            missing_permissions = self.required_permissions - user_permissions
            if missing_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission denied. Required permissions missing: {[p.value for p in missing_permissions]}"
                )

        return current_user

# Convenience Shortcut Dependency Injectors
def require_role(*roles: UserRole) -> Callable:
    """Dependency injector enforcing user role."""
    from app.api.deps import get_current_user
    checker = PermissionChecker(roles=list(roles))
    def dependency(current_user: User = Depends(get_current_user)):
        return checker(current_user)
    return dependency

def require_permission(*permissions: Permission) -> Callable:
    """Dependency injector enforcing granular permissions."""
    from app.api.deps import get_current_user
    checker = PermissionChecker(permissions=list(permissions))
    def dependency(current_user: User = Depends(get_current_user)):
        return checker(current_user)
    return dependency
