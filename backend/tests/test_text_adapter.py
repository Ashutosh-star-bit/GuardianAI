"""
GuardianAI TextAdapter Unit & Edge Cases Pytest Suite
Purpose: Tests validation, normalization, homoglyph deobfuscation, and edge cases for TextAdapter.
"""

import pytest
from app.adapters.text_adapter import TextAdapter, TextAdapterError
from app.adapters.schemas import UniversalAnalysisRequest

@pytest.mark.asyncio
async def test_text_adapter_normal_payload():
    """Tests TextAdapter processing normal plain text payload."""
    adapter = TextAdapter()
    raw = "  URGENT: Verify PayPal account at http://paypa1-check.top  "

    req: UniversalAnalysisRequest = await adapter.adapt_to_request(raw_payload=raw, source="WEB_APP")

    assert req.input_type == "TEXT"
    assert "paypa1-check.top" in req.raw_content
    assert req.metadata.original_format == "TEXT"
    assert req.metadata.extracted_urls_count == 1
    assert req.source == "WEB_APP"

@pytest.mark.asyncio
async def test_text_adapter_homoglyph_deobfuscation():
    """Tests TextAdapter homoglyph replacement (e.g. Cyrillic 'а' to Latin 'a')."""
    adapter = TextAdapter()
    # 'раура1' contains Cyrillic homoglyphs
    raw = "Verify раура1 account"

    req = await adapter.adapt_to_request(raw_payload=raw)

    assert "paypa1" in req.raw_content

@pytest.mark.asyncio
async def test_text_adapter_edge_cases_and_errors():
    """Tests TextAdapter edge case rejections (Null Bytes, Empty, Max Length)."""
    adapter = TextAdapter()

    # 1. Null Byte Rejection
    with pytest.raises(TextAdapterError, match="null byte"):
        await adapter.adapt_to_request("URGENT\x00Message")

    # 2. Empty / Whitespace Only Rejection
    with pytest.raises(TextAdapterError, match="empty or whitespace"):
        await adapter.adapt_to_request("   ")

    # 3. None Rejection
    with pytest.raises(TextAdapterError, match="cannot be None"):
        await adapter.adapt_to_request(None)

    # 4. Exceeding Max Length Rejection
    long_text = "A" * 10001
    with pytest.raises(TextAdapterError, match="exceeds max limit"):
        await adapter.adapt_to_request(long_text)
