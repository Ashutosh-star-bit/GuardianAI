"""
GuardianAI VotingService Pytest Suite
"""

import pytest
from app.services.voting_service import VotingService, VotingServiceError
from app.community_intel.schemas import VoteType

@pytest.fixture
def voting_service():
    return VotingService()

def test_voting_service_instantiation(voting_service):
    assert voting_service is not None
