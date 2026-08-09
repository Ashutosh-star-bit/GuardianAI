# GuardianAI: Master Engineering Sprint Roadmap

**Document Title:** Milestone-Based Engineering Sprint Roadmap for GuardianAI  
**Document Version:** 1.0.0  
**Status:** Approved for Sprint Planning & Execution  
**Authors:** Leadership Team (Principal Software Architect, Principal AI Engineer, Principal Cybersecurity Engineer, Senior Product Manager, Senior UX Designer)  
**Total Timeline:** 8 Weeks (4 Two-Week Sprints)  
**Target Release:** Production MVP Release (Q3 2026)  

---

## Executive Summary & Sprint Master Timeline

This document outlines the milestone-based engineering roadmap for GuardianAI. Development is structured across **4 two-week sprints** (8 weeks total), prioritizing core P0 security, privacy, and Explainable AI (XAI) features to deliver a production-quality, serverless SaaS platform.

```
+----------------------------------------------------------------------------------------------------+
|                                    GUARDIAN-AI SPRINT TIMELINE                                     |
+----------------------------------------------------------------------------------------------------+
| SPRINT   | TIMELINE    | CORE FOCUS & MILESTONE DELIVERABLE                                        |
+----------+-------------+---------------------------------------------------------------------------+
| Sprint 1 | Weeks 1 - 2 | Foundation, Edge PII Scrubbing & Multimodal Payload Ingestion Scanners.   |
| Sprint 2 | Weeks 3 - 4 | AI Reasoning Engine, XAI Visual Highlights & Senior Citizen Accessibility. |
| Sprint 3 | Weeks 5 - 6 | Email Header Engine, Supabase Auth, PgVector & Scan History Persistence.  |
| Sprint 4 | Weeks 7 - 8 | Chrome Extension, Automated FTC Reporting, B2B API & Production Launch.   |
+----------+-------------+---------------------------------------------------------------------------+
```

---

## 1. Sprint 1: Foundation, Edge PII & Multimodal Ingestion (Weeks 1–2)

### 1.1 Tasks
* **Task 1.1:** Initialize monorepo directory topology (`apps/web`, `backend`, `ai`, `database`, `docs`).
* **Task 1.2:** Build Next.js 14 App Router frontend shell with responsive Tailwind CSS modules.
* **Task 1.3:** Develop client-side Web Worker PII sanitizer (Regex + SpaCy-lite NER for Names, Credit Cards, SSNs, Phone Numbers).
* **Task 1.4:** Construct FastAPI backend gateway with initial endpoints (`POST /scan/text`, `POST /scan/url`, `POST /scan/qr`).
* **Task 1.5:** Implement URL WHOIS age lookup, homoglyph typosquatting detector, and OpenCV/ZBar QR code decoder.

### 1.2 Dependencies
* Node.js 20+, Python 3.11, Docker Engine installed.
* Access to WHOIS/DNS lookup libraries (`python-whois`, `dnspython`).

### 1.3 Verification
* Client-side Web Worker verifies 100% PII removal before sending JSON payloads over the network.
* API Gateway processes valid text, URL, and QR payloads and returns raw feature vectors within **300ms**.

### 1.4 Testing
* **Unit Tests:** Regex PII scrubbing test suite (`test_pii_sanitizer.py`).
* **API Integration Tests:** Pytest handlers verifying 200 OK responses for `/scan/text`, `/scan/url`, and `/scan/qr`.

### 1.5 Deliverables
* Complete monorepo repository structure.
* Working Web Scanner Console UI.
* Functional client PII scrubbing Web Worker.
* Stateless FastAPI backend with Text, URL, and QR feature extraction scanners.

### 1.6 Completion Criteria
* All Sprint 1 unit and integration tests pass with $>90\%$ code coverage.
* Client-side PII scrubbing latency remains below **50ms**.

### 1.7 Risk Mitigation
* *Risk:* QR Code OCR processing causes browser UI freezes.  
  * *Mitigation:* Offload QR image decoding to a dedicated Web Worker thread in the browser.

---

## 2. Sprint 2: AI Reasoning, XAI Highlights & Accessibility (Weeks 3–4)

### 2.1 Tasks
* **Task 2.1:** Train and integrate lightweight statistical ensemble classifier (DistilBERT + XGBoost) for intent scoring.
* **Task 2.2:** Build Dual-Pass AI System Prompt sandbox (`PROMPT-01`) targeting Groq Llama-3-8B API for rationale synthesis.
* **Task 2.3:** Implement Anti-Prompt Injection guardrails and Pydantic JSON schema response validator.
* **Task 2.4:** Develop Visual Text Span Highlight Attribution engine mapping character offsets to UI marker components.
* **Task 2.5:** Implement **Senior Citizen High-Contrast Mode** UI preset and Web Speech audio narration player.

### 2.2 Dependencies
* Sprint 1 Text/URL/QR feature scanners.
* Groq API Key provisioned for fast Llama-3 inference.

### 2.3 Verification
* AI Engine extracts signals for all 14 threat categories (Urgency, Typosquatting, OTP, UPI, etc.).
* End-to-end execution time from text submission to XAI highlight rendering completes under **1.8 seconds**.

### 2.4 Testing
* **Security Tests:** Adversarial prompt injection test suite (50+ jailbreak payloads tested with 0% system overrides).
* **Accessibility Tests:** Automated Lighthouse & axe-core audits ensuring **100% WCAG 2.1 AA** compliance.

