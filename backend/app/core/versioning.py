"""
GuardianAI API Versioning, Deprecation & Migration Policy Engine
Purpose: Provides header-based deprecation management emitting:
         1. X-API-Version: v1.0.0 / v2.0.0-alpha
         2. X-API-Deprecation-Date: 2027-01-01 (ISO Date)
         3. X-API-Sunset-Date: 2027-06-01 (ISO Date)
         4. Link header pointing to API v1-v2 migration guide.
"""

from typing import Callable, Dict, Any, Optional
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

class APIVersioningMiddleware(BaseHTTPMiddleware):
    """API Versioning & Deprecation Policy Middleware."""

    DEPRECATION_CONFIG = {
        "/api/v1": {
            "version": "v1.0.0",
            "is_deprecated": False,
            "deprecation_date": "2027-01-01T00:00:00Z",
            "sunset_date": "2027-06-01T00:00:00Z",
            "migration_guide": "https://guardianai.io/docs/api/v1-v2-migration"
        },
        "/api/v2": {
            "version": "v2.0.0-alpha",
            "is_deprecated": False,
            "deprecation_date": None,
            "sunset_date": None,
            "migration_guide": None
        }
    }

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        path = request.url.path

        # Match version prefix
        matched_prefix = None
        for prefix in self.DEPRECATION_CONFIG:
            if path.startswith(prefix):
                matched_prefix = prefix
                break

        if matched_prefix:
            cfg = self.DEPRECATION_CONFIG[matched_prefix]
            response.headers["X-API-Version"] = cfg["version"]

            if cfg["is_deprecated"]:
                response.headers["X-API-Deprecation-Date"] = cfg["deprecation_date"]
                response.headers["X-API-Sunset-Date"] = cfg["sunset_date"]
                response.headers["Link"] = f'<{cfg["migration_guide"]}>; rel="successor-version"'

        return response
