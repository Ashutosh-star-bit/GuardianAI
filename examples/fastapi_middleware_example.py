"""
GuardianAI FastAPI Middleware Integration Example
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../sdks/python")))
from guardianai import GuardianAIClient

app = FastAPI(title="Partner App with GuardianAI Anti-Scam Shield")
guardian_client = GuardianAIClient(api_key="gai_live_88f92a110099xza21_prod")

@app.middleware("http")
async def guardianai_anti_scam_middleware(request: Request, call_next):
    """Pre-screens incoming form submissions for scam signatures."""
    if request.method == "POST" and "/submit-comment" in request.url.path:
        body_bytes = await request.body()
        text_payload = body_bytes.decode("utf-8", errors="ignore")

        # Scan with GuardianAI SDK
        result = guardian_client.scan_text(text_payload)
        if result.threat_score > 80:
            return JSONResponse(
                status_code=400,
                content={
                    "error": "SCAM_BLOCKED",
                    "message": "Comment submission blocked due to high phishing risk score.",
                    "threat_score": result.threat_score
                }
            )

    return await call_next(request)

@app.get("/")
async def root():
    return {"message": "Partner app running with GuardianAI Anti-Scam middleware."}
