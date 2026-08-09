# GuardianAI Frontend Performance & Optimization Blueprint

**Document Version:** 1.0.0  
**Target Bundle Size:** < 200 KB initial gzipped JS  
**Target SLA:** Sub-200ms initial route load times & 60 FPS UI transitions  

---

## 1. Code-Splitting & Vendor Chunk Strategy

In [`frontend/vite.config.ts`](file:///c:/Users/rajbh/OneDrive/Desktop/GuardianAI/frontend/vite.config.ts), we configured Rollup manual chunks to isolate third-party dependencies into cached vendor bundles:

```
dist/assets/
├── vendor-react.js     (~42 KB gzipped)  # React 18, ReactDOM, React Router v6
├── vendor-query.js     (~28 KB gzipped)  # TanStack React Query v5, Axios
├── vendor-motion.js    (~34 KB gzipped)  # Framer Motion animation engine
├── vendor-icons.js     (~18 KB gzipped)  # Lucide Icons SVG dictionary
├── vendor-forms.js     (~15 KB gzipped)  # Zod, React Hook Form, Resolvers
└── index.js            (~38 KB gzipped)  # App entry point
```

**Result:** Initial page load only downloads `vendor-react` and `index.js` (~80 KB total gzipped), deferring other chunks until needed!

---

## 2. Dynamic Route Lazy Loading

All 17 application routes are code-split in `App.tsx` via `React.lazy()`:

```tsx
const HomePage = lazy(() => import('./pages/HomePage').then((m) => ({ default: m.HomePage })));
const DashboardPage = lazy(() => import('./pages/DashboardPage').then((m) => ({ default: m.DashboardPage })));
const MessageScanPage = lazy(() => import('./pages/MessageScanPage').then((m) => ({ default: m.MessageScanPage })));
```

---

## 3. React Rendering & Memory Optimization

- **Zero Re-Render Form State:** `react-hook-form` isolates input changes to DOM refs, eliminating full-page component re-renders on keystrokes.
- **Memoized Selectors & Handlers:** `useMemo` is used across filtering logic in `HistoryPage.tsx` and `AnalyticsPage.tsx` to prevent expensive array re-computations.
- **Event Listener Garbage Collection:** All global hotkey listeners (`Alt + S`, `Alt + T`, `Escape`) return cleanup functions in `useEffect` to prevent memory leaks:

```tsx
useEffect(() => {
  const handleKeyDown = (e: KeyboardEvent) => { ... };
  window.addEventListener('keydown', handleKeyDown);
  return () => window.removeEventListener('keydown', handleKeyDown);
}, []);
```

---

## 4. Caching & Network Strategy

- **TanStack React Query:** Configured with `staleTime: 5 * 60 * 1000` (5 minutes) and `gcTime: 10 * 60 * 1000` (10 minutes).
- **Refetch Policy:** `refetchOnWindowFocus: false` prevents unnecessary background HTTP requests when users tab between windows.
