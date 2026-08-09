# GuardianAI Developer Platform & Integration Guide

**Document Version:** 1.0.0  
**Target Audience:** Software Engineers, Security Architects & System Integrators  
**Base URL:** `https://api.guardianai.io/api/v1`  
**Interactive Swagger UI:** `https://api.guardianai.io/docs`  

---

## 1. Quick Start (5-Minute Integration)

Follow these 3 steps to integrate GuardianAI Anti-Scam protection into your application:

### Step 1: Obtain your API Key
Log in to the **GuardianAI Developer Portal** at `https://guardianai.io/developer` and click **Generate New API Key**. Keep your key secret:
- Live Key Prefix: `gai_live_...`
- Test Key Prefix: `gai_test_...`

### Step 2: Install Official SDK Client Library
Choose your language package manager:
```bash
# Python SDK
pip install guardianai-sdk

# Node.js / TypeScript SDK
npm install @guardianai/sdk

# Go SDK
go get github.com/guardianai/sdk-go
```

### Step 3: Run your First Inspection Request (Python)
```python
from guardianai import GuardianAIClient

client = GuardianAIClient(api_key="gai_live_88f92a110099xza21_prod")
result = client.scan_url("http://hdfc-verify.top")

print(f"Threat Score: {result.threat_score}/100")
print(f"Action: {result.recommended_action}")
```

---

## 2. Authentication & Authorization

All API requests to `/api/v1/public/*` require a valid Bearer token passed in the `Authorization` header:

```http
POST /api/v1/public/scan/url HTTP/1.1
Host: api.guardianai.io
Authorization: Bearer gai_live_88f92a110099xza21_prod
Content-Type: application/json
```

---

## 3. Rate Limits & Quotas SLA Matrix

| Subscription Tier | Sliding Window Rate Limit | Daily Request Quota | HTTP 429 Reset Headers |
| :--- | :--- | :--- | :--- |
| **Free Sandbox** | 10 requests / second | 1,000 requests / day | `X-RateLimit-Reset: 60` |
| **Pro Business** | 100 requests / second | 50,000 requests / day | `X-RateLimit-Reset: 60` |
| **Enterprise SLA** | 1,000 requests / second | 20,000,000 requests / day | `X-RateLimit-Reset: 60` |

---

## 4. RFC 7807 Error Codes Catalog

| HTTP Status | Error Code String | Cause & Resolution Guidance |
| :--- | :--- | :--- |
| `HTTP 400` | `SECURITY_VIOLATION` | Payload contains SQLi or XSS injection scripts. Sanitize inputs. |
| `HTTP 401` | `UNAUTHORIZED_KEY` | Missing or invalid API Key. Check `Authorization: Bearer gai_*`. |
| `HTTP 403` | `FORBIDDEN_SCOPE` | Key lacks scope (`scan:read`). Request scope elevation. |
| `HTTP 429` | `RATE_LIMIT_EXCEEDED` | Rate limit exceeded. Backoff using `X-RateLimit-Reset` header. |

---

## 5. Enterprise Integration Best Practices

1. **Never Commit API Keys to Source Control:** Store secrets in environment variables (`GUARDIANAI_API_KEY`).
2. **Implement Exponential Backoff:** Retry transient HTTP 5xx errors with jittered backoff (1s, 2s, 4s).
3. **Verify Webhook HMAC Signatures:** Check `X-GuardianAI-Signature` using your webhook secret (`whsec_*`).
