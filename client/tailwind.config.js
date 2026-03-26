/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: 'var(--tw-auto-background)',
        card: 'var(--tw-auto-card)',
        cardborder: 'var(--tw-auto-border)',
        accent1: '#2563eb',
        accent2: '#7c3aed',
        textMain: 'var(--tw-auto-text-main)',
        textMuted: 'var(--tw-auto-text-muted)'
      },
      animation: {
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        glow: {
          '0%': { boxShadow: '0 0 5px rgba(37, 99, 235, 0.2)' },
          '100%': { boxShadow: '0 0 20px rgba(124, 58, 237, 0.6)' },
        }
      }
    },
  },
  plugins: [],
}
