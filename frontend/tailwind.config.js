/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Cores do FilmersHub
        void: '#0B0B11',
        obsidian: '#15151F',
        graphite: '#1E1E2E',
        slate: '#2A2A3A',
        iris: '#7C5CFC',
        ember: '#FF6B35',
        jade: '#22C55E',
        amber: '#F59E0B',
        crimson: '#EF4444',
        azure: '#3B82F6',
        snow: '#E8E8ED',
        ash: '#8B8B9E',
        muted: '#55556A',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [],
}
