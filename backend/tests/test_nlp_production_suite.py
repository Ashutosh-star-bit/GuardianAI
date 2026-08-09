"""
GuardianAI Text Intelligence Production Pytest Suite
Purpose: Unit and integration tests covering Short Messages, Long Messages, Emails, WhatsApp, Unicode, Emojis,
         Spam Payloads, Normal Safe Conversations, and Edge Cases.
"""

import pytest

from app.nlp.preprocessing import TextPreprocessor
from app.nlp.features import FeatureExtractor
from app.nlp.patterns import PatternDetector
from app.nlp.entities import EntityExtractor
from app.nlp.url_extractor import URLExtractorEngine
from app.nlp.domain_intelligence import DomainIntelligenceEngine
from app.nlp.validators import TextPayloadValidator, PayloadValidationError
from app.nlp.engine import TextIntelligenceEngine
from app.nlp.pipeline import TextIntelligencePipeline

# 1. SHORT MESSAGES TEST
def test_short_message_validation_and_analysis():
    """Tests processing of short SMS messages near minimum length threshold."""
    short_text = "URGENT: Click http://paypa1-check.com"
    clean_text = TextPayloadValidator.validate_full_payload(short_text, min_len=5)
    assert len(clean_text) >= 5

    res = TextIntelligenceEngine.analyze_text("scn_short_1", clean_text, channel_type="SMS")
    assert res.features.urgency_score > 0.0
    assert len(res.entities) > 0

# 2. LONG MESSAGES TEST
def test_long_message_analysis():
    """Tests processing of large email body payloads (5,000+ characters)."""
    header = "Subject: Urgent Executive Wire Transfer Request\n\nDear Finance Department,\n"
    body = "Please process urgent wire transfer of $45,000 to merchant@okaxis immediately. " * 100
    long_text = header + body

    clean_text = TextPayloadValidator.validate_full_payload(long_text, max_len=10_000)
    assert len(clean_text) > 4,000

    features = FeatureExtractor.extract_features(clean_text)
    assert features.financial_coercion_score > 0.4
    assert features.urgency_score > 0.4

# 3. EMAILS & BEC FRAUD TEST
def test_email_bec_wire_fraud():
    """Tests BEC (Business Email Compromise) wire transfer fraud in Email payloads."""
    email_text = (
        "From: CEO <ceo@corporate-executive.com>\n"
        "Subject: Urgent Wire Transfer Required\n\n"
        "I am currently in a meeting. Process an urgent wire transfer of $14,500 "
        "to account 9876543210 at Bank of America immediately. Contact Officer John for confirmation."
    )
    res = TextIntelligenceEngine.analyze_text("scn_eml_1", email_text, channel_type="Email")
    assert res.channel_type == "Email"
    assert any(e.text == "Bank of America" for e in res.entities)
    assert any(e.entity_type == "MONEY" for e in res.entities)

# 4. WHATSAPP MESSAGES TEST
def test_whatsapp_job_offer_scam():
    """Tests WhatsApp high-yield part-time job offer scam payloads."""
    wa_text = "Hi! Work from home part-time and earn $500 daily income! Contact us on wa.me/18005550199"
    res = TextIntelligenceEngine.analyze_text("scn_wa_1", wa_text, channel_type="WhatsApp")
    assert res.channel_type == "WhatsApp"
    assert res.scam_category_hint == "JOB_SCAM"

# 5. UNICODE & HOMOGLYPH OBFUSCATION TEST
def test_unicode_homoglyph_deobfuscation():
    """Tests NFKC normalization and homoglyph deobfuscation (P@ypal -> paypal)."""
    raw_unicode = "URGENT: P@ypal account locked! Update at paypa1-check.com"
    deobfuscated = TextPreprocessor.deobfuscate_homoglyphs(raw_unicode)
    assert "paypal" in deobfuscated.lower()

# 6. EMOJI TRANSLATION TEST
def test_emoji_security_translation():
    """Tests conversion of security emojis (🚨 -> [ALERT], 💰 -> [MONEY])."""
    raw_emoji = "🚨 URGENT: 💰 Transfer $500 to unlock account 🔒!"
    translated = TextPreprocessor.translate_emojis(raw_emoji)
    assert "[ALERT]" in translated
    assert "[MONEY]" in translated
    assert "[LOCK]" in translated

# 7. SPAM & HIGH-RISK SMISHING TEST
def test_high_risk_smishing_spam():
    """Tests smishing payload featuring typosquatting links and fake bank account locks."""
    smishing_text = "FINAL WARNING: Your PayPal account is suspended. Verify at http://paypa1-check.top"
    res = TextIntelligenceEngine.analyze_text("scn_spam_1", smishing_text, channel_type="SMS")
    assert res.features.urgency_score > 0.5
    assert res.explainability.plain_summary is not None

# 8. NORMAL SAFE CONVERSATION TEST
def test_normal_safe_conversation():
    """Tests safe non-fraudulent conversation payload."""
    safe_text = "Hey Jane, let's meet tomorrow at 2:00 PM for lunch at the cafe."
    res = TextIntelligenceEngine.analyze_text("scn_safe_1", safe_text, channel_type="SMS")
    assert res.features.urgency_score < 0.3
    assert res.features.financial_coercion_score == 0.0
    assert "No suspicious" in res.explainability.plain_summary

# 9. EDGE CASES TEST (REPEATED CHARS, WHITESPACE, NULL BYTES)
def test_edge_cases_handling():
    """Tests edge cases: excessive repeated characters, whitespace padding, and null byte rejection."""
    # 1. Repeated characters
    raw_repeated = "URGENTTTTT ACTION REQUIRED!!!!"
    cleaned = TextPreprocessor.reduce_repeated_characters(raw_repeated)
    assert "URGENT" in cleaned

    # 2. Whitespace padding
    raw_spaces = "   URGENT:    Verify    account    now.   "
    normalized_space = TextPreprocessor.normalize_whitespace(raw_spaces)
    assert normalized_space == "URGENT: Verify account now."

    # 3. Illegal Null Byte Rejection
    with pytest.raises(PayloadValidationError):
        TextPayloadValidator.validate_full_payload("URGENT\x00Payload")

# 10. END-TO-END PIPELINE ASYNC INTEGRATION TEST
@pytest.mark.asyncio
async def test_pipeline_async_integration():
    """Tests end-to-end TextIntelligencePipeline async execution."""
    pipeline = TextIntelligencePipeline()
    res = await pipeline.execute_pipeline(
        scan_id="scn_async_prod",
        raw_text="URGENT: Bank alert! Account blocked. Click http://paypa1-check.com",
        channel_type="SMS"
    )
    assert res.scan_id == "scn_async_prod"
    assert res.analysis.threat_score > 0
    assert res.telemetry.total_tokens > 0
