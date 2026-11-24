// Adapted from 21st.dev "Comparison Section" (Hirael comparison-03, MIT · Mohammad Shehadeh).
import { Check, CircleCheck, CircleSlash, Minus } from "lucide-react";
import type { Item } from "@/lib/content";
import { SectionHead } from "./section-head";

export function Scope({ title, intro, is, isnt }: {
  title: string; intro: string; is: { title: string; items: Item[] }; isnt: { title: string; items: Item[] };
}) {
  return (
    <section aria-labelledby="scope" className="border-b border-border bg-card">
      <div className="mx-auto max-w-6xl px-5 py-20 sm:px-8 lg:py-28">
        <SectionHead id="scope" eyebrow="Scope" title={title} intro={intro} />
        <div className="mt-12 grid gap-px overflow-hidden rounded-lg border border-border bg-border md:grid-cols-2">
          <div className="bg-background p-7 sm:p-9">
            <div className="flex items-center gap-2 text-primary">
              <CircleCheck aria-hidden className="size-5" />
              <h3 className="text-sm font-semibold uppercase tracking-[0.12em]" dangerouslySetInnerHTML={{ __html: is.title }} />
            </div>
            <ul className="mt-6 flex flex-col gap-4">
              {is.items.map((item) => (
                <li key={item.html} className="flex gap-3 text-base">
                  <Check aria-hidden className="mt-1 size-4 shrink-0 text-primary" strokeWidth={2.5} />
                  <span dangerouslySetInnerHTML={{ __html: item.html }} />
                </li>
              ))}
            </ul>
          </div>
          <div className="bg-muted p-7 sm:p-9">
            <div className="flex items-center gap-2 text-muted-foreground">
              <CircleSlash aria-hidden className="size-5" />
              <h3 className="text-sm font-semibold uppercase tracking-[0.12em]" dangerouslySetInnerHTML={{ __html: isnt.title }} />
            </div>
            <ul className="mt-6 flex flex-col gap-4">
              {isnt.items.map((item) => (
                <li key={item.html} className="flex gap-3 text-base text-muted-foreground">
                  <Minus aria-hidden className="mt-1 size-4 shrink-0" />
                  <span dangerouslySetInnerHTML={{ __html: item.html }} />
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
}
