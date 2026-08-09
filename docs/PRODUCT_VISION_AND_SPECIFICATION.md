# GuardianAI: Product Vision, Architecture & Strategic Specification

**Document Version:** 1.0.0  
**Authoring Roles:** Principal Software Architect, Principal AI Engineer, Principal Cybersecurity Engineer, Senior Product Manager, Senior UX Designer  
**Target Platform:** GuardianAI (Production-Quality AI Anti-Scam SaaS)  
**Date:** July 2026  

---

## Executive Summary

GuardianAI is a next-generation, privacy-first, explainable anti-scam platform designed to protect individuals and business personnel against modern online threats—including AI-synthesized phishing, smishing (SMS scams), quishing (QR code fraud), spear-phishing, and recruitment scams. Unlike traditional black-box security filters, GuardianAI pairs deep multimodal analysis with Explainable AI (XAI) to breakdown **why** content is dangerous, providing clear, actionable mitigation steps while strictly preserving user privacy and operating efficiently within serverless and free-tier infrastructure.

---

## 1. Vision

> **To create a scam-free digital ecosystem where every individual and enterprise can interact with incoming communications confidently, backed by transparent, privacy-first AI protection.**

GuardianAI envisions a world where scam detection is not an opaque binary score, but a trusted advisor. By democratizing access to enterprise-grade threat intelligence and demystifying AI decision-making, GuardianAI empowers users across all digital literacy levels to understand, avoid, and report cyber deception in real-time.

---

## 2. Mission

> **GuardianAI protects users against modern online scams by analyzing suspicious messages, emails, URLs, and QR codes using Explainable AI—delivering instant risk scoring, clear threat explanations, actionable recommendations, and zero-compromise privacy.**

### Core Pillars
1. **Multimodal Vigilance:** Unified protection covering Text/SMS, Email headers & bodies, Web URLs, and QR code visual payloads.
2. **Transparent Explainability:** Replacing cryptic security warnings with human-readable, evidence-backed breakdowns (highlighting suspicious linguistic triggers, domain spoofing, domain age mismatch, and urgency tactics).
3. **Privacy-by-Design:** Local and edge PII sanitization ensuring sensitive user data is stripped prior to AI analysis.
4. **Accessible Actionability:** Step-by-step guidance tailored to the user's technical literacy level (e.g., plain language for seniors vs. forensic details for IT administrators).
5. **Frugal & Modular Architecture:** Highly optimized serverless architecture deployable on free/low-cost platforms without sacrificing scalability or throughput.

---

## 3. Target Audience & User Personas

GuardianAI addresses a wide spectrum of users, ranging from digitally vulnerable individuals to enterprise employees.

| User Segment | Key Pain Points & Vulnerabilities | Core GuardianAI Needs | UX & Delivery Requirements |
| :--- | :--- | :--- | :--- |
| **Senior Citizens** | High target for impersonation, tech support scams, imposter family texts, complex jargon in existing tools. | Easy copy-paste or screenshot upload; plain-language explanations ("This is claiming to be your bank, but the link goes elsewhere"). | Large typography, high contrast, zero technical jargon, one-click "Is this safe?" input. |
| **Students & Job Seekers** | Fake remote job offers, fee phishing, scholarship scams, malicious QR codes on flyers. | Verification of recruiter domains, QR code destination inspection, payment request warnings. | Mobile-first UX, instant QR scanning, fast response times (< 1.5s), browser extensions. |
| **Parents** | Urgent fake billing alerts, school/child emergency smishing, compromised subscription emails. | SMS & email rapid verification, clear guidance on verification steps before clicking or paying. | Simple dashboard, quick risk badge (Safe / Caution / Dangerous), shareable safety link. |
| **Employees** | Business Email Compromise (BEC), spear-phishing targeting credentials, invoice fraud. | Header analysis, spoofed domain checking, malicious URL deep inspection, SOC-compatible logs. | Gmail/Outlook add-in integration, subtle background check, detailed risk report export. |
| **Recruiters & HR** | Malicious candidate resumes, dangerous drive links, fake candidate profiles. | Document payload parsing, URL sandbox checking, safe preview of external links. | Drag-and-drop file/link analysis, bulk inspection API, low false-positive rate. |
| **Small Businesses (SMBs)** | Limited/no dedicated IT security team; vulnerable to invoice fraud, domain squatting. | Centralized threat dashboard, light administrative controls, automated threat reporting. | Multi-tenant organization workspace, simple team management, compliance reports. |

