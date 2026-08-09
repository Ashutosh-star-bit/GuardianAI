"""
GuardianAI Enterprise User Trust & Reputation Score Engine
Purpose: Dynamically computes user trust score (0 to 100) using 5 core reputation signals:
         1. Approved Scam Reports (+5 pts)
         2. Rejected Reports (-10 pts)
         3. Spam Report Strikes (-30 pts)
         4. Helpful Votes Aligned with Consensus (+1 pt)
         5. Moderator Actions / Tier Bonus (+15 pts).
"""

from typing import Dict, Any, Optional

class UserTrustTierName:
    NOVICE = "NOVICE"         # Trust Score 0 - 25
    TRUSTED = "TRUSTED"       # Trust Score 26 - 70
    EXPERT = "EXPERT"         # Trust Score 71 - 90
    MODERATOR = "MODERATOR"   # Trust Score 91 - 100

class TrustScoreEngine:
    """Enterprise Fair User Trust & Reputation Calculation Engine."""

    INITIAL_BASE_SCORE = 50

    # Reputation Signal Point Weights
    POINTS_APPROVED_REPORT = 5
    POINTS_REJECTED_REPORT = -10
    POINTS_SPAM_STRIKE = -30
    POINTS_HELPFUL_VOTE = 1
    POINTS_MODERATOR_BONUS = 15

    @classmethod
    def compute_trust_score(
        cls,
        approved_reports_count: int = 0,
        rejected_reports_count: int = 0,
        spam_reports_count: int = 0,
        helpful_votes_count: int = 0,
        is_moderator: bool = False
    ) -> int:
        """
        Calculates scalar trust score (0 to 100) from historical user contribution signals.
        """
        score = cls.INITIAL_BASE_SCORE

        score += (approved_reports_count * cls.POINTS_APPROVED_REPORT)
        score += (rejected_reports_count * cls.POINTS_REJECTED_REPORT)
        score += (spam_reports_count * cls.POINTS_SPAM_STRIKE)
        score += (helpful_votes_count * cls.POINTS_HELPFUL_VOTE)

        if is_moderator:
            score += cls.POINTS_MODERATOR_BONUS

        # Clamp within bounds [0, 100]
        clamped_score = max(0, min(100, score))
        return clamped_score

    @classmethod
    def get_trust_tier(cls, trust_score: int) -> str:
        """Maps trust score to human-readable Trust Tier."""
        if trust_score >= 91:
            return UserTrustTierName.MODERATOR
        elif trust_score >= 71:
            return UserTrustTierName.EXPERT
        elif trust_score >= 26:
            return UserTrustTierName.TRUSTED
        return UserTrustTierName.NOVICE

    @classmethod
    def get_vote_weight(cls, trust_score: int) -> float:
        """
        Computes weighted vote multiplier: W_v = 1.0 + (TrustScore / 100.0)
        """
        clamped = max(0, min(100, trust_score))
        return round(1.0 + (clamped / 100.0), 2)
