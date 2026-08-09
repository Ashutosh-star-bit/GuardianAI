"""
GuardianAI Comprehensive Threat Intelligence Testing Dataset & Reusable Pytest Fixtures
Purpose: Provides reusable datasets for Safe URLs, Phishing URLs, Typosquatting Examples, Government Domains,
         Corporate Domains, Suspicious Emails, Legitimate Emails, UPI IDs, Phone Numbers, and Edge Cases.
"""

from typing import Dict, List, Any
import pytest

# 1. SAFE URLS
SAFE_URLS: List[str] = [
    "https://paypal.com/signin",
    "https://www.google.com/search?q=security",
    "https://amazon.com/dp/B08N5WRWNW",
    "https://github.com/login"
]

# 2. PHISHING URLS
PHISHING_URLS: List[str] = [
    "http://admin:secret@192.168.1.1:8080/login/secure",
    "http://paypa1-check.top/verify?token=xyz",
    "https://paypa1-check.com/redirect?next_url=http%3A%2F%2Fmalicious-site.com",
    "http://192.168.1.1/admin/login.php"
]

# 3. TYPOSQUATTING EXAMPLES
TYPOSQUATTING_DOMAINS: List[Dict[str, str]] = [
    {"domain": "paypa1-check.top", "expected_brand": "paypal"},
    {"domain": "xn--pypal-4ve.com", "expected_brand": "paypal"},
    {"domain": "amazn-security.xyz", "expected_brand": "amazon"},
    {"domain": "bankofamrica-login.info", "expected_brand": "bankofamerica"}
]

# 4. GOVERNMENT DOMAINS
GOVERNMENT_DOMAINS: List[str] = [
    "agent@irs.gov",
    "support@ftc.gov",
    "contact@nic.gov.in",
    "info@gov.uk"
]

# 5. CORPORATE DOMAINS
CORPORATE_DOMAINS: List[str] = [
    "security@paypal.com",
    "support@bankofamerica.com",
    "billing@amazon.com",
    "admin@microsoft.com"
]

# 6. SUSPICIOUS EMAILS
SUSPICIOUS_EMAILS: List[Dict[str, Any]] = [
    {"header": '"CEO John Smith" <john.smith@gmail.com>', "reason": "EXECUTIVE_SPOOFING"},
    {"header": "user123@mailinator.com", "reason": "DISPOSABLE_EMAIL"},
    {"header": '"PayPal Support" <verify@paypa1-check.top>', "reason": "BRAND_SPOOFING"}
]

# 7. LEGITIMATE EMAILS
LEGITIMATE_EMAILS: List[str] = [
    "service@paypal.com",
    "support@bankofamerica.com",
    "auto-confirm@amazon.com"
]

# 8. UPI IDS
UPI_TEST_DATA: List[Dict[str, Any]] = [
    {"upi_id": "support.refund@okaxis", "suspicious": True, "provider": "Google Pay"},
    {"upi_id": "merchant.pay@ybl", "suspicious": False, "provider": "PhonePe"},
    {"upi_id": "kyc.helpdesk@paytm", "suspicious": True, "provider": "Paytm"},
    {"upi_id": "user@scambank", "suspicious": True, "provider": None}
]

# 9. PHONE NUMBERS
PHONE_TEST_DATA: List[Dict[str, Any]] = [
    {"phone": "+1 (800) 555-0199", "premium": False, "valid": True},
    {"phone": "+1 (900) 555-9999", "premium": True, "valid": True},
    {"phone": "+91-9999999999-XXX", "repeated": True, "obfuscated": True}
]

# 10. EDGE CASES
EDGE_CASE_PAYLOADS: List[Dict[str, Any]] = [
    {"input": "   https://paypal.com/signin   ", "description": "WHITESPACE_PADDING"},
    {"input": "http://sub.verify.security.paypal.com.check.top", "description": "EXCESSIVE_SUBDOMAIN_DEPTH"},
    {"input": "x89z1a09qw4b21c9.com", "description": "DGA_SHANNON_ENTROPY"}
]

# PYTEST FIXTURES PROVIDER
@pytest.fixture
def dataset_safe_urls() -> List[str]:
    return SAFE_URLS

@pytest.fixture
def dataset_phishing_urls() -> List[str]:
    return PHISHING_URLS

@pytest.fixture
def dataset_typosquatting_domains() -> List[Dict[str, str]]:
    return TYPOSQUATTING_DOMAINS

@pytest.fixture
def dataset_suspicious_emails() -> List[Dict[str, Any]]:
    return SUSPICIOUS_EMAILS

@pytest.fixture
def dataset_upi_data() -> List[Dict[str, Any]]:
    return UPI_TEST_DATA

@pytest.fixture
def dataset_phone_data() -> List[Dict[str, Any]]:
    return PHONE_TEST_DATA
