"""
GuardianAI Prompt Versioning & Rollback Unit Test Suite
Purpose: Tests prompt metadata registration, active version resolution, listing versions, and rollback mechanics.
"""

import pytest
from app.ai.prompt_versioning import (
    PromptVersionManager,
    PromptVersionRecord,
    PromptStatus
)

def test_prompt_version_registration():
    """Tests registering prompt versions with complete metadata."""
    active = PromptVersionManager.get_active_version("smishing_detector")
    assert active.id == "smishing_detector"
    assert active.version == "v1.0.0"
    assert active.owner == "sec-team@guardianai.io"
    assert active.status == PromptStatus.ACTIVE
    assert active.created_date is not None

def test_prompt_rollback():
    """Tests rolling back active prompt to a previous version."""
    # Register v2.0.0 as ACTIVE
    v2 = PromptVersionRecord(
        id="smishing_detector",
        version="v2.0.0",
        description="Major update v2.0.0",
        owner="sec-team@guardianai.io",
        status=PromptStatus.ACTIVE,
        system_prompt="v2 system prompt",
        user_prompt="v2 user prompt"
    )
    PromptVersionManager.register_version(v2)

    # Currently active should be v2.0.0
    assert PromptVersionManager.get_active_version("smishing_detector").version == "v2.0.0"

    # Rollback to v1.0.0
    rolled_back = PromptVersionManager.rollback_template("smishing_detector", "v1.0.0")
    assert rolled_back.version == "v1.0.0"
    assert rolled_back.status == PromptStatus.ACTIVE

    # Check active version after rollback is v1.0.0
    assert PromptVersionManager.get_active_version("smishing_detector").version == "v1.0.0"

def test_list_versions():
    """Tests listing all registered versions for a template ID."""
    versions = PromptVersionManager.list_versions("smishing_detector")
    assert len(versions) >= 2
    ver_strings = [v.version for v in versions]
    assert "v1.0.0" in ver_strings
    assert "v2.0.0" in ver_strings