---

## 4. Business Goals & SaaS Strategy

### 4.1 Short-Term Business Objectives (Months 1–6)
* **User Acquisition:** Reach 50,000 monthly active users (MAU) across Web & Browser extension.
* **Conversion & Monetization:** Achieve a 3.5% conversion rate from Free Tier to Pro ($4.99/mo) and Team Tier ($14.99/user/mo).
* **Cost Efficiency:** Maintain operational infrastructure costs under $50/month by maximizing free-tier serverless services (Vercel, Cloudflare, Supabase, Hugging Face Inference).

### 4.2 Long-Term Business Objectives (Months 7–24)
* **B2B Expansion:** Launch enterprise API monetization for email gateways and HR software platforms.
* **Data Flywheel (Privacy-Preserved):** Build an anonymized threat dataset to train proprietary, lightweight open-source scam detection models.
* **Strategic Partnerships:** Integrate with educational institutions, anti-fraud non-profits, and digital literacy campaigns.

### 4.3 SaaS Tiering & Packaging Strategy

```
+------------------------+------------------------+------------------------+
|      FREE FOREVER      |        PRO TIER        |     BUSINESS / TEAMS   |
|     ($0/mo - Hook)     |   ($4.99/mo - B2C)     | ($14.99/user/mo - B2B) |
+------------------------+------------------------+------------------------+
| - 50 scans / month     | - Unlimited scans      | - All Pro Features     |
| - Text, URL, QR Code   | - Email header analysis| - Team Admin Dashboard |
| - Basic XAI Rationale  | - Deep URL Sandboxing  | - Organization Threat  |
| - Standard Speed       | - Real-time Browser    |   Feed & Export        |
| - Privacy Guarantee    |   Extension Shield     | - Custom Domain        |
|                        | - Priority AI Engine   |   Whitelisting & API   |
+------------------------+------------------------+------------------------+
```

---

## 5. Functional Goals

### 5.1 Input & Payload Processing
* **SMS & Text Analysis:** Detect urgency markers, financial requests, suspicious shortcodes, and brand impersonation.
* **Email Body & Header Forensic Inspection:** Parse SPF, DKIM, DMARC alignment, sender domain age, reply-to discrepancies, and hidden malicious HTML links.
* **URL & Domain Deep Analysis:** Detect typosquatting (e.g., `paypa1.com`), WHOIS registration age (<30 days flag), redirect chains, SSL/TLS certificate validity, and reputation blacklists.
* **QR Code (Quishing) Decoding:** Optical character recognition (OCR) and visual decoding of QR codes from uploaded images, extracting hidden payloads, and executing URL checks safely.

### 5.2 Explainable AI (XAI) Engine
* **Visual Highlight Extraction:** Highlight exact spans of text triggering risk flags (e.g., urgent payment demands, suspicious links).
* **Multi-Factor Risk Scoring:** Calculate a unified Threat Index (0–100) split into three intuitive bands:
  * `0 - 29: SAFE (Green)`
  * `30 - 69: SUSPICIOUS / CAUTION (Yellow)`
  * `70 - 100: DANGEROUS / SCAM (Red)`
* **Layered Explanation Hierarchy:**
  * **Summary View:** 1-sentence plain-language explanation (e.g., *"This message claims to be FedEx, but the link goes to an untrusted site registered yesterday."*).
  * **Detailed Forensic View:** Granular analysis of domain parameters, linguistic manipulation tactics, and technical header mismatches.

