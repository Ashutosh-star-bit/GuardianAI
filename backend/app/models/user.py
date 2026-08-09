"""
GuardianAI User SQLAlchemy 2.0 ORM Model
Purpose: Defines the users table schema with role-based authorization, soft delete, status flags, and scan relationship.
"""

from typing import List, TYPE_CHECKING
from sqlalchemy import String, Boolean, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin, DictSerializerMixin

if TYPE_CHECKING:
    from app.models.scan import Scan

class User(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin, DictSerializerMixin):
    """User Entity Model representing registered accounts."""
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
        comment="User primary email address (lowercase)"
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="BCrypt/Argon2 cryptographic password hash"
    )
    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        comment="User full display name"
    )
    role: Mapped[str] = mapped_column(
        String(50),
        default="user",
        nullable=False,
        index=True,
        comment="Role-based access control (user, admin, analyst)"
    )
    subscription_tier: Mapped[str] = mapped_column(
        String(32),
        default="free",
        nullable=False,
        comment="Tier: free, pro, enterprise"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Account active status flag"
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Email verification status flag"
    )

    # Relationships
    scans: Mapped[List["Scan"]] = relationship(
        "Scan",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    __table_args__ = (
        Index("ix_users_email_active", "email", "is_active"),
        Index("ix_users_role_status", "role", "is_active"),
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, role={self.role}, is_active={self.is_active})>"
