/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        mospi: {
          50: '#f0f5fa',
          100: '#e1ecf5',
          200: '#c3daeb',
          300: '#94c0dd',
          400: '#5e9fcb',
          500: '#3b82b6',
          600: '#2a689b',
          700: '#22537e',
          800: '#1e4669',
          900: '#0f2b5c', // MoSPI Navy Primary
          950: '#0a1a38',
        },
        saffron: {
          50: '#fffaf0',
          100: '#feeedb',
          200: '#fddbb3',
          300: '#fbc181',
          400: '#f99e4b',
          500: '#ff9933', // India Saffron
          600: '#e67300',
          700: '#bf5300',
          800: '#993d00',
          900: '#7a3100',
        },
        indiaGreen: {
          50: '#f0fdf4',
          100: '#dcfce7',
          500: '#138808',
          600: '#16a34a',
          700: '#15803d',
        }
      },
    },
  },
  plugins: [],
};
