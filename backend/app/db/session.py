"""
GuardianAI Database Engine, Session Management & Dependency Injection
Purpose: Configures SQLAlchemy 2.0 engine, thread-safe sessionmaker, connection pooling,
         SQLite Foreign Key PRAGMA enforcer, and FastAPI get_db dependency injection.
"""

import logging
from typing import Generator
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

logger = logging.getLogger("guardianai.db")

# 1. Configure Engine Parameters (SQLite vs PostgreSQL)
is_sqlite = settings.DATABASE_URL.startswith("sqlite")
connect_args = {"check_same_thread": False} if is_sqlite else {}

engine_kwargs = {
    "connect_args": connect_args,
    "echo": settings.DEBUG and settings.ENVIRONMENT == "development",
    "pool_pre_ping": True, # Prevents stale connection errors
}

# Apply Connection Pooling for PostgreSQL / MySQL
if not is_sqlite:
    engine_kwargs.update({
        "pool_size": settings.DB_POOL_SIZE,
        "max_overflow": settings.DB_MAX_OVERFLOW,
    })

# Initialize SQLAlchemy 2.0 Engine
engine = create_engine(settings.DATABASE_URL, **engine_kwargs)

# SQLite Foreign Key Enforcer Listener
if is_sqlite:
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

# 2. Thread-Safe Session Factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session
)

# 3. FastAPI Dependency Injection Generator
def get_db() -> Generator[Session, None, None]:
    """
    FastAPI Dependency yielding a transactional database session per HTTP request.
    Automatically commits on clean completion, rolls back on uncaught exception,
    and returns session to connection pool.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Database session rollback due to exception: {str(e)}", exc_info=True)
        raise
    finally:
        db.close()
