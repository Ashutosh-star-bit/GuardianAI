# GuardianAI: Master Folder & Repository Architecture

**Document Title:** Enterprise Directory Topology & Workspace Structure for GuardianAI  
**Document Version:** 1.0.0  
**Status:** Approved for Monorepo & Project Organization  
**Authors:** Leadership Team (Principal Software Architect, Principal AI Engineer, Principal Cybersecurity Engineer, Senior Product Manager, Senior UX Designer)  
**Target Platform:** GuardianAI SaaS Platform (Web, Extension, Backend, AI Engine)  

---

## 1. Master Repository Directory Tree

```
GuardianAI/
├── .github/                       # CI/CD Workflows & GitHub Configuration
│   ├── workflows/                 # Automated Build, Test, Security & Deploy Pipelines
│   ├── ISSUE_TEMPLATE/            # Standardized GitHub Issue Templates
│   └── PULL_REQUEST_TEMPLATE.md   # Pull Request Guidelines & Review Checklist
├── .vscode/                       # Workspace IDE Settings & Debug Launch Profiles
├── apps/                          # Monorepo Application Packages
│   ├── web/                       # Frontend Next.js 14 Web & PWA Application
│   │   ├── public/                # Static Public Assets (Favicons, Manifest, Logos)
│   │   ├── src/                   # Next.js App Router Source Code
│   │   │   ├── app/               # Next.js 14 App Router Pages, Layouts, & API Routes
│   │   │   ├── components/        # React UI Component Library
│   │   │   │   ├── ui/            # Atomic Base UI Controls (Buttons, Inputs, Badges)
│   │   │   │   ├── scanner/       # Scanning Interfaces (Text, URL, QR, Email)
│   │   │   │   ├── xai/           # Explainable AI Visualization & Highlight Components
│   │   │   │   ├── dashboard/     # Threat Analytics & Workspace Dashboards
│   │   │   │   └── accessibility/ # Senior Mode & High-Contrast Preset Controllers
│   │   │   ├── hooks/             # Custom React Hooks (State, Camera, Audio, Workers)
│   │   │   ├── lib/               # Utility Functions, API Clients, & Formatters
│   │   │   ├── providers/         # React Context Providers (Theme, Auth, Accessibility)
│   │   │   ├── stores/            # Zustand Client State Stores
│   │   │   ├── styles/            # Vanilla CSS Tokens, Global CSS, & Module Styles
│   │   │   └── workers/           # Client-Side Web Workers (Local PII Scrubbing)
│   │   └── package.json           # Frontend Dependencies & Scripts
│   └── extension/                 # Browser Extension Source (Manifest V3)
│       ├── src/                   # Background Scripts, Content Scripts, & Popup UI
│       └── manifest.json          # Extension Manifest V3 Metadata
├── backend/                       # Core FastAPI / Python Backend Services
│   ├── app/                       # Application Core Package
│   │   ├── api/                   # API Route Handlers & Endpoint Controllers
│   │   │   ├── v1/                # API Version 1 Endpoints (Scan, Auth, User, Org)
│   │   │   └── middlewares/       # Rate Limiting, CORS, PII Guardrails, & Auth Middlewares
│   │   ├── core/                  # Core Application Settings, Security & Constants
│   │   ├── db/                    # Database ORM, Migrations, & Connection Pooling
│   │   ├── models/                # Pydantic Schemas & SQLAlchemy/Supabase Data Models
│   │   ├── services/              # Business Logic & External Service Integrations
│   │   │   ├── scanners/          # Feature Extractor Modules (DNS, WHOIS, SPF/DKIM)
│   │   │   ├── queue/             # Async Task Queue Handlers (QStash / Redis)
│   │   │   └── reporting/         # Automated FTC / APWG Fraud Dispatch Service
│   │   └── utils/                 # Helper Functions, Regex Parsers, & Encoders
│   ├── main.py                    # Serverless FastAPI Entrypoint
│   └── requirements.txt           # Python Production Dependencies
├── ai/                            # AI Model Pipelines, Prompt Templates, & XAI Engine
│   ├── classifiers/               # Lightweight Statistical ML Models (DistilBERT/XGBoost)
│   ├── prompts/                   # Structured System Prompt Templates & Few-Shot Examples
│   │   ├── rationale/             # Plain-Language Explanation Prompt Templates
│   │   ├── guardrails/            # Anti-Prompt Injection Defense System Prompts
│   │   └── forensic/              # Detailed Technical Evidence Prompt Templates
│   ├── xai/                       # Feature Attribution, SHAP, & Highlight Span Mappers
│   └── evaluation/                # Model Benchmarking & Accuracy Evaluation Scripts
├── config/                        # Shared Infrastructure & Application Configuration
│   ├── redis/                     # Redis Caching & Rate Limit Configuration
│   ├── supabase/                  # Supabase Policies, Vector DB Settings, & RLS Rules
│   └── logger/                    # Logging Formatters, Filters, & Transport Configs
├── database/                      # Relational Schemas, Migrations, & Seeds
│   ├── migrations/                # Alembic / Supabase Sequential Migration Files
│   ├── seeds/                     # Database Seed Data & Benchmark Threat Hashes
│   └── functions/                 # PostgreSQL Stored Procedures, Triggers, & RLS Policies
├── deploy/                        # Infrastructure as Code & Deployment Configurations
│   ├── vercel/                    # Vercel Serverless Function & CDN Manifests
│   ├── cloudflare/                # Cloudflare Workers Edge Rules & Headers
│   └── k8s/                       # Future Microservices Kubernetes Manifests
├── docker/                        # Containerization Files & Environment Composes
│   ├── Dockerfile.frontend        # Frontend Production Container Build
│   ├── Dockerfile.backend         # Backend Production Container Build
│   ├── Dockerfile.ai              # AI Inference Sandbox Build
│   └── docker-compose.yml         # Local Multi-Container Development Environment
├── docs/                          # Project Documentation & Architectural Specs
│   ├── PRODUCT_VISION_AND_SPECIFICATION.md
│   ├── PRODUCT_REQUIREMENTS_DOCUMENT.md
│   ├── FEATURE_INVENTORY.md
│   ├── SYSTEM_ARCHITECTURE.md
│   └── FOLDER_STRUCTURE.md
├── monitoring/                    # Observability, Telemetry, & Alerting Configs
│   ├── prometheus/                # Prometheus Metrics Exporters & Rules
│   ├── grafana/                   # Grafana Dashboard Definitions
│   └── sentry/                    # Sentry Error Classification & Filtering Configs
├── analytics/                     # Product & Threat Intelligence Analytics
│   ├── telemetry/                 # Privacy-Sanitized Event Telemetry Definitions
│   └── dashboards/                # Custom Metric Queries & Aggregations
├── scripts/                       # DevOps, Data Processing, & Utility Automation
│   ├── setup.sh                   # One-Command Local Environment Setup Script
│   ├── seed_db.sh                 # Database Seeding Automation
│   └── benchmark_ai.py            # AI Model Latency & Accuracy Benchmark Runner
├── tests/                         # Comprehensive Testing Suite
│   ├── unit/                      # Unit Tests for Utility Functions & Parsers
│   ├── integration/               # API Endpoint & Database Integration Tests
│   ├── security/                  # PII Scrubbing, Injection, & Penetration Tests
│   ├── e2e/                       # End-to-End Browser Tests (Playwright)
│   └── fixtures/                  # Mock Phishing Payload & Email Test Fixtures
├── uploads/                       # Temporary Local Storage Directory (Development Only)
│   └── .gitkeep                   # Ensures Directory Structure in Version Control
├── logs/                          # Temporary Local Execution Logs (Development Only)
│   └── .gitkeep                   # Ensures Directory Structure in Version Control
├── .env.example                   # Master Environment Variables Template
├── .env.local                     # Local Development Overrides (Git Ignored)
└── README.md                      # Primary Repository Overview & Getting Started Guide
```

