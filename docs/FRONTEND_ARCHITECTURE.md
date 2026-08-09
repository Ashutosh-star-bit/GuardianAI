# GuardianAI Production-Ready Frontend Architecture Specification

**Document Version:** 1.0.0  
**Author:** Senior Frontend Architect & Staff React Engineer  
**Core Technologies:** React 18, TypeScript 5, Vite 5, TailwindCSS 3, React Router DOM 6, TanStack React Query v5, Axios, Framer Motion, React Hook Form, Zod, Lucide Icons  

---

## 1. Architectural Overview

GuardianAI's frontend is engineered as a **High-Performance, Privacy-First, Accessible Single-Page Application (SPA)**.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        React DOM Root App                              │
├────────────────────────────────────────────────────────────────────────┤
│ 1. QueryClientProvider        (TanStack React Query Cache Engine)     │
│  └─ 2. ErrorBoundary          (UI Crash Protection & 1-Click Recovery) │
│      └─ 3. AccessibilityContext (Dark/Light Theme & Senior Mode AAA) │
│          └─ 4. ToastProvider   (Global Alert Notification Stack)       │
│              └─ 5. BrowserRouter (React Router DOM Nested Navigation) │
│                  └─ 6. Suspense (Lazy Code-Splitting Chunk Loader)    │
│                      └─ 7. MainLayout (Navbar + Sidebar + Outlet)     │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Directory & Component Topology

```
frontend/src/
├── api/                           # API Route Constants Dictionary (endpoints.ts)
├── services/                      # Service Layer Infrastructure
│   └── api/
│       ├── axiosClient.ts         # Axios instance with JWT interceptors & RFC 7807 error parsing
│       ├── queryClient.ts         # TanStack QueryClient with 5-min staleTime & caching policy
│       └── scanService.ts         # Scan API service methods (text, url, email, qr)
├── context/                       # React Context Providers
│   ├── AccessibilityContext.tsx   # Dark/Light Theme & Senior Citizen High-Contrast state
│   └── ToastContext.tsx           # Global Toast Notification stack provider
├── hooks/                         # Custom React Hooks
│   └── useScanMutation.ts         # Typed React Query mutation hook with automatic toast feedback
├── utils/                         # Validation & Utilities
│   └── validation.ts              # Zod form validation schemas (TextScan, UrlScan, Login)
├── components/                    # Component Architecture
│   ├── common/                    # Shared Atomic UI Controls
│   │   ├── Button.tsx             # Accessible Button component
│   │   ├── Card.tsx               # Container Card component
│   │   ├── LoadingSpinner.tsx     # Pulse loading spinner & full-page loader
│   │   ├── Skeleton.tsx           # Pulse Skeleton UI placeholder
│   │   ├── Toast.tsx              # Toast alert component
│   │   ├── ErrorBoundary.tsx      # React Error Boundary component
│   │   ├── PageTransition.tsx     # Framer Motion route entrance transition
│   │   └── FadeIn.tsx             # Framer Motion fade-in animation wrapper
│   └── layout/                    # Layout Hierarchy Shell
│       ├── MainLayout.tsx         # Responsive shell layout
│       ├── Navbar.tsx             # Top Navbar with logo & action buttons
│       ├── Sidebar.tsx            # Desktop side nav + Mobile bottom tab bar
│       └── Footer.tsx             # Application footer
├── pages/                         # 12 Code-Split Page Components
│   ├── HomePage.tsx               # Hero landing page
│   ├── DashboardPage.tsx          # Security command hub
│   ├── MessageScanPage.tsx        # Text & SMS scam inspector
│   ├── EmailScanPage.tsx          # Email header BEC inspector
│   ├── UrlScanPage.tsx            # URL & domain inspector
│   ├── QrScanPage.tsx             # Quishing QR code inspector
│   ├── HistoryPage.tsx            # Scan history log
│   ├── AnalyticsPage.tsx          # Threat analytics & trends
│   ├── ReportsPage.tsx            # Automated fraud reporting
│   ├── ProfilePage.tsx            # User profile & subscription
│   ├── SettingsPage.tsx           # Accessibility & API settings
│   └── NotFoundPage.tsx           # 404 fallback screen
└── workers/                       # Background Web Workers
    └── piiSanitizer.worker.ts     # Client-side PII scrubber thread
```

---

## 3. Detailed Architecture Specifications

### 3.1 State Management Strategy
- **Server State:** Managed exclusively via `@tanstack/react-query` (`QueryClient`). Handles data caching, stale-time management (5 mins), and mutation invalidations.
- **Global UI State:** Managed via lightweight React Context (`AccessibilityContext`, `ToastContext`).
- **Form State:** Managed via `react-hook-form` paired with `@hookform/resolvers/zod` for zero-re-render form performance.
- **Local Component State:** Standard `useState` / `useCallback` for transient UI toggles.

### 3.2 API Layer & Network Resiliency
- **Axios HTTP Client (`services/api/axiosClient.ts`):**
  - Automatic `Authorization: Bearer <token>` injection via request interceptors.
  - Automatic correlation tracking (`X-Request-ID`).
  - Standardized error normalization (`NormalizedApiError`) parsing RFC 7807 backend responses.

### 3.3 Theme Management & Accessibility (WCAG 2.1 AAA)
- **Dark Mode Baseline:** Deep midnight canvas (`#030712`).
- **Light Mode Theme:** Clean slate theme (`#f8fafc`).
- **Senior Citizen Mode:** $12:1$ warm light contrast ratio, $20\text{px}+$ base font, 3px solid black borders, and keyboard shortcuts (`Alt + S` for Senior Mode, `Alt + T` for Theme).

### 3.4 Lazy Loading & Code-Splitting
- All 12 pages are lazy-loaded via `React.lazy()` inside `App.tsx`.
- Bundles are automatically split into separate JavaScript chunks during Vite production build (`npm run build`), ensuring sub-200ms initial page load times.
- Visual loading states are gracefully handled via `<Suspense fallback={<LoadingSpinner fullPage />}>`.

### 3.5 Error Boundary & Crash Protection
- Wrapped in `<ErrorBoundary>` component. Catches unhandled UI render crashes, logs errors silently, and displays a friendly recovery screen with a 1-click button to return to safety.

---

## 4. Summary Matrix

| Section | Solution / Technology | Purpose |
| :--- | :--- | :--- |
| **Data Fetching** | `@tanstack/react-query` + `axios` | Server state caching, stale management, mutation feedback |
| **Form Validation** | `react-hook-form` + `zod` | Type-safe form validation with zero re-render lag |
| **Animations** | `framer-motion` | Smooth route transitions & card fade-in entrance animations |
| **Routing & Splits**| `react-router-dom` + `React.lazy()` | Lazy-loaded code-split page routes |
| **Theme & Contrast**| `AccessibilityContext` + Tailwind | Dark Mode, Light Mode, & Senior Citizen WCAG AAA $12:1$ contrast |
| **Notifications** | `ToastContext` + `Toast` | Non-blocking alert notifications for scan completion and errors |
