"""
GuardianAI Large Master Decision Engine Testing Dataset & Reusable Pytest Fixtures
Purpose: Provides reusable datasets for Safe Messages, Lottery Scams, Investment Scams, Job Scams, OTP Scams,
         Courier Scams, Government Scams, Mixed Cases, False Positives, False Negatives, and Edge Cases.
"""

from typing import Dict, List, Any
import pytest

# 1. SAFE MESSAGES
DECISION_SAFE_MESSAGES: List[Dict[str, Any]] = [
    {"text": "Hey Jane, let's meet tomorrow at 2:00 PM for lunch at the cafe.", "expected_risk": "SAFE"},
    {"text": "Your dentist appointment is confirmed for Friday at 10:00 AM.", "expected_risk": "SAFE"},
    {"text": "Hi team, please find attached the quarterly project review slides.", "expected_risk": "SAFE"}
]

# 2. LOTTERY SCAMS
DECISION_LOTTERY_SCAMS: List[Dict[str, Any]] = [
    {"text": "CONGRATULATIONS! You won $10,000 in the International Lottery Jackpot. Claim now at http://lottery-claim.top", "expected_risk": "CRITICAL"},
    {"text": "Claim your $5,000 prize reward immediately! Contact agent on wa.me/18005550199", "expected_risk": "HIGH"}
]

# 3. INVESTMENT SCAMS
DECISION_INVESTMENT_SCAMS: List[Dict[str, Any]] = [
    {"text": "Earn 100% daily profit on your crypto investment! Risk-free guaranteed returns. Visit http://crypto-double.xyz", "expected_risk": "CRITICAL"},
    {"text": "Guaranteed 50% weekly yield on bitcoin trading. Deposit cash to merchant@okaxis now.", "expected_risk": "HIGH"}
]

# 4. JOB SCAMS
DECISION_JOB_SCAMS: List[Dict[str, Any]] = [
    {"text": "Work from home part-time and earn $500 daily income! No experience needed. Contact wa.me/18005550199", "expected_risk": "HIGH"},
    {"text": "Immediate hiring for online product review manager. Earn $300 daily. Send $50 registration fee to support.job@ybl", "expected_risk": "CRITICAL"}
]

# 5. OTP SCAMS
DECISION_OTP_SCAMS: List[Dict[str, Any]] = [
    {"text": "URGENT BANK ALERT: Share your 6-digit OTP code immediately to unlock your suspended bank account.", "expected_risk": "CRITICAL"},
    {"text": "Verification required: Provide your account pass-code to representative Officer John.", "expected_risk": "HIGH"}
]

# 6. COURIER SCAMS
DECISION_COURIER_SCAMS: List[Dict[str, Any]] = [
    {"text": "Parcel delivery pending! Pay unpaid $2.99 customs fee at http://dhl-parcel-fee.top or package will be returned.", "expected_risk": "HIGH"},
    {"text": "Tracking AWB-998877: Delivery held due to incomplete address. Update info at http://fedex-update.xyz", "expected_risk": "HIGH"}
]

# 7. GOVERNMENT SCAMS
DECISION_GOVERNMENT_SCAMS: List[Dict[str, Any]] = [
    {"text": "IRS FINAL NOTICE: An arrest warrant has been issued against your SSN. Call police department at +1 (900) 555-9999 immediately.", "expected_risk": "CRITICAL"},
    {"text": "Income Tax Department: Pay overdue penalty tax of $500 to government handle @okaxis or face court action.", "expected_risk": "CRITICAL"}
]

# 8. MIXED CASES
DECISION_MIXED_CASES: List[Dict[str, Any]] = [
    {"text": "URGENT: Your PayPal account is suspended. Verify at http://paypa1-check.top or send $500 to support.refund@okaxis or call +1-800-555-0199", "expected_risk": "CRITICAL"}
]

# 9. FALSE POSITIVES
DECISION_FALSE_POSITIVES: List[Dict[str, Any]] = [
    {"text": "Your Amazon order #112-9876543 has shipped! Track your package at https://amazon.com/tb", "expected_risk": "SAFE"},
    {"text": "Your official security password reset code is 123456. Do not share this code.", "expected_risk": "SAFE"}
]

# 10. EDGE CASES
DECISION_EDGE_CASES: List[Dict[str, Any]] = [
    {"text": "   URGENT:    Verify    account    now.   ", "expected_risk": "HIGH"},
    {"text": "x89z1a09qw4b21c9.com", "expected_risk": "MEDIUM"}
]

# PYTEST FIXTURES PROVIDER
@pytest.fixture
def decision_safe_dataset() -> List[Dict[str, Any]]:
    return DECISION_SAFE_MESSAGES

@pytest.fixture
def decision_scams_dataset() -> List[Dict[str, Any]]:
    return (
        DECISION_LOTTERY_SCAMS +
        DECISION_INVESTMENT_SCAMS +
        DECISION_JOB_SCAMS +
        DECISION_OTP_SCAMS +
        DECISION_COURIER_SCAMS +
        DECISION_GOVERNMENT_SCAMS +
        DECISION_MIXED_CASES
    )

@pytest.fixture
def decision_false_positives_dataset() -> List[Dict[str, Any]]:
    return DECISION_FALSE_POSITIVES
