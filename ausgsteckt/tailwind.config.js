/** @type {import('tailwindcss').Config} */
// Paths are relative to this file so the same config works locally and inside
// the container, where this directory is copied to /usr/local/app.
module.exports = {
  content: ["./**/templates/**/*.html"],
  theme: {
    extend: {
      fontFamily: {
        serif: ["Newsreader", "ui-serif", "Georgia", "serif"],
        sans: ["Work Sans", "ui-sans-serif", "system-ui", "sans-serif"],
      },
      colors: {
        bg: "oklch(96% 0.018 85)",
        paper: "oklch(99% 0.006 85)",
        surface: "oklch(93% 0.022 78)",
        ink: "oklch(23% 0.025 40)",
        "ink-soft": "oklch(46% 0.03 45)",
        "ink-faint": "oklch(62% 0.02 50)",
        border: "oklch(87% 0.02 70)",
        burgundy: {
          DEFAULT: "oklch(34% 0.12 18)",
          hover: "oklch(28% 0.12 18)",
          tint: "oklch(91% 0.03 18)",
        },
        gold: {
          DEFAULT: "oklch(52% 0.11 75)",
          tint: "oklch(90% 0.04 78)",
        },
        sage: {
          DEFAULT: "oklch(46% 0.09 150)",
          tint: "oklch(92% 0.045 150)",
        },
        terracotta: {
          DEFAULT: "oklch(48% 0.13 35)",
          tint: "oklch(92% 0.045 35)",
        },
      },
    },
  },
  plugins: [require("@tailwindcss/typography")],
};
