"""
GuardianAI API v1 Main Router Aggregator
"""

from fastapi import APIRouter
from app.api.v1.endpoints import (
    root,
    health,
    auth,
    oauth,
    users,
    messages,
    emails,
    urls,
    threat,
    decision,
    analyse,
    qr,
    ocr,
    voice,
    community,
    reports,
    analytics,
    admin,
    settings,
    upload,
    feature_flags,
    api_keys,
    public_api,
    developer_analytics,
    system_metrics
)

api_v1_router = APIRouter()

# 1. System, Health Diagnostics & Metrics
api_v1_router.include_router(root.router, tags=["System"])
api_v1_router.include_router(health.router, tags=["System"])
api_v1_router.include_router(system_metrics.router, tags=["System Metrics Telemetry"])

# 2. Authentication, OAuth & User Management
api_v1_router.include_router(auth.router, tags=["Authentication"])
api_v1_router.include_router(oauth.router, tags=["OAuth Authentication"])
api_v1_router.include_router(users.router, tags=["Users"])

# 3. Master Pipeline, Document Intelligence, Voice & Threat Scanners
api_v1_router.include_router(analyse.router, tags=["Scam Analysis Pipeline"])
api_v1_router.include_router(ocr.router, tags=["Document Intelligence OCR"])
api_v1_router.include_router(voice.router, tags=["Voice Intelligence"])
api_v1_router.include_router(messages.router, tags=["Message Scans"])
api_v1_router.include_router(emails.router, tags=["Email Scans"])
api_v1_router.include_router(urls.router, tags=["URL Scans"])
api_v1_router.include_router(threat.router, tags=["Threat Intelligence"])
api_v1_router.include_router(decision.router, tags=["Master Decision Engine"])
api_v1_router.include_router(qr.router, tags=["QR Scans"])

# 4. Intelligence, Community & HITL Reporting
api_v1_router.include_router(community.router, tags=["Community Intelligence & HITL"])
api_v1_router.include_router(reports.router, tags=["Reports"])
api_v1_router.include_router(analytics.router, tags=["Analytics"])

# 5. Administration, Settings, Feature Flags, API Keys & Developer Analytics
api_v1_router.include_router(admin.router, tags=["Admin"])
api_v1_router.include_router(settings.router, tags=["Settings"])
api_v1_router.include_router(upload.router, tags=["Uploads"])
api_v1_router.include_router(feature_flags.router, tags=["Feature Flags"])
api_v1_router.include_router(api_keys.router, tags=["Developer Platform API Keys"])
api_v1_router.include_router(public_api.router, tags=["Public Developer API"])
api_v1_router.include_router(developer_analytics.router, tags=["Developer Platform Analytics"])
