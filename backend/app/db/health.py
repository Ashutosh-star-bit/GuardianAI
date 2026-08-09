"""
GuardianAI Database Health Check Diagnostic Service
Purpose: Provides lightweight database connection verification, latency measurement, and health telemetry.
"""

import time
import logging
from typing import Dict, Any
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db.session import engine

logger = logging.getLogger("guardianai.db.health")

def check_database_health(db: Session = None) -> Dict[str, Any]:
    """
    Executes a SELECT 1 query to verify database connection viability and measure query SLA latency.
    """
    start_time = time.perf_counter()
    try:
        if db is not None:
            result = db.execute(text("SELECT 1")).scalar()
        else:
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1")).scalar()

        latency_ms = (time.perf_counter() - start_time) * 1000

        is_healthy = result == 1
        db_type = "sqlite" if engine.url.drivername.startswith("sqlite") else engine.url.drivername

        return {
            "status": "healthy" if is_healthy else "unhealthy",
            "database_type": db_type,
            "latency_ms": round(latency_ms, 2),
            "connection_pool": {
                "size": getattr(engine.pool, "size", lambda: 1)(),
                "checked_in": getattr(engine.pool, "checkedin", lambda: 1)(),
            }
        }
    except Exception as e:
        latency_ms = (time.perf_counter() - start_time) * 1000
        logger.error(f"Database health check failed: {str(e)}", exc_info=True)
        return {
            "status": "unhealthy",
            "error": str(e),
            "latency_ms": round(latency_ms, 2),
        }
