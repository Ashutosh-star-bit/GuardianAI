"""
GuardianAI Robust JSON Validation & Auto-Repair Pipeline
Purpose: Parses raw LLM text outputs, auto-repairs malformed JSON syntax (markdown fences, trailing commas, single quotes, unquoted keys),
         and validates payloads against Pydantic v2 schemas with detailed error diagnostics.
"""

import json
import re
from typing import Type, TypeVar, Any, Dict, List, Tuple
from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)

class JSONValidationError(Exception):
    """Raised when JSON parsing or Pydantic schema validation fails after auto-repair attempts."""
    def __init__(self, message: str, errors: List[Dict[str, str]] = None):
        super().__init__(message)
        self.message = message
        self.errors = errors or []

class JSONValidationEngine:
    """Robust JSON extraction, syntax auto-repair, and Pydantic schema validator."""

    @staticmethod
    def strip_markdown_fences(text: str) -> str:
        """Removes markdown code blocks (```json ... ```) from raw LLM string."""
        if not text:
            return ""
        text_str = text.strip()
        match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text_str, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return text_str

    @classmethod
    def auto_repair_json_syntax(cls, raw_json_str: str) -> str:
        """
        Attempts heuristics to auto-repair malformed LLM JSON string syntax:
        1. Strips markdown fences
        2. Fixes single quotes to double quotes
        3. Removes trailing commas before closing braces/brackets
        4. Adds quotes around unquoted object keys
        """
        cleaned = cls.strip_markdown_fences(raw_json_str)

        # 1. Replace single quotes wrapping keys/values with double quotes
        # Matches 'key': or 'value'
        cleaned = re.sub(r"(?<=[{\s,])'([a-zA-Z0-9_]+)':", r'"\1":', cleaned)
        cleaned = re.sub(r":\s*'([^'\"]*)'", r': "\1"', cleaned)

        # 2. Fix unquoted keys: {threat_score: 90} -> {"threat_score": 90}
        cleaned = re.sub(r"(?<=[{\s,])([a-zA-Z_][a-zA-Z0-9_]*)\s*:", r'"\1":', cleaned)

        # 3. Remove trailing commas in objects and arrays: {"a": 1,} -> {"a": 1}
        cleaned = re.sub(r",\s*([}\]])", r"\1", cleaned)

        # 4. Extract outer JSON bounds if trailing conversational filler text exists
        start_idx = cleaned.find("{")
        end_idx = cleaned.rfind("}")
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            cleaned = cleaned[start_idx:end_idx + 1]

        return cleaned.strip()

    @classmethod
    def parse_json(cls, raw_output: str) -> Tuple[Dict[str, Any], bool]:
        """
        Parses raw text into Python dict.
        Returns tuple of (parsed_dict, was_repaired_boolean).
        """
        if not raw_output or not isinstance(raw_output, str):
            raise JSONValidationError("Raw LLM output is empty or non-string.")

        # Attempt 1: Direct JSON parse
        cleaned_first = cls.strip_markdown_fences(raw_output)
        try:
            parsed = json.loads(cleaned_first)
            return parsed, False
        except json.JSONDecodeError:
            pass

        # Attempt 2: Auto-repair malformed syntax
        repaired_str = cls.auto_repair_json_syntax(raw_output)
        try:
            parsed = json.loads(repaired_str)
            return parsed, True
        except json.JSONDecodeError as e:
            raise JSONValidationError(
                message=f"JSON parsing failed after auto-repair heuristics: {str(e)}",
                errors=[{"field": "json_syntax", "issue": str(e)}]
            ) from e

    @classmethod
    def validate_and_repair(cls, raw_output: str, schema_class: Type[T]) -> T:
        """
        Parses, auto-repairs, and validates raw LLM output against target Pydantic schema_class.
        Returns validated Pydantic model instance.
        """
        parsed_dict, was_repaired = cls.parse_json(raw_output)

        try:
            validated_model = schema_class.model_validate(parsed_dict)
            return validated_model
        except ValidationError as e:
            formatted_errors = [
                {
                    "field": ".".join(str(loc) for loc in err["loc"]),
                    "issue": err["msg"]
                }
                for err in e.errors()
            ]
            raise JSONValidationError(
                message=f"Pydantic schema validation failed for '{schema_class.__name__}'.",
                errors=formatted_errors
            ) from e
