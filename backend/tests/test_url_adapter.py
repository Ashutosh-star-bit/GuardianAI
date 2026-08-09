"""
GuardianAI URLAdapter Unit & Malformed URLs Pytest Suite
Purpose: Tests validation, scheme normalization, domain extraction, and malformed URL handling for URLAdapter.
"""

import pytest
from app.adapters.url_adapter import URLAdapter, URLAdapterError
from app.adapters.schemas import UniversalAnalysisRequest

@pytest.mark.asyncio
async def test_url_adapter_normal_and_missing_scheme():
    """Tests URLAdapter with standard URL and missing http scheme."""
    adapter = URLAdapter()

    # Standard URL
    req1: UniversalAnalysisRequest = await adapter.adapt_to_request("https://paypa1-check.top/login?user=admin")
    assert req1.input_type == "URL"
    assert req1.raw_content == "https://paypa1-check.top/login?user=admin"
    assert req1.metadata.extra_attributes["hostname"] == "paypa1-check.top"
    assert req1.metadata.extra_attributes["domain"] == "paypa1-check.top"

    # Missing scheme (prepending http://)
    req2 = await adapter.adapt_to_request("www.secure-bank-login.com")
    assert req2.raw_content == "http://www.secure-bank-login.com"
    assert req2.metadata.extra_attributes["domain"] == "secure-bank-login.com"

@pytest.mark.asyncio
async def test_url_adapter_ip_and_port():
    """Tests URLAdapter handling IP address URLs and custom ports."""
    adapter = URLAdapter()
    req = await adapter.adapt_to_request("http://192.168.1.1:8080/admin")

    assert req.metadata.extra_attributes["hostname"] == "192.168.1.1"
    assert req.metadata.extra_attributes["port"] == 8080

@pytest.mark.asyncio
async def test_url_adapter_malformed_urls_and_errors():
    """Tests URLAdapter rejecting malformed URLs, null bytes, and empty inputs."""
    adapter = URLAdapter()

    # 1. Null Byte Rejection
    with pytest.raises(URLAdapterError, match="null byte"):
        await adapter.adapt_to_request("http://paypa1-check.top\x00/login")

    # 2. Empty / Whitespace Rejection
    with pytest.raises(URLAdapterError, match="cannot be empty"):
        await adapter.adapt_to_request("   ")

    # 3. Malformed Domain Structure (No TLD)
    with pytest.raises(URLAdapterError, match="Invalid domain/TLD structure"):
        await adapter.adapt_to_request("invalid_domain_name_without_tld")
