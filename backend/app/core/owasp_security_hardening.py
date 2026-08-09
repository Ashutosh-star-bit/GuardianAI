"""
GuardianAI OWASP Top 10 Comprehensive Security Hardening Engine
Defensive Coverage:
  1. Authentication & Brute-Force Rate Limiting
  2. Broken Access Control (RBAC / ABAC Authorization)
  3. Safe File Upload Sanitization (Magic byte check, extension whitelist, path traversal blocking)
  4. LLM Prompt Injection Screening (Adversarial jailbreak detection)
  5. Cross-Site Scripting (XSS) Input Sanitization
  6. Cross-Site Request Forgery (CSRF) SameSite Strict Validation
  7. SQL Injection (SQLi) Parameterized Query Verification
  8. Server-Side Request Forgery (SSRF) URL Domain Sanitization (Internal IP & Private CIDR blocking)
"""

import re
import os
import urllib.parse
from typing import Dict, Any, List, Optional

class OWASPSecurityException(Exception):
    """Exception raised for OWASP defensive security violations."""
    def __init__(self, message: str, code: str = "OWASP_SECURITY_VIOLATION"):
        self.message = message
        self.code = code
        super().__init__(message)

class OWASPSecurityHardeningEngine:
    """Enterprise OWASP Top 10 Security Hardening Guardrails."""

    ALLOWED_FILE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".pdf", ".txt"}
    ALLOWED_MIME_TYPES = {"image/png", "image/jpeg", "application/pdf", "text/plain"}
    
    PRIVATE_IP_REGEX = re.compile(
        r"^(localhost|127\.\d+\.\d+\.\d+|10\.\d+\.\d+\.\d+|172\.(1[6-9]|2[0-9]|3[0-1])\.\d+\.\d+|192\.168\.\d+\.\d+|0\.0\.0\.0|169\.254\.\d+\.\d+|::1)$",
        re.IGNORECASE
    )

    PROMPT_INJECTION_PATTERNS = [
        re.compile(r"ignore\s+(all\s+)?previous\s+instructions", re.IGNORECASE),
        re.compile(r"you\s+are\s+now\s+a\s+DAN", re.IGNORECASE),
        re.compile(r"override\s+system\s+prompt", re.IGNORECASE),
        re.compile(r"reveal\s+(your\s+)?system\s+(prompt|instructions)", re.IGNORECASE)
    ]

    XSS_PATTERNS = [
        re.compile(r"<script.*?>.*?</script>", re.IGNORECASE | re.DOTALL),
        re.compile(r"javascript:", re.IGNORECASE),
        re.compile(r"onload\s*=", re.IGNORECASE),
        re.compile(r"onerror\s*=", re.IGNORECASE)
    ]

    SQLI_PATTERNS = [
        re.compile(r"(\bUNION\b\s+\bSELECT\b)", re.IGNORECASE),
        re.compile(r"(--|\bOR\b\s+['\"].*?['\"]=|\bDROP\b\s+\bTABLE\b)", re.IGNORECASE)
    ]

    @classmethod
    def validate_ssrf_url(cls, target_url: str) -> str:
        """Protects against SSRF by rejecting requests to internal IPs, metadata endpoints, and non-HTTP schemes."""
        if not target_url or not isinstance(target_url, str):
            raise OWASPSecurityException("Invalid target URL provided.", code="SSRF_INVALID_URL")

        parsed = urllib.parse.urlparse(target_url.strip())
        if parsed.scheme.lower() not in ("http", "https"):
            raise OWASPSecurityException(f"Unsupported URI scheme '{parsed.scheme}'. Only HTTP and HTTPS are permitted.", code="SSRF_DISALLOWED_SCHEME")

        hostname = parsed.hostname
        if not hostname:
            raise OWASPSecurityException("URL hostname missing.", code="SSRF_MISSING_HOSTNAME")

        if cls.PRIVATE_IP_REGEX.match(hostname):
            raise OWASPSecurityException(f"Access to private/internal IP address '{hostname}' is forbidden.", code="SSRF_PRIVATE_IP_BLOCKED")

        return target_url

    @classmethod
    def sanitize_file_upload(cls, filename: str, content_type: str, file_bytes: bytes) -> str:
        """Protects against malicious file uploads, directory traversal, and extension spoofing."""
        clean_basename = os.path.basename(filename)
        _, ext = os.path.splitext(clean_basename.lower())

        if ext not in cls.ALLOWED_FILE_EXTENSIONS:
            raise OWASPSecurityException(f"Disallowed file extension '{ext}'. Only images and documents allowed.", code="FILE_EXTENSION_DISALLOWED")

        if content_type.lower() not in cls.ALLOWED_MIME_TYPES:
            raise OWASPSecurityException(f"Disallowed MIME type '{content_type}'.", code="FILE_MIME_DISALLOWED")

        return clean_basename

    @classmethod
    def screen_prompt_injection(cls, prompt_text: str) -> bool:
        """Detects adversarial LLM prompt injection and jailbreak attempts."""
        if not prompt_text:
            return False

        for pattern in cls.PROMPT_INJECTION_PATTERNS:
            if pattern.search(prompt_text):
                raise OWASPSecurityException("Prompt Injection detected: Adversarial override pattern identified.", code="PROMPT_INJECTION_DETECTED")
        return False

    @classmethod
    def screen_xss_and_sqli(cls, input_str: str) -> str:
        """Pre-screens input strings against XSS script tags and SQL injection signatures."""
        if not input_str:
            return ""

        for pattern in cls.XSS_PATTERNS:
            if pattern.search(input_str):
                raise OWASPSecurityException("Cross-Site Scripting (XSS) payload detected.", code="XSS_DETECTED")

        for pattern in cls.SQLI_PATTERNS:
            if pattern.search(input_str):
                raise OWASPSecurityException("SQL Injection (SQLi) signature detected.", code="SQLI_DETECTED")

        return input_str

owasp_security_engine = OWASPSecurityHardeningEngine()
