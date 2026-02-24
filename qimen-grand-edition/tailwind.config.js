/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        'qimen-gold': '#b8905b',
        'qimen-dark': '#0f172a',
        'qimen-accent': '#00bfa5',
        'qimen-red': '#ef4444',
      },
    },
  },
  plugins: [],
}
