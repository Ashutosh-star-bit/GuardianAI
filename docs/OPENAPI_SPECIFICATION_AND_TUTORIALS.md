# GuardianAI Master OpenAPI 3.0 Specification, Tutorials & Developer Reference

**Document Version:** 1.0.0  
**OpenAPI Standard:** OpenAPI 3.0.3  
**Base URL:** `https://api.guardianai.io/api/v1`  
**Swagger UI:** `https://api.guardianai.io/docs`  
**ReDoc UI:** `https://api.guardianai.io/redoc`  

---

## 1. Authentication & Security Schemes

GuardianAI supports two primary authentication mechanisms:

1. **Developer API Keys (`Bearer gai_live_*` or `Bearer gai_test_*`):**  
   Header: `Authorization: Bearer gai_live_88f92a110099xza21_prod`
2. **User JWT Access Tokens (`Bearer <token>`):**  
   Issued via `POST /api/v1/auth/login`.

---

## 2. Standardized Response Envelope & RFC 7807 Error Catalog

### Success Response Envelope (`HTTP 200 OK`):
```json
{
  "success": true,
  "message": "Text payload analysis complete.",
  "data": {
    "scam_category": "DIGITAL_ARREST",
    "threat_score": 98,
    "confidence": 0.99,
    "recommended_action": "BLOCK_AND_REPORT"
  },
  "errors": [],
  "timestamp": "2026-08-01T04:42:00Z",
  "request_id": "req_88a91102"
}
```

### Error Response Catalog (RFC 7807 Problem Details):

| HTTP Status | Error Code String | Description & Resolution |
| :--- | :--- | :--- |
| `HTTP 400` | `SECURITY_VIOLATION` | Malicious payload signature (SQLi / XSS script) detected. |
| `HTTP 401` | `UNAUTHORIZED_KEY` | API Key missing, expired, or invalid secret hash. |
| `HTTP 403` | `FORBIDDEN_SCOPE` | Key lacks required scope permission (`scan:read`). |
| `HTTP 423` | `ACCOUNT_LOCKED` | Account locked for 15 minutes after 5 failed login attempts. |
| `HTTP 429` | `RATE_LIMIT_EXCEEDED` | Tier rate limit (RPS or daily quota) exceeded. |
| `HTTP 500` | `INTERNAL_ENGINE_ERROR` | Unexpected backend pipeline exception. |

---

## 3. Quickstart Integration Tutorials

### Tutorial 1: Inspecting Text Smishing Messages (Python SDK):
```python
from guardianai import GuardianAIClient

client = GuardianAIClient(api_key="gai_live_88f92a110099xza21_prod")
result = client.scan_text("URGENT: Update HDFC netbanking at http://hdfc-verify.top")

if result.threat_score > 80:
    print(f"ALERT: Scam Detected ({result.threat_score}/100)! Action: {result.recommended_action}")
```

### Tutorial 2: Inspecting URL Typosquatting (TypeScript SDK):
```typescript
import { GuardianAIClient } from '@guardianai/sdk';

const client = new GuardianAIClient({ apiKey: 'gai_live_88f92a110099xza21_prod' });
const result = await client.scanUrl('http://hdfc-bank-login.top');

console.log(`Target URL: http://hdfc-bank-login.top, Risk: ${result.threat_score}`);
```

### Tutorial 3: Querying Threat Intelligence IOCs (cURL):
```bash
curl -X GET "https://api.guardianai.io/api/v1/public/threat-intel?indicator=hdfc-verify.top" \
  -H "Authorization: Bearer gai_live_88f92a110099xza21_prod"
```

---

## 4. Complete Public API Endpoint Reference

- `POST /api/v1/public/scan/text`: Text / SMS Smishing Inspection
- `POST /api/v1/public/scan/url`: URL Typosquatting Inspection
- `POST /api/v1/public/scan/email`: BEC Wire Fraud Inspection
- `POST /api/v1/public/scan/ocr`: Document OCR Text Inspection
- `POST /api/v1/public/scan/voice`: Voice Deepfake Audio Inspection
- `GET  /api/v1/public/threat-intel`: Threat Intelligence IOC Lookup
- `POST /api/v1/public/decision`: Master Decision Engine Evaluation
- `GET  /api/v1/public/community/reports`: Read-Only Crowdsourced Feed
