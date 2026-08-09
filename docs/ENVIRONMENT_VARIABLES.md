# GuardianAI Environment Variables & Configuration Reference

**Document Version:** 1.0.0  
**Target Platform:** GuardianAI Backend & Frontend Services  

---

## 1. Overview

GuardianAI uses environment variables for zero-hardcoding configuration management.
- **Backend (Python 3.12 / FastAPI):** Loaded and validated via `Pydantic Settings` in `app/core/config.py`.
- **Frontend (React 18 / Vite):** Loaded into client bundle via `import.meta.env` (only variables prefixed with `VITE_`).

---

## 2. Master Environment Variable Matrix

| Variable Name | Scope | Default Value | Security Sensitivity | Description & Allowed Options |
| :--- | :--- | :--- | :--- | :--- |
| `PROJECT_NAME` | Backend | `"GuardianAI"` | Low | Display name of the SaaS platform. |
| `ENVIRONMENT` | Backend | `"development"` | Medium | Options: `development`, `staging`, `production`. Enforces strict security & logging policies. |
| `DEBUG` | Backend | `true` | Medium | Toggles verbose traceback logging and query echoing. Must be `false` in production. |
| `API_V1_STR` | Both | `"/api/v1"` | Low | Global API version prefix path. |
| `HOST` | Backend | `"0.0.0.0"` | Low | Server IP binding. |
| `PORT` / `BACKEND_PORT` | Backend | `8000` | Low | Uvicorn server listening port. |
| `DATABASE_URL` | Backend | `"sqlite:///./guardianai.db"` | High (Prod) | Database connection URI (`sqlite` or `postgresql`). |
| `SECRET_KEY` | Backend | `"dev_secret_key..."` | **CRITICAL** | Master cryptographic signing key for JWT tokens. Minimum 32 chars. **MUST BE CHANGED IN PROD**. |
| `ALGORITHM` | Backend | `"HS256"` | Medium | JWT token signing algorithm (`HS256` or `RS256`). |
| `ACCESS_TOKEN_EXPIRE_MINUTES`| Backend| `15` | Medium | Lifetime of access tokens before requiring refresh. |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Backend| `7` | Medium | Lifetime of refresh tokens before requiring re-login. |
| `CORS_ORIGINS` | Backend | `"http://localhost:5173..."`| High | Comma-separated list of whitelisted frontend origins permitted to execute API requests. |
| `RATE_LIMIT_PER_MINUTE` | Backend | `60` | Medium | Maximum allowed API requests per minute per IP. |
| `UPLOAD_FOLDER` | Backend | `"./uploads"` | Low | Directory location for temporary file uploads. |
| `LOG_LEVEL` | Backend | `"INFO"` | Low | Verbosity level (`DEBUG`, `INFO`, `WARNING`, `ERROR`). |
| `GEMINI_API_KEY` | Backend | `"your-gemini-key..."` | **HIGH** | Primary API key for Google Gemini 1.5 Pro / Flash XAI model inference. |
| `GROQ_API_KEY` | Backend | `"your-groq-key..."` | **HIGH** | Secondary Tier 1 Llama-3 high-speed inference API key. |
| `HUGGINGFACE_API_KEY` | Backend | `"your-huggingface-key..."`| **HIGH** | Tertiary Tier 2 Hugging Face inference key. |
| `VIRUSTOTAL_API_KEY` | Backend | `"your-virustotal-key..."` | **HIGH** | Threat intelligence API key for domain/URL inspection. |
| `VITE_API_BASE_URL` | Frontend| `"http://localhost:8000/api/v1"`| Low | Base URL target for frontend API requests. |
| `VITE_ENABLE_SENIOR_MODE_DEFAULT`| Frontend| `false` | Low | Toggles whether Senior Mode starts ON by default. |
| `VITE_ENABLE_CLIENT_PII_SCRUBBING`| Frontend| `true` | Medium | Enables Web Worker local PII scrubbing before API dispatch. |
| `OCR_ENGINE_PROVIDER` | Backend | `"local_tesseract"` | Low | Future OCR engine choice (`local_tesseract`, `google_vision`). |
| `VOICE_SPEECH_TO_TEXT_PROVIDER`| Backend| `"local_whisper"` | Low | Future Speech-to-text provider (`local_whisper`, `deepgram`). |
| `BROWSER_EXTENSION_ALLOWED_IDS`| Backend| `"ext_chrome..."` | Medium | Authorized browser extension IDs for WebSocket connection security. |

---

## 3. Security Audit & Best Practices

1. **Zero Hardcoded Secrets:** All files in version control (`.env.example`) contain strictly dummy placeholders. Real credentials must be injected at runtime via environment variables or secret vaults (AWS Secrets Manager / HashiCorp Vault).
2. **CORS Restrictions:** In production, wildcard `CORS_ORIGINS="*"` is strictly forbidden. Explicit domain names (`https://app.guardianai.com`) must be specified.
3. **Secret Key Entropy:** In production, generate `SECRET_KEY` using a cryptographically secure random generator:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```
