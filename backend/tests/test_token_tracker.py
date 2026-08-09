"""
GuardianAI Token Tracking & Cost Analytics Unit Test Suite
Purpose: Tests usage recording, USD cost calculation, and daily/monthly aggregation reporting.
"""

from app.ai.token_tracker import TokenTracker

def test_token_cost_calculation():
    """Tests USD cost calculation for prompt and completion tokens."""
    # 100,000 prompt tokens @ $0.075/1M = $0.0075
    # 50,000 completion tokens @ $0.30/1M = $0.0150
    # Total = $0.0225
    cost = TokenTracker.calculate_usd_cost(100_000, 50_000)
    assert cost == 0.0225

def test_record_usage_transaction():
    """Tests recording token usage transaction."""
    rec = TokenTracker.record_usage(
        scan_id="scn_token_123",
        prompt_tokens=1000,
        completion_tokens=500,
        model_id="gemini-3.6-flash-high",
        user_id="usr_test_1"
    )
    assert rec.scan_id == "scn_token_123"
    assert rec.total_tokens == 1500
    assert rec.estimated_cost_usd > 0.0

def test_analytics_report_aggregation():
    """Tests dashboard analytics report generates daily and monthly metrics."""
    # Record multiple transactions
    TokenTracker.record_usage("scn_agg_1", 2000, 1000)
    TokenTracker.record_usage("scn_agg_2", 4000, 2000)

    report = TokenTracker.get_analytics_report()
    assert report.total_lifetime_requests >= 2
    assert report.total_lifetime_tokens >= 9000
    assert report.today_summary.total_tokens >= 9000
    assert report.current_month_summary.total_tokens >= 9000