### 5.3 Actionable Remediation Guidance
* **Contextual Next Steps:** Provide precise actions based on classification:
  * *"Do NOT click the link."*
  * *"Contact your bank using the official phone number on the back of your card, NOT the number in this message."*
  * *"One-click copy report to FTC / Anti-Phishing Working Group (APWG)."*

### 5.4 Privacy & Security Guardrails
* **Client-Side/Edge PII Redaction:** Automatically scrub Names, Phone Numbers, Credit Card Numbers, SSNs, and Personal Addresses before sending payloads to AI models.
* **Zero-Knowledge Retention Option:** User-configurable toggle to process requests strictly in-memory without saving inputs to logs or databases.

---

## 6. Technical Goals

### 6.1 Architectural Principles
* **Decoupled Modular Services:** Clear separation between Web Frontend, PII Sanitizer, Threat Scanners, XAI Orchestrator, and AI Inference Engine.
* **Vendor-Agnostic AI Pipelines:** Abstraction layer allowing seamless switching between OpenAI, Anthropic, Hugging Face, or self-hosted Ollama models without breaking downstream code.
* **Edge-Native Deployment:** Host API gateways and sanitizers on Cloudflare Workers / Vercel Edge for microsecond latency.

### 6.2 High-Level System Architecture Diagram

```
                 +-------------------------------------------------+
                 |            Client Applications                  |
                 | (React Web App / Extension / Mobile Browser PWA)|
                 +------------------------+------------------------+
                                          |
                                  HTTPS / WSS Request
                                          |
                                          v
                 +-------------------------------------------------+
                 |        Edge Gateway & Local PII Scrubbing       |
                 |     (Vercel / Cloudflare Edge Middleware)       |
                 +------------------------+------------------------+
                                          |
                               Sanitized Request Payload
                                          |
                                          v
                 +-------------------------------------------------+
                 |           API Routing & Auth Engine             |
                 |          (FastAPI / Node.js Serverless)         |
                 +----+-------------------+-------------------+----+
                      |                   |                   |
                      v                   v                   v
      +-------------------+ +-------------------+ +-------------------+
      | Text/Email Scanner| |  URL/Domain Engine| | QR/Visual Scanner |
      |  (Regex + NLP)    | |(WHOIS/DNS/Threat| |(OCR/OpenCV/ZBar)  |
      |                   | |     Feeds)        | |                   |
      +---------+---------+ +---------+---------+ +---------+---------+
                |                     |                     |
                +---------------------+---------------------+
                                      |
                                  Features
                                      |
                                      v
                 +-------------------------------------------------+
                 |          XAI & Multi-Model Inference Engine     |
                 |  - Ensemble Classifier (LightGBM/BERT)          |
                 |  - Rationale Generator (LLM with Guardrails)      |
                 |  - Feature Attribution (SHAP/Linguistic Rules)  |
                 +------------------------+------------------------+
                                          |
                                    Result Package
                                          |
                                          v
                 +-------------------------------------------------+
                 |          Database & Analytics Layer             |
                 |         (Supabase PostgreSQL + Redis)           |
                 +-------------------------------------------------+
```

### 6.3 Technical Goals & Free-Tier Infrastructure Blueprint

| Component | Target Technology Stack | Free-Tier Deployment Target | Resource Limits & Strategy |
| :--- | :--- | :--- | :--- |
| **Frontend UI** | Next.js / React, Vanilla CSS modules, Lucide icons | Vercel / Cloudflare Pages | Unlimited static bandwidth, zero idle cost. |
| **API Gateway** | FastAPI (Python) or Hono.js (TypeScript) | Vercel Serverless / Cloudflare Workers | Free tier: 100k requests/day. |
| **Database** | PostgreSQL + PgVector | Supabase / Neon Free Tier | 500MB storage, automated connection pooling. |
| **Cache & Rate Limit** | Redis / Upstash | Upstash Serverless Redis | 10,000 requests/day free. |
| **AI Threat Model** | Quantized DistilBERT + Llama-3-8B-Instruct | Hugging Face Inference API / Groq Free Tier | High-throughput low-latency inference. |
| **Domain & Threat Intelligence** | Google Safe Browsing API, VirusTotal API, Cloudflare RDAP | Free Community API Tiers | Multi-vendor fallback pipeline to avoid hitting single API rate limits. |

