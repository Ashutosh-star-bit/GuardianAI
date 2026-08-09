"""
GuardianAI Dynamic User Trust & Reputation Scoring Engine
Purpose: Calculates user reputation score (0 to 100), trust tiers, and weighted vote impacts.
"""

from typing import Dict, Any

class UserTrustTier:
    NOVICE = "NOVICE"         # Trust Score 0 - 25 (Weight 1.0x)
    TRUSTED = "TRUSTED"       # Trust Score 26 - 70 (Weight 1.5x)
    EXPERT = "EXPERT"         # Trust Score 71 - 90 (Weight 2.0x)
    MODERATOR = "MODERATOR"   # Trust Score 91 - 100 (Weight 3.0x)

class UserTrustEngine:
    """Enterprise Reputation & Dynamic Trust Scoring Engine."""

    @classmethod
    def calculate_trust_tier(cls, trust_score: int) -> str:
        """Determines trust tier from scalar trust score (0-100)."""
        if trust_score >= 91:
            return UserTrustTier.MODERATOR
        elif trust_score >= 71:
            return UserTrustTier.EXPERT
        elif trust_score >= 26:
            return UserTrustTier.TRUSTED
        return UserTrustTier.NOVICE

    @classmethod
    def calculate_vote_weight(cls, trust_score: int) -> float:
        """
        Calculates weighted vote multiplier based on user trust score:
        Weight = 1.0 + (TrustScore / 100.0)
        """
        clamped_score = max(0, min(100, trust_score))
        return round(1.0 + (clamped_score / 100.0), 2)

    @classmethod
    def update_reputation_on_action(cls, current_score: int, action_type: str) -> int:
        """
        Updates user reputation score based on moderation or voting outcome:
        - REPORT_VERIFIED: +5
        - REPORT_REJECTED: -10
        - SPAM_FLAGGED: -30
        - VOTE_ALIGNED: +1
        """
        delta = 0
        if action_type == "REPORT_VERIFIED":
            delta = 5
        elif action_type == "REPORT_REJECTED":
            delta = -10
        elif action_type == "SPAM_FLAGGED":
            delta = -30
        elif action_type == "VOTE_ALIGNED":
            delta = 1

        new_score = max(0, min(100, current_score + delta))
        return new_score
