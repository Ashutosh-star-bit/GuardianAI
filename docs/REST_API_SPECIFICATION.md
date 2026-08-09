# GuardianAI Master Public REST API Specification & Developer Guide

**Document Version:** 1.0.0  
**OpenAPI Standard:** 3.0.3  
**Base URL:** `https://api.guardianai.io/api/v1`  
**Interactive Swagger UI:** `https://api.guardianai.io/docs`  

---

## 1. Authentication & Security Schemes

GuardianAI public REST endpoints require Bearer Token authorization passed in the HTTP request header:

### Developer API Key Authentication:
```http
Authorization: Bearer gai_live_88f92a110099xza21_prod
```

---

## 2. Standardized Response Envelope & RFC 7807 Error Catalog

### Unified 6-Field JSON Response Envelope (`HTTP 200 OK`):
```json
{
  "success": true,
  "message": "URL phishing analysis complete.",
  "data": {
    "target_url": "http://hdfc-verify.top",
    "scam_category": "TYPOSQUATTING",
    "threat_score": 98,
    "confidence": 0.99,
    "recommended_action": "BLOCK_AND_REPORT",
    "explanation": "Homoglyph domain spoofing HDFC Bank."
  },
  "errors": [],
  "timestamp": "2026-08-01T13:15:00Z",
  "request_id": "req_88a91102"
}
```

### RFC 7807 Problem Details Error Catalog:

| HTTP Status | Error Code String | Trigger Condition | Solution Guidance |
| :--- | :--- | :--- | :--- |
| `HTTP 400` | `SECURITY_VIOLATION` | Malicious payload signature (SQLi / XSS script) detected. | Sanitize query inputs & strip script tags. |
| `HTTP 401` | `UNAUTHORIZED_KEY` | Missing, expired, or invalid secret key. | Pass valid `Authorization: Bearer gai_live_*`. |
| `HTTP 403` | `FORBIDDEN_SCOPE` | Key lacks required scope permission (`scan:read`). | Elevate scope in Developer Portal. |
| `HTTP 429` | `RATE_LIMIT_EXCEEDED` | Tier rate limit reached. | Backoff using `X-RateLimit-Reset` header. |

---

## 3. Public REST API Endpoint Reference

### 1. Inspect Text Message (`POST /api/v1/public/scan/text`)
**Request Body:**
```json
{
  "text": "URGENT: Your HDFC account is suspended. Update KYC at http://hdfc-verify.top"
}
```

### 2. Inspect URL Typosquatting (`POST /api/v1/public/scan/url`)
**Request Body:**
```json
{
  "url": "http://hdfc-bank-login.top"
}
```

### 3. Inspect BEC Email Wire Fraud (`POST /api/v1/public/scan/email`)
**Request Body:**
```json
{
  "subject": "Urgent Wire Transfer Authorization",
  "body": "Please wire $50,000 to account 99887766 immediately."
}
```

### 4. Inspect Document OCR Text (`POST /api/v1/public/scan/ocr`)
**Request Body:**
```json
{
  "document_text": "POLICE NOTICE: Digital arrest warrant issued. Pay fine via UPI."
}
```

### 5. Inspect Voice Deepfake Transcript (`POST /api/v1/public/scan/voice`)
**Request Body:**
```json
{
  "audio_transcript": "This is Officer Sharma from Cyber Cell. Transfer fine via UPI."
}
```

---

## 4. Integration Tutorials

### Python SDK (`pip install guardianai-sdk`):
```python
from guardianai import GuardianAIClient

client = GuardianAIClient(api_key="gai_live_88f92a110099xza21_prod")
result = client.scan_url("http://hdfc-verify.top")
print(f"Risk Score: {result.threat_score}, Action: {result.recommended_action}")
```

### TypeScript SDK (`npm install @guardianai/sdk`):
```typescript
import { GuardianAIClient } from '@guardianai/sdk';

const client = new GuardianAIClient({ apiKey: 'gai_live_88f92a110099xza21_prod' });
const result = await client.scanUrl('http://hdfc-verify.top');
console.log(`Risk Score: ${result.threat_score}`);
```