---

## 7. Success Metrics

GuardianAI measures success across accuracy, explainability quality, performance, user trust, and business sustainability.

### 7.1 Accuracy & AI Security Metrics
* **Scam Classification F1-Score:** $\ge 0.96$ on benchmark scam datasets (Enron Phishing, SMS Spam Collection, Quishing test suites).
* **False Positive Rate (FPR):** $< 0.8\%$ (Critical to avoid user alert fatigue on legitimate communications).
* **Adversarial Resilience:** $> 90\%$ detection rate against prompt-injected or obfuscated text (homoglyph attacks, zero-width spaces).

### 7.2 Explainable AI (XAI) & UX Metrics
* **XAI Comprehension Index:** $> 88\%$ user comprehension score in user testing surveys (ability of non-technical users to explain *why* a message was flagged).
* **Action Completion Rate:** $> 85\%$ of warned users take the recommended safety action (e.g., reporting or deleting without clicking).
* **Time-to-Insight:** Total execution latency from submission to XAI report rendering $< 1.8$ seconds.

### 7.3 Operational & Business Metrics
* **Monthly Active Users (MAU):** 50k within 6 months.
* **Monthly Recurring Revenue (MRR):** Reach $5,000 within 6 months of Pro tier launch.
* **Cost Per Scan (CPS):** Keep average marginal API/infrastructure cost per scan under **$0.0008**.

---

## 8. Future Roadmap

```
+-----------------------------------------------------------------------------------+
| PHASE 1: MVP Core (Months 1 - 2)                                                  |
| - Text, SMS, URL & QR Code Analysis Web Portal.                                   |
| - Basic XAI Rationale (Linguistic triggers, domain age, threat score).            |
| - Local PII Redaction Engine.                                                     |
| - Free-tier deployment on Vercel + Supabase + Groq.                               |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| PHASE 2: Protection Expansion & UX Polish (Months 3 - 4)                          |
| - Email Header (.eml file upload & raw parser) with DMARC/DKIM/SPF verifier.      |
| - Chrome & Firefox Browser Extension (Auto-inspect highlights on web pages).       |
| - Pro Tier Billing Integration (Stripe).                                          |
| - Accessible UX modes (Senior High-Contrast Mode & Audio Summary).                |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| PHASE 3: Business & API Ecosystem (Months 5 - 8)                                  |
| - GuardianAI REST API & Webhooks for B2B/Developer integration.                    |
| - Team Workspace & Centralized Threat Log Dashboard.                              |
| - One-Click Fraud Reporting (Automated filing to FTC, IC3, and APWG).             |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| PHASE 4: Autonomous Threat Graph & ML Flywheel (Months 9 - 12)                    |
| - Active learning pipeline with privacy-sanitized user submission feedback.      |
| - Localized browser-side lightweight ML classification (ONNX WebAssembly).        |
| - Enterprise SIEM / Slack / Teams alert integrations.                              |
+-----------------------------------------------------------------------------------+
```

---

## 9. Product Principles

1. **Explainability Over Utility:** A security score without an explanation is useless. Always explain the decision in terms accessible to the user's technical level.
2. **Privacy as a Non-Negotiable Core:** User content belongs to the user. No raw PII or un-sanitized message content is logged, sold, or used for public AI training.
3. **Non-Alarmist UX Design:** Inform and guide without inciting panic. Use clear, objective, color-coded threat signals combined with calm, actionable next steps.
4. **Frugal & Resilient Engineering:** Design for high availability on serverless infrastructure. Systems must fail safely (e.g., if AI service is down, fall back to rule-based domain checks rather than failing silently).
5. **Defense-in-Depth:** Never rely solely on LLMs. Combine heuristic rules, domain reputation feeds, computer vision (for QR/logos), and ML classifiers for robust detection.

