"""
GuardianAI Prometheus Metrics Pytest Suite
"""

import pytest
from app.core.telemetry_prometheus import prometheus_engine

def test_prometheus_metrics_format():
    text = prometheus_engine.generate_prometheus_metrics_text()
    assert "guardianai_http_requests_total 142850" in text
    assert "guardianai_llm_tokens_total 2465000" in text
    assert "guardianai_redis_cache_hits_total 89400" in text
