# GuardianAI API Foundation & Envelopes Specification

**Document Version:** 1.0.0  
**Target Platform:** GuardianAI REST API  
**Standards:** OpenAPI 3.0, RFC 7807 Problem Details, Semantic Versioning 2.0  

---

## 1. Overview & API Versioning

All GuardianAI API routes are versioned under explicit path prefixes:
- **Base Endpoint URL:** `/api/v1`
- **OpenAPI Schema Definition:** `/api/v1/openapi.json`
- **Interactive Swagger UI:** `/docs`
- **Interactive ReDoc UI:** `/redoc`

---

## 2. Global Response Envelopes

To maintain consistency across all endpoints, GuardianAI wraps API responses in standard JSON envelopes.

### 2.1 Success Response Envelope (`ApiResponse[T]`)

```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "service": "GuardianAI",
    "version": "1.0.0",
    "uptimeSeconds": 1420
  },
  "meta": {
    "requestId": "req_8f3a9d2e1b4c5678",
    "timestamp": "2026-07-28T23:25:00.123Z",
    "version": "1.0.0"
  }
}
```

### 2.2 Standard Error Model (RFC 7807 `ApiErrorEnvelope`)

```json
{
  "success": false,
  "error": {
    "code": "UNPROCESSABLE_ENTITY",
    "message": "Input request payload validation failed",
    "status": 422,
    "requestId": "req_8f3a9d2e1b4c5678",
    "timestamp": "2026-07-28T23:25:00.456Z",
    "details": [
      {
        "field": "body.payload",
        "issue": "Field required"
      }
    ]
  }
}
```

---

## 3. Correlation Request IDs (`X-Request-ID`)

Every incoming HTTP request passes through `RequestIDMiddleware`:
1. Checks for an incoming `X-Request-ID` header (from API gateways or frontends).
2. If missing, automatically generates a unique UUIDv4 string (`req_8f3a9d2e1b4c5678`).
3. Attaches `request.state.request_id` for use in application loggers.
4. Exposes `X-Request-ID` in the HTTP response headers for debugging and distributed tracing.

---

## 4. HTTP Middleware Pipeline

```
Incoming Request
      │
      ▼
┌───────────────────────────────────────────┐
│ 1. RequestIDMiddleware                    │ Generates/extracts X-Request-ID
└─────────────────────┬─────────────────────┘
                      │
                      ▼
┌───────────────────────────────────────────┐
│ 2. ProcessTimeMiddleware                  │ Measures execution time (X-Process-Time)
└─────────────────────┬─────────────────────┘
                      │
                      ▼
┌───────────────────────────────────────────┐
│ 3. SecurityHeadersMiddleware              │ Injects CSP, HSTS, X-Frame-Options
└─────────────────────┬─────────────────────┘
                      │
                      ▼
┌───────────────────────────────────────────┐
│ 4. CORSMiddleware                         │ Validates Whitelisted Origins
└─────────────────────┬─────────────────────┘
                      │
                      ▼
                Route Controller
```

---

## 5. OpenAPI & Swagger UI Configuration

- **Title:** `GuardianAI API Engine`
- **Exposed Headers:** `X-Request-ID`, `X-Process-Time`
- **Tags Categorization:**
  - `System`: Health and root metadata endpoints
  - `Authentication`: User registration and JWT login routes
  - `Scans`: Text, Email, URL, and QR code XAI analysis endpoints
