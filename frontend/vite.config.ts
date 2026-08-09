import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

/**
 * GuardianAI High-Performance Vite Configuration
 * Purpose: Configures React plugin, path aliases, dev server proxy, and advanced Rollup code-splitting chunks.
 */

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5173,
    host: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
    },
  },
  build: {
    target: 'es2022',
    outDir: 'dist',
    sourcemap: false,
    minify: 'esbuild',
    cssCodeSplit: true,
    chunkSizeWarningLimit: 600,
    rollupOptions: {
      output: {
        // Clean Vendor Code-Splitting Strategy preventing circular chunk warnings
        manualChunks(id) {
          if (id.includes('node_modules')) {
            if (id.includes('react/') || id.includes('react-dom/') || id.includes('react-router-dom/')) {
              return 'vendor-core-react';
            }
            if (id.includes('@tanstack') || id.includes('axios')) {
              return 'vendor-query';
            }
            if (id.includes('framer-motion')) {
              return 'vendor-motion';
            }
            if (id.includes('lucide-react')) {
              return 'vendor-icons';
            }
          }
        },
      },
    },
  },
});
