// Direction C scope panel ("Instrument"): what the check looks at, as a table with status pills.
import type { Item } from "@/lib/content";
import { SectionHead } from "./section-head";

function Pill({ on }: { on: boolean }) {
  return on ? (
    <span className="inline-flex whitespace-nowrap rounded-full bg-primary/10 px-2.5 py-0.5 text-[13px] font-semibold text-primary">Included</span>
  ) : (
    <span className="inline-flex whitespace-nowrap rounded-full bg-muted px-2.5 py-0.5 text-[13px] font-semibold text-muted-foreground">Not included</span>
  );
}

export function Scope({ title, intro, included, excluded }: { title: string; intro: string; included: Item[]; excluded: Item[] }) {
  const rows = [...included.map((i) => ({ ...i, on: true })), ...excluded.map((i) => ({ ...i, on: false }))];
  return (
    <section id="scope" aria-labelledby="scope-h" className="border-b border-border">
      <div className="mx-auto grid max-w-6xl gap-12 px-5 py-20 sm:px-8 lg:grid-cols-[0.9fr_1.1fr] lg:py-28">
        <SectionHead id="scope-h" eyebrow="Scope" title={title} intro={intro} />
        <div className="overflow-hidden rounded-xl border border-border bg-card shadow-[0_20px_50px_-30px_rgb(18_26_38/0.3)]">
          <div className="flex justify-between gap-3 border-b border-border bg-muted px-5 py-3 font-mono text-xs uppercase tracking-wide text-muted-foreground">
            <span>Scope of the check</span><span>Read-only</span>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full border-collapse text-[15px]">
              <thead>
                <tr className="text-left font-mono text-xs uppercase tracking-wide text-muted-foreground">
                  <th scope="col" className="px-5 py-3 font-medium">Area</th>
                  <th scope="col" className="px-5 py-3 font-medium">What is looked at</th>
                  <th scope="col" className="px-5 py-3 font-medium">Status</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((r) => (
                  <tr key={r.term} className={r.on ? "border-t border-border" : "border-t border-border text-muted-foreground"}>
                    <th scope="row" className="px-5 py-3.5 text-left font-semibold" dangerouslySetInnerHTML={{ __html: r.term }} />
                    <td className={r.on ? "px-5 py-3.5 text-muted-foreground" : "px-5 py-3.5"} dangerouslySetInnerHTML={{ __html: r.text }} />
                    <td className="px-5 py-3.5"><Pill on={r.on} /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>
  );
}
