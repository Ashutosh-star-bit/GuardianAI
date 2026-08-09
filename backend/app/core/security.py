"""
GuardianAI Cryptographic & JWT Security Utilities
Purpose: Password hashing/verification using BCrypt and JWT Access & Refresh Token issuance and decoding.
"""

import bcrypt
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Any, Union, Dict, Optional
import jwt
from app.core.config import settings

def _get_pwd_bytes(password: str) -> bytes:
    """Safely encodes and truncates password to 71 bytes for BCrypt compatibility."""
    if not password:
        return b""
    return password.encode("utf-8")[:71]

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain text password against a stored hashed password."""
    if not plain_password or not hashed_password:
        return False
    try:
        return bcrypt.checkpw(_get_pwd_bytes(plain_password), hashed_password.encode("utf-8"))
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    """Generates a secure BCrypt cryptographic hash for a plain text password."""
    pwd_bytes = _get_pwd_bytes(password)
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")

def create_access_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Generates a JWT access token containing expiration and user subject ID."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "access",
        "iss": settings.PROJECT_NAME
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Generates a long-lived JWT refresh token for session renewal."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "refresh",
        "iss": settings.PROJECT_NAME
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> Dict[str, Any]:
    """Decodes and validates a JWT token signature and expiration."""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_exp": True, "verify_iss": True},
            issuer=settings.PROJECT_NAME
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired.")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid cryptographic token signature.")