---

## 10. Risks & Mitigations

| Risk Domain | Identified Risk | Impact | Probability | Mitigation Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Cybersecurity / AI** | **Prompt Injection / Jailbreaking:** Attackers embed hidden instructions inside suspicious text to force the XAI to label it "Safe". | High | Medium | Dual-pass architecture: Pre-classify using non-LLM feature extractors (DistilBERT/XGBoost) before LLM rationale generation. Wrap LLM context in strict system prompt sandboxes. |
| **Privacy & Compliance** | **PII Leakage:** Accidental logging of user emails, credit cards, or names in telemetry data. | High | Low | Client-side Regex + SpaCy NER PII anonymization prior to API transmission. Enforce strict database column encryption and zero-log defaults. |
| **User Experience** | **False Positive Alert Fatigue:** Legitimate emails marked as scams cause users to ignore future alerts. | High | Medium | Calibrate risk threshold carefully ($\text{FPR} < 0.8\%$). Introduce "Caution" middle-tier instead of binary Scam/Not Scam. Provide one-click "False Positive" reporting. |
| **Infrastructure / Cost** | **Free Tier Rate Limit Exhaustion:** Viral traffic spikes cause serverless provider caps to shut down the app. | Medium | High | Implement Upstash Redis IP/User rate limiting, Cloudflare caching, and multi-provider fallback (e.g., failover from Groq to Hugging Face to local ONNX model). |
| **Legal / Regulatory** | **Misclassification Liability:** User sues after falling for a scam marked as "Safe" by GuardianAI. | High | Low | Clear Terms of Service disclaimers; position tool as an "AI Advisory Assistant", not a legal guarantee. Continuous model benchmarking. |

---

## 11. Document Review & Self-Improvement

### 11.1 Self-Review Assessment

As part of our commitment to engineering excellence, the cross-functional leadership team reviewed the initial specification draft and identified three critical areas requiring refinement:

1. **XAI Ambiguity:** Initial drafts described "Explainable AI" conceptually without specifying the mechanical implementation. Non-technical users need simple rationale, while technical users need verifiable evidence.
2. **Privacy vs. ML Improvement Contradiction:** Goal 3 (Protect Privacy) and Goal 5 (Support Future ML Improvements) create a natural architectural tension. Storing data for model re-training risks violating privacy guarantees.
3. **Free-Tier Robustness vs. High Latency:** Relying heavily on free LLM APIs risks severe latency spikes during queue congestion, violating our $<1.8\text{s}$ responsiveness goal.

### 11.2 Concrete Enhancements Implemented in Specification

* **Enhancement 1: Multi-Tiered XAI Engine Specification**  
  * *Refinement:* Defined an explicit dual-layer XAI output structure. Layer 1 generates human linguistic summaries using template-bound LLM prompts. Layer 2 generates structural feature attributions (highlighted text spans, DNS registration delta, SPF/DKIM verification matrix).
* **Enhancement 2: Zero-Knowledge Privacy-Preserving Feedback Flywheel**  
  * *Refinement:* Resolved the ML improvement vs. privacy conflict by implementing **Differential Privacy & On-Device Feature Vector Extraction**. User feedback converts submissions into abstract, non-reversible mathematical feature vectors (e.g., token length, entropy score, domain age delta) without retaining raw text or PII.
* **Enhancement 3: Hybrid Local/Cloud Inference Cascade**  
  * *Refinement:* Implemented a tiered fallback cascade to enforce latency limits. Stage 1 executes local JavaScript/WebAssembly checks for domain typosquatting and PII scrubbing (0ms latency). Stage 2 hits a lightweight serverless classifier model (<200ms). Stage 3 triggers LLM rationale generation asynchronously while returning preliminary threat indicators immediately.

---
*End of Specification Document.*
