import localFont from "next/font/local";

export const inter = localFont({
  src: [
    { path: "../app/fonts/inter-latin-400-normal.woff2", weight: "400", style: "normal" },
    { path: "../app/fonts/inter-latin-600-normal.woff2", weight: "600", style: "normal" },
  ],
  variable: "--font-inter",
  display: "swap",
});

export const serif4 = localFont({
  src: [
    { path: "../app/fonts/source-serif-4-latin-600-normal.woff2", weight: "600", style: "normal" },
    { path: "../app/fonts/source-serif-4-latin-700-normal.woff2", weight: "700", style: "normal" },
  ],
  variable: "--font-serif4",
  display: "swap",
});
