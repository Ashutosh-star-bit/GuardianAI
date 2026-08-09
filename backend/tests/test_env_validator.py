"""
GuardianAI Environment Manager Pytest Suite
"""

import pytest
from app.core.env_validator import EnvironmentManager, EnvironmentValidationError, EnvironmentType

def test_validate_development_defaults():
    config = EnvironmentManager.validate_environment({
        "ENVIRONMENT": "development",
        "SECRET_KEY": "dev_key",
        "DATABASE_URL": "sqlite:///./guardian_ai.db"
    })
    assert config.environment == EnvironmentType.DEVELOPMENT
    assert config.is_debug is True

def test_validate_production_insecure_secret_error():
    with pytest.raises(EnvironmentValidationError) as exc:
        EnvironmentManager.validate_environment({
            "ENVIRONMENT": "production",
            "SECRET_KEY": "secret",
            "DATABASE_URL": "postgresql://user:pass@localhost:5432/db"
        })
    assert "SECRET_KEY must be a secure random string" in str(exc.value)

def test_validate_production_sqlite_error():
    with pytest.raises(EnvironmentValidationError) as exc:
        EnvironmentManager.validate_environment({
            "ENVIRONMENT": "production",
            "SECRET_KEY": "prod_super_secure_random_key_string_998877",
            "DATABASE_URL": "sqlite:///./guardian_ai.db"
        })
    assert "SQLite cannot be used in production" in str(exc.value)

def test_validate_production_valid_config():
    config = EnvironmentManager.validate_environment({
        "ENVIRONMENT": "production",
        "SECRET_KEY": "prod_super_secure_random_key_string_998877",
        "DATABASE_URL": "postgresql://user:pass@localhost:5432/db"
    })
    assert config.environment == EnvironmentType.PRODUCTION
    assert config.is_debug is False
