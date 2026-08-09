"""
GuardianAI Prompt Versioning & Lifecycle Management Engine
Purpose: Manages prompt metadata (ID, version, created date, description, owner, status) and provides rollback capabilities.
"""

from datetime import datetime, timezone
from typing import Dict, List, Optional
from enum import Enum
from pydantic import BaseModel, Field

class PromptStatus(str, Enum):
    """Prompt Lifecycle Status Enum."""
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    DRAFT = "draft"
    ARCHIVED = "archived"

class PromptVersionRecord(BaseModel):
    """Metadata container for a versioned prompt template."""
    id: str = Field(description="Unique prompt template identifier e.g. smishing_detector")
    version: str = Field(description="Semantic version string e.g. v1.0.0")
    created_date: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    description: str = Field(description="Description of prompt changes or purpose")
    owner: str = Field(default="GuardianAI-Security-Team", description="Author or team owner")
    status: PromptStatus = Field(default=PromptStatus.ACTIVE)
    system_prompt: str
    user_prompt: str

class PromptVersionManager:
    """Prompt Lifecycle & Rollback Management Engine."""

    # Storage layout: _registry[template_id][version] = PromptVersionRecord
    _registry: Dict[str, Dict[str, PromptVersionRecord]] = {}

    @classmethod
    def register_version(cls, record: PromptVersionRecord) -> None:
        """Registers a new prompt version. If status is ACTIVE, deactivates older active versions."""
        tid = record.id
        ver = record.version

        if tid not in cls._registry:
            cls._registry[tid] = {}

        if record.status == PromptStatus.ACTIVE:
            # Mark previous ACTIVE versions as DEPRECATED
            for v_record in cls._registry[tid].values():
                if v_record.status == PromptStatus.ACTIVE:
                    v_record.status = PromptStatus.DEPRECATED

        cls._registry[tid][ver] = record

    @classmethod
    def get_active_version(cls, template_id: str) -> PromptVersionRecord:
        """Returns the currently ACTIVE version for a given template_id."""
        if template_id not in cls._registry:
            raise KeyError(f"Prompt template '{template_id}' is not registered.")

        for record in cls._registry[template_id].values():
            if record.status == PromptStatus.ACTIVE:
                return record

        # Fallback to latest registered version if none is marked ACTIVE
        latest_ver = sorted(cls._registry[template_id].keys())[-1]
        return cls._registry[template_id][latest_ver]

    @classmethod
    def rollback_template(cls, template_id: str, target_version: str) -> PromptVersionRecord:
        """
        Rolls back the active prompt template to target_version.
        Marks target_version as ACTIVE and all other versions as DEPRECATED.
        """
        if template_id not in cls._registry:
            raise KeyError(f"Prompt template '{template_id}' is not registered.")

        if target_version not in cls._registry[template_id]:
            raise KeyError(f"Version '{target_version}' for template '{template_id}' does not exist.")

        # Deactivate all versions
        for v_record in cls._registry[template_id].values():
            v_record.status = PromptStatus.DEPRECATED

        # Activate target version
        target_record = cls._registry[template_id][target_version]
        target_record.status = PromptStatus.ACTIVE
        return target_record

    @classmethod
    def list_versions(cls, template_id: str) -> List[PromptVersionRecord]:
        """Returns all registered version records for a template_id."""
        if template_id not in cls._registry:
            return []
        return sorted(list(cls._registry[template_id].values()), key=lambda x: x.version, reverse=True)

# Register Core Default Prompt Version Records
PromptVersionManager.register_version(
    PromptVersionRecord(
        id="smishing_detector",
        version="v1.0.0",
        description="Initial release of smishing detection prompt",
        owner="sec-team@guardianai.io",
        status=PromptStatus.ACTIVE,
        system_prompt="You are GuardianAI. Inspect SMS messages for fraud.",
        user_prompt="Inspect SMS payload: {raw_content}"
    )
)

PromptVersionManager.register_version(
    PromptVersionRecord(
        id="smishing_detector",
        version="v1.1.0",
        description="Added homoglyph domain age heuristics to smishing prompt",
        owner="sec-team@guardianai.io",
        status=PromptStatus.DRAFT,
        system_prompt="You are GuardianAI. Inspect SMS and zero-day links for fraud.",
        user_prompt="Inspect SMS payload and URLs: {raw_content}"
    )
)
