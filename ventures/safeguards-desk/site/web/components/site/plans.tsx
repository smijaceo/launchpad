// Adapted from 21st.dev "Two-Plan Pricing Cards" (ln-dev7/pricing-16).
import { ArrowRight, Check } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export type Plan = { id: string; name: string; price: string; description: string; features: string[]; cta: string; href: string };

export function Plans({ plans, heading, intro }: { plans: Plan[]; heading?: string; intro?: string }) {
  return (
    <section aria-labelledby="plans" className="border-b border-border bg-card">
      <div className="mx-auto max-w-5xl px-5 py-20 sm:px-8 lg:py-28">
        {!heading && <h2 id="plans" className="sr-only">Plans</h2>}
        {heading && (
          <div className="mx-auto mb-12 max-w-xl text-center">
            <p className="font-mono text-xs uppercase tracking-[0.08em] text-primary">Pricing</p>
            <h2 id="plans" className="mt-3 text-3xl font-semibold tracking-[-0.02em] sm:text-[2.5rem]" dangerouslySetInnerHTML={{ __html: heading }} />
            {intro && <p className="mt-4 text-lg text-muted-foreground" dangerouslySetInnerHTML={{ __html: intro }} />}
          </div>
        )}
        <div className="grid grid-cols-1 gap-5 md:grid-cols-2">
          {plans.map((plan, i) => {
            const highlight = i === 0;
            return (
              <article
                key={plan.id}
                className={cn("relative flex flex-col gap-7 rounded-2xl border border-border bg-background p-7 sm:p-8", highlight && "border-primary/50 ring-1 ring-primary/30")}
              >
                {highlight && (
                  <span className="absolute -top-3 left-7 inline-flex items-center rounded-full bg-primary px-3 py-0.5 text-xs font-semibold text-primary-foreground">
                    For office owners
                  </span>
                )}
                <div className="flex flex-col gap-2">
                  <h3 className="text-xl font-semibold tracking-tight" dangerouslySetInnerHTML={{ __html: plan.name }} />
                  <p className="text-sm leading-relaxed text-muted-foreground" dangerouslySetInnerHTML={{ __html: plan.description }} />
                </div>
                <p className="border-y border-border py-5 text-4xl font-semibold tracking-[-0.02em] tabular-nums" dangerouslySetInnerHTML={{ __html: plan.price }} />
                <ul className="flex flex-col gap-3">
                  {plan.features.map((f) => (
                    <li key={f} className="flex items-start gap-2.5 text-sm">
                      <Check className="mt-0.5 size-4 shrink-0 text-primary" strokeWidth={2.5} aria-hidden />
                      <span dangerouslySetInnerHTML={{ __html: f }} />
                    </li>
                  ))}
                </ul>
                <Button asChild size="lg" variant={highlight ? "default" : "outline"} className="mt-auto h-12 w-full rounded-lg">
                  <a href={plan.href}>
                    {plan.cta} <ArrowRight aria-hidden />
                  </a>
                </Button>
              </article>
            );
          })}
        </div>
      </div>
    </section>
  );
}
