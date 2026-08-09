"""
GuardianAI Production Environment Management & Validator Engine
Supported Environments: development, testing, staging, production
"""

import os
from typing import Dict, Any, List, Optional
from enum import Enum
from pydantic import BaseModel, Field

class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"

class EnvironmentConfig(BaseModel):
    environment: EnvironmentType
    secret_key: str
    database_url: str
    redis_url: str
    cors_origins: List[str]
    is_debug: bool = False

class EnvironmentValidationError(Exception):
    pass

class EnvironmentManager:
    """Enterprise Environment & Secrets Validator."""

    INSECURE_SECRET_DEFAULTS = [
        "CHANGE_ME_IN_PRODUCTION_SECRET_KEY_12345",
        "secret",
        "password",
        "123456",
        "dev_secret_key_12345"
    ]

    @classmethod
    def validate_environment(cls, config_dict: Optional[Dict[str, Any]] = None) -> EnvironmentConfig:
        """Strictly validates environment variables before service startup."""
        env_str = (config_dict.get("ENVIRONMENT") if config_dict else os.getenv("ENVIRONMENT")) or "development"
        try:
            env_type = EnvironmentType(env_str.lower())
        except ValueError:
            raise EnvironmentValidationError(f"Invalid ENVIRONMENT '{env_str}'. Must be one of: development, testing, staging, production")

        secret_key = (config_dict.get("SECRET_KEY") if config_dict else os.getenv("SECRET_KEY")) or "dev_secret_key_12345"
        database_url = (config_dict.get("DATABASE_URL") if config_dict else os.getenv("DATABASE_URL")) or "sqlite:///./guardian_ai.db"
        redis_url = (config_dict.get("REDIS_URL") if config_dict else os.getenv("REDIS_URL")) or "redis://localhost:6379/0"

        # Production Hardening Rules
        if env_type == EnvironmentType.PRODUCTION:
            if secret_key in cls.INSECURE_SECRET_DEFAULTS or len(secret_key) < 32:
                raise EnvironmentValidationError("PRODUCTION FATAL: SECRET_KEY must be a secure random string >= 32 characters.")

            if "sqlite" in database_url.lower():
                raise EnvironmentValidationError("PRODUCTION FATAL: SQLite cannot be used in production. Must configure PostgreSQL database.")

        return EnvironmentConfig(
            environment=env_type,
            secret_key=secret_key,
            database_url=database_url,
            redis_url=redis_url,
            cors_origins=["https://guardianai.io", "https://api.guardianai.io"],
            is_debug=(env_type == EnvironmentType.DEVELOPMENT)
        )

env_manager = EnvironmentManager()