---

## 2. Directory Purpose & Scalability Explanation

### 2.1 Apps (`/apps`)
* **Purpose:** Houses all client-side applications in a monorepo format.
  * `/apps/web`: Next.js 14 web application, mobile PWA, and dashboard UI.
  * `/apps/extension`: Chrome and Firefox Manifest V3 browser extension.
* **Scalability Benefit:** Allows shared React components and TypeScript types between the web application and browser extension without duplicate code.

### 2.2 Backend (`/backend`)
* **Purpose:** Contains the core API handling business logic, payload route controllers, external scanner integrations, and queue producers.
* **Scalability Benefit:** Modular folder architecture enables effortless migration of individual sub-packages (e.g., `/backend/app/services/scanners`) into independent containerized microservices as load increases.

### 2.3 AI & Prompt Templates (`/ai`)
* **Purpose:** Dedicated directory isolating AI model wrappers, XAI highlight attributions, and version-controlled prompt templates.
  * `/ai/prompts`: System prompts for rationale generation, anti-prompt injection, and forensic breakdowns.
  * `/ai/xai`: Character-offset span attribution math and feature importance mapping.
* **Scalability Benefit:** Keeps AI models and system prompts completely decoupled from HTTP API handler code, simplifying prompt engineering iterations and LLM provider switching (Groq vs. OpenAI vs. local models).

