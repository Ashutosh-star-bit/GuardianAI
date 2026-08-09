"""
GuardianAI Abstract BaseInputAdapter Interface
Purpose: Defines the polymorphic contract for all input format adapters.
"""

from abc import ABC, abstractmethod
from typing import Any
from app.adapters.schemas import UniversalAnalysisRequest

class BaseInputAdapter(ABC):
    """Abstract Base Class for all Polymorphic Input Adapters."""

    @abstractmethod
    async def adapt_to_request(self, raw_payload: Any, **kwargs: Any) -> UniversalAnalysisRequest:
        """Converts raw heterogeneous input payload into a standardized UniversalAnalysisRequest DTO."""
        pass
