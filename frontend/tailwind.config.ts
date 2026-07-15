import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        border: "rgb(var(--color-border) / <alpha-value>)",
        blue: "rgb(var(--color-blue) / <alpha-value>)",
        blueSoft: "rgb(var(--color-blue-soft) / <alpha-value>)",
        greenSoft: "rgb(var(--color-green-soft) / <alpha-value>)",
        surface: "rgb(var(--color-surface) / <alpha-value>)",
        muted: "rgb(var(--color-muted) / <alpha-value>)",
        ink: "rgb(var(--color-ink) / <alpha-value>)",
        accent: "rgb(var(--color-accent) / <alpha-value>)",
        tealSoft: "rgb(var(--color-teal-soft) / <alpha-value>)",
      },
      boxShadow: {
        soft: "0 20px 45px -30px rgb(15 23 42 / 0.35)",
        product: "0 32px 80px -42px rgb(37 99 235 / 0.42)",
      },
    },
  },
  plugins: [],
} satisfies Config;
