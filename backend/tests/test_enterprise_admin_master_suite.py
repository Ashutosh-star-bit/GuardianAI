"""
GuardianAI Enterprise Admin Master Integration Pytest Suite
Purpose: End-to-end master test suite verifying all 10 Enterprise Admin Dashboards & Subsystems:
         1. Master Command Center Dashboard Telemetry
         2. User & Role Management (RBAC Matrix)
         3. Threat Intelligence IOC Feed Operations
         4. AI Token & Cost Metering Analytics
         5. Platform Analytics Engine (DAU, MAU, Accuracy, SLA)
         6. Immutable Compliance Audit Logs (SHA-256 Hash Chain)
         7. Notification & Security Alert Broadcast Center
         8. Secure Export Center (CSV / JSON with Formula Injection Shield)
         9. Dynamic Feature Flags Engine
        10. Enterprise Master Settings & Security Defenses
"""

import pytest
from fastapi.testclient import TestClient
from main import app
from app.admin.admin_orchestrator import enterprise_admin_orchestrator
from app.analytics.analytics_engine import platform_analytics_engine
from app.core.admin_auth import enterprise_admin_auth_service, AdminRole, AdminPermission
from app.core.role_management import role_management_service, SystemPermission
from app.core.feature_flags import feature_flag_service, FeatureKey
from app.core.admin_security import enterprise_admin_security_engine
from app.admin.export_center import secure_export_engine
from app.models.audit_log import AuditLog

@pytest.fixture
def client():
    return TestClient(app)

def test_01_command_center_telemetry(client):
    metrics = enterprise_admin_orchestrator.get_command_center_metrics()
    assert metrics["system_health"] == "HEALTHY"
    assert "cpu_usage_percent" in metrics["infrastructure"]

    response = client.get("/api/v1/admin/command-center")
    assert response.status_code == 200
    assert response.json()["data"]["system_health"] == "HEALTHY"

def test_02_user_and_role_management(client):
    login_res = enterprise_admin_auth_service.authenticate_admin("admin_master", "AdminSecurePassword123!", mfa_code="123456")
    assert login_res["role"] == "SUPER_ADMIN"

    # Verify Builtin Roles
    roles = role_management_service.get_all_roles()
    assert len(roles) >= 6

    # Create Custom Role
    custom = role_management_service.create_custom_role("SOC Lead", "Lead analyst role", [SystemPermission.THREAT_INTEL_READ])
    assert custom.role_id == "CUSTOM_SOC_LEAD"

def test_03_threat_intel_analytics(client):
    response = client.get("/api/v1/community/trending")
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True
    assert "top_scam_categories" in res["data"]

def test_04_ai_token_metrics(client):
    ai_metrics = enterprise_admin_orchestrator.get_ai_token_metrics()
    assert ai_metrics["total_tokens_consumed_today"] > 0

    response = client.get("/api/v1/admin/ai-metrics")
    assert response.status_code == 200
    assert response.json()["data"]["gemini_flash_tokens"] > 0

def test_05_platform_analytics_engine():
    summary = platform_analytics_engine.get_realtime_analytics_summary()
    assert summary["daily_active_users_dau"] == 14280
    assert summary["monthly_active_users_mau"] == 128400
    assert summary["detection_accuracy_percent"] > 95.0

def test_06_immutable_audit_logs():
    h0 = "0" * 64
    h1 = AuditLog.compute_record_hash("usr_admin", "LOGIN", "AUTH", "2026-08-01T04:00:00Z", h0)
    assert len(h1) == 64

    logs_chain = [
        {"id": "1", "previous_hash": h0, "record_hash": h1}
    ]
    assert enterprise_admin_security_engine.verify_audit_log_chain_integrity(logs_chain) is True

def test_07_notification_broadcast(client):
    payload = {"title": "Cyber Security Warning", "message": "Digital arrest surge", "severity": "CRITICAL"}
    response = client.post("/api/v1/admin/broadcast", json=payload)
    assert response.status_code == 201
    assert response.json()["data"]["severity"] == "CRITICAL"

def test_08_secure_export_center():
    unsafe_val = "=CMD|' /C calc'!A0"
    clean_val = secure_export_engine.sanitize_csv_value(unsafe_val)
    assert clean_val.startswith("'=")

    data = [{"id": "1", "payload": unsafe_val}]
    csv_str = secure_export_engine.export_to_csv(data)
    assert "'=CMD" in csv_str

def test_09_feature_flags_engine(client):
    assert feature_flag_service.is_enabled(FeatureKey.OCR_PROCESSOR) is True

    # Toggle via API
    response = client.put("/api/v1/feature-flags/feature:ocr_processor?is_enabled=false")
    assert response.status_code == 200
    assert response.json()["data"]["is_enabled"] is False

    # Restore
    client.put("/api/v1/feature-flags/feature:ocr_processor?is_enabled=true")

def test_10_enterprise_settings_api(client):
    response = client.get("/api/v1/settings/admin")
    assert response.status_code == 200
    assert "ai" in response.json()["config"]

    update_payload = {"ai": {"temperature": 0.1}}
    update_res = client.put("/api/v1/settings/admin", json=update_payload)
    assert update_res.status_code == 200
    assert update_res.json()["config"]["ai"]["temperature"] == 0.1