### 2.5 Deliverables
* Integrated 3-Tier AI Inference Pipeline (Classifier $\rightarrow$ Groq LLM $\rightarrow$ Rule Fallback).
* XAI Visual Highlight text rendering component.
* Senior Citizen Accessibility Theme Provider & Audio Narration Player.

### 2.6 Completion Criteria
* Classification F1-Score reaches $\ge 0.96$ on benchmark phishing test sets.
* Senior Mode UI passes WCAG 2.1 AA contrast ($\ge 7:1$) and screen reader ARIA checks.

### 2.7 Risk Mitigation
* *Risk:* Third-party Groq API rate limits cause 429 errors during load testing.  
  * *Mitigation:* Implement Tier 3 local rule-based fallback scorer returning instantaneous template rationales.

---

## 3. Sprint 3: Email Engine, Auth & Database Persistence (Weeks 5–6)

### 3.1 Tasks
* **Task 3.1:** Develop raw `.eml` email header parser evaluating SPF, DKIM, DMARC, and reply-to domain mismatches.
* **Task 3.2:** Deploy Supabase PostgreSQL database schemas (16 production tables including `scans`, `messages`, `urls`, `audit_logs`).
* **Task 3.3:** Configure PgVector IVFFlat vector indexing for similarity lookups against emerging scam signatures.
* **Task 3.4:** Integrate Supabase Auth (RS256 JWTs) supporting OAuth 2.0, Magic Links (Senior friendly), and PostgreSQL Row Level Security (RLS).
* **Task 3.5:** Build Scan History dashboard (`/history`) and Personal Threat Analytics views (`/analytics`).

### 3.2 Dependencies
* Sprint 2 AI Reasoning Engine.
* Supabase project instance provisioned.

### 3.3 Verification
* SPF/DKIM/DMARC authentication failures flag Business Email Compromise (BEC) attempts with 100% accuracy.
* Database RLS policies verify complete tenant isolation (`auth.uid() = user_id`).

### 3.4 Testing
* **Database Tests:** Migration roll-back tests and RLS authorization boundary penetration tests.
* **Integration Tests:** End-to-end email upload and authentication flows (`POST /scan/email`).

### 3.5 Deliverables
* Operational Email Header Inspector (`POST /scan/email`).
* Deployed Supabase PostgreSQL database with PgVector & RLS policies enabled.
* Working User Authentication & Paginated Scan History Dashboard.

### 3.6 Completion Criteria
* All 16 database tables deployed and verified with RLS security policies.
* Scan history queries return in $<100\text{ms}$.

### 3.7 Risk Mitigation
* *Risk:* Large `.eml` file attachments cause server memory bloat.  
  * *Mitigation:* Stream file uploads directly to S3 storage via presigned URLs, inspecting headers in isolated memory slices.

---

## 4. Sprint 4: Extension, Fraud Reporting, API & Launch (Weeks 7–8)

### 4.1 Tasks
* **Task 4.1:** Build Chrome & Firefox Browser Extension (Manifest V3) with auto-highlight page inspection.
* **Task 4.2:** Develop automated FTC / APWG fraud report dispatch pipeline (`POST /reports/dispatch`).
* **Task 4.3:** Build Developer API Key Console (`/settings`) and enforce Upstash Redis token bucket rate limiting.
* **Task 4.4:** Setup GitHub Actions CI/CD automated pipeline for zero-downtime deployment to Vercel and Cloudflare Pages.
* **Task 4.5:** Perform full production security penetration audit, load testing, and final launch readiness review.

### 4.2 Dependencies
* Sprint 3 Auth and Database infrastructure.
* Upstash Redis instance provisioned.

### 4.3 Verification
* Chrome Extension successfully detects and highlights suspicious links on live web pages in real time.
* API Gateway enforces rate limits (429 response) when requests exceed free/pro quotas.

### 4.4 Testing
* **E2E Tests:** Playwright cross-browser UI test suite covering user sign-up, scan execution, and settings customization.
* **Load Tests:** Locust load test simulating 1,000 concurrent users with zero p99 latency degradation.

### 4.5 Deliverables
* Published Manifest V3 Browser Extension package.
* Automated FTC / APWG Fraud Reporting Service.
* Production CI/CD Pipeline & Live Deployed SaaS Platform on `https://guardianai.com`.

### 4.6 Completion Criteria
* All 4 Sprints complete with zero open P0/P1 bugs.
* Production platform running live on Vercel + Supabase + Groq with $99.9\%$ uptime.

### 4.7 Risk Mitigation
* *Risk:* Chrome Web Store review delays for Manifest V3 extension.  
  * *Mitigation:* Submit extension for early store review during Week 7 while finalizing web portal Polish.

---

## 5. Timeline Realism & Resource Allocation Audit

The cross-functional leadership team evaluated the sprint timeline against feasibility standards:

1. **Velocity Realism:** 2-week sprint cadence balances rapid iterations with strict QA testing.
2. **Dependency Sequencing:** Scanners (Sprint 1) precede AI Engine (Sprint 2), which precedes Persistence (Sprint 3), which precedes Ecosystem Integrations (Sprint 4).
3. **Buffer Management:** Week 8 includes a dedicated 3-day buffer for final security penetration auditing and performance tuning before public launch.

---
*End of Master Engineering Sprint Roadmap Document.*
