# GuardianAI Production Logging & Observability Strategy

**Document Version:** 1.0.0  
**Target Platform:** GuardianAI Backend & AI Reasoning Services  
**Compliance Standard:** ISO/IEC 27001, GDPR Zero-Knowledge PII Protection, OWASP Logging Standard  

---

## 1. Executive Overview

GuardianAI employs a **Structured, Multi-Category, Privacy-First Logging Strategy**.
- **Development Environment:** Human-readable colorized logs directed to `sys.stdout`.
- **Production / Staging Environment:** ISO 8601 timestamped **Structured JSON Logs** written to stdout and rotating log files inside `logs/`, designed for direct ingestion into Datadog, ELK Stack, Grafana Loki, or CloudWatch.

All log output passes through a mandatory **PII Scrubbing Stream Filter** to Anonymize Credit Cards, SSNs, IBANs, Phone Numbers, and User Passwords *before* disk write or transport.

---

## 2. Log Category Topology & Directory Structure

```
logs/
├── access.log        # HTTP request/response metrics, latency, & status codes
├── error.log         # Uncaught exceptions, 5xx errors, & stack traces
├── security.log      # Auth attempts, JWT validation failures, rate limits, & prompt injections
├── ai_inference.log  # Gemini/Llama model execution, token count, risk band, & latency
└── .gitkeep
```

---

## 3. Log Category Specifications & JSON Schemas

### 3.1 HTTP Access & Request/Response Logging (`logs/access.log`)
Tracks every incoming HTTP request, client IP (anonymized in prod), status code, response time, and user agent.

```json
{
  "timestamp": "2026-07-28T22:58:00.123Z",
  "category": "access",
  "level": "INFO",
  "service": "GuardianAI",
  "environment": "production",
  "request": {
    "id": "req_8f3a9d2e1b4c",
    "method": "POST",
    "path": "/api/v1/scan/text",
    "clientIp": "192.168.x.x",
    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
  },
  "response": {
    "status": 200,
    "processTimeMs": 142.8
  }
}
```

### 3.2 Security & Authentication Logging (`logs/security.log`)
Records authentication logins, failed password attempts, rate limit violations, and detected prompt injection attempts.

```json
{
  "timestamp": "2026-07-28T22:58:15.456Z",
  "category": "security",
  "level": "WARNING",
  "service": "GuardianAI",
  "environment": "production",
  "event": "AUTH_FAILED",
  "actor": {
    "userId": "usr_99a8b7c6",
    "email": "u***r@example.com"
  },
  "securityContext": {
    "reason": "INVALID_PASSWORD_HASH",
    "ip": "203.0.113.45",
    "failedAttempts": 3
  }
}
```

### 3.3 AI Model Inference Logging (`logs/ai_inference.log`)
Measures LLM inference performance, primary/fallback model selection, token counts, and output threat scores.

```json
{
  "timestamp": "2026-07-28T22:58:30.789Z",
  "category": "ai_inference",
  "level": "INFO",
  "service": "GuardianAI",
  "environment": "production",
  "inference": {
    "scanId": "scn_a1b2c3d4e5f6",
    "provider": "google_gemini_1_5_flash",
    "fallbackTier": 1,
    "promptTokens": 320,
    "completionTokens": 85,
    "latencyMs": 310.4,
    "threatScore": 88,
    "riskBand": "dangerous",
    "piiScrubCount": 2
  }
}
```

### 3.4 Exception & Error Logging (`logs/error.log`)
Captures 500 internal server errors, database connectivity drops, and unhandled tracebacks.

```json
{
  "timestamp": "2026-07-28T22:58:45.012Z",
  "category": "error",
  "level": "ERROR",
  "service": "GuardianAI",
  "environment": "production",
  "error": {
    "code": "DATABASE_CONNECTION_TIMEOUT",
    "message": "OperationalError: connection to server at localhost:5432 failed",
    "exception": "sqlalchemy.exc.OperationalError",
    "stackTrace": "Traceback (most recent call last):\n  File 'app/db/session.py', line 18..."
  }
}
```

---

## 4. Environment-Aware Configuration Strategy

| Feature | Development Mode | Staging / Production Mode |
| :--- | :--- | :--- |
| **Output Target** | `sys.stdout` Console | `sys.stdout` + Rotating File Handlers (`logs/*.log`) |
| **Format** | Colorized Human-Readable Strings | Structured JSON Strings (Single-line per record) |
| **Log Level** | `DEBUG` | `INFO` (Warnings & Errors isolated) |
| **Max File Size** | N/A | 10 MB per log file |
| **Backup Retention**| N/A | 14 Rotating Backups (Compressed `.gz`) |
| **PII Redaction** | Active (All environments) | Active (All environments) |

---

## 5. Observability & Telemetry Metrics Integration

In addition to structured log files, GuardianAI exports standard OpenTelemetry & Prometheus metrics:
- `guardianai_http_requests_total{method, path, status}` — Total request counter.
- `guardianai_http_request_duration_seconds` — Histogram of request latencies.
- `guardianai_scams_detected_total{risk_band}` — Counter of evaluated threat bands.
- `guardianai_ai_inference_duration_ms{provider}` — Histogram of LLM response latencies.
