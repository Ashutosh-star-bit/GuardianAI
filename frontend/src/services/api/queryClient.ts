import { QueryClient } from '@tanstack/react-query';

/**
 * GuardianAI React Query Master QueryClient Configuration
 * Purpose: Provides global data fetching, caching, stale-time policies, and retry strategies.
 */

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes stale time
      gcTime: 10 * 60 * 1000, // 10 minutes garbage collection time
      retry: 1, // Retry failed queries once before showing error UI
      refetchOnWindowFocus: false, // Prevent redundant background refetches
      refetchOnReconnect: true,
    },
    mutations: {
      retry: 0, // Do not auto-retry failed POST scan mutations
    },
  },
});
