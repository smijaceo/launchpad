// How it works as three step cards (direction C), adapted from the 21st.dev how-it-works block.
import type { Item } from "@/lib/content";
import { SectionHead } from "./section-head";

export function Steps({ title, intro, items }: { title: string; intro: string; items: Item[] }) {
  return (
    <section aria-labelledby="steps" className="border-b border-border">
      <div className="mx-auto max-w-6xl px-5 py-20 sm:px-8 lg:py-28">
        <SectionHead id="steps" eyebrow="How it works" title={title} intro={intro} />
        <ol className="mt-12 grid gap-5 md:grid-cols-3">
          {items.map((item, i) => (
            <li key={item.term} className="relative flex flex-col gap-3 rounded-xl border border-border bg-card p-6">
              <p className="font-mono text-xs uppercase tracking-wide text-primary">Step {i + 1}</p>
              <h3 className="text-xl font-semibold tracking-tight" dangerouslySetInnerHTML={{ __html: item.term }} />
              <p className="leading-relaxed text-muted-foreground" dangerouslySetInnerHTML={{ __html: item.text }} />
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}
