"""
GuardianAI Rate Limiting Placeholder Middleware
Purpose: Implements sliding-window in-memory IP rate limiting (e.g. 120 requests/min per IP) to prevent DDoS attacks.
"""

import time
from typing import Dict, List
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response, JSONResponse
from app.core.logging import log_security_event

class RateLimitMiddleware(BaseHTTPMiddleware):
    """In-memory sliding window rate limiter placeholder per IP address."""

    def __init__(self, app, requests_per_minute: int = 120):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.request_history: Dict[str, List[float]] = {}

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        client_ip = request.client.host if request.client else "127.0.0.1"
        now = time.time()
        window_start = now - 60.0

        # Clean history for client_ip
        if client_ip in self.request_history:
            self.request_history[client_ip] = [
                t for t in self.request_history[client_ip] if t > window_start
            ]
        else:
            self.request_history[client_ip] = []

        # Check limit threshold
        if len(self.request_history[client_ip]) >= self.requests_per_minute:
            log_security_event(
                event="RATE_LIMIT_EXCEEDED",
                ip_address=client_ip,
                reason=f"Exceeded {self.requests_per_minute} requests/min limit"
            )
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "status": 429,
                    "title": "Too Many Requests",
                    "detail": f"Rate limit of {self.requests_per_minute} requests per minute exceeded. Please try again shortly.",
                },
                headers={
                    "Retry-After": "60",
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0"
                }
            )

        self.request_history[client_ip].append(now)

        response = await call_next(request)
        remaining = max(0, self.requests_per_minute - len(self.request_history[client_ip]))
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        return response
