"""
GuardianAI Pytest Test Fixtures Suite
Purpose: Provides reusable fixtures for isolated in-memory SQLite database sessions, FastAPI TestClient injection,
         authenticated user headers, and AI API mocks.
"""

import sys
import os
import pytest
from typing import Generator, Dict
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

# Ensure backend root directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from app.db.base import Base
from app.db.session import get_db
from app.models.user import User
from app.models.scan import Scan
from app.core.security import get_password_hash, create_access_token

# In-Memory SQLite Engine for fast isolated tests
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)

@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """Creates a fresh in-memory SQLite schema per test function."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """FastAPI TestClient with overridden database session dependency."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def test_user(db_session: Session) -> User:
    """Creates and returns a standard test user in the test database."""
    user = User(
        email="testuser@guardianai.io",
        hashed_password=get_password_hash("TestPassword123!"),
        full_name="Standard Test User",
        role="user",
        subscription_tier="free",
        is_active=True,
        is_verified=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture(scope="function")
def admin_user(db_session: Session) -> User:
    """Creates and returns an administrator test user in the test database."""
    admin = User(
        email="adminuser@guardianai.io",
        hashed_password=get_password_hash("AdminPassword123!"),
        full_name="Administrator Test User",
        role="admin",
        subscription_tier="enterprise",
        is_active=True,
        is_verified=True
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin

@pytest.fixture(scope="function")
def auth_headers(test_user: User) -> Dict[str, str]:
    """Returns valid Authorization Bearer headers for standard test user."""
    access_token = create_access_token(subject=test_user.id)
    return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture(scope="function")
def admin_auth_headers(admin_user: User) -> Dict[str, str]:
    """Returns valid Authorization Bearer headers for admin test user."""
    access_token = create_access_token(subject=admin_user.id)
    return {"Authorization": f"Bearer {access_token}"}
