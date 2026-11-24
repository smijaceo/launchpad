import { ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";

// Direction C hero: grid ground, mono eyebrow, the deliverable as the picture (generated illustration, D11).
export function Hero(props: {
  status: string; eyebrow: string; title: string; lead: string;
  primary: string; primaryHref: string; secondary: string; secondaryHref: string;
}) {
  return (
    <section className="relative overflow-hidden border-b border-border">
      <div aria-hidden className="pointer-events-none absolute inset-0 [background-image:linear-gradient(var(--border)_1px,transparent_1px),linear-gradient(90deg,var(--border)_1px,transparent_1px)] [background-size:40px_40px] [mask-image:radial-gradient(ellipse_at_30%_40%,black,transparent_75%)] opacity-70" />
      <div className="relative mx-auto grid max-w-6xl items-center gap-12 px-5 pb-16 pt-12 sm:px-8 lg:grid-cols-[1.05fr_1fr] lg:pb-24 lg:pt-20">
        <div className="flex flex-col items-start gap-6">
          <p className="inline-flex items-center gap-2 rounded-full border border-primary/30 bg-background px-3 py-1 text-sm font-medium text-primary">
            <span className="size-1.5 rounded-full bg-primary" aria-hidden />
            {props.status}
          </p>
          <p className="font-mono text-xs uppercase tracking-[0.08em] text-muted-foreground">{props.eyebrow}</p>
          <h1 className="text-[2.6rem] font-semibold leading-[1.02] tracking-[-0.03em] text-foreground sm:text-6xl lg:text-[4.25rem]"
            dangerouslySetInnerHTML={{ __html: props.title }} />
          <p className="max-w-xl text-lg leading-relaxed text-muted-foreground" dangerouslySetInnerHTML={{ __html: props.lead }} />
          <div className="flex w-full flex-col gap-3 sm:w-auto sm:flex-row">
            <Button asChild size="lg" className="h-12 rounded-lg px-6 text-base">
              <a href={props.primaryHref}>{props.primary} <ArrowRight aria-hidden /></a>
            </Button>
            <Button asChild size="lg" variant="outline" className="h-12 rounded-lg bg-background px-6 text-base">
              <a href={props.secondaryHref}>{props.secondary}</a>
            </Button>
          </div>
        </div>
        <figure className="relative">
          <div className="overflow-hidden rounded-2xl border border-border bg-[#F6F3EE] shadow-[0_30px_60px_-35px_rgb(18_26_38/0.45)]">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src="/illustrations/hero-desk.webp" width={1024} height={688} alt="A laptop, client folders and a printed report with a green check seal on a desk" className="h-auto w-full" fetchPriority="high" />
          </div>
          <figcaption className="absolute -bottom-5 left-5 flex items-center gap-3 rounded-xl border border-border bg-background px-4 py-3 shadow-sm sm:left-8">
            <span className="grid size-8 place-items-center rounded-full bg-primary/10 font-mono text-xs text-primary">$</span>
            <span className="text-sm"><span className="font-semibold">$490 fixed</span><span className="text-muted-foreground"> · dated report on delivery</span></span>
          </figcaption>
        </figure>
      </div>
    </section>
  );
}
