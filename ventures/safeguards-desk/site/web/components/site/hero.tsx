import { ArrowRight, Check } from "lucide-react";
import { Button } from "@/components/ui/button";
import { LogoMark } from "./logo";
import type { Item } from "@/lib/content";

// The hero shows the real deliverable: the outline of the dated report, never sample findings.
export function Hero(props: {
  status: string; title: string; lead: string; primary: string; primaryHref: string;
  secondary: string; secondaryHref: string; reportTitle: string; reportItems: Item[];
}) {
  return (
    <section className="relative overflow-hidden border-b border-border">
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 opacity-[0.5] [background-image:linear-gradient(var(--border)_1px,transparent_1px)] [background-size:100%_2.25rem] [mask-image:linear-gradient(to_bottom,black,transparent_85%)]"
      />
      <div className="relative mx-auto grid max-w-6xl items-center gap-12 px-5 pb-16 pt-12 sm:px-8 lg:grid-cols-[1.15fr_1fr] lg:gap-16 lg:pb-24 lg:pt-20">
        <div className="flex flex-col items-start gap-6">
          <p className="inline-flex items-center gap-2 rounded-full border border-primary/40 bg-card px-3 py-1 text-sm font-semibold text-primary">
            <span className="size-1.5 rounded-full bg-primary" aria-hidden />
            {props.status}
          </p>
          <h1
            className="font-serif text-[2.4rem] font-bold leading-[1.06] tracking-tight text-foreground sm:text-5xl lg:text-[3.6rem]"
            dangerouslySetInnerHTML={{ __html: props.title }}
          />
          <p className="max-w-xl text-lg leading-relaxed text-muted-foreground" dangerouslySetInnerHTML={{ __html: props.lead }} />
          <div className="flex w-full flex-col gap-3 sm:w-auto sm:flex-row">
            <Button asChild size="lg" className="h-12 rounded-full px-7 text-base">
              <a href={props.primaryHref}>
                {props.primary} <ArrowRight aria-hidden />
              </a>
            </Button>
            <Button asChild size="lg" variant="outline" className="h-12 rounded-full border-ink/30 px-7 text-base text-ink hover:bg-ink hover:text-background">
              <a href={props.secondaryHref}>{props.secondary}</a>
            </Button>
          </div>
        </div>

        <figure className="relative mx-auto w-full max-w-md lg:max-w-none" aria-label={props.reportTitle}>
          <div aria-hidden className="absolute -right-3 top-4 hidden h-full w-full rotate-[2.5deg] rounded-lg border border-border bg-card/70 sm:block" />
          <div className="relative rounded-lg border border-border bg-card p-6 shadow-[0_24px_60px_-30px_rgb(22_32_46/0.35)] sm:p-8">
            <div className="flex items-start justify-between gap-4 border-b border-border pb-5">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.14em] text-muted-foreground">Safeguards testing check</p>
                <p className="mt-1 font-serif text-xl font-semibold text-foreground" dangerouslySetInnerHTML={{ __html: props.reportTitle }} />
              </div>
              <span className="text-ink"><LogoMark className="size-10" /></span>
            </div>
            <dl className="grid grid-cols-2 gap-4 border-b border-border py-4 text-sm">
              <div><dt className="text-muted-foreground">Prepared for</dt><dd className="font-semibold">Your office</dd></div>
              <div><dt className="text-muted-foreground">Report date</dt><dd className="font-semibold">On delivery</dd></div>
            </dl>
            <ul className="divide-y divide-border">
              {props.reportItems.map((item) => (
                <li key={item.term} className="flex items-start gap-3 py-3">
                  <span className="mt-0.5 grid size-5 shrink-0 place-items-center rounded-full bg-primary/12 text-primary">
                    <Check className="size-3.5" strokeWidth={3} aria-hidden />
                  </span>
                  <span className="min-w-0 text-sm">
                    <span className="font-semibold text-foreground" dangerouslySetInnerHTML={{ __html: item.term }} />
                    <span className="text-muted-foreground">: </span>
                    <span className="text-muted-foreground" dangerouslySetInnerHTML={{ __html: item.text }} />
                  </span>
                </li>
              ))}
            </ul>
            <div className="mt-5 flex items-end justify-between gap-4 border-t border-dashed border-border pt-4">
              <svg viewBox="0 0 160 40" className="h-9 w-36 text-ink" aria-hidden>
                <path d="M4 28 C 20 6, 30 36, 44 20 S 66 8, 72 24 S 96 34, 110 16 S 140 18, 156 22" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" />
              </svg>
              <p className="text-right text-xs uppercase tracking-[0.14em] text-muted-foreground">Countersigned<br />on delivery</p>
            </div>
          </div>
        </figure>
      </div>
    </section>
  );
}
