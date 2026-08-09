# GuardianAI Design System Specification

**Version:** 1.0.0  
**Target Platform:** GuardianAI Web Application & Extension  
**Aesthetic Philosophy:** Premium Dark Mode Baseline + High-Contrast Senior Citizen Accessibility Mode  

---

## 1. Color System & Palettes

The GuardianAI color palette is built around psychological safety, high visual contrast, and clear threat communication.

### 1.1 Primary Palette (Guardian Sky Blue)
Conveys trust, technological precision, and calm assurance.

| Token | Hex Code | HSL Value | Purpose / Usage |
| :--- | :--- | :--- | :--- |
| `primary-50` | `#f0f7ff` | `hsl(210, 100%, 97%)` | Subtly tinted background overlays |
| `primary-100` | `#e0effe` | `hsl(210, 96%, 94%)` | Light badges & active pill backgrounds |
| `primary-400` | `#38bdf8` | `hsl(198, 93%, 60%)` | Interactive highlights & link states |
| `primary-500` | `#0284c7` | `hsl(199, 98%, 39%)` | Primary button baseline |
| `primary-600` | `#0265d6` | `hsl(212, 98%, 42%)` | Primary hover button state |
| `primary-900` | `#0c4a6e` | `hsl(201, 80%, 24%)` | Dark mode container borders |

### 1.2 Neutral / Dark Mode Canvas Palette
Deep midnight slate palette preventing eye fatigue during night monitoring.

| Token | Hex Code | Purpose / Usage |
| :--- | :--- | :--- |
| `bg-canvas` | `#030712` | Main page body canvas |
| `bg-card` | `#090d16` | Container card & modal background |
| `bg-card-hover` | `#111827` | Hovered list items & rows |
| `border-subtle` | `#1f2937` | Card borders & divider lines |
| `text-heading` | `#f9fafb` | Primary text headings |
| `text-body` | `#d1d5db` | Body text copy |
| `text-muted` | `#9ca3af` | Secondary labels & timestamps |

### 1.3 Threat Risk Level Colors

```
[ SAFE (0-29) ] ------> Emerald Green  (#16a34a / #22c55e)
[ CAUTION (30-69) ] --> Amber Gold     (#d97706 / #f59e0b)
[ DANGEROUS (70-100) ]> Crimson Red    (#dc2626 / #ef4444)
```

| Threat Level | Score Range | Primary Hex | Background Tint | Badge Border |
| :--- | :--- | :--- | :--- | :--- |
| **SAFE** | 0 – 29 | `#22c55e` | `#052e16` | `#15803d` |
| **CAUTION** | 30 – 69 | `#f59e0b` | `#451a03` | `#b45309` |
| **DANGEROUS** | 70 – 100 | `#ef4444` | `#450a0a` | `#b91c1c` |

### 1.4 Senior Citizen High-Contrast Warm Light Palette
Activated via Senior Mode toggle. Guarantees $12:1$ contrast ratio exceeding WCAG 2.1 AAA.

- **Background Canvas:** `#ffffff` (Pure White)
- **Primary Text:** `#000000` (Pure Black)
- **Primary Action Buttons:** `#0055ff` with 3px `#000000` solid border
- **Warning Accent:** `#d97706` (Deep Amber)
- **Base Font Size:** `20px` (1.25rem)

---

## 2. Typography System

### 2.1 Font Families
- **Primary UI Sans:** `Inter`, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif.
- **Monospace Payload Code:** `JetBrains Mono`, `Fira Code`, ui-monospace, SFMono-Regular, monospace.

### 2.2 Scale & Line Heights

