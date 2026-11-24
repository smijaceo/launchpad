import type { Metadata } from "next";
import { bookingUrl, getPage, html, inline, listItems, navPages, paragraphs, sections, subLists } from "@/lib/content";
import { SiteHeader } from "@/components/site/site-header";
import { Hero } from "@/components/site/hero";
import { Scope } from "@/components/site/scope";
import { Included } from "@/components/site/included";
import { Steps } from "@/components/site/steps";
import { Plans } from "@/components/site/plans";
import { Rule } from "@/components/site/rule";
import { Fit } from "@/components/site/fit";
import { CtaBand } from "@/components/site/cta-band";
import { planList } from "@/lib/plans";

const page = getPage("index");

export const metadata: Metadata = {
  title: { absolute: `Countersign Security: ${page.meta.title}` },
  description: page.meta.description,
  alternates: { canonical: "/" },
};

// Direction C "Instrument" (D11). Every sentence comes from copy/site/index.md (claim-checked).
export default function Home() {
  const { intro, sections: s } = sections(page.body);
  const by = (id: string) => s.find((x) => x.id === id)!;
  const h1 = intro.match(/^# (.+)$/m)![1];
  const lead = intro.split("\n").filter((l) => l && !l.startsWith("#"))[0];
  const scope = by("scope"), included = by("included"), steps = by("steps"), rule = by("rule");
  const fit = by("fit"), founder = by("founder"), cta = by("cta");
  const notIncluded = subLists(scope.raw)[0];

  return (
    <>
      <SiteHeader links={navPages()} current="/" bookingUrl={bookingUrl} />
      <main id="main" tabIndex={-1} className="outline-none">
        <Hero
          status={page.meta.status}
          eyebrow={page.meta.eyebrow}
          title={inline(h1)}
          lead={inline(lead)}
          primary={page.meta.cta_primary}
          primaryHref={bookingUrl}
          secondary={page.meta.cta_secondary}
          secondaryHref={page.meta.cta_secondary_href}
        />
        <Scope title={inline(scope.title)} intro={paragraphs(scope.tokens)[0]} included={listItems(scope.tokens)} excluded={notIncluded?.items ?? []} />
        <Included title={inline(included.title)} intro={paragraphs(included.tokens)[0]} items={listItems(included.tokens)} />
        <Steps title={inline(steps.title)} intro={paragraphs(steps.tokens)[0]} items={listItems(steps.tokens)} />
        <Plans plans={planList()} heading="One fixed price" intro="No subscription and no automatic renewal." />
        <Rule title={inline(rule.title)} paras={paragraphs(rule.tokens)} />
        <Fit title={inline(fit.title)} intro={paragraphs(fit.tokens)[0]} items={listItems(fit.tokens)} />
        <section aria-labelledby="founder" className="border-b border-border">
          <div className="mx-auto grid max-w-6xl gap-8 px-5 py-20 sm:px-8 lg:grid-cols-[0.9fr_1.1fr]">
            <div className="flex flex-col gap-3">
              <p className="font-mono text-xs uppercase tracking-[0.08em] text-primary">The person doing the work</p>
              <h2 id="founder" className="text-3xl font-semibold tracking-[-0.02em] sm:text-[2.5rem]" dangerouslySetInnerHTML={{ __html: inline(founder.title) }} />
            </div>
            <div className="prose prose-lg max-w-none text-muted-foreground prose-a:text-ink" dangerouslySetInnerHTML={{ __html: html(founder.raw) }} />
          </div>
        </section>
        <CtaBand title={inline(cta.title)} text={paragraphs(cta.tokens)[0]} href={bookingUrl} label={page.meta.cta_primary} />
      </main>
    </>
  );
}
