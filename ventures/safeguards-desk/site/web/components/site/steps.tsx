// Adapted from 21st.dev "How It Works Timeline" (olewandowski1/how-it-works-2).
import { RiChat3Line, RiFileList3Line, RiQuillPenLine, RiShieldCheckLine } from "@remixicon/react";
import type { Item } from "@/lib/content";
import { SectionHead } from "./section-head";

const ICONS = [RiChat3Line, RiQuillPenLine, RiShieldCheckLine, RiFileList3Line];

export function Steps({ title, intro, items }: { title: string; intro: string; items: Item[] }) {
  return (
    <section aria-labelledby="steps" className="border-b border-border">
      <div className="mx-auto grid max-w-6xl gap-12 px-5 py-20 sm:px-8 lg:grid-cols-[1fr_1.3fr] lg:py-28">
        <div className="lg:sticky lg:top-28 lg:self-start">
          <SectionHead id="steps" eyebrow="How it works" title={title} intro={intro} />
        </div>
        <ol className="flex flex-col">
          {items.map((item, index) => {
            const Icon = ICONS[index % ICONS.length];
            const isLast = index === items.length - 1;
            return (
              <li key={item.term} className="flex gap-5 sm:gap-6">
                <div className="flex flex-col items-center">
                  <span className="flex size-11 shrink-0 items-center justify-center rounded-full border border-border bg-background text-ink">
                    <Icon className="size-5" aria-hidden="true" />
                  </span>
                  {!isLast && <span className="mt-1 w-px flex-1 bg-border" />}
                </div>
                <div className={isLast ? "pb-0" : "pb-10"}>
                  <p className="font-mono text-xs text-primary tabular-nums">Step {index + 1}</p>
                  <h3 className="mt-1 text-lg font-semibold" dangerouslySetInnerHTML={{ __html: item.term }} />
                  <p className="mt-1.5 leading-relaxed text-muted-foreground" dangerouslySetInnerHTML={{ __html: item.text }} />
                </div>
              </li>
            );
          })}
        </ol>
      </div>
    </section>
  );
}
