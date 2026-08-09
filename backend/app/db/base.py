"""
GuardianAI Reusable SQLAlchemy 2.0 Base Models & Mixins
Purpose: Provides thread-safe declarative base class, UUID v4 primary keys, timezone-aware UTC timestamps,
         soft-delete mechanisms, and dictionary serialization mixins for all database ORM entities.
"""

import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from sqlalchemy import String, DateTime, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    """Abstract Declarative Base Class for all SQLAlchemy ORM models."""
    pass

class UUIDMixin:
    """Mixin adding standard 36-character UUID primary key string."""
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )

class TimestampMixin:
    """Mixin adding auto-managed timezone-aware created_at and updated_at UTC timestamps."""
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

class SoftDeleteMixin:
    """Mixin providing non-destructive soft-delete capability."""
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
        index=True
    )

    @property
    def is_deleted(self) -> bool:
        """Returns True if record has been soft-deleted."""
        return self.deleted_at is not None

    def soft_delete(self) -> None:
        """Marks record as deleted with current UTC timestamp."""
        self.deleted_at = datetime.now(timezone.utc)

    def restore(self) -> None:
        """Restores a soft-deleted record by clearing deleted_at timestamp."""
        self.deleted_at = None

class DictSerializerMixin:
    """Mixin adding to_dict helper method for JSON serialization."""
    def to_dict(self, exclude: Optional[set] = None) -> Dict[str, Any]:
        """Converts model instance attributes into a Python dictionary."""
        exclude = exclude or set()
        result = {}
        for col in self.__table__.columns:
            if col.name in exclude:
                continue
            val = getattr(self, col.name)
            if isinstance(val, datetime):
                val = val.isoformat()
            result[col.name] = val
        return result

class FullBaseModel(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin, DictSerializerMixin):
    """
    Abstract Master Base Model combining UUID v4 primary key, UTC timestamps,
    soft-delete mechanics, and dictionary serialization.
    """
    __abstract__ = True
