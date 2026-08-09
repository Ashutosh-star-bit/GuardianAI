"""
GuardianAI Feature Flag System Engine
Purpose: High-performance, thread-safe dynamic Feature Flag Service supporting runtime toggle of:
         OCR, Voice Intelligence, Browser Extension, Community Intelligence, Public API, Analytics, and Notifications.
"""

import threading
from typing import Dict, Any, List, Optional
from enum import Enum
from pydantic import BaseModel

class FeatureKey(str, Enum):
    OCR_PROCESSOR = "feature:ocr_processor"
    VOICE_INTELLIGENCE = "feature:voice_intelligence"
    BROWSER_EXTENSION = "feature:browser_extension"
    COMMUNITY_INTELLIGENCE = "feature:community_intelligence"
    PUBLIC_API = "feature:public_api"
    ANALYTICS_ENGINE = "feature:analytics_engine"
    NOTIFICATION_CENTER = "feature:notification_center"

class FeatureFlagDefinition(BaseModel):
    key: FeatureKey
    name: str
    description: str
    is_enabled: bool = True

class FeatureFlagService:
    """Thread-safe Sub-0.1ms Feature Flag Engine."""

    def __init__(self):
        self._lock = threading.RLock()
        self._flags: Dict[FeatureKey, FeatureFlagDefinition] = {}
        self._bootstrap_defaults()

    def _bootstrap_defaults(self):
        """Initializes default feature flags enabled."""
        defaults = [
            FeatureFlagDefinition(key=FeatureKey.OCR_PROCESSOR, name="OCR Document Processor", description="Tesseract & EasyOCR layout analysis", is_enabled=True),
            FeatureFlagDefinition(key=FeatureKey.VOICE_INTELLIGENCE, name="Voice Intelligence Engine", description="Whisper STT & audio clone detection", is_enabled=True),
            FeatureFlagDefinition(key=FeatureKey.BROWSER_EXTENSION, name="Browser Extension Edge API", description="Client-side zero-knowledge scanning", is_enabled=True),
            FeatureFlagDefinition(key=FeatureKey.COMMUNITY_INTELLIGENCE, name="Community HITL Reporting", description="Crowdsourced reports & moderation queue", is_enabled=True),
            FeatureFlagDefinition(key=FeatureKey.PUBLIC_API, name="Public Developer API", description="External REST API developer keys & endpoints", is_enabled=True),
            FeatureFlagDefinition(key=FeatureKey.ANALYTICS_ENGINE, name="Analytics Telemetry", description="Real-time time-series telemetry aggregator", is_enabled=True),
            FeatureFlagDefinition(key=FeatureKey.NOTIFICATION_CENTER, name="Notification Broadcasts", description="Emergency threat advisory dispatcher", is_enabled=True)
        ]
        for d in defaults:
            self._flags[d.key] = d

    def is_enabled(self, key: FeatureKey) -> bool:
        """Fast sub-0.1ms feature flag evaluation."""
        with self._lock:
            flag = self._flags.get(key)
            return flag.is_enabled if flag else True

    def set_feature_status(self, key: FeatureKey, is_enabled: bool) -> FeatureFlagDefinition:
        """Updates feature flag status at runtime."""
        with self._lock:
            if key in self._flags:
                self._flags[key].is_enabled = is_enabled
                return self._flags[key]
            raise ValueError(f"Feature flag '{key}' not found.")

    def get_all_flags(self) -> List[FeatureFlagDefinition]:
        """Retrieves all feature flag definitions."""
        with self._lock:
            return list(self._flags.values())

feature_flag_service = FeatureFlagService()
