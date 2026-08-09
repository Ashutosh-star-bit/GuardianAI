"""
GuardianAI AI Response Parser & JSON Validation Pipeline
Purpose: Extracts raw JSON objects from LLM text outputs (stripping markdown backticks) and validates outputs against Pydantic schemas.
"""

import json
import re
from typing import Type, TypeVar, Any, Dict
from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)

class AIResponseParseException(Exception):
    """Raised when raw AI output cannot be parsed into valid JSON."""
    pass

class AIResponseValidationError(Exception):
    """Raised when parsed JSON fails Pydantic schema validation."""
    pass

class AIResponseParser:
    """Parser and validator for LLM text outputs."""

    @staticmethod
    def extract_json_string(raw_output: str) -> str:
        """Strips markdown code blocks (```json ... ```) and extracts raw JSON string."""
        if not raw_output or not isinstance(raw_output, str):
            raise AIResponseParseException("Empty or non-string AI response output.")

        text = raw_output.strip()

        # Remove markdown code block fences
        match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
        if match:
            return match.group(1).strip()

        # Look for curly brace JSON boundaries
        start_idx = text.find("{")
        end_idx = text.rfind("}")
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            return text[start_idx:end_idx + 1].strip()

        return text

    @classmethod
    def parse_and_validate(cls, raw_output: str, schema_class: Type[T]) -> T:
        """
        Extracts JSON string, parses into Python dict, and validates against Pydantic schema_class.
        """
        json_str = cls.extract_json_string(raw_output)

        try:
            parsed_dict = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise AIResponseParseException(f"Failed to parse AI output as JSON: {str(e)}. Raw extracted text: '{json_str[:200]}'") from e

        try:
            validated_model = schema_class.model_validate(parsed_dict)
            return validated_model
        except ValidationError as e:
            raise AIResponseValidationError(f"AI response failed Pydantic schema validation: {str(e)}") from e
