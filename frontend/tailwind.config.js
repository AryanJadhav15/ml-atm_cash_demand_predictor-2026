export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        panel: "#171717",
        surface: "#202020",
        ink: "#f6f2e8",
        muted: "#a7a29a",
        accent: "#36d399",
      },
      boxShadow: {
        glow: "0 0 0 1px rgba(255,255,255,0.06), 0 16px 50px rgba(0,0,0,0.35)",
      },
    },
  },
  plugins: [],
};
