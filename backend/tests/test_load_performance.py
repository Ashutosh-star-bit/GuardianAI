"""
GuardianAI High-Concurrency Load Testing Pytest Suite
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../scripts")))
from load_test_locust import GuardianAILoadUser

def test_load_user_task_declarations():
    user = GuardianAILoadUser
    tasks = user.tasks
    assert len(tasks) == 4
