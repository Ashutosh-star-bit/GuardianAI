# GuardianAI Threat Intelligence Engine Architecture Specification

**Document Version:** 1.0.0  
**Architect:** Principal Cybersecurity Architect  
**Target Module:** Threat Intelligence Engine (`app/threat_intel/`)  
**Date:** July 2026  
**Status:** **APPROVED ARCHITECTURAL DESIGN**  

---

## 1. Architectural Overview & System Design

The **GuardianAI Threat Intelligence Engine** is a high-throughput, modular threat analysis system designed to evaluate indicators of compromise (IOCs) across **URLs, Domains, Email Addresses, Phone Numbers, UPI IDs**, and future extensions (**QR Code Payloads and IP Addresses**).

### Core Architectural Principles:
1. **Zero-Latency Offline First:** Core threat evaluation relies on pre-compiled regex, Levenshtein edit distance, and local threat dictionaries to guarantee **Sub-50ms SLA Latency**.
2. **Pluggable Intelligence Adapters:** External API integrations (Google Safe Browsing, VirusTotal, OpenPhish, PhishTank) are encapsulated behind an abstract adapter layer, executing asynchronously in non-blocking background workers.
3. **Multi-Factor Threat Scoring:** Combines technical IOC risk scores with psychological manipulation metrics into a unified 0 - 100 Threat Index.

---

## 2. Modular Subsystem Architecture

```
                               Incoming Threat Payload
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 ▼                                               ▼
      ┌─────────────────────┐                         ┌─────────────────────┐
      │  URL Intelligence   │                         │ Domain Intelligence │
      │  (url_intel.py)     │                         │ (domain_intel.py)   │
      └──────────┬──────────┘                         └──────────┬──────────┘
                 │                                               │
      ┌──────────┴──────────┐                         ┌──────────┴──────────┐
      │ Email Intelligence  │                         │ Phone Intelligence  │
      │ (email_intel.py)    │                         │ (phone_intel.py)    │
      └──────────┬──────────┘                         └──────────┬──────────┘
                 │                                               │
      ┌──────────┴──────────┐                         ┌──────────┴──────────┐
      │  UPI Intelligence   │                         │ Future: QR & IP     │
      │  (upi_intel.py)     │                         │ (qr_ip_intel.py)    │
      └──────────┬──────────┘                         └──────────┬──────────┘
                 └───────────────────────┬───────────────────────┘
                                         │
                                         ▼
                             ┌──────────────────────┐
                             │ Threat Scoring Engine│
                             │ (scoring.py)         │
                             └──────────┬───────────┘
                                         │
                     ┌───────────────────┴───────────────────┐
                     ▼                                       ▼
         ┌───────────────────────┐               ┌───────────────────────┐
         │  Evidence Collection  │               │ Explainability Engine │
         │  (evidence.py)        │               │ (explainability.py)   │
         └───────────────────────┘               └───────────────────────┘
                     │                                       │
                     └───────────────────┬───────────────────┘
                                         │
                                         ▼
                            ThreatIntelligenceResult DTO
```

---

## 3. Threat Intelligence Component Specifications

### 3.1 URL Intelligence Module (`url_intel.py`)
- **Typosquatting & Homoglyphs:** Identifies character substitutions (`paypa1-check.com` → `paypal`).
- **Shortener Expansion:** Identifies shortened link hostnames (`bit.ly`, `t.co`, `tinyurl.com`, `t.me`).
- **URL Structure Entropy:** Analyzes path length, query param entropy, embedded IP addresses, and custom port declarations (`:8080`).

### 3.2 Domain Intelligence Module (`domain_intel.py`)
- **TLD Risk Rating:** Classifies high-risk TLDs (`.top`, `.xyz`, `.info`, `.online`, `.click`).
- **Punycode IDN Detection:** Identifies Internationalized Domain Names using `xn--` prefixes.
- **Brand Distance Matching:** Computes Levenshtein edit distance against global target brands (PayPal, Bank of America, Amazon, FedEx).

### 3.3 Email Intelligence Module (`email_intel.py`)
- **Authentication Check:** Evaluates SPF, DKIM, and DMARC verification headers (`FAIL` / `REJECT`).
- **Executive Impersonation:** Detects CEO / CFO display name spoofing paired with wire transfer prompts.
- **Disposable Provider Detection:** Flags temporary email services (`guerrillamail.com`, `10minutemail.com`).

### 3.4 Phone Intelligence Module (`phone_intel.py`)
- **Country Code Verification:** Validates international E.164 phone formatting.
- **VoIP / Virtual Number Indicator:** Flags virtual phone numbers commonly used in SMS smishing attacks.

### 3.5 UPI Intelligence Module (`upi_intel.py`)
- **VPA Handle Verification:** Inspects Virtual Payment Address handles (`merchant@okaxis`, `payee@ybl`).
- **Merchant vs. Personal Risk:** Flags personal UPI handles masquerading as corporate customer support desks.

---

## 4. Threat Scoring & Evidence Collection Engine

### 4.1 Weighted Threat Scoring Algorithm (`scoring.py`)
Threat Scores (0 - 100) are assigned to one of three qualitative risk bands:
- **`safe` (0 - 29):** Low risk payload with verified domain/brand identity.
- **`caution` (30 - 69):** Medium risk containing suspicious urgency or unverified links.
- **`dangerous` (70 - 100):** High risk containing confirmed typosquatting, spoofed SPF/DKIM, or fraudulent payment requests.

$$\text{Threat Score} = \min\left(100, \sum (\text{Indicator Weight} \times \text{Severity Multiplier})\right)$$

### 4.2 Evidence Collection & Explainability (`evidence.py`, `explainability.py`)
Gathers structured evidence items detailing technical threat indicators, formatting them into non-technical plain-language summaries and actionable safety guidance for end users.

---

## 5. Future Threat Intelligence API Adapters Layer (`adapters/`)

The architecture incorporates an abstract adapter interface (`BaseThreatAdapter`) allowing non-blocking background enrichment via third-party security APIs:

```
app/threat_intel/adapters/
├── base_adapter.py        # Abstract Base Class for Threat APIs
├── google_safebrowsing.py # Google Safe Browsing API v4 Adapter
├── virustotal.py          # VirusTotal v3 API Adapter
├── openphish.py           # OpenPhish Live Feed Adapter
└── phishtank.py           # PhishTank Live Feed Adapter
```

---

## 6. Scalability & SLA Guarantees

1. **Async Non-Blocking Execution:** Third-party API calls run in background tasks (`BackgroundTasks`), ensuring core API responses complete in **< 50ms**.
2. **Pre-Compiled Regex Catalog:** Zero heap allocations per request for pattern matchers.
3. **In-Memory Caching:** Caches domain threat evaluations in Redis / in-memory LRU cache to prevent duplicate WHOIS/DNS lookups.
