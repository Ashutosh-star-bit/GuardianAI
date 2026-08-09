"""
GuardianAI Backup Strategy Pytest Suite
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../scripts")))
from backup_database import execute_database_backup

def test_database_backup_execution(tmp_path):
    res = execute_database_backup(backup_dir=str(tmp_path))
    assert res["status"] == "SUCCESS"
    assert os.path.exists(res["filepath"]) is True
    assert res["size_bytes"] > 0
