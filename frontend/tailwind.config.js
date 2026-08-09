/** @type {import('tailwindcss').Config} */
// GuardianAI Design System Tailwind Configuration
// Purpose: Configures primary, secondary, threat risk color palettes, custom font families, spacing grid, shadows, and animation keyframes.

export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Primary Brand Colors (Guardian Sky Blue)
        brand: {
          50: '#f0f7ff',
          100: '#e0effe',
          200: '#bae0fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0284c7',
          600: '#0265d6',
          700: '#034aa6',
          800: '#075985',
          900: '#0c4a6e',
          950: '#082f49',
        },
        // Threat Risk Level Colors
        risk: {
          safe: {
            DEFAULT: '#16a34a',
            light: '#4ade80',
            bg: '#052e16',
            border: '#15803d',
          },
          caution: {
            DEFAULT: '#d97706',
            light: '#fbbf24',
            bg: '#451a03',
            border: '#b45309',
          },
          dangerous: {
            DEFAULT: '#dc2626',
            light: '#f87171',
            bg: '#450a0a',
            border: '#b91c1c',
          },
        },
        // Canvas Dark Mode Palette
        canvas: {
          dark: '#030712',
          card: '#090d16',
          border: '#1f2937',
          hover: '#111827',
        },
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'ui-monospace', 'monospace'],
      },
      boxShadow: {
        'sky-glow': '0 0 25px -5px rgba(2, 132, 199, 0.4)',
        'danger-glow': '0 0 25px -5px rgba(239, 68, 68, 0.4)',
        'safe-glow': '0 0 25px -5px rgba(34, 197, 94, 0.4)',
        'card-elevated': '0 10px 30px -10px rgba(0, 0, 0, 0.5)',
      },
      borderRadius: {
        '2xl': '1rem',
        '3xl': '1.5rem',
      },
      animation: {
        'radar-sweep': 'radar 3s linear infinite',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        radar: {
          '0%': { transform: 'rotate(0deg)' },
          '100%': { transform: 'rotate(360deg)' },
        },
      },
    },
  },
  plugins: [],
}
