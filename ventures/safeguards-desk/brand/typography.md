# Typography

| Use | Font | Weights | Why |
|---|---|---|---|
| Headings, wordmark | **Source Serif 4** (Google Fonts, SIL OFL) | 600, 700 | Reads like a well-set document or letterhead: what a tax or mortgage owner trusts. Not a "hacker" monospace. |
| Body, UI, buttons | **Inter** (Google Fonts, SIL OFL) | 400, 600 | Highly legible at small sizes and on phones. |
| Code / technical appendix only | system monospace | — | Reports only, never marketing. |

- Fonts are **self-hosted** (from the `@fontsource` npm packages), not loaded from Google's servers: faster and no third-party request with the visitor's IP.
- Body 18px / 1.6 on desktop, 17px on phones; measure ≤ 70 characters.
- Headings in sentence case. No all-caps except the small "SECURITY" lockup in the wordmark.
- Fallbacks: `Georgia, 'Times New Roman', serif` and `system-ui, 'Segoe UI', Arial, sans-serif`.
