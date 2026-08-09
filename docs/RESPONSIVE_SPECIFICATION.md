# GuardianAI Cross-Device & Responsive Viewport Specification

**Document Version:** 1.0.0  
**Target Viewports:** Mobile Portrait (320px+), Mobile Landscape (568px+), Tablet (768px+), Laptop (1024px+), Desktop (1280px+), Ultra-Wide (1536px - 4K)  
**Evaluation Standard:** 100% Pixel-Perfect Fluid Responsive Layouts  

---

## 1. Responsive Viewport Grid Breakdown

```
┌────────────────────────────────────────────────────────────────────────┐
│                        Viewport Breakpoint Matrix                      │
├─────────────────┬───────────────────┬──────────────────────────────────┤
│ Breakpoint Tag  │ Min Width Range   │ Target Devices & Layout Mode     │
├─────────────────┼───────────────────┼──────────────────────────────────┤
│ Mobile Portrait │ < 640px           │ iPhone, Android, Mobile Bottom   │
│                 │                   │ Tab Bar (48px+ Touch Targets)    │
├─────────────────┼───────────────────┼──────────────────────────────────┤
│ Mobile Landscape│ 640px - 767px     │ Landscape Phones, Small Tablets  │
├─────────────────┼───────────────────┼──────────────────────────────────┤
│ Tablet          │ 768px - 1023px    │ iPad, Android Tablets (2-Column) │
├─────────────────┼───────────────────┼──────────────────────────────────┤
│ Laptop          │ 1024px - 1279px   │ MacBook Air, Laptops (3-Column)  │
├─────────────────┼───────────────────┼──────────────────────────────────┤
│ Desktop         │ 1280px - 1535px   │ Desktop Monitors, Fixed Sidebar  │
├─────────────────┼───────────────────┼──────────────────────────────────┤
│ Ultra-Wide 4K   │ >= 1536px         │ 4K / Curved Monitors (Centered)  │
└─────────────────┴───────────────────┴──────────────────────────────────┘
```

---

## 2. Component Adaptation Rules

### 2.1 Navigation (Navbar & Sidebar)
- **Mobile (`< 768px`):** Renders a fixed bottom tab bar with 48px+ touch targets for thumb navigation (`Home`, `Dashboard`, `Message`, `Email`, `URL`). Top navbar displays compact brand logo and shrink-proof `whitespace-nowrap` trigger buttons.
- **Desktop (`>= 768px`):** Renders a fixed left sidebar (`w-64`) with active tab indicators and section headers (`PLATFORM HUB`).

### 2.2 Tables & Data Grids
- Wrapped in `.table-responsive` containers (`overflow-x-auto`) to prevent horizontal page breaks on narrow mobile viewports.

### 2.3 Cards & Typography
- Padding scales fluidly from `p-4` (Mobile) to `p-6` (Desktop/Ultra-Wide).
- Base font size scales from $16\text{px}$ (Mobile) to $20\text{px}+$ (Senior Mode).

### 2.4 Ultra-Wide Monitor Support
- Outer shell container capped at `max-w-7xl 2xl:max-w-[1600px]` with `mx-auto` centering, ensuring dashboard cards never awkwardly stretch across 4K or 34-inch curved ultra-wide monitors.
