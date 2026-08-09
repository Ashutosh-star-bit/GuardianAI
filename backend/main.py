"""
GuardianAI FastAPI Master Entrypoint
Purpose: Initializes FastAPI instance, configures OpenAPI/Swagger documentation with Bearer Security,
         registers Middleware stack (API Gateway, Versioning, Request ID, Process Time, Security Headers, CORS, Rate Limiter),
         and mounts API v1 & v2 routes with RFC 7807 global exception handlers.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.core.config import settings
from app.core.logging import logger
from app.core.handlers import register_exception_handlers
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.process_time import ProcessTimeMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.gateway.api_gateway import APIGatewayMiddleware
from app.core.versioning import APIVersioningMiddleware
from app.api.v1.router import api_v1_router
from app.api.v2.router import api_v2_router
from app.db.session import engine
from app.db.base import Base

from sqlalchemy import text

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler executing startup database initialization and shutdown cleanup."""
    logger.info(f"Starting {settings.PROJECT_NAME} API v{settings.VERSION} [{settings.ENVIRONMENT}]...")
    Base.metadata.create_all(bind=engine)
    
    # Auto-migration check: Ensure all User model columns exist in SQLite table
    with engine.begin() as conn:
        cols_to_add = [
            ("full_name", "VARCHAR(255)"),
            ("role", "VARCHAR(50) DEFAULT 'user'"),
            ("is_verified", "BOOLEAN DEFAULT 0"),
            ("updated_at", "DATETIME"),
            ("deleted_at", "DATETIME"),
        ]
        for col_name, col_type in cols_to_add:
            try:
                conn.execute(text(f"ALTER TABLE users ADD COLUMN {col_name} {col_type};"))
            except Exception:
                pass # Column already exists

    yield
    logger.info(f"Shutting down {settings.PROJECT_NAME} API service gracefully...")

tags_metadata = [
    {"name": "System", "description": "System root welcome metadata & health probes."},
    {"name": "Authentication", "description": "User authentication & OAuth routes."},
    {"name": "OAuth Authentication", "description": "Google, GitHub, and Microsoft Entra OAuth2 SSO."},
    {"name": "Users", "description": "User profile management."},
    {"name": "Public Developer API", "description": "Public developer REST API endpoints for Text, URL, Email, OCR, Voice, Threat Intel, and Decision Engine."},
    {"name": "Developer Platform API Keys", "description": "API Key management (Generate, Rotate, Disable, Delete)."},
    {"name": "Developer Platform Analytics", "description": "API Usage, Latency p95/p99, Token Usage, and Bandwidth Telemetry."},
    {"name": "Feature Flags", "description": "Sub-0.1ms thread-safe platform feature flag toggles."},
    {"name": "API v2 (Preview)", "description": "Future major version v2 preview endpoints."}
]

app_description = """
# GuardianAI Anti-Scam Platform REST API & Developer Gateway

Welcome to the **GuardianAI REST API & Public Developer Gateway Documentation**. GuardianAI is a **Privacy-First Explainable AI (XAI) Anti-Scam Engine** designed to detect and explain online fraud across Text, Email, URL, and QR code payloads.

---

## 🔑 Authentication Schemes
- **Developer API Keys:** `Authorization: Bearer gai_live_*`
- **User JWT Access Tokens:** `Authorization: Bearer <your_jwt_token>`

---

## 🛡️ Response Envelope Standard
All successful responses return a unified 6-field JSON envelope:
- `success`: boolean
- `message`: human-readable string
- `data`: payload object or array
- `errors`: empty array
- `timestamp`: ISO 8601 UTC string
- `request_id`: correlation string (`req_...`)

Error responses adhere to **RFC 7807 Problem Details** format.
"""

app = FastAPI(
    title=f"{settings.PROJECT_NAME} REST API Engine",
    version=settings.VERSION,
    description=app_description,
    openapi_tags=tags_metadata,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Custom OpenAPI Generator adding OAuth2 Bearer Security Scheme
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=f"{settings.PROJECT_NAME} REST API Engine",
        version=settings.VERSION,
        description=app_description,
        routes=app.routes,
        tags=tags_metadata
    )

    # Inject Security Scheme for Interactive Swagger Authorize Button
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter your JWT Access Token or Developer API Key gai_live_*"
        }
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Register Custom Middlewares Stack
app.add_middleware(APIVersioningMiddleware)
app.add_middleware(APIGatewayMiddleware)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(ProcessTimeMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware, requests_per_minute=120)

# Configure Trusted Host Header Middleware
if settings.ENVIRONMENT in ["production", "staging"]:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1", "*.guardianai.io"]
    )

# Configure CORS Middleware
if settings.CORS_ORIGINS:
    origins = settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else [settings.CORS_ORIGINS]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID", "X-Process-Time", "X-RateLimit-Limit", "X-RateLimit-Remaining", "X-Correlation-ID", "X-API-Version", "X-API-Deprecation-Date", "X-API-Sunset-Date"]
    )

# Register Global RFC 7807 Exception Handlers
register_exception_handlers(app)

# Mount API v1 & v2 Routers
app.include_router(api_v1_router, prefix=settings.API_V1_STR)
app.include_router(api_v2_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
