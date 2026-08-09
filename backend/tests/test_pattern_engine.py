"""
GuardianAI Pattern Engine Unit Test Suite
Purpose: Tests pattern detection across all 10 required threat categories and dynamic pattern extension.
"""

import pytest
from app.nlp.patterns import PatternEngine, PatternDefinition

def test_detect_all_10_pattern_categories():
    """Tests pattern detection across all 10 threat categories in composite test payloads."""
    test_cases = [
        ("Please share your OTP code immediately.", "OTP_REQUEST"),
        ("Send money to UPI merchant@okaxis now.", "MONEY_REQUEST"),
        ("Buy Apple gift cards and send gift card code.", "GIFT_CARD"),
        ("Get guaranteed investment return on your funds.", "INVESTMENT"),
        ("Earn 100% return on your capital in 24 hours.", "HIGH_RETURNS"),
        ("An arrest warrant has been issued by police.", "THREATS"),
        ("Final warning: immediate attention required.", "WARNINGS"),
        ("Your account has been suspended by support.", "ACCOUNT_SUSPENSION"),
        ("Congratulations! Claim your $10,000 prize now.", "PRIZE_CLAIM"),
        ("You are eligible for a refund of $500 today.", "REFUND_CLAIM"),
    ]

    for text, expected_category in test_cases:
        matches = PatternEngine.detect_patterns(text)
        assert len(matches) > 0, f"Failed to detect pattern for category: {expected_category}"
        matched_categories = [m.pattern.category for m in matches]
        assert expected_category in matched_categories, f"Expected category {expected_category} not in {matched_categories}"

def test_dynamic_pattern_registration():
    """Tests dynamic registration of custom threat patterns."""
    custom_pattern = PatternDefinition(
        pattern_id="pat_crypto_seed",
        category="CREDENTIAL_THEFT",
        pattern_name="Crypto Wallet Seed Phrase Request",
        regex=r"(?:send your (?:seed phrase|private key))",
        severity="Critical",
        description="Solicits crypto wallet recovery phrase"
    )
    PatternEngine.register_pattern(custom_pattern)

    matches = PatternEngine.detect_patterns("Notice: Send your seed phrase to unlock wallet.")
    assert len(matches) > 0
    assert matches[0].pattern.pattern_id == "pat_crypto_seed"
