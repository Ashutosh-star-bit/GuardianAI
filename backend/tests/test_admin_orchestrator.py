"""
GuardianAI Enterprise Admin Orchestrator Pytest Suite
"""

import pytest
from app.admin.admin_orchestrator import EnterpriseAdminOrchestrator

@pytest.fixture
def admin_orchestrator():
    return EnterpriseAdminOrchestrator()

def test_command_center_metrics(admin_orchestrator):
    metrics = admin_orchestrator.get_command_center_metrics()
    assert metrics["system_health"] == "HEALTHY"
    assert "cpu_usage_percent" in metrics["infrastructure"]
    assert metrics["active_scans_per_sec"] > 0

def test_ai_token_metrics(admin_orchestrator):
    ai_metrics = admin_orchestrator.get_ai_token_metrics()
    assert ai_metrics["total_tokens_consumed_today"] > 0
    assert "average_latency_ms" in ai_metrics

def test_admin_audit_logging(admin_orchestrator):
    admin_orchestrator.log_admin_action("mod_admin", "REVOKE_API_KEY", "key_100", "Compromised key")
    logs = admin_orchestrator.get_audit_logs()
    assert len(logs) == 1
    assert logs[0]["action"] == "REVOKE_API_KEY"

def test_system_broadcast_creation(admin_orchestrator):
    b = admin_orchestrator.create_system_broadcast("Security Alert", "High volume digital arrest scam reported", "WARNING")
    assert b["severity"] == "WARNING"
    assert b["title"] == "Security Alert"
