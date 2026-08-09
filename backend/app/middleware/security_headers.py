"""
GuardianAI Security Headers Middleware
Purpose: Injects baseline security headers while allowing CDN script/style assets for Swagger UI (/docs) and ReDoc (/redoc).
"""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)

        # Baseline Security Headers
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Apply CSP header (allowing CDN assets for Swagger UI & ReDoc docs rendering)
        if request.url.path in ["/docs", "/redoc", "/api/v1/openapi.json"]:
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                "img-src 'self' data: https://fastapi.tiangolo.com;"
            )
        else:
            response.headers["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none';"

        return response
