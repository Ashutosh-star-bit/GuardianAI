"""
GuardianAI Standardized Global Exception Handlers
Purpose: Catches domain exceptions, validation errors, database failures, and unhandled exceptions,
         returning RFC 7807 problem details JSON envelopes containing correlation request IDs.
"""

from datetime import datetime, timezone
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError
from app.core.exceptions import BaseAppException
from app.core.logging import logger, log_application_error

def format_rfc7807_error(
    title: str,
    detail: str,
    status_code: int,
    request_id: str,
    path: str,
    errors: list = None
) -> JSONResponse:
    """Utility to build standardized RFC 7807 problem details JSON envelopes."""
    return JSONResponse(
        status_code=status_code,
        headers={"X-Request-ID": request_id, "Content-Type": "application/problem+json"},
        content={
            "type": "about:blank",
            "title": title,
            "status": status_code,
            "detail": detail,
            "instance": path,
            "request_id": request_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "errors": errors or []
        }
    )

def register_exception_handlers(app: FastAPI) -> None:
    """Registers global exception handlers with FastAPI application instance."""

    # 1. Custom Domain Exception Handler
    @app.exception_handler(BaseAppException)
    async def custom_app_exception_handler(request: Request, exc: BaseAppException):
        request_id = getattr(request.state, "request_id", "req_unknown")
        logger.warning(f"Domain Exception [{exc.code}] ReqID={request_id} on {request.url.path}: {exc.message}")
        return format_rfc7807_error(
            title=exc.code,
            detail=exc.message,
            status_code=exc.status_code,
            request_id=request_id,
            path=request.url.path,
            errors=exc.details
        )

    # 2. Pydantic Request Validation Error Handler (HTTP 422)
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        request_id = getattr(request.state, "request_id", "req_unknown")
        logger.warning(f"Request Validation Error ReqID={request_id} on {request.url.path}: {exc.errors()}")
        errors = [{"field": ".".join(str(loc) for loc in err["loc"]), "issue": err["msg"]} for err in exc.errors()]
        return format_rfc7807_error(
            title="Unprocessable Entity",
            detail="Input request payload validation failed.",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            request_id=request_id,
            path=request.url.path,
            errors=errors
        )

    # 3. FastAPI / Starlette HTTP Exception Handler
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        request_id = getattr(request.state, "request_id", "req_unknown")
        logger.warning(f"HTTP Exception [{exc.status_code}] ReqID={request_id} on {request.url.path}: {exc.detail}")
        return format_rfc7807_error(
            title="HTTP Error",
            detail=str(exc.detail),
            status_code=exc.status_code,
            request_id=request_id,
            path=request.url.path
        )

    # 4. Database SQLAlchemy Error Handler (HTTP 500)
    @app.exception_handler(SQLAlchemyError)
    async def database_exception_handler(request: Request, exc: SQLAlchemyError):
        request_id = getattr(request.state, "request_id", "req_unknown")
        log_application_error(
            message=f"Database transaction failure on {request.url.path}",
            exc_info=exc,
            request_id=request_id
        )
        return format_rfc7807_error(
            title="Database Error",
            detail="A database query or transaction constraint failed.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            request_id=request_id,
            path=request.url.path
        )

    # 5. Global Unhandled Exception Handler (HTTP 500)
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        request_id = getattr(request.state, "request_id", "req_unknown")
        log_application_error(
            message=f"Unhandled internal server error on {request.url.path}",
            exc_info=exc,
            request_id=request_id
        )
        return format_rfc7807_error(
            title="Internal Server Error",
            detail="An unexpected server error occurred. Please try again later.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            request_id=request_id,
            path=request.url.path
        )
