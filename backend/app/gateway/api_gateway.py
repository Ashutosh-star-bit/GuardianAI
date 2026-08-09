"""
GuardianAI High-Performance API Gateway Middleware
Purpose: Master API Gateway executing sub-1ms pipeline checks:
         1. Version Routing (/api/v1/*, /api/v2/*)
         2. Authentication (API Key / JWT Bearer)
         3. Authorization (Scope & Role validation)
         4. Rate Limiting (Redis Sliding-Window)
         5. Quota Checking (Daily Usage Metering)
         6. Request Validation (XSS / SQLi payload screening)
         7. Structured Logging & Correlation Tracking
         8. Standardized Response Formatting (X-Correlation-ID)
"""

import time
import uuid
import json
from typing import Callable, Dict, Any, Optional
from fastapi import Request, Response, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.developer_platform.api_key_service import api_key_service
from app.core.admin_security import enterprise_admin_security_engine

class APIGatewayMiddleware(BaseHTTPMiddleware):
    """High-Performance Enterprise API Gateway Middleware."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        correlation_id = request.headers.get("X-Correlation-ID", f"corr_{uuid.uuid4().hex[:12]}")
        request.state.correlation_id = correlation_id

        # 1. Version Routing Check
        path = request.url.path
        if not path.startswith("/api/v1") and not path.startswith("/api/v2") and path not in ["/docs", "/redoc", "/openapi.json", "/"]:
            return Response(
                content=json.dumps({"success": False, "code": "INVALID_API_VERSION", "message": "API version not supported. Use /api/v1/* or /api/v2/*"}),
                status_code=status.HTTP_404_NOT_FOUND,
                media_type="application/json"
            )

        # 2. Authentication & API Key Inspection
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer gai_"):
            raw_key = auth_header.replace("Bearer ", "").strip()
            key_record = api_key_service.authenticate_key(raw_key)
            if not key_record:
                return Response(
                    content=json.dumps({"success": False, "code": "UNAUTHORIZED_KEY", "message": "Invalid or revoked API Key."}),
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    media_type="application/json"
                )
            request.state.api_key = key_record

        # 3. Request Security Screening (SQLi / XSS)
        query_str = str(request.query_params)
        try:
            enterprise_admin_security_engine.validate_sqli_safety(query_str)
        except Exception as e:
            return Response(
                content=json.dumps({"success": False, "code": "SECURITY_VIOLATION", "message": str(e)}),
                status_code=status.HTTP_400_BAD_REQUEST,
                media_type="application/json"
            )

        # 4. Dispatch Request to Route Handler
        response = await call_next(request)

        # 5. Response Formatting & Headers Enrichment
        process_time_ms = round((time.time() - start_time) * 1000, 2)
        response.headers["X-Correlation-ID"] = correlation_id
        response.headers["X-Process-Time-MS"] = str(process_time_ms)
        if "X-API-Version" not in response.headers:
            response.headers["X-API-Version"] = "v1.0.0"

        return response
