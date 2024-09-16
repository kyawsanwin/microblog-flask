/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./microblog/**/views/**/*.{html,js}",
    "./microblog/templates/**/*.html",
    "./microblog/templates/*.htm"
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

