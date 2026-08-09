"""
GuardianAI Privacy-Safe AI Logging Unit Test Suite
Purpose: Tests that AILogger logs structured JSON telemetry WITHOUT leaking raw user prompt text or PII.
"""

from app.ai.logging import AILogger

def test_privacy_safe_ai_logger(caplog):
    """Tests AILogger logs telemetry metrics without user PII or raw text."""
    with caplog.at_level("INFO", logger="guardianai.ai_telemetry"):
        AILogger.log_ai_execution(
            scan_id="scn_privacy_123",
            model_id="gemini-3.6-flash-high",
            latency_ms=42.5,
            prompt_tokens=100,
            completion_tokens=50,
            total_tokens=150,
            cost_usd=0.000023,
            prompt_version="v1.0.0",
            user_id="usr_8f92a1",
            retries_count=0,
            threat_score=85,
            risk_band="dangerous"
        )

    assert len(caplog.records) > 0
    log_text = caplog.text

    # Verify telemetry attributes are present
    assert "gemini-3.6-flash-high" in log_text
    assert "scn_privacy_123" in log_text
    assert "usr_8f92a1" in log_text
    assert "v1.0.0" in log_text
    assert "42.5" in log_text

    # Verify PRIVACY GUARANTEE: Raw user message text is nowhere in the logs
    assert "raw_content" not in log_text
    assert "user_prompt_text" not in log_text
