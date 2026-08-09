"""
GuardianAI Platform Settings API Endpoint
Purpose: Serves system settings, developer API key regeneration, PII scrubbing preferences, and Enterprise Config.
"""

from typing import Dict, Any
from fastapi import APIRouter, Request, Depends, status, Body
from app.core.response import success_response
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/settings", tags=["Settings"])

# Global Enterprise System Configuration Store
enterprise_system_config: Dict[str, Any] = {
    "ai": {
        "model_variant": "gemini-1.5-flash",
        "temperature": 0.2,
        "max_output_tokens": 1024,
        "fallback_trigger_rate_limit": 5
    },
    "api": {
        "rate_limit_per_min": 1000,
        "api_key_expiration_days": 365,
        "cors_origins": ["*"]
    },
    "security": {
        "session_timeout_minutes": 30,
        "password_expiration_days": 90,
        "max_failed_attempts": 5,
        "enforce_mfa": True
    },
    "uploads": {
        "max_upload_size_mb": 10,
        "verify_magic_signatures": True,
        "allowed_mime_types": ["image/jpeg", "image/png", "application/pdf"]
    },
    "ocr": {
        "default_language": "eng+hin",
        "binarization_threshold": 128,
        "worker_threads": 4
    },
    "voice": {
        "stt_engine": "whisper-medium",
        "silence_suppression_ms": 500,
        "audio_cache_ttl_sec": 86400
    },
    "notifications": {
        "admin_alert_email": "security-alerts@guardianai.io",
        "telegram_webhook_enabled": True,
        "alert_severity_threshold": "HIGH"
    },
    "extension": {
        "client_edge_pii_scrubbing": True,
        "auto_update_check_hrs": 24
    },
    "community": {
        "approved_report_reputation_pts": 5,
        "rejected_report_penalty_pts": -10,
        "spam_strike_penalty_pts": -30
    },
    "analytics": {
        "log_retention_days": 90,
        "anonymize_user_ips": True,
        "ws_telemetry_freq_ms": 1000
    }
}

@router.get("", status_code=status.HTTP_200_OK, summary="Get Basic System Settings")
def get_system_settings(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Returns application settings, developer API key, and scrubbing status."""
    settings_payload = {
        "api_key": "gai_live_88f92a110099xza21_prod",
        "rate_limit_sla": "1,000 requests / minute",
        "pii_scrubbing": "STRICT Client & Edge Enforcement",
        "homoglyph_detection": True,
        "senior_mode_support": True
    }

    return success_response(
        data=settings_payload,
        message="System settings retrieved.",
        request=request
    )

@router.get("/admin", status_code=status.HTTP_200_OK, summary="Get Full Enterprise Admin Configuration")
def get_enterprise_settings():
    """Retrieves full 10-module Enterprise Admin Configuration dictionary."""
    return {
        "success": True,
        "message": "Enterprise configuration retrieved successfully.",
        "config": enterprise_system_config
    }

@router.put("/admin", status_code=status.HTTP_200_OK, summary="Update Enterprise Admin Configuration")
def update_enterprise_settings(payload: Dict[str, Any] = Body(...)):
    """Updates and persists Enterprise Admin Configuration settings."""
    global enterprise_system_config
    for module_key, settings_dict in payload.items():
        if module_key in enterprise_system_config and isinstance(settings_dict, dict):
            enterprise_system_config[module_key].update(settings_dict)

    return {
        "success": True,
        "message": "Enterprise settings updated successfully.",
        "config": enterprise_system_config
    }
