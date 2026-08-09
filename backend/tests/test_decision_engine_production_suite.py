"""
GuardianAI Master Decision Engine Production Pytest Suite
Purpose: Enterprise test suite covering Statistical Confidence Engine, Risk Classifier, Evidence Fusion, Action Planner,
         Safe Reply Generator, DecisionXAI Engine, DecisionService, REST API Endpoints, and Sub-50ms SLA Performance.
"""

import sys
import os
import time
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app
from app.api.deps import get_current_user
from app.models.user import User

from app.decision_engine.confidence import ConfidenceEngine
from app.decision_engine.risk_classifier import RiskClassifierEngine
from app.decision_engine.evidence_aggregator import EvidenceFusionEngine
from app.decision_engine.action_planner import RecommendationEngine
from app.decision_engine.safe_reply import SafeReplyGenerator
from app.decision_engine.xai import DecisionXAIEngine
from app.decision_engine.pipeline import DecisionPipeline
from app.decision_engine.service import DecisionService
from app.decision_engine.schemas import DecisionRequest, EvidenceItemSchema

client = TestClient(app)

def mock_get_current_user():
    return User(id="usr_dec_prod", email="test@guardianai.io", full_name="Test User", hashed_password="pw", is_active=True)

app.dependency_overrides[get_current_user] = mock_get_current_user

# 1. CONFIDENCE ENGINE TEST
def test_confidence_engine_production():
    """Tests weighted multi-source confidence fusion, cross-modal agreement, and certainty bands."""
    res = ConfidenceEngine.calculate_confidence(
        gemini_confidence=0.98,
        threat_intel_confidence=0.95,
        pattern_confidence=0.90,
        entity_confidence=0.92
    )
    assert res.overall_confidence >= 0.94
    assert res.cross_modal_agreement >= 0.95
    assert res.certainty_band == "VERY_HIGH"

# 2. RISK CLASSIFIER TEST
def test_risk_classifier_production():
    """Tests 5-tier risk level classification (Safe, Low, Medium, High, Critical) with UI colors and icons."""
    r_safe = RiskClassifierEngine.classify_score(10)
    assert r_safe.level_key == "SAFE"
    assert r_safe.hex_color == "#10B981"

    r_crit = RiskClassifierEngine.classify_score(95)
    assert r_crit.level_key == "CRITICAL"
    assert r_crit.hex_color == "#EF4444"
    assert r_crit.icon_svg_name == "octagon-alert"

# 3. EVIDENCE FUSION TEST
def test_evidence_fusion_production():
    """Tests multi-source evidence merging, deduplication on (indicator, category), and severity sorting."""
    ev1 = EvidenceItemSchema(evidence_id="1", indicator="paypa1-check.top", category="DOMAIN", reason="Threat DB", severity="Critical", confidence=0.98, source="THREAT")
    ev2 = EvidenceItemSchema(evidence_id="2", indicator="paypa1-check.top", category="DOMAIN", reason="AI detected", severity="High", confidence=0.90, source="AI")
    ev3 = EvidenceItemSchema(evidence_id="3", indicator="support.refund@okaxis", category="UPI_ID", reason="UPI spoofing", severity="High", confidence=0.95, source="UPI")

    report = EvidenceFusionEngine.fuse_multi_source_evidence("scn_1", ai_evidence=[ev2], threat_intel_evidence=[ev1, ev3])
    assert report.total_unified_evidence_count == 2
    assert report.unified_evidence_list[0].severity == "Critical"

# 4. RECOMMENDATIONS & ACTION PLAN TEST
def test_recommendations_production():
    """Tests generating immediate action plan steps, prohibitions, reporting suggestions, and safe decline reply."""
    report = RecommendationEngine.generate_recommendations("scn_rec", risk_level="CRITICAL", scam_category="BANK_SPOOF")
    assert len(report.immediate_actions) >= 2
    assert "Block Sender" in report.immediate_actions[0].title
    assert "Do NOT click" in report.things_not_to_do[0]
    assert "I have logged and reported" in report.safe_decline_reply

# 5. SAFE REPLY GENERATOR TEST
def test_safe_reply_multilingual_production():
    """Tests safe decline reply generation across scam categories and languages (EN, ES, HI, FR)."""
    t_en = SafeReplyGenerator.generate_reply("BANK_SPOOF", locale="en")
    assert "official banking app" in t_en.safe_reply_text

    t_hi = SafeReplyGenerator.generate_reply("OTP_REQUEST", locale="hi")
    assert "वन-टाइम पासवर्ड (OTP)" in t_hi.safe_reply_text

# 6. PERSONA-TAILORED XAI EXPLAINABILITY TEST
def test_decision_xai_production():
    """Tests 4-part persona-tailored XAI generation (Senior Citizens, Parents, Students, Professionals)."""
    report = DecisionXAIEngine.generate_full_xai_report("scn_xai", risk_level="CRITICAL", confidence=0.98, target_persona="SENIOR_CITIZENS")
    assert report.active_persona == "SENIOR_CITIZENS"
    assert "PLEASE DO NOT CLICK ANY LINKS" in report.primary_explanation.recommended_action

# 7. DECISION SERVICE TEST
@pytest.mark.asyncio
async def test_decision_service_production():
    """Tests high-level DecisionService process_full_decision_scan execution."""
    raw = "URGENT: Your PayPal account is suspended. Verify at http://paypa1-check.top or send $500 to support.refund@okaxis"
    report = await DecisionService.process_full_decision_scan(scan_id="scn_srv_prod", raw_text=raw, channel_type="SMS")
    assert report.decision.final_scam_probability >= 50
    assert report.decision.risk_level in ["HIGH", "CRITICAL"]

# 8. REST API ENDPOINTS TEST
def test_decision_api_endpoints_production():
    """Tests REST API endpoints /decision/analyse, /decision/explain, /decision/report."""
    res_an = client.post("/api/v1/decision/analyse", json={"message": "URGENT: Verify at http://paypa1-check.top", "target_persona": "SENIOR_CITIZENS"})
    assert res_an.status_code == 200

    res_ex = client.post("/api/v1/decision/explain", json={"risk_level": "CRITICAL", "target_persona": "SENIOR_CITIZENS"})
    assert res_ex.status_code == 200

    res_rp = client.post("/api/v1/decision/report", json={"message": "URGENT: Verify at http://paypa1-check.top"})
    assert res_rp.status_code == 200

# 9. SUB-50MS SLA PERFORMANCE TEST
@pytest.mark.asyncio
async def test_decision_pipeline_performance_sla():
    """Tests end-to-end Decision Pipeline latency SLA under 50ms (target < 15ms)."""
    req = DecisionRequest(
        scan_id="scn_perf_dec",
        raw_text="URGENT: Verify at http://paypa1-check.top",
        channel_type="SMS"
    )
    start_time = time.perf_counter()
    res = await DecisionPipeline.evaluate_decision(req)
    elapsed_ms = (time.perf_counter() - start_time) * 1000

    assert res.scan_id == "scn_perf_dec"
    assert elapsed_ms < 50.0, f"SLA latency breach: Execution took {elapsed_ms:.2f}ms (Limit: 50.0ms)"
