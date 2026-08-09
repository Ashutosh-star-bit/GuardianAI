"""
GuardianAI Enterprise Prompt Template Engine
Purpose: Provides reusable, versioned, validated, and multilingual prompt template rendering,
         eliminating hardcoded prompt strings across the codebase.
"""

from typing import Dict, List, Set, Optional, Any
from pydantic import BaseModel, Field, field_validator

class PromptVariableMissingError(Exception):
    """Raised when required template variables are missing during rendering."""
    pass

class PromptTemplateNotFoundError(Exception):
    """Raised when a requested prompt template or version is not registered."""
    pass

class PromptTemplateDefinition(BaseModel):
    """Structured Prompt Template Definition DTO."""
    template_id: str = Field(description="Unique template identifier e.g. threat_analysis")
    version: str = Field(description="Semantic version string e.g. v1.0.0")
    locale: str = Field(default="en", description="Language locale code e.g. en, es, fr, hi")
    description: str
    required_variables: List[str] = Field(default_factory=list, description="List of required variable names")
    system_prompt: str
    user_prompt: str

    def validate_variables(self, provided_vars: Dict[str, Any]) -> None:
        """Validates that all required variables exist in provided_vars."""
        missing = [var for var in self.required_variables if var not in provided_vars or provided_vars[var] is None]
        if missing:
            raise PromptVariableMissingError(
                f"Missing required template variables for '{self.template_id}' [{self.version}]: {', '.join(missing)}"
            )

    def render(self, **kwargs: Any) -> Dict[str, str]:
        """
        Validates variables and renders system and user prompt strings.
        Returns dict with 'system_prompt' and 'user_prompt'.
        """
        self.validate_variables(kwargs)
        rendered_system = self.system_prompt.format(**kwargs) if self.system_prompt else ""
        rendered_user = self.user_prompt.format(**kwargs) if self.user_prompt else ""
        return {
            "system_prompt": rendered_system,
            "user_prompt": rendered_user
        }

class PromptTemplateEngine:
    """Enterprise Prompt Engine managing multilingual and multi-version prompt templates."""

    # Storage layout: _templates[template_id][locale][version] = PromptTemplateDefinition
    _templates: Dict[str, Dict[str, Dict[str, PromptTemplateDefinition]]] = {}

    @classmethod
    def register(cls, template: PromptTemplateDefinition) -> None:
        """Registers a prompt template definition into the global registry."""
        tid = template.template_id
        loc = template.locale.lower()
        ver = template.version

        if tid not in cls._templates:
            cls._templates[tid] = {}
        if loc not in cls._templates[tid]:
            cls._templates[tid][loc] = {}

        cls._templates[tid][loc][ver] = template

    @classmethod
    def get_template(
        cls,
        template_id: str,
        version: Optional[str] = None,
        locale: str = "en"
    ) -> PromptTemplateDefinition:
        """
        Retrieves requested prompt template by ID, locale, and version.
        Defaults to 'en' locale and latest version if unassigned.
        """
        loc = locale.lower()
        if template_id not in cls._templates:
            raise PromptTemplateNotFoundError(f"Template '{template_id}' is not registered.")

        locales = cls._templates[template_id]
        if loc not in locales:
            # Fallback to English if requested locale is missing
            loc = "en"
            if loc not in locales:
                raise PromptTemplateNotFoundError(f"Locale '{locale}' for template '{template_id}' is unavailable.")

        versions = locales[loc]
        if version:
            if version not in versions:
                raise PromptTemplateNotFoundError(f"Version '{version}' for template '{template_id}' ({loc}) not found.")
            return versions[version]

        # Return latest registered semantic version
        latest_ver = sorted(versions.keys())[-1]
        return versions[latest_ver]

    @classmethod
    def render_prompt(
        cls,
        template_id: str,
        variables: Dict[str, Any],
        version: Optional[str] = None,
        locale: str = "en"
    ) -> Dict[str, str]:
        """Convenience method to retrieve and render a prompt template in a single step."""
        template = cls.get_template(template_id=template_id, version=version, locale=locale)
        return template.render(**variables)

# Register Reusable Core Templates
PromptTemplateEngine.register(
    PromptTemplateDefinition(
        template_id="smishing_detector",
        version="v1.0.0",
        locale="en",
        description="SMS smishing threat analysis prompt",
        required_variables=["raw_content"],
        system_prompt=(
            "You are GuardianAI, a cybersecurity AI engine. "
            "Analyze SMS text messages for artificial urgency, impersonation, and zero-day links. "
            "Return JSON matching required schema."
        ),
        user_prompt=(
            "Inspect the following SMS message for smishing triggers:\n\n"
            "SMS Payload:\n{raw_content}\n\n"
            "Evaluate threat score (0 - 100) and risk band."
        )
    )
)

PromptTemplateEngine.register(
    PromptTemplateDefinition(
        template_id="smishing_detector",
        version="v1.0.0",
        locale="es",
        description="SMS smishing threat analysis prompt in Spanish",
        required_variables=["raw_content"],
        system_prompt=(
            "Eres GuardianAI, un motor de ciberseguridad con inteligencia artificial. "
            "Analiza mensajes SMS en busca de urgencia artificial, suplantación de identidad y enlaces maliciosos. "
            "Devuelve un objeto JSON con el formato requerido."
        ),
        user_prompt=(
            "Inspecciona el siguiente mensaje SMS en busca de amenazas de smishing:\n\n"
            "Contenido del SMS:\n{raw_content}\n\n"
            "Evalúa la puntuación de amenaza (0 - 100) y la banda de riesgo."
        )
    )
)