### 2.4 Database & Migrations (`/database`)
* **Purpose:** Version-controlled database migration scripts, initial seed threat vectors, and PostgreSQL Row-Level Security (RLS) policies.
* **Scalability Benefit:** Guarantees deterministic database schema state across local, staging, and production Supabase environments.

### 2.5 Security, Privacy & PII Modules (`/apps/web/src/workers` & `/backend/app/api/middlewares`)
* **Purpose:** Client-side Web Workers and Edge Middlewares responsible for Regex and SpaCy-lite PII anonymization.
* **Scalability Benefit:** PII scrubbing runs at the outer boundary (browser/edge), preventing sensitive data from hitting core servers or database logs.

### 2.6 Docker & Infrastructure Deployment (`/docker` & `/deploy`)
* **Purpose:** Containerization manifests (`Dockerfile`, `docker-compose.yml`) and platform deployment configs for Vercel, Cloudflare, and Kubernetes.
* **Scalability Benefit:** Enables developers to run the entire stack locally with one command (`docker compose up`) while providing production IaC manifests.

### 2.7 Testing (`/tests`)
* **Purpose:** Consolidated test suites covering unit tests, API integration tests, adversarial prompt injection security tests, and Playwright E2E UI flows.
* **Scalability Benefit:** Prevents regression bugs across client, backend, and AI inference layers prior to CI/CD deployments.

### 2.8 Monitoring & Analytics (`/monitoring` & `/analytics`)
* **Purpose:** Configuration files for Sentry error tracking, Prometheus exporters, Grafana dashboards, and privacy-preserved product telemetry schemas.
* **Scalability Benefit:** Provides complete operational visibility and empirical performance metrics ($p95 < 1.8\text{s}$).

### 2.9 Temporary Storage & Logs (`/uploads` & `/logs`)
* **Purpose:** Local development directories for temporary `.eml`/image processing and local server logs. Protected by `.gitkeep` and excluded in `.gitignore`.
* **Scalability Benefit:** Prevents accidental storage of transient files in source control.

---

## 3. Directory Scalability & Monorepo Audit

The cross-functional leadership team audited the folder structure against production criteria:

1. **Monorepo Ready:** Organized to support Turborepo / Nx workspace orchestration seamlessly.
2. **Clear Separation of Concerns:** Clean boundaries between Frontend UI (`/apps/web`), Backend APIs (`/backend`), AI/Prompts (`/ai`), and Database (`/database`).
3. **Security Hardened:** Explicit locations for PII scrubbing workers and security testing fixtures (`/tests/security`).

---
*End of Master Folder Structure Specification.*
