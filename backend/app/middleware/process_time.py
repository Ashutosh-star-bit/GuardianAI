"""
GuardianAI Request Process Time Middleware
Purpose: Measures request execution duration, appends X-Process-Time response header, and emits structured access logs to logs/access.log.
"""

import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from app.core.logging import access_logger

class ProcessTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time
        process_time_ms = round(process_time * 1000, 2)

        response.headers["X-Process-Time"] = f"{process_time_ms}ms"

        access_logger.info(
            f"HTTP {request.method} {request.url.path} - Status: {response.status_code} - Completed in {process_time_ms}ms"
        )

        return response
