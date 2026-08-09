"""
GuardianAI Correlation Request ID Middleware
Purpose: Generates or propagates a unique UUIDv4 correlation ID for every HTTP request, storing it in request state and appending X-Request-ID response header.
"""

import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Extract existing X-Request-ID header or generate new UUIDv4
        request_id = request.headers.get("X-Request-ID") or f"req_{uuid.uuid4().hex[:16]}"
        request.state.request_id = request_id

        response = await call_next(request)

        # Inject X-Request-ID into HTTP response headers
        response.headers["X-Request-ID"] = request_id
        return response
