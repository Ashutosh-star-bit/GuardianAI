"""
GuardianAI Enterprise Role & Dynamic Permission Management Engine
Purpose: Provides dynamic Role-Based & Attribute-Based Access Control (RBAC/ABAC) supporting:
         Built-in Roles (Super Admin, Admin, Moderator, Analyst, Developer, Read Only)
         + Custom Dynamic Roles with granular permission bitmasking.
"""

from typing import Dict, Any, List, Set, Optional
from enum import Enum
from pydantic import BaseModel

class SystemPermission(str, Enum):
    # Admin & System
    ALL_ACCESS = "*"
    ADMIN_MANAGE_USERS = "admin:users:manage"
    ADMIN_MANAGE_ROLES = "admin:roles:manage"
    ADMIN_SYSTEM_HEALTH = "admin:system:health"
    
    # Threat Operations
    THREAT_INTEL_READ = "threat:intel:read"
    THREAT_INTEL_WRITE = "threat:intel:write"
    
    # Moderation
    MODERATE_REPORTS = "moderation:reports:write"
    MODERATE_USERS = "moderation:users:trust"
    
    # Analytics & AI
    ANALYTICS_READ = "analytics:view"
    AI_METRICS_READ = "ai:metrics:view"
    
    # Audit & Read Only
    AUDIT_READ = "audit:logs:view"
    READ_ONLY_GLOBAL = "global:read_only"

class RoleDefinition(BaseModel):
    role_id: str
    name: str
    description: str
    is_custom: bool = False
    permissions: Set[SystemPermission]

class RoleManagementService:
    """Enterprise Role & Permission Management Service Engine."""

    def __init__(self):
        self._roles: Dict[str, RoleDefinition] = {}
        self._bootstrap_builtin_roles()

    def _bootstrap_builtin_roles(self):
        """Initializes default built-in enterprise roles."""
        builtins = [
            RoleDefinition(
                role_id="SUPER_ADMIN",
                name="Super Administrator",
                description="Unrestricted system-wide access to all management consoles and configuration settings.",
                is_custom=False,
                permissions={SystemPermission.ALL_ACCESS}
            ),
            RoleDefinition(
                role_id="ADMIN",
                name="Administrator",
                description="Administrative control over users, system telemetry, and audit logs.",
                is_custom=False,
                permissions={
                    SystemPermission.ADMIN_MANAGE_USERS,
                    SystemPermission.ADMIN_SYSTEM_HEALTH,
                    SystemPermission.THREAT_INTEL_READ,
                    SystemPermission.MODERATE_REPORTS,
                    SystemPermission.ANALYTICS_READ,
                    SystemPermission.AUDIT_READ
                }
            ),
            RoleDefinition(
                role_id="MODERATOR",
                name="Community Moderator",
                description="Manages community scam report moderation queue and user reputation trust scores.",
                is_custom=False,
                permissions={
                    SystemPermission.MODERATE_REPORTS,
                    SystemPermission.MODERATE_USERS,
                    SystemPermission.THREAT_INTEL_READ
                }
            ),
            RoleDefinition(
                role_id="ANALYST",
                name="SOC Analyst",
                description="Monitors real-time threat intelligence feeds, AI model metrics, and analytics.",
                is_custom=False,
                permissions={
                    SystemPermission.THREAT_INTEL_READ,
                    SystemPermission.THREAT_INTEL_WRITE,
                    SystemPermission.ANALYTICS_READ,
                    SystemPermission.AI_METRICS_READ
                }
            ),
            RoleDefinition(
                role_id="DEVELOPER",
                name="Platform Developer",
                description="Access to API key management, system health telemetry, and developer logs.",
                is_custom=False,
                permissions={
                    SystemPermission.ADMIN_SYSTEM_HEALTH,
                    SystemPermission.AI_METRICS_READ,
                    SystemPermission.ANALYTICS_READ
                }
            ),
            RoleDefinition(
                role_id="READ_ONLY",
                name="Read Only Auditor",
                description="Read-only visibility for compliance auditing and governance reviews.",
                is_custom=False,
                permissions={
                    SystemPermission.READ_ONLY_GLOBAL,
                    SystemPermission.AUDIT_READ,
                    SystemPermission.ANALYTICS_READ
                }
            )
        ]
        for r in builtins:
            self._roles[r.role_id] = r

    def get_all_roles(self) -> List[RoleDefinition]:
        """Retrieves all registered built-in and custom roles."""
        return list(self._roles.values())

    def create_custom_role(self, name: str, description: str, permissions: List[SystemPermission]) -> RoleDefinition:
        """Creates a new dynamic custom enterprise role."""
        role_id = f"CUSTOM_{name.upper().replace(' ', '_')}"
        role_def = RoleDefinition(
            role_id=role_id,
            name=name,
            description=description,
            is_custom=True,
            permissions=set(permissions)
        )
        self._roles[role_id] = role_def
        return role_def

    def has_permission(self, role_id: str, required_permission: SystemPermission) -> bool:
        """Sub-1ms set-based permission check."""
        role = self._roles.get(role_id)
        if not role:
            return False

        if SystemPermission.ALL_ACCESS in role.permissions:
            return True

        return required_permission in role.permissions

role_management_service = RoleManagementService()
