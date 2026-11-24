import type { Metadata, Viewport } from "next";
import "./globals.css";
import { inter, serif4 } from "@/lib/fonts";
import { bookingUrl, footerPages, isPreview, navPages, site } from "@/lib/content";
import { SiteFooter } from "@/components/site/site-footer";

export const metadata: Metadata = {
  metadataBase: new URL(site.base_url),
  title: { default: site.name, template: `%s · ${site.name}` },
  robots: isPreview ? { index: false, follow: false } : { index: true, follow: true },
  openGraph: { type: "website", siteName: site.name, images: [{ url: "/og.png", width: 1200, height: 630 }] },
  twitter: { card: "summary_large_image" },
};

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#FAF8F4" },
    { media: "(prefers-color-scheme: dark)", color: "#0F1620" },
  ],
  colorScheme: "light dark",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${inter.variable} ${serif4.variable}`}>
      <body className="min-h-dvh font-sans">
        <a
          href="#main"
          className="skip-link fixed left-4 top-0 z-50 -translate-y-full rounded-b-md bg-ink px-4 py-2 font-semibold text-background transition-transform focus-visible:translate-y-0"
        >
          Skip to Main Content
        </a>
        {isPreview && (
          <div role="note" className="bg-warn px-4 py-1.5 text-center text-sm font-semibold text-background">
            Preview build: not published. Founder confirmation and legal review pending.
          </div>
        )}
        {children}
        <SiteFooter links={navPages()} legal={footerPages()} />
      </body>
    </html>
  );
}
