"""
GuardianAI Authentication Pydantic v2 DTO Schemas
Purpose: Validation schemas for JWT Access/Refresh tokens, Login requests, and Token refreshes.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class Token(BaseModel):
    """Token response schema returned upon successful authentication."""
    access_token: str = Field(description="JWT Access Token")
    refresh_token: str = Field(description="JWT Refresh Token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(description="Access token expiration window in seconds")

class TokenPayload(BaseModel):
    """Decoded JWT Token Payload schema."""
    sub: Optional[str] = None
    exp: Optional[int] = None
    type: Optional[str] = None

class LoginRequest(BaseModel):
    """Payload schema for user login request."""
    email: EmailStr = Field(description="User login email address")
    password: str = Field(min_length=1, description="User plaintext password")

class RefreshTokenRequest(BaseModel):
    """Payload schema for refreshing expired access tokens."""
    refresh_token: str = Field(description="JWT Refresh Token")
