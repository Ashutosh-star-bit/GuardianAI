import { Variants } from 'framer-motion';

/**
 * GuardianAI Centralized Framer Motion Animation System
 * Purpose: Provides hardware-accelerated 60 FPS animation variants for page transitions, card hover, scan radar, risk gauges, modals, and error shakes.
 */

// 1. Page Entrance Transition
export const pageVariants: Variants = {
  initial: { opacity: 0, y: 12, scale: 0.99 },
  animate: { opacity: 1, y: 0, scale: 1, transition: { duration: 0.25, ease: 'easeOut' } },
  exit: { opacity: 0, y: -12, scale: 0.99, transition: { duration: 0.15, ease: 'easeIn' } },
};

// 2. Staggered Container & Children
export const staggerContainer: Variants = {
  initial: {},
  animate: {
    transition: {
      staggerChildren: 0.08,
    },
  },
};

export const staggerItem: Variants = {
  initial: { opacity: 0, y: 16 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.3, ease: 'easeOut' } },
};

// 3. Card Hover Elevation
export const cardHoverVariants: Variants = {
  initial: { scale: 1, y: 0 },
  hover: { scale: 1.015, y: -3, transition: { duration: 0.2, ease: 'easeOut' } },
  tap: { scale: 0.98, y: 0 },
};

// 4. Button Micro-Interactions
export const buttonHoverVariants: Variants = {
  initial: { scale: 1 },
  hover: { scale: 1.03, transition: { duration: 0.15, ease: 'easeOut' } },
  tap: { scale: 0.97 },
};

// 5. Error Shake Keyframes
export const errorShakeVariants: Variants = {
  shake: {
    x: [0, -8, 8, -6, 6, -3, 3, 0],
    transition: { duration: 0.4 },
  },
};

// 6. Modal & Backdrop Overlay
export const backdropVariants: Variants = {
  closed: { opacity: 0 },
  open: { opacity: 1, transition: { duration: 0.2 } },
};

export const modalVariants: Variants = {
  closed: { opacity: 0, scale: 0.95, y: 10 },
  open: { opacity: 1, scale: 1, y: 0, transition: { duration: 0.25, ease: 'easeOut' } },
};

// 7. Sidebar Slide-In
export const sidebarVariants: Variants = {
  closed: { x: '-100%', transition: { type: 'spring', damping: 25, stiffness: 200 } },
  open: { x: 0, transition: { type: 'spring', damping: 25, stiffness: 200 } },
};
