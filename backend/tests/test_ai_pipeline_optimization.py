"""
GuardianAI AI Pipeline Optimization Pytest Suite
"""

import pytest
from app.decision_engine.ai_pipeline_optimization import ai_pipeline_optimization

def test_compress_prompt_text():
    raw = "  URGENT:   Your    bank   account   is   suspended.   \n\n   Update   KYC   now.   "
    compressed = ai_pipeline_optimization.compress_prompt_text(raw)
    assert compressed == "URGENT: Your bank account is suspended. Update KYC now."
    assert len(compressed) < len(raw)

def test_execute_optimized_llm_inference():
    res = ai_pipeline_optimization.execute_optimized_llm_inference("URGENT KYC UPDATE")
    assert res.threat_score == 98
    assert res.recommended_action == "BLOCK_AND_REPORT"
    assert res.confidence == 0.99
