"""
GuardianAI Feature Flag Pytest Suite
"""

import pytest
from app.core.feature_flags import FeatureFlagService, FeatureKey

@pytest.fixture
def ff_service():
    return FeatureFlagService()

def test_feature_flags_default_enabled(ff_service):
    assert ff_service.is_enabled(FeatureKey.OCR_PROCESSOR) is True
    assert ff_service.is_enabled(FeatureKey.VOICE_INTELLIGENCE) is True
    assert ff_service.is_enabled(FeatureKey.COMMUNITY_INTELLIGENCE) is True

def test_feature_flag_toggle(ff_service):
    # Disable Voice Intelligence
    ff_service.set_feature_status(FeatureKey.VOICE_INTELLIGENCE, False)
    assert ff_service.is_enabled(FeatureKey.VOICE_INTELLIGENCE) is False

    # Re-enable
    ff_service.set_feature_status(FeatureKey.VOICE_INTELLIGENCE, True)
    assert ff_service.is_enabled(FeatureKey.VOICE_INTELLIGENCE) is True

def test_get_all_flags(ff_service):
    flags = ff_service.get_all_flags()
    assert len(flags) == 7
