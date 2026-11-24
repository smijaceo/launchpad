import type { Item } from "@/lib/content";
import { SectionHead } from "./section-head";

export function Fit({ title, intro, items }: { title: string; intro: string; items: Item[] }) {
  return (
    <section aria-labelledby="fit" className="border-b border-border">
      <div className="mx-auto max-w-6xl px-5 py-20 sm:px-8 lg:py-24">
        <SectionHead id="fit" eyebrow="Straight answer" title={title} intro={intro} />
        <ol className="mt-10 grid gap-5 md:grid-cols-2">
          {items.map((item, i) => (
            <li key={i} className="rounded-xl border border-border bg-card p-6">
              <p className="font-mono text-xs uppercase tracking-wide text-muted-foreground">Case {i + 1}</p>
              <p className="mt-3 leading-relaxed text-foreground/85" dangerouslySetInnerHTML={{ __html: item.html }} />
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}
