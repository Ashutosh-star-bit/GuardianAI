"""
GuardianAI Versioned AI Response Parser Engine
Purpose: Converts Gemini LLM text outputs into Python Pydantic DTO objects, handling malformed syntax,
         supporting versioned schemas, and raising clean domain exceptions.
"""

from typing import Type, TypeVar, Dict, Tuple, Optional, Any
from pydantic import BaseModel
from app.ai.json_validator import JSONValidationEngine, JSONValidationError
from app.ai.gemini_client import GeminiResponse

T = TypeVar("T", bound=BaseModel)

class AIParserException(Exception):
    """Base exception for AI Response Parser failures."""
    pass

class SchemaVersionNotFoundError(AIParserException):
    """Raised when a requested schema identifier or version tag is unmapped."""
    pass

class MalformedAIOutputError(AIParserException):
    """Raised when raw AI output cannot be repaired into valid JSON syntax."""
    pass

class SchemaValidationError(AIParserException):
    """Raised when repaired JSON fails Pydantic schema validation."""
    def __init__(self, message: str, errors: list = None):
        super().__init__(message)
        self.errors = errors or []

class SchemaRegistry:
    """Registry maintaining versioned Pydantic schema classes."""
    # Storage layout: _schemas[(schema_id, version)] = PydanticModelClass
    _schemas: Dict[Tuple[str, str], Type[BaseModel]] = {}

    @classmethod
    def register(cls, schema_id: str, version: str, schema_class: Type[BaseModel]) -> None:
        """Registers a versioned Pydantic schema class."""
        cls._schemas[(schema_id, version)] = schema_class

    @classmethod
    def get_schema(cls, schema_id: str, version: str = "v1.0.0") -> Type[BaseModel]:
        """Retrieves a registered Pydantic schema class by schema_id and version tag."""
        key = (schema_id, version)
        if key not in cls._schemas:
            raise SchemaVersionNotFoundError(f"Schema '{schema_id}' version '{version}' is not registered.")
        return cls._schemas[key]

class AIResponseParserEngine:
    """Enterprise parser converting Gemini LLM responses into versioned Python objects."""

    @classmethod
    def parse_gemini_response(
        cls,
        response_input: Any, # Accepts raw str or GeminiResponse object
        schema_id_or_class: Any,
        version: str = "v1.0.0"
    ) -> BaseModel:
        """
        Converts Gemini text or GeminiResponse into validated Pydantic object.
        Supports passing either a Pydantic class directly OR a schema_id string with version tag.
        """
        # 1. Extract raw text string
        if isinstance(response_input, GeminiResponse):
            raw_text = response_input.raw_text
        elif isinstance(response_input, str):
            raw_text = response_input
        else:
            raise AIParserException("Unsupported response_input type. Must be str or GeminiResponse.")

        # 2. Resolve target Pydantic schema class
        if isinstance(schema_id_or_class, str):
            target_schema_class = SchemaRegistry.get_schema(schema_id_or_class, version=version)
        elif issubclass(schema_id_or_class, BaseModel):
            target_schema_class = schema_id_or_class
        else:
            raise AIParserException("schema_id_or_class must be a schema_id string or a Pydantic BaseModel subclass.")

        # 3. Parse & Validate JSON with Auto-Repair
        try:
            validated_object = JSONValidationEngine.validate_and_repair(
                raw_output=raw_text,
                schema_class=target_schema_class
            )
            return validated_object
        except JSONValidationError as e:
            if "parsing failed" in str(e).lower():
                raise MalformedAIOutputError(f"Failed to extract valid JSON from Gemini output: {e.message}") from e
            else:
                raise SchemaValidationError(f"Gemini output failed schema validation: {e.message}", errors=e.errors) from e
