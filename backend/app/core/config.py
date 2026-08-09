"""
GuardianAI Enterprise Production Configuration Management System
Purpose: Modular, Pydantic v2 BaseSettings loading, validating, and casting environment variables from .env files.
Enforces environment-specific security constraints for Development, Staging, and Production modes.
"""

import sys
import logging
from typing import List, Union, Literal
from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger("guardianai.config")

# Environment Modes
EnvironmentMode = Literal["development", "staging", "production", "testing"]

class DatabaseSettings(BaseSettings):
    """Database Persistence Settings."""
    DATABASE_URL: str = Field(
        default="sqlite:///./guardianai.db",
        description="SQLAlchemy Database URL connection string (SQLite for dev, PostgreSQL for prod)"
    )
    DB_POOL_SIZE: int = Field(default=5, ge=1, le=100)
    DB_MAX_OVERFLOW: int = Field(default=10, ge=0, le=100)
    DB_POOL_PRE_PING: bool = Field(default=True)
    DB_ECHO: bool = Field(default=False)

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        if not v or not (v.startswith("sqlite") or v.startswith("postgresql") or v.startswith("postgres")):
            raise ValueError("DATABASE_URL must begin with sqlite://, postgresql://, or postgres://")
        return v

class SecuritySettings(BaseSettings):
    """Cryptographic & JWT Authentication Security Settings."""
    SECRET_KEY: str = Field(
        default="dev_secret_key_change_in_production_environment_32chars",
        min_length=32,
        description="Master cryptographic key for JWT signature encoding"
    )
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, ge=1, le=43200) # Max 30 days
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, ge=1, le=365)
    BCRYPT_ROUNDS: int = Field(default=12, ge=4, le=16)

class CorsSettings(BaseSettings):
    """Cross-Origin Resource Sharing (CORS) Whitelist Settings."""
    CORS_ORIGINS: Union[str, List[str]] = Field(
        default="http://localhost:5173,http://127.0.0.1:5173",
        description="Allowed CORS origin domains (comma-separated string or JSON list)"
    )

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            if v.startswith("[") and v.endswith("]"):
                import json
                try:
                    return json.loads(v)
                except Exception:
                    pass
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            return v
        raise ValueError(f"Invalid CORS origins format: {v}")

class AIServiceSettings(BaseSettings):
    """Third-Party Threat Detection AI & Threat Intelligence API Settings."""
    GROQ_API_KEY: str = Field(default="", description="Groq AI reasoning engine API key")
    HUGGINGFACE_API_KEY: str = Field(default="", description="Hugging Face inference API key")
    VIRUSTOTAL_API_KEY: str = Field(default="", description="VirusTotal domain WHOIS API key")

class Settings(BaseSettings):
    """Master Application Configuration Settings Aggregator."""
    PROJECT_NAME: str = Field(default="GuardianAI")
    VERSION: str = Field(default="1.0.0")
    ENVIRONMENT: EnvironmentMode = Field(default="development")
    DEBUG: bool = Field(default=True)
    API_V1_STR: str = Field(default="/api/v1")

    # Host & Server Execution
    HOST: str = Field(default="127.0.0.1")
    PORT: int = Field(default=8000, ge=1024, le=65535)
    LOG_LEVEL: str = Field(default="INFO")

    # Modular Settings Groups
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    cors: CorsSettings = Field(default_factory=CorsSettings)
    ai: AIServiceSettings = Field(default_factory=AIServiceSettings)

    # Legacy Flattened Compatibility Properties
    @property
    def DATABASE_URL(self) -> str:
        return self.db.DATABASE_URL

    @property
    def DB_POOL_SIZE(self) -> int:
        return self.db.DB_POOL_SIZE

    @property
    def DB_MAX_OVERFLOW(self) -> int:
        return self.db.DB_MAX_OVERFLOW

    @property
    def SECRET_KEY(self) -> str:
        return self.security.SECRET_KEY

    @property
    def ALGORITHM(self) -> str:
        return self.security.ALGORITHM

    @property
    def ACCESS_TOKEN_EXPIRE_MINUTES(self) -> int:
        return self.security.ACCESS_TOKEN_EXPIRE_MINUTES

    @property
    def REFRESH_TOKEN_EXPIRE_DAYS(self) -> int:
        return self.security.REFRESH_TOKEN_EXPIRE_DAYS

    @property
    def CORS_ORIGINS(self) -> List[str]:
        return self.cors.CORS_ORIGINS

    @property
    def GROQ_API_KEY(self) -> str:
        return self.ai.GROQ_API_KEY

    @property
    def HUGGINGFACE_API_KEY(self) -> str:
        return self.ai.HUGGINGFACE_API_KEY

    @property
    def VIRUSTOTAL_API_KEY(self) -> str:
        return self.ai.VIRUSTOTAL_API_KEY

    @model_validator(mode="after")
    def validate_environment_security(self) -> "Settings":
        """Strict production security validation checks."""
        if self.ENVIRONMENT in ["production", "staging"]:
            # Enforce DEBUG=False in production
            if self.DEBUG:
                logger.warning("Overriding DEBUG=True to False for %s environment", self.ENVIRONMENT)
                object.__setattr__(self, "DEBUG", False)

            # Prevent using weak default secret key in production
            if "dev_secret_key" in self.security.SECRET_KEY or "change_in_production" in self.security.SECRET_KEY:
                raise ValueError(
                    f"CRITICAL SECURITY ERROR: Default dev SECRET_KEY cannot be used in {self.ENVIRONMENT} environment. "
                    "Set a secure 32+ character SECRET_KEY in your production environment variables."
                )

            # Enforce non-SQLite database for production
            if self.db.DATABASE_URL.startswith("sqlite"):
                logger.warning(
                    "DATABASE_URL is set to SQLite in %s environment. PostgreSQL is strongly recommended for production.",
                    self.ENVIRONMENT
                )

        return self

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True
    )

# Instantiate Master Settings Singleton
settings = Settings()
