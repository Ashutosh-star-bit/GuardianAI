"""
GuardianAI Sample Applications Pytest Suite
"""

import sys
import os
import pytest

# Add examples path to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../examples")))
from python_example import main as run_python_demo

def test_python_sample_application(capsys):
    run_python_demo()
    captured = capsys.readouterr()
    assert "GuardianAI Python Anti-Scam Inspection Demo" in captured.out
    assert "Threat Score: 98/100" in captured.out
