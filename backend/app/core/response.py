"""
GuardianAI Standardized Response Builder Utilities
Purpose: Provides reusable helper functions to construct unified API responses with request correlation IDs.
"""

import math
from typing import Any, List, Optional
from datetime import datetime, timezone
from fastapi import Request
from fastapi.responses import JSONResponse
from app.schemas.response import APIResponse

def get_request_id_from_request(request: Optional[Request]) -> str:
    """Extracts X-Request-ID correlation string from FastAPI Request state or headers."""
    if request and hasattr(request.state, "request_id"):
        return request.state.request_id
    if request and "X-Request-ID" in request.headers:
        return request.headers["X-Request-ID"]
    return "req_unknown"

def success_response(
    data: Any = None,
    message: str = "Operation completed successfully.",
    status_code: int = 200,
    request: Optional[Request] = None,
    request_id: Optional[str] = None
) -> JSONResponse:
    """Constructs a unified HTTP 2xx success response envelope."""
    req_id = request_id or get_request_id_from_request(request)
    
    payload = APIResponse(
        success=True,
        message=message,
        data=data,
        errors=[],
        timestamp=datetime.now(timezone.utc).isoformat(),
        request_id=req_id
    )

    return JSONResponse(
        status_code=status_code,
        headers={"X-Request-ID": req_id},
        content=payload.model_dump(mode="json")
    )

def error_response(
    message: str = "An error occurred while processing the request.",
    errors: Optional[List[Any]] = None,
    status_code: int = 400,
    request: Optional[Request] = None,
    request_id: Optional[str] = None
) -> JSONResponse:
    """Constructs a unified HTTP 4xx/5xx error response envelope."""
    req_id = request_id or get_request_id_from_request(request)

    payload = APIResponse(
        success=False,
        message=message,
        data=None,
        errors=errors or [],
        timestamp=datetime.now(timezone.utc).isoformat(),
        request_id=req_id
    )

    return JSONResponse(
        status_code=status_code,
        headers={"X-Request-ID": req_id},
        content=payload.model_dump(mode="json")
    )

def paginated_response(
    items: List[Any],
    total: int,
    page: int,
    size: int,
    message: str = "Paginated records retrieved successfully.",
    status_code: int = 200,
    request: Optional[Request] = None
) -> JSONResponse:
    """Constructs a unified HTTP 200 paginated list response envelope."""
    req_id = get_request_id_from_request(request)
    pages_count = math.ceil(total / size) if size > 0 else 1

    paginated_data = {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages_count
    }

    payload = APIResponse(
        success=True,
        message=message,
        data=paginated_data,
        errors=[],
        timestamp=datetime.now(timezone.utc).isoformat(),
        request_id=req_id
    )

    return JSONResponse(
        status_code=status_code,
        headers={"X-Request-ID": req_id},
        content=payload.model_dump(mode="json")
    )
