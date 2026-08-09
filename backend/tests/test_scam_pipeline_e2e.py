"""
GuardianAI End-to-End (E2E) Master Scam Analysis Pipeline Test Suite
Purpose: Reusable E2E test suite covering 10 real-world threat scenarios:
         Safe Message, Lottery Scam, Investment Scam, Courier Scam, OTP Scam, Job Scam,
         Government Scam, Mixed Scam, False Positive, and False Negative Benchmark.
"""

import pytest
from app.pipeline import ScamAnalysisPipeline, ScamAnalysisPipelineResult
from app.pipeline.history_service import HistoryService
from app.pipeline.analytics_recorder import AnalyticsRecorder

@pytest.fixture(autouse=True)
def clean_pipeline_environment():
    HistoryService.clear_all()
    AnalyticsRecorder.clear_all()
    yield
    HistoryService.clear_all()
    AnalyticsRecorder.clear_all()

# 1. SAFE MESSAGE SCENARIO
@pytest.mark.asyncio
async def test_e2e_safe_message_scenario():
    """E2E Test: Normal non-scam text message."""
    raw = "Hey Jane, let's meet tomorrow at 2:00 PM for lunch at the cafe."
    res: ScamAnalysisPipelineResult = await ScamAnalysisPipeline.execute_full_scam_analysis(raw_input=raw)

    assert res.decision.risk_level == "SAFE"
    assert res.decision.final_scam_probability < 20
    assert "Standard Vigilance" in res.decision.action_plan[0].title

# 2. LOTTERY SCAM SCENARIO
@pytest.mark.asyncio
async def test_e2e_lottery_scam_scenario():
    """E2E Test: Jackpot claim scam with typosquatting link."""
    raw = "CONGRATULATIONS! You won $10,000 in International Lottery Jackpot. Claim winnings at http://lottery-claim.top"
    res = await ScamAnalysisPipeline.execute_full_scam_analysis(raw_input=raw)

    assert res.decision.final_scam_probability >= 20
    assert res.decision.risk_level in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    assert "lottery-claim.top" in str(res.decision.evidence)

# 3. INVESTMENT SCAM SCENARIO
@pytest.mark.asyncio
async def test_e2e_investment_scam_scenario():
    """E2E Test: Crypto high-yield investment scam."""
    raw = "Earn 100% daily profit on your crypto investment! Risk-free guaranteed returns. Deposit to merchant@okaxis"
    res = await ScamAnalysisPipeline.execute_full_scam_analysis(raw_input=raw)

    assert res.decision.final_scam_probability >= 20
    assert res.decision.risk_level in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

# 4. COURIER SCAM SCENARIO
@pytest.mark.asyncio
async def test_e2e_courier_scam_scenario():
    """E2E Test: Pending parcel delivery fee smishing."""
    raw = "Parcel delivery pending! Pay unpaid $2.99 customs fee at http://dhl-parcel-fee.top or package will be returned."
    res = await ScamAnalysisPipeline.execute_full_scam_analysis(raw_input=raw)

    assert res.decision.final_scam_probability >= 20
    assert "dhl-parcel-fee.top" in str(res.decision.evidence)

# 5. OTP SCAM SCENARIO
@pytest.mark.asyncio
async def test_e2e_otp_scam_scenario():
    """E2E Test: One-Time Passcode solicitation smishing."""
    raw = "URGENT BANK ALERT: Share your 6-digit OTP code immediately to unlock your suspended bank account."
    res = await ScamAnalysisPipeline.execute_full_scam_analysis(raw_input=raw)

    assert res.decision.final_scam_probability >= 20
    assert "One-Time Passwords" in str(res.decision.recommendations)

# 6. JOB SCAM SCENARIO
@pytest.mark.asyncio
async def test_e2e_job_scam_scenario():
    """E2E Test: Part-time work-from-home income scam."""
    raw = "Work from home part-time and earn $500 daily income! No experience needed. Contact wa.me/18005550199"
    res = await ScamAnalysisPipeline.execute_full_scam_analysis(raw_input=raw)

    assert res.decision.final_scam_probability >= 20

# 7. GOVERNMENT SCAM SCENARIO
@pytest.mark.asyncio
async def test_e2e_government_scam_scenario():
    """E2E Test: IRS tax penalty / SSN arrest warrant threat."""
    raw = "IRS FINAL NOTICE: An arrest warrant has been issued against your SSN. Call police department at +1 (900) 555-9999 immediately."
    res = await ScamAnalysisPipeline.execute_full_scam_analysis(raw_input=raw)

    assert res.decision.final_scam_probability >= 20

# 8. MIXED SCAM SCENARIO
@pytest.mark.asyncio
async def test_e2e_mixed_scam_scenario():
    """E2E Test: Multi-vector smishing payload (Typosquatting link + UPI handle + Bank account lock)."""
    raw = "URGENT: Your PayPal account is suspended. Verify at http://paypa1-check.top or send $500 to support.refund@okaxis"
    res = await ScamAnalysisPipeline.execute_full_scam_analysis(raw_input=raw)

    assert res.decision.final_scam_probability >= 20
    assert len(res.decision.evidence) >= 2

# 9. FALSE POSITIVE SCENARIO
@pytest.mark.asyncio
async def test_e2e_false_positive_scenario():
    """E2E Test: Legitimate Amazon order shipping notification."""
    raw = "Your Amazon order #112-9876543 has shipped! Track your package at https://amazon.com/tb"
    res = await ScamAnalysisPipeline.execute_full_scam_analysis(raw_input=raw)

    assert res.decision.risk_level in ["SAFE", "LOW"]
    assert res.decision.final_scam_probability < 30

# 10. FALSE NEGATIVE BENCHMARK SCENARIO
@pytest.mark.asyncio
async def test_e2e_false_negative_benchmark_scenario():
    """E2E Test: Subtle social engineering attempt."""
    raw = "Hi Mom, I lost my phone. Please send $200 to my new UPI handle payee@ybl until I get my card back."
    res = await ScamAnalysisPipeline.execute_full_scam_analysis(raw_input=raw)

    assert res.decision.final_scam_probability >= 20
    assert res.decision.risk_level in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
