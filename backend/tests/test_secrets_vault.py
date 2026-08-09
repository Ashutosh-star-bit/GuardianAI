"""
GuardianAI Secrets Vault Pytest Suite
"""

import pytest
from app.core.secrets_vault import secrets_vault

def test_get_secret():
    jwt_key = secrets_vault.get_secret("jwt_signing_key")
    assert len(jwt_key) > 20

def test_rotate_secret_zero_downtime():
    orig_secret = secrets_vault.get_secret("jwt_signing_key")
    result = secrets_vault.rotate_secret("jwt_signing_key")
    assert result["new_version"] == 2
    
    new_secret = secrets_vault.get_secret("jwt_signing_key")
    assert new_secret != orig_secret
    assert new_secret.startswith("rotated_jwt_signing_key_")
