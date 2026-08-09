"""
GuardianAI Dependency Security Pytest Suite
"""

import os
import pytest

def test_requirements_file_exists():
    req_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../requirements.txt"))
    assert os.path.exists(req_path) is True

def test_dockerfile_security_pinning():
    docker_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Dockerfile.backend"))
    with open(docker_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Verify non-root user execution
    assert "USER appuser" in content
    assert "HEALTHCHECK" in content
