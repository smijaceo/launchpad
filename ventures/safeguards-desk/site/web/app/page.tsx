import type { Metadata } from "next";
import { bookingUrl, getPage, html, inline, listItems, navPages, paragraphs, sections, subLists } from "@/lib/content";
import { SiteHeader } from "@/components/site/site-header";
import { Hero } from "@/components/site/hero";
import { Rule } from "@/components/site/rule";
import { Included } from "@/components/site/included";
import { Scope } from "@/components/site/scope";
import { Fit } from "@/components/site/fit";
import { Steps } from "@/components/site/steps";
import { Plans } from "@/components/site/plans";
import { CtaBand } from "@/components/site/cta-band";
import { planList } from "@/lib/plans";

const page = getPage("index");

export const metadata: Metadata = {
  title: { absolute: `Countersign Security: ${page.meta.title}` },
  description: page.meta.description,
  alternates: { canonical: "/" },
};

export default function Home() {
  const { intro, sections: s } = sections(page.body);
  const by = (id: string) => s.find((x) => x.id === id)!;
  const h1 = intro.match(/^# (.+)$/m)![1];
  const lead = intro.split("\n").filter((l) => l && !l.startsWith("#"))[0];
  const report = by("report"), rule = by("rule"), included = by("included"), scope = by("scope");
  const fit = by("fit"), steps = by("steps"), founder = by("founder"), cta = by("cta");
  const scopeLists = subLists(scope.raw);
  const includedMore = included.tokens.find((t) => t.type === "paragraph" && t.raw.includes("full details"));

  return (
    <>
      <SiteHeader links={navPages()} current="/" bookingUrl={bookingUrl} />
      <main id="main" tabIndex={-1} className="outline-none">
        <Hero
          status={page.meta.status}
          title={inline(h1)}
          lead={inline(lead)}
          primary={page.meta.cta_primary}
          primaryHref={bookingUrl}
          secondary={page.meta.cta_secondary}
          secondaryHref={page.meta.cta_secondary_href}
          reportTitle={inline(report.title)}
          reportItems={listItems(report.tokens)}
        />
        <Rule title={inline(rule.title)} paras={paragraphs(rule.tokens)} />
        <Included
          title={inline(included.title)}
          intro={paragraphs(included.tokens)[0]}
          items={listItems(included.tokens)}
          moreHref="/check/"
          moreLabel={includedMore ? "Read the Full Details" : "The Check"}
        />
        <Scope title={inline(scope.title)} intro={paragraphs(scope.tokens)[0]} is={scopeLists[0]} isnt={scopeLists[1]} />
        <Steps title={inline(steps.title)} intro={paragraphs(steps.tokens)[0]} items={listItems(steps.tokens)} />
        <Plans plans={planList()} heading="One fixed price" intro="No subscription and no automatic renewal." />
        <Fit title={inline(fit.title)} intro={paragraphs(fit.tokens)[0]} items={listItems(fit.tokens)} />
        <section aria-labelledby="founder" className="border-b border-border bg-card">
          <div className="mx-auto max-w-3xl px-5 py-20 text-center sm:px-8">
            <p className="text-xs font-semibold uppercase tracking-[0.16em] text-primary">The person doing the work</p>
            <h2 id="founder" className="mt-3 font-serif text-3xl font-semibold tracking-tight sm:text-[2.6rem]" dangerouslySetInnerHTML={{ __html: inline(founder.title) }} />
            <div className="prose prose-lg mx-auto mt-5 text-muted-foreground prose-a:text-ink" dangerouslySetInnerHTML={{ __html: html(founder.raw) }} />
          </div>
        </section>
        <CtaBand title={inline(cta.title)} text={paragraphs(cta.tokens)[0]} href={bookingUrl} label={page.meta.cta_primary} />
      </main>
    </>
  );
}
