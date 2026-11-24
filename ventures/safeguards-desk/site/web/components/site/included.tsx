// Deliverable cards with the generated illustration set (D11); layout after Superpower/Function on Mobbin.
import type { Item } from "@/lib/content";
import { SectionHead } from "./section-head";

const ART = [
  { src: "/illustrations/scan-office.webp", alt: "A small office building with scan rings around it and a green check above" },
  { src: "/illustrations/m365-mail.webp", alt: "An envelope, a mailbox with a forwarding arrow and a padlock" },
  { src: "/illustrations/report-dated.webp", alt: "A printed report with a desk calendar and a green rubber stamp" },
  { src: "/illustrations/call-walkthrough.webp", alt: "A headset next to two speech-bubble cards" },
];

export function Included({ title, intro, items }: { title: string; intro: string; items: Item[] }) {
  return (
    <section aria-labelledby="included" className="border-b border-border bg-muted">
      <div className="mx-auto max-w-6xl px-5 py-20 sm:px-8 lg:py-28">
        <SectionHead id="included" eyebrow="What you get" title={title} intro={intro} />
        <ul className="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
          {items.map((item, i) => (
            <li key={item.term} className="group flex flex-col overflow-hidden rounded-xl border border-border bg-card transition-transform duration-200 hover:-translate-y-0.5">
              <div className="aspect-[4/3] overflow-hidden bg-[#F6F3EE]">
                {ART[i] && (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img src={ART[i].src} alt={ART[i].alt} width={800} height={603} loading="lazy" className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-[1.03]" />
                )}
              </div>
              <div className="flex flex-col gap-2 p-5">
                <p className="font-mono text-xs text-primary">{String(i + 1).padStart(2, "0")}</p>
                <h3 className="text-lg font-semibold tracking-tight" dangerouslySetInnerHTML={{ __html: item.term }} />
                <p className="text-[15px] leading-relaxed text-muted-foreground" dangerouslySetInnerHTML={{ __html: item.text }} />
              </div>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
