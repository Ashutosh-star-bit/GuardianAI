"""
GuardianAI Master Decision Engine Dataset Fixtures Unit Test Suite
Purpose: Consumes decision dataset fixtures to verify Decision Pipeline risk classification accuracy.
"""

import pytest
from app.decision_engine import DecisionPipeline, DecisionRequest, DecisionResult
from tests.fixtures.decision_engine_dataset import (
    decision_safe_dataset,
    decision_scams_dataset,
    decision_false_positives_dataset
)

@pytest.mark.asyncio
async def test_fixture_safe_messages(decision_safe_dataset):
    """Tests Decision Pipeline against dataset of safe messages."""
    for item in decision_safe_dataset:
        req = DecisionRequest(scan_id="scn_fix_safe", raw_text=item["text"], channel_type="SMS")
        res: DecisionResult = await DecisionPipeline.evaluate_decision(req)
        assert res.final_scam_probability < 30
        assert res.risk_level == "SAFE"

@pytest.mark.asyncio
async def test_fixture_scam_messages(decision_scams_dataset):
    """Tests Decision Pipeline against dataset of high-risk scam messages."""
    for item in decision_scams_dataset:
        req = DecisionRequest(
            scan_id="scn_fix_scam",
            raw_text=item["text"],
            channel_type="SMS",
            threat_intelligence={"scoring_result": {"technical_risk_score": 75}}
        )
        res = await DecisionPipeline.evaluate_decision(req)
        assert res.final_scam_probability >= 50
        assert res.risk_level in ["HIGH", "CRITICAL"]

@pytest.mark.asyncio
async def test_fixture_false_positives(decision_false_positives_dataset):
    """Tests Decision Pipeline against dataset of false positive legitimate messages."""
    for item in decision_false_positives_dataset:
        req = DecisionRequest(scan_id="scn_fix_fp", raw_text=item["text"], channel_type="SMS")
        res = await DecisionPipeline.evaluate_decision(req)
        assert res.risk_level == "SAFE"
