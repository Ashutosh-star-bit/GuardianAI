"""
GuardianAI User Pydantic v2 Schemas
Purpose: Strict data validation and serialization DTO schemas for User Registration, Profile Updates, and Responses.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator

class UserBase(BaseModel):
    """Base User DTO containing shared public attributes."""
    email: EmailStr = Field(description="User primary email address")
    full_name: Optional[str] = Field(default=None, max_length=255, description="Full display name")
    role: str = Field(default="user", description="Account role: user, admin, analyst")
    subscription_tier: str = Field(default="free", description="Subscription tier: free, pro, enterprise")
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)

    @field_validator("email", mode="before")
    @classmethod
    def lowercase_email(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip().lower()
        return v

class UserCreate(BaseModel):
    """Schema for User Registration request payload."""
    email: EmailStr = Field(description="User registration email address")
    password: str = Field(min_length=8, max_length=128, description="Plaintext password (min 8 chars)")
    full_name: Optional[str] = Field(default=None, max_length=255)

    @field_validator("password")
    @classmethod
    def validate_password_complexity(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        return v

class UserUpdate(BaseModel):
    """Schema for Profile & User Update request payload."""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = Field(default=None, min_length=8, max_length=128)
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None

class UserResponse(UserBase):
    """Public User Response DTO for API output."""
    id: str = Field(description="User primary key UUID string")
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserInDB(UserResponse):
    """Internal Database User Schema including password hash."""
    hashed_password: str
