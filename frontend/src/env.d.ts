/// <reference types="vite/client" />

/**
 * GuardianAI Frontend Environment Variables Interface
 * Purpose: Provides strong TypeScript type-safety for Vite environment variables.
 */
interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string;
  readonly VITE_ENABLE_ANALYTICS?: string;
  readonly VITE_APP_TITLE?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
