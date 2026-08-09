"""
GuardianAI TrustScoreEngine Pytest Suite
"""

import pytest
from app.community_intel.trust_score_engine import TrustScoreEngine, UserTrustTierName

def test_initial_base_score():
    score = TrustScoreEngine.compute_trust_score()
    assert score == 50
    assert TrustScoreEngine.get_trust_tier(score) == UserTrustTierName.TRUSTED
    assert TrustScoreEngine.get_vote_weight(score) == 1.5

def test_approved_reports_reputation_boost():
    score = TrustScoreEngine.compute_trust_score(approved_reports_count=5)
    assert score == 75 # 50 base + 25 = 75
    assert TrustScoreEngine.get_trust_tier(score) == UserTrustTierName.EXPERT

def test_spam_strike_reputation_penalty():
    score = TrustScoreEngine.compute_trust_score(spam_reports_count=2)
    assert score == 0 # 50 base - 60 = -10 -> clamped to 0
    assert TrustScoreEngine.get_trust_tier(score) == UserTrustTierName.NOVICE
    assert TrustScoreEngine.get_vote_weight(score) == 1.0

def test_moderator_bonus():
    score = TrustScoreEngine.compute_trust_score(approved_reports_count=8, is_moderator=True)
    assert score == 100 # 50 base + 40 + 15 = 105 -> clamped to 100
    assert TrustScoreEngine.get_trust_tier(score) == UserTrustTierName.MODERATOR
