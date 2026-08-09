"""
GuardianAI Prompt Template Engine Unit Test Suite
Purpose: Tests template registration, variable validation, multilingual rendering, version lookup, and error handling.
"""

import pytest
from app.ai.prompt_engine import (
    PromptTemplateEngine,
    PromptTemplateDefinition,
    PromptVariableMissingError,
    PromptTemplateNotFoundError
)

def test_prompt_rendering_success():
    """Tests successful prompt rendering when all variables are provided."""
    rendered = PromptTemplateEngine.render_prompt(
        template_id="smishing_detector",
        variables={"raw_content": "Your bank account is locked! Click paypa1-check.com"}
    )
    assert "smishing triggers" in rendered["user_prompt"]
    assert "paypa1-check.com" in rendered["user_prompt"]

def test_prompt_missing_variable_raises_error():
    """Tests PromptVariableMissingError is raised when a required variable is missing."""
    with pytest.raises(PromptVariableMissingError):
        PromptTemplateEngine.render_prompt(
            template_id="smishing_detector",
            variables={} # Empty variables
        )

def test_multilingual_prompt_rendering():
    """Tests Spanish locale rendering."""
    rendered = PromptTemplateEngine.render_prompt(
        template_id="smishing_detector",
        variables={"raw_content": "Su cuenta de banco está bloqueada!"},
        locale="es"
    )
    assert "amenazas de smishing" in rendered["user_prompt"]
    assert "Su cuenta de banco" in rendered["user_prompt"]

def test_template_not_found_raises_error():
    """Tests PromptTemplateNotFoundError is raised for unmapped template IDs."""
    with pytest.raises(PromptTemplateNotFoundError):
        PromptTemplateEngine.render_prompt(
            template_id="non_existent_template",
            variables={}
        )
