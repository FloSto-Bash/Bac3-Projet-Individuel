/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{html,js,svelte,ts}"],

  plugins: [require("@tailwindcss/typography"), require('daisyui')],

  daisyui: {
    themes: ["light", "sunset"],
    darkTheme:"sunset",
    logs : true
  }
};