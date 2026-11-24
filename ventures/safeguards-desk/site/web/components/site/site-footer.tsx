// Adapted from 21st.dev "Minimal Two-Column Footer" (ln-dev7/footer-17).
import { Wordmark } from "./logo";

type Link = { label: string; href: string };

export function SiteFooter({ links, legal }: { links: Link[]; legal: Link[] }) {
  return (
    <footer className="border-t border-border bg-background text-foreground">
      <div className="mx-auto max-w-6xl px-5 py-14 sm:px-8">
        <div className="flex flex-col gap-10 sm:flex-row sm:items-start sm:justify-between">
          <div className="flex max-w-sm flex-col gap-4">
            <a href="/" className="w-fit rounded-md" aria-label="Countersign Security home">
              <Wordmark />
            </a>
            <p className="text-sm leading-relaxed text-muted-foreground">
              A fixed-fee Safeguards testing check for small tax, accounting and mortgage offices.
            </p>
          </div>
          <div className="flex flex-col gap-3">
            <h2 className="text-xs font-semibold uppercase tracking-widest text-muted-foreground">Navigate</h2>
            <ul className="grid grid-cols-2 gap-x-10 gap-y-1">
              {[...links, ...legal].map((link) => (
                <li key={link.href}>
                  <a href={link.href} className="inline-block py-1.5 text-sm text-foreground/80 underline-offset-4 transition-colors hover:text-foreground hover:underline">
                    {link.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>
        <div className="mt-12 flex flex-col gap-2 border-t border-border pt-6 text-xs text-muted-foreground sm:flex-row sm:items-center sm:justify-between">
          <p>General information, not legal advice. Not affiliated with the Federal Trade Commission or the Internal Revenue Service.</p>
          <p translate="no">© {new Date().getFullYear()} Countersign Security</p>
        </div>
      </div>
    </footer>
  );
}
