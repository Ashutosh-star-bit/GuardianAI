"""
GuardianAI JWT Authentication API Endpoints
Purpose: Implements Signup, Register, Login, Refresh Token renewal, and Current User Profile routes.
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import Token, LoginRequest, RefreshTokenRequest
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token
)
from app.core.config import settings
from app.api.deps import get_current_user
from app.services.email_service import send_verification_email
import random
from pydantic import BaseModel, EmailStr

router = APIRouter()

class SendVerificationCodeRequest(BaseModel):
    email: EmailStr
    name: str = ""
    otp_code: str

@router.post("/auth/send-verification-code", summary="Dispatch 6-Digit Email Verification Code via SMTP")
def send_verification_code_route(payload: SendVerificationCodeRequest, background_tasks: BackgroundTasks):
    """Dispatches the exact 6-digit verification code asynchronously in background task."""
    background_tasks.add_task(
        send_verification_email,
        to_email=payload.email,
        otp_code=payload.otp_code,
        user_name=payload.name
    )
    return {
        "success": True,
        "message": f"Verification code dispatched asynchronously to {payload.email}",
        "email": payload.email,
        "otp_sent": payload.otp_code
    }

@router.post("/auth/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Register User")
@router.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Register User Alias")
def signup_user(user_in: UserCreate, db: Session = Depends(get_db), background_tasks: BackgroundTasks = None):
    """Registers a new user account with BCrypt password hashing and dispatches 6-digit verification email."""
    existing_user = db.query(User).filter(User.email == user_in.email.lower()).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address already exists."
        )

    otp_code = str(random.randint(100000, 999999))

    user = User(
        email=user_in.email.lower(),
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        role="user",
        subscription_tier="free",
        is_active=True,
        is_verified=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Dispatch real email in background task
    if background_tasks:
        background_tasks.add_task(send_verification_email, to_email=user.email, otp_code=otp_code, user_name=user.full_name)

    return user

@router.post("/auth/login", response_model=Token, summary="Login User for JWT Access & Refresh Tokens")
def login_user(credentials: LoginRequest, db: Session = Depends(get_db)):
    """Authenticates email & password, returning JWT Access and Refresh Tokens."""
    user = db.query(User).filter(User.email == credentials.email.lower(), User.deleted_at.is_(None)).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.id, "email": user.email, "role": user.role})
    refresh_token = create_refresh_token(data={"sub": user.id, "email": user.email})

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user=user
    )

@router.post("/auth/refresh", response_model=Token, summary="Renew Expired JWT Access Token")
def refresh_token_route(payload: RefreshTokenRequest, db: Session = Depends(get_db)):
    """Generates a new access token using a valid, unexpired refresh token."""
    decoded = decode_token(payload.refresh_token, token_type="refresh")
    user_id = decoded.get("sub")
    
    user = db.query(User).filter(User.id == user_id, User.is_active.is_(True), User.deleted_at.is_(None)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User account is inactive or revoked.")

    new_access = create_access_token(data={"sub": user.id, "email": user.email, "role": user.role})
    new_refresh = create_refresh_token(data={"sub": user.id, "email": user.email})

    return Token(
        access_token=new_access,
        refresh_token=new_refresh,
        token_type="bearer",
        user=user
    )

@router.get("/users/me", response_model=UserResponse, summary="Get Current User Profile")
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Returns authenticated user profile details from validated JWT token."""
    return current_user
