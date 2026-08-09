"""
GuardianAI Pipeline AnalysisContext State Manager
Purpose: Thread-safe, stateful AnalysisContext DTO storing Request ID, Scan ID, Timestamp, User ID, Input Format,
         Original Input, Extracted Indicators, Threat Intelligence, Decision, Executive Report, Metadata, and Execution Latency.
"""

import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, ConfigDict

class AnalysisContext(BaseModel):
    """Pipeline Execution State Context DTO passed through all pipeline stages."""
    request_id: str = Field(description="Unique request correlation ID e.g. req_8f92a11009")
    scan_id: str = Field(description="Unique scan payload ID e.g. scn_9901a11009")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    user_id: Optional[str] = Field(default=None, description="Authenticated User ID if present")
    input_type: str = Field(default="TEXT", description="TEXT, EMAIL, URL, QR, JSON, OCR, VOICE")
    original_input: str
    cleaned_text: Optional[str] = None
    extracted_indicators: Optional[Dict[str, Any]] = None
    text_intelligence: Optional[Dict[str, Any]] = None
    threat_intelligence: Optional[Dict[str, Any]] = None
    gemini_analysis: Optional[Dict[str, Any]] = None
    decision: Optional[Dict[str, Any]] = None
    executive_report: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    start_time_perf: float = Field(default_factory=time.perf_counter, exclude=True)
    execution_time_ms: float = Field(default=0.0, description="Total pipeline execution latency in milliseconds")

    # Future Extensibility: Allow arbitrary runtime context attachments
    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)

    def mark_completed(self) -> float:
        """Calculates total elapsed latency in milliseconds and marks completion time."""
        elapsed = (time.perf_counter() - self.start_time_perf) * 1000.0
        self.execution_time_ms = round(elapsed, 2)
        return self.execution_time_ms

    def set_metadata(self, key: str, value: Any) -> None:
        """Sets a key/value pair in runtime metadata dictionary."""
        self.metadata[key] = value
