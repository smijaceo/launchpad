import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { allPages, bookingUrl, getPage, html, inline, navPages, sections } from "@/lib/content";
import { SiteHeader } from "@/components/site/site-header";
import { Plans } from "@/components/site/plans";
import { Faq } from "@/components/site/faq";
import { CtaBand } from "@/components/site/cta-band";
import { planList } from "@/lib/plans";

export const dynamicParams = false;

export function generateStaticParams() {
  return allPages().filter((p) => p.slug !== "index").map((p) => ({ slug: p.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const p = getPage(slug);
  return { title: p.meta.title, description: p.meta.description, alternates: { canonical: p.meta.path } };
}

function stripCta(body: string) {
  return body.replace(/<p class="cta-row">[\s\S]*?<\/p>/g, "").replace(/<p class="fineprint">([\s\S]*?)<\/p>/g, "");
}

export default async function Sub({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  if (!allPages().some((p) => p.slug === slug)) notFound();
  const page = getPage(slug);
  const body = stripCta(page.body);
  const { intro, sections: s } = sections(body);
  const h1 = intro.match(/^# (.+)$/m)?.[1] ?? page.meta.title;
  const lead = intro.replace(/^# .+$/m, "").trim();
  const legal = page.meta.legal_draft === "true";

  let content: React.ReactNode;
  if (slug === "faq") {
    content = (
      <div className="mx-auto max-w-3xl px-5 py-14 sm:px-8">
        <h2 className="sr-only">Answers</h2>
        <Faq items={s.map((x) => ({ q: inline(x.title), a: html(x.raw) }))} />
      </div>
    );
  } else if (slug === "pricing") {
    const rest = s.filter((x) => !x.raw.includes("<!--plan:"));
    content = (
      <>
        <Plans plans={planList()} />
        <div className="prose prose-lg mx-auto max-w-3xl px-5 py-14 sm:px-8 prose-headings:font-serif prose-a:text-ink"
          dangerouslySetInnerHTML={{ __html: rest.map((x) => html(`## ${x.title}\n${x.raw}`)).join("") }} />
      </>
    );
  } else {
    content = (
      <article
        className="prose prose-lg mx-auto max-w-3xl px-5 py-14 sm:px-8 prose-headings:font-serif prose-headings:tracking-tight prose-h2:mt-14 prose-a:text-ink prose-strong:text-foreground prose-table:text-base prose-th:bg-muted prose-th:px-3 prose-td:px-3 dark:prose-invert"
        dangerouslySetInnerHTML={{ __html: html(s.map((x) => `## ${x.title}\n${x.raw}`).join("\n")) }}
      />
    );
  }

  return (
    <>
      <SiteHeader links={navPages()} current={page.meta.path} bookingUrl={bookingUrl} />
      <main id="main" tabIndex={-1} className="outline-none">
        <header className="border-b border-border bg-card">
          <div className="mx-auto max-w-3xl px-5 py-14 sm:px-8 lg:py-20">
            {legal && (
              <p className="mb-5 inline-block rounded-md border-l-4 border-warn bg-background px-3 py-1.5 text-sm font-semibold text-warn">
                Draft: a lawyer must review this before the site goes live.
              </p>
            )}
            <h1 className="font-serif text-4xl font-bold leading-[1.08] tracking-tight sm:text-5xl" dangerouslySetInnerHTML={{ __html: inline(h1) }} />
            {lead && (
              <div className="mt-5 text-lg leading-relaxed text-muted-foreground [&_.draft]:hidden"
                dangerouslySetInnerHTML={{ __html: html(lead) }} />
            )}
          </div>
        </header>
        {content}
        {!legal && (
          <CtaBand
            title="Start with a free scoping call"
            text="Twenty minutes, by phone or video. If the check isn’t a fit for your office, you’ll hear that on the call."
            href={bookingUrl}
            label={slug === "msp" ? "Talk About a Pilot" : "Book a 20-Minute Scoping Call"}
          />
        )}
        <p className="mx-auto max-w-3xl px-5 py-6 text-sm text-muted-foreground sm:px-8">
          General information, not legal advice. Countersign Security isn’t affiliated with the FTC or the Internal Revenue Service.
        </p>
      </main>
    </>
  );
}
