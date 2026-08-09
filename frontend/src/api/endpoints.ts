/**
 * GuardianAI API Endpoints Dictionary
 * Purpose: Centralizes all API route constants for consistency across the frontend application.
 */

export const API_ENDPOINTS = {
  HEALTH: '/health',
  AUTH: {
    REGISTER: '/auth/register',
    LOGIN: '/auth/login',
    MAGIC_LINK: '/auth/magic-link',
  },
  SCAN: {
    TEXT: '/scan/text',
    EMAIL: '/scan/email',
    URL: '/scan/url',
    QR: '/scan/qr',
  },
  HISTORY: '/history',
  ANALYTICS: {
    DASHBOARD: '/analytics/dashboard',
  },
  FEEDBACK: '/feedback',
  REPORTS: {
    DISPATCH: '/reports/dispatch',
  },
  COMMUNITY: {
    REPORTS: '/community/reports',
    REPORT: '/community/report',
    VOTE: '/community/vote',
    FEEDBACK: '/community/feedback',
    TRENDING: '/community/trending',
  },
  SETTINGS: '/settings',
  DEVELOPER: {
    KEYS: '/developer/keys',
  },
} as const;
