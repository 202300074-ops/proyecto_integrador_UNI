/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        honey: {
          50: '#fdf8ee',
          100: '#f8ecd2',
          200: '#f0d6a3',
          300: '#e6ba6d',
          400: '#d99a3e',
          500: '#c9822a',
          600: '#a9631f',
          700: '#874b1d',
          800: '#6f3d1e',
          900: '#5d341c'
        },
        cream: '#f7f0e3',
        forest: {
          700: '#2c4a38',
          800: '#1f3b2c',
          900: '#14261c'
        },
        charcoal: '#26241f'
      },
      fontFamily: {
        display: ['Fraunces', 'Georgia', 'serif'],
        sans: ['Inter', 'system-ui', 'sans-serif']
      },
      boxShadow: {
        soft: '0 24px 60px -30px rgba(38, 36, 31, 0.35)'
      }
    }
  },
  plugins: []
};
