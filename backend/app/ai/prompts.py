"""
GuardianAI Prompt Templates & Versioning System
Purpose: Provides versioned, immutable prompt templates for system and user prompts, supporting parameter interpolation and template auditing.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class VersionedPromptTemplate(BaseModel):
    """Immutable prompt template model with version tag, system prompt, and user prompt template."""
    template_id: str
    version: str = Field(description="Semantic version string e.g. v1.0.0")
    system_prompt: str
    user_prompt_template: str
    description: str

    def format_user_prompt(self, **kwargs: Any) -> str:
        """Formats the user prompt template with provided keyword parameters."""
        return self.user_prompt_template.format(**kwargs)

class PromptRegistry:
    """Registry maintaining versioned prompt templates for threat inspection tasks."""
    _templates: Dict[str, Dict[str, VersionedPromptTemplate]] = {}

    @classmethod
    def register(cls, template: VersionedPromptTemplate) -> None:
        """Registers a prompt template revision."""
        if template.template_id not in cls._templates:
            cls._templates[template.template_id] = {}
        cls._templates[template.template_id][template.version] = template

    @classmethod
    def get(cls, template_id: str, version: Optional[str] = None) -> VersionedPromptTemplate:
        """Retrieves a specific version or the latest registered template version."""
        if template_id not in cls._templates:
            raise KeyError(f"Prompt template '{template_id}' not found in registry.")

        versions = cls._templates[template_id]
        if version:
            if version not in versions:
                raise KeyError(f"Version '{version}' for template '{template_id}' not found.")
            return versions[version]

        # Return latest registered version
        latest_version = sorted(versions.keys())[-1]
        return versions[latest_version]

# Register Standard Default Threat Analysis Prompt Template (v1.0.0)
PromptRegistry.register(
    VersionedPromptTemplate(
        template_id="threat_analysis_generic",
        version="v1.0.0",
        system_prompt=(
            "You are GuardianAI, an expert Explainable AI (XAI) cybersecurity threat intelligence engine. "
            "Your task is to analyze user-provided payloads (text, emails, URLs, QR codes) for fraud, smishing, BEC, or typosquatting. "
            "You must return ONLY a structured JSON response matching the required schema."
        ),
        user_prompt_template=(
            "Inspect the following {payload_type} payload for scam indicators:\n\n"
            "Payload Content:\n{raw_content}\n\n"
            "Analyze artificial urgency, spoofed domains, impersonation tactics, and return your structured threat evaluation."
        ),
        description="Default Explainable AI threat analysis prompt template v1.0.0"
    )
)