| Style Class | Font Size | Line Height | Weight | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| `display-xl` | 48px (3rem) | 1.15 | 900 (Black) | Hero headings |
| `heading-lg` | 30px (1.875rem)| 1.25 | 800 (ExtraBold) | Page titles |
| `heading-md` | 24px (1.5rem) | 1.3 | 700 (Bold) | Section headers & cards |
| `body-lg` | 18px (1.125rem) | 1.6 | 400 (Normal) | Lead rationale text |
| `body-md` | 16px (1rem) | 1.5 | 400 (Normal) | Body text |
| `body-sm` | 14px (0.875rem) | 1.4 | 500 (Medium) | Labels & controls |
| `caption` | 12px (0.75rem) | 1.3 | 600 (SemiBold) | Badges & timestamps |

---

## 3. Spacing & Border Radius Tokens

### 3.1 Spacing Grid (4px Baseline)
- `space-1`: 4px | `space-2`: 8px | `space-3`: 12px | `space-4`: 16px
- `space-6`: 24px | `space-8`: 32px | `space-12`: 48px | `space-16`: 64px

### 3.2 Border Radius System
- `radius-sm`: 6px (`0.375rem`) — Badges, tooltips
- `radius-md`: 12px (`0.75rem`) — Buttons, input fields
- `radius-lg`: 16px (`1rem`) — Cards, modals
- `radius-xl`: 24px (`1.5rem`) — Scanner console containers

---

## 4. Shadows & Elevation System

- `shadow-card`: `0 10px 30px -10px rgba(0, 0, 0, 0.5)`
- `shadow-sky-glow`: `0 0 20px -5px rgba(2, 132, 199, 0.4)`
- `shadow-danger-glow`: `0 0 25px -5px rgba(239, 68, 68, 0.4)`
- `shadow-safe-glow`: `0 0 20px -5px rgba(34, 197, 94, 0.4)`

---

## 5. Animation Guidelines & Motion Rules

1. **Micro-Interactions:** Fast 150ms-200ms `ease-out` curves for button presses and tab switches.
2. **Threat Score Gauge Animation:** Animated counter transitioning threat score from 0 to target score over 600ms.
3. **Radar Scanning Sweep:** Subtly glowing radar sweep line across scanner text area while AI models process input (`animate-radar`).
4. **Reduced Motion:** Respects `prefers-reduced-motion: reduce` media query by disabling loop animations.

---

## 6. UI Component Specifications

### 6.1 Buttons
- **Primary:** Sky blue background (`bg-sky-600`), white text, sky glow shadow on hover.
- **Secondary:** Dark slate background (`bg-slate-900`), border `border-slate-800`.
- **Danger:** Crimson background (`bg-red-600`), white text.
- **Senior Mode:** 20px font size, 3px solid black border, warm amber hover.

### 6.2 Cards
- Dark canvas background (`#090d16`), 1px subtle border (`#1f2937`), rounded corners (`16px`).
- Left indicator accent bar for threat risk levels (`border-l-4 border-red-500`).

### 6.3 Input Fields & Textareas
- Dark background (`#0b1120`), border (`#1e293b`), focus ring (`ring-2 ring-sky-500`).
- Monospace font styling for raw headers or link inputs.

### 6.4 Risk Indicators & Badges
- Threat Score Pills: Large numeric score + color icon (CheckCircle for Safe, AlertTriangle for Caution/Dangerous).
- Highlights: Inline background highlights over scam text (`bg-red-950/80 text-red-200 border-b-2 border-red-500`).

---

## 7. Accessibility & WCAG 2.1 AAA Guidelines

1. **Multi-Sensory Threat Messaging:** Never rely solely on color to indicate danger. Always pair colors with clear text labels ("DANGEROUS") and distinct SVG icons.
2. **Keyboard Focus:** Every interactive control features a visible 3px focus ring (`focus-visible:ring-sky-400 focus-visible:ring-offset-2`).
3. **Screen Reader Live Regions:** XAI threat evaluation results announce score changes via `aria-live="polite"`.
4. **Contrast Compliance:** All text body colors maintain a minimum $7:1$ contrast ratio against dark backgrounds, and $12:1$ in Senior Mode.
