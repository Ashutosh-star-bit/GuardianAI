"""
GuardianAI Authentication API Endpoints (v1)
Purpose: User registration (signup), authentication (login), token renewal (refresh), and profile retrieval (me).
"""

from fastapi import APIRouter, Depends, HTTPException, status
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

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    """Registers a new user account with BCrypt password hashing."""
    existing_user = db.query(User).filter(User.email == user_in.email.lower()).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address already exists."
        )

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
    return user

@router.post("/login", response_model=Token)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """Authenticates email & password, returning JWT Access and Refresh Tokens."""
    user = db.query(User).filter(User.email == credentials.email.lower(), User.deleted_at.is_(None)).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account."
        )

    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

@router.post("/refresh", response_model=Token)
def refresh_token(payload_in: RefreshTokenRequest, db: Session = Depends(get_db)):
    """Issues a new JWT Access Token using a valid Refresh Token."""
    try:
        decoded = decode_token(payload_in.refresh_token)
        if decoded.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type.")
        user_id = decoded.get("sub")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    user = db.query(User).filter(User.id == user_id, User.deleted_at.is_(None)).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP0_401_UNAUTHORIZED, detail="User account unavailable.")

    new_access_token = create_access_token(subject=user.id)
    new_refresh_token = create_refresh_token(subject=user.id)

    return Token(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Returns profile information for currently authenticated user."""
    return current_user
